#!/usr/bin/env python3
"""Garde de confiance AZDone : classe une commande shell selon .azdone/trust.yaml.

Appelé par hooks/azd-trust-guard.sh (PreToolUse Bash sous Claude Code,
beforeShellExecution sous Cursor). Bibliothèque standard seulement.

Entrée sur stdin (JSON) :
  Claude Code : {"hook_event_name":"PreToolUse","tool_input":{"command":"..."},"cwd":"..."}
  Cursor      : {"hook_event_name":"beforeShellExecution","command":"...","cwd":"...","workspace_roots":[...]}

Sortie :
  autoriser : rien sur stdout, exit 0.
  refuser   : Claude Code -> {"hookSpecificOutput":{"hookEventName":"PreToolUse",
                              "permissionDecision":"deny","permissionDecisionReason":"..."}}
              Cursor      -> {"permission":"deny","user_message":"...","agent_message":"..."}
              exit 0 dans les deux cas.

Règles :
  - fichier absent ou `enforcement: declared` : tout passe, silencieusement ;
  - politique `enforced` illisible : refus (fail-closed) ;
  - la commande est découpée sur && || ; | et sauts de ligne, chaque segment est classé ;
  - les actions de la liste toujours-pause (force-push, suppression de données,
    credentials, réécriture d'historique partagé, écriture de trust.yaml,
    message à un client) sont refusées quel que soit `actions.*` ou `autonomy` ;
  - les autres actions suivent `actions.<action>` : auto | conditional | ask | never,
    avec les défauts du niveau `autonomy` quand la clé manque.

AZD_TRUST_FILE force le chemin de trust.yaml (tests).
"""
from __future__ import annotations

import json
import os
import re
import shlex
import subprocess
import sys
import time

WITNESS_MAX_AGE_SECONDS = 1800

LEVEL_DEFAULTS = {
    "guided": {"commit": "ask", "push": "ask", "open_pr": "ask", "merge": "ask", "deploy": "ask",
               "install_global": "ask", "external_message": "ask", "spawn_agent": "ask"},
    "assisted": {"commit": "auto", "push": "ask", "open_pr": "ask", "merge": "ask", "deploy": "ask",
                 "install_global": "ask", "external_message": "ask", "spawn_agent": "ask"},
    "autonomous": {"commit": "auto", "push": "auto", "open_pr": "auto", "merge": "conditional",
                   "deploy": "ask", "install_global": "ask", "external_message": "ask", "spawn_agent": "ask"},
    "full": {"commit": "auto", "push": "auto", "open_pr": "auto", "merge": "auto",
             "deploy": "conditional", "install_global": "auto", "external_message": "auto", "spawn_agent": "auto"},
}
LEVEL_ORDER = ("guided", "assisted", "autonomous", "full")
RISK_ORDER = {"rapid": 0, "standard": 1, "critical": 2}
WITNESS_KEYS = ("commit", "ci", "review", "reviewer_id", "author_id", "risk", "files_changed", "lanes", "written_at")
LEDGER_HEADER = "| date | run_id | risk | verdict | actions_auto | rollback | override | niveau_effectif | série | événement |"
LEDGER_SEPARATOR = "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"

ALWAYS_PAUSE = {
    "force_push": "force-push (git push --force, -f, --force-with-lease ou refspec +)",
    "delete_data": "suppression de données ou de branches non fusionnées",
    "credentials": "usage ou création de credentials",
    "rewrite_shared_history": "réécriture d'historique partagé",
    "trust_file": "écriture de .azdone/trust.yaml par l'agent",
    "customer_message": "message à un client ou à un tiers",
}

PROTECTED_BRANCHES = ("main", "master", "trunk", "develop", "production", "prod", "release")
SAFE_DELETE_BASENAMES = {
    "node_modules", "dist", "build", "out", ".cache", "__pycache__", ".pytest_cache", ".mypy_cache",
    ".ruff_cache", "target", ".venv", "venv", ".next", ".nuxt", ".turbo", "coverage", "tmp", ".tmp",
    ".parcel-cache", ".gradle", ".tox", "htmlcov",
}
READ_ONLY_COMMANDS = {
    "cat", "less", "more", "head", "tail", "grep", "rg", "egrep", "fgrep", "diff", "ls", "stat", "wc",
    "file", "cut", "sort", "uniq", "jq", "bat", "tree", "pwd", "echo", "printf", "test", "[", "true",
    "which", "type", "column", "md5sum", "sha256sum", "shasum", "realpath", "readlink", "basename",
    "dirname", "yq", "awk",
}
SHELL_WRAPPERS = ("sudo", "env", "nice", "time", "nohup", "exec", "command", "builtin", "doas")
CUSTOMER_MESSAGE_PATTERNS = re.compile(
    r"api\.twilio\.com|api\.sendgrid\.com|api\.mailgun\.net|api\.postmarkapp\.com|customer\.io|"
    r"api\.intercom\.io|api\.brevo\.com|api\.resend\.com|\bsendmail\b|\bmailx?\b|\bmutt\b",
    re.IGNORECASE,
)
TEAM_MESSAGE_PATTERNS = re.compile(
    r"hooks\.slack\.com|discord(app)?\.com/api/webhooks|api\.telegram\.org|hooks\.zapier\.com|"
    r"chat\.googleapis\.com|webhook\.office\.com",
    re.IGNORECASE,
)
SECRET_ASSIGNMENT = re.compile(
    r"\b[A-Za-z0-9_]*(SECRET|TOKEN|PASSWORD|PASSWD|API_KEY|APIKEY|PRIVATE_KEY|ACCESS_KEY)[A-Za-z0-9_]*=\S+",
)
SQL_DESTRUCTIVE = re.compile(r"\b(drop\s+(table|database|schema)|truncate\s+table)\b", re.IGNORECASE)
SQL_UNBOUNDED = re.compile(r"\b(delete\s+from\s+\S+|update\s+\S+\s+set\s+[^;]*?)(?![^;]*\bwhere\b)[^;]*(;|$)", re.IGNORECASE)
HTTP_CLIENTS = ("curl", "wget", "http", "https", "xh", "httpie")
LOCAL_HOSTS = re.compile(r"https?://(localhost|127\.0\.0\.1|\[?::1\]?|0\.0\.0\.0)(:\d+)?", re.IGNORECASE)
WRITE_COMMANDS = {"cp", "mv", "tee", "install", "rsync", "ln", "truncate", "dd", "patch", "touch", "chmod", "chown"}
PIPE_TO_SHELL = re.compile(r"\b(curl|wget)\b[^|;&]*\|\s*(sudo\s+)?(ba|z|da)?sh\b")
DEPLOY_SCRIPT = re.compile(r"(^|/)(deploy|release|publish)[^/]*\.(sh|py|js|ts|rb)$", re.IGNORECASE)


# --------------------------------------------------------------------------- YAML minimal

def parse_trust_yaml(text: str) -> dict:
    """Parseur volontairement minimal pour le schéma plat de trust.yaml."""
    root: dict = {}
    current_key: str | None = None
    for raw in text.splitlines():
        line = _strip_comment(raw).rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        body = line.strip()
        if indent == 0:
            if body.endswith(":"):
                current_key = body[:-1].strip()
                root.setdefault(current_key, {})
            else:
                key, _, value = body.partition(":")
                root[key.strip()] = _scalar(value)
                current_key = None
            continue
        if current_key is None:
            continue
        container = root.get(current_key)
        if body.startswith("- "):
            if not isinstance(container, list):
                container = [] if not container else container
                root[current_key] = container
            container.append(_scalar(body[2:]))
            continue
        if isinstance(container, dict):
            if indent >= 4 and container:
                last = list(container)[-1]
                if isinstance(container[last], dict):
                    key, _, value = body.partition(":")
                    container[last][key.strip()] = _scalar(value)
                    continue
            key, _, value = body.partition(":")
            container[key.strip()] = {} if body.endswith(":") else _scalar(value)
    return root


def _strip_comment(line: str) -> str:
    out = []
    quote = None
    for index, char in enumerate(line):
        if quote:
            out.append(char)
            if char == quote:
                quote = None
            continue
        if char in ("'", '"'):
            quote = char
            out.append(char)
            continue
        if char == "#" and (index == 0 or line[index - 1] in " \t"):
            break
        out.append(char)
    return "".join(out)


def _scalar(value: str):
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        return [_scalar(item) for item in value[1:-1].split(",") if item.strip()]
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    lowered = value.lower()
    if lowered in ("true", "yes"):
        return True
    if lowered in ("false", "no"):
        return False
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


# --------------------------------------------------------------------------- entrée

def read_payload() -> tuple[str, str, str, str]:
    raw = sys.stdin.read()
    try:
        data = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        data = {}
    is_claude = isinstance(data, dict) and (
        "tool_input" in data or data.get("hook_event_name") == "PreToolUse"
    )
    fmt = "claude" if is_claude else "cursor"
    file_path = ""
    if fmt == "claude":
        tool_input = data.get("tool_input") or {}
        command = str(tool_input.get("command") or "")
        if str(data.get("tool_name") or "") in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
            file_path = str(tool_input.get("file_path") or tool_input.get("notebook_path") or "")
    else:
        command = str(data.get("command") or "")
        file_path = str(data.get("file_path") or "")
    cwd = str(data.get("cwd") or "")
    if not cwd:
        roots = data.get("workspace_roots") or []
        cwd = str(roots[0]) if roots else ""
    if not cwd:
        cwd = os.environ.get("CLAUDE_PROJECT_DIR") or os.environ.get("CURSOR_PROJECT_DIR") or os.getcwd()
    return fmt, command, cwd, file_path


def find_trust_file(cwd: str) -> str | None:
    forced = os.environ.get("AZD_TRUST_FILE")
    if forced:
        return forced if os.path.isfile(forced) else None
    candidates = [cwd, os.environ.get("CLAUDE_PROJECT_DIR"), os.environ.get("CURSOR_PROJECT_DIR")]
    for start in candidates:
        if not start:
            continue
        path = os.path.abspath(start)
        while True:
            trust = os.path.join(path, ".azdone", "trust.yaml")
            if os.path.isfile(trust):
                return trust
            parent = os.path.dirname(path)
            if parent == path:
                break
            path = parent
    return None


# --------------------------------------------------------------------------- découpage

def split_segments(command: str) -> list[str]:
    """Découpe sur && || ; | et sauts de ligne hors guillemets, et ouvre bash -c / eval / $( )."""
    segments: list[str] = []
    current: list[str] = []
    quote = None
    index = 0
    length = len(command)
    while index < length:
        char = command[index]
        if quote:
            current.append(char)
            if char == "\\" and index + 1 < length:
                current.append(command[index + 1])
                index += 2
                continue
            if char == quote:
                quote = None
            index += 1
            continue
        if char in ("'", '"'):
            quote = char
            current.append(char)
            index += 1
            continue
        two = command[index:index + 2]
        if two in ("&&", "||"):
            segments.append("".join(current))
            current = []
            index += 2
            continue
        if char in (";", "|", "\n", "`"):
            segments.append("".join(current))
            current = []
            index += 1
            continue
        if two == "$(":
            segments.append("".join(current))
            current = []
            index += 2
            continue
        if char == ")":
            segments.append("".join(current))
            current = []
            index += 1
            continue
        current.append(char)
        index += 1
    segments.append("".join(current))

    expanded: list[str] = []
    for segment in segments:
        segment = segment.strip()
        if not segment:
            continue
        expanded.append(segment)
        words = tokenize(segment)
        words = strip_wrappers(words)
        if len(words) >= 3 and words[0] in ("bash", "sh", "zsh", "dash") and words[1] in ("-c", "-lc", "-ec"):
            expanded.extend(split_segments(words[2]))
        elif words and words[0] == "eval":
            expanded.extend(split_segments(" ".join(words[1:])))
    return expanded


def tokenize(segment: str) -> list[str]:
    try:
        return shlex.split(segment, posix=True)
    except ValueError:
        return segment.split()


def strip_wrappers(words: list[str]) -> list[str]:
    while words and (words[0] in SHELL_WRAPPERS or re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=.*", words[0])):
        if words[0] in ("sudo", "doas"):
            return words  # sudo est classé plus bas comme install_global
        words = words[1:]
        while words and words[0].startswith("-") and words[0] not in ("-", "--"):
            words = words[1:]
    return words


# --------------------------------------------------------------------------- classification

class Verdict:
    def __init__(self, kind: str, action: str, reason: str):
        self.kind = kind          # "always_pause" | "action"
        self.action = action
        self.reason = reason


def classify(segment: str, cwd: str, protected: list[str], trust_root: str) -> Verdict | None:
    words = tokenize(segment)
    if not words:
        return None
    if words[0] in ("sudo", "doas"):
        return Verdict("action", "install_global", "commande sous sudo (changement de machine)")
    words = strip_wrappers(words)
    if not words:
        return None
    head = os.path.basename(words[0])
    args = words[1:]
    lowered = segment.lower()

    if SECRET_ASSIGNMENT.search(segment):
        return Verdict("always_pause", "credentials", ALWAYS_PAUSE["credentials"])
    if CUSTOMER_MESSAGE_PATTERNS.search(segment):
        return Verdict("always_pause", "customer_message", ALWAYS_PAUSE["customer_message"])
    if SQL_DESTRUCTIVE.search(segment) or SQL_UNBOUNDED.search(segment):
        return Verdict("always_pause", "delete_data", ALWAYS_PAUSE["delete_data"])
    if is_trust_tool(head, args):
        return Verdict("action", "record_run", "journal de confiance (azd-trust-guard.py record|witness)")
    spawn = classify_spawn_agent(head, args)
    if spawn:
        return spawn
    outside = outside_root_write(segment, words, cwd, trust_root)
    if outside:
        return outside

    protected_hit = protected_path_write(segment, words, cwd, protected, trust_root)
    if protected_hit:
        return protected_hit

    if head == "git":
        return classify_git(args, cwd)
    if head == "gh":
        return classify_gh(args)
    if head == "glab":
        sub = " ".join(args[:2])
        if sub == "mr create":
            return Verdict("action", "open_pr", "création de merge request")
        if sub == "mr merge":
            return Verdict("action", "merge", "merge request fusionnée")
        if sub in ("mr note", "issue note", "issue create"):
            return Verdict("action", "external_message", "commentaire ou issue GitLab")
        if args[:1] == ["auth"]:
            return Verdict("always_pause", "credentials", ALWAYS_PAUSE["credentials"])
        return None
    if head == "rm":
        return classify_rm(args, cwd)
    if head == "find" and "-delete" in args:
        return Verdict("always_pause", "delete_data", ALWAYS_PAUSE["delete_data"])
    if head in ("shred", "mkfs", "mkfs.ext4", "wipefs", "diskutil") or (head == "dd" and any(a.startswith("of=/dev/") for a in args)):
        return Verdict("always_pause", "delete_data", ALWAYS_PAUSE["delete_data"])

    credentials = classify_credentials(head, args)
    if credentials:
        return credentials
    deploy = classify_deploy(head, args, lowered)
    if deploy:
        return deploy
    install = classify_install(head, args, segment)
    if install:
        return install
    if TEAM_MESSAGE_PATTERNS.search(segment) or head in ("slack",):
        return Verdict("action", "external_message", "message vers un canal d'équipe")
    if head in HTTP_CLIENTS and is_non_get_request(head, args) and not LOCAL_HOSTS.search(segment):
        return Verdict("action", "external_message", f"requête sortante non GET ({head})")
    return None


def is_trust_tool(head: str, args: list[str]) -> bool:
    script = ""
    if head in ("python3", "python") and args:
        script = os.path.basename(args[0])
        sub = args[1] if len(args) > 1 else ""
    else:
        script = head
        sub = args[0] if args else ""
    return script == "azd-trust-guard.py" and sub in ("record", "witness", "status")


def classify_spawn_agent(head: str, args: list[str]) -> Verdict | None:
    if head == "codex" and args[:1] == ["exec"]:
        joined = " ".join(args)
        if not re.search(r"(^|\s)(-s|--sandbox)(\s+|=)read-only\b", joined):
            return Verdict("action", "spawn_agent", "codex exec sans -s read-only")
        return None
    if head == "claude" and ("-p" in args or "--print" in args):
        joined = " ".join(args)
        read_only = re.search(r"--permission-mode(\s+|=)plan\b", joined) or re.search(r"--allowedTools|--allowed-tools", joined)
        if not read_only:
            return Verdict("action", "spawn_agent", "claude -p sans mode lecture seule")
        return None
    if head in ("agent", "cursor-agent") and ("-p" in args or "--print" in args):
        return Verdict("action", "spawn_agent", "CLI Cursor sans mode lecture seule")
    return None


def is_non_get_request(head: str, args: list[str]) -> bool:
    joined = " ".join(args)
    if head in ("http", "https", "xh", "httpie"):
        return any(a.upper() in ("POST", "PUT", "PATCH", "DELETE") for a in args[:2]) or "=" in joined
    if re.search(r"(^|\s)(-X|--request)\s*(POST|PUT|PATCH|DELETE)\b", joined, re.IGNORECASE):
        return True
    return re.search(r"(^|\s)(-d|--data(-\w+)?|-F|--form|--json|--upload-file|-T)(\s|=|$)", joined) is not None


def outside_root_write(segment: str, words: list[str], cwd: str, trust_root: str) -> Verdict | None:
    """Écriture vers un chemin absolu ou ~ hors du dépôt et hors /tmp."""
    head = os.path.basename(words[0]) if words else ""
    is_write = head in WRITE_COMMANDS or (head in ("sed", "perl") and any(a.startswith("-i") for a in words[1:]))
    redirect_targets = re.findall(r"(?:^|[^<>|&])>{1,2}\s*([^\s;&|]+)", segment)
    targets = list(redirect_targets)
    if is_write and len(words) > 1:
        targets.append(words[-1])
    for target in targets:
        cleaned = target.strip("'\"")
        if cleaned.startswith("~") or cleaned.startswith("$HOME"):
            return Verdict("protected", "outside_root", f"écriture hors du dépôt ({cleaned})")
        if cleaned.startswith("/") and not cleaned.startswith(("/tmp/", "/private/tmp/", "/dev/null", "/dev/std")):
            root = (trust_root or "").rstrip("/") + "/"
            if not cleaned.startswith(root):
                return Verdict("protected", "outside_root", f"écriture hors du dépôt ({cleaned})")
    return None


def classify_file_write(file_path: str, cwd: str, protected: list[str], trust_root: str) -> Verdict | None:
    """Outils natifs Write/Edit : mêmes règles que le shell pour les chemins."""
    if not file_path:
        return None
    absolute = file_path if os.path.isabs(file_path) else os.path.join(cwd or trust_root, file_path)
    absolute = os.path.normpath(absolute)
    root = (trust_root or "").rstrip("/")
    relative = os.path.relpath(absolute, root) if root and absolute.startswith(root + "/") else absolute
    if relative == ".azdone/trust.yaml":
        return Verdict("always_pause", "trust_file", ALWAYS_PAUSE["trust_file"])
    if os.path.isabs(relative) and not relative.startswith(("/tmp/", "/private/tmp/")):
        return Verdict("protected", "outside_root", f"écriture hors du dépôt ({relative})")
    for entry in protected:
        if _path_matches(relative, entry):
            return Verdict("protected", "protected_path", f"écriture dans un chemin protégé ({relative})")
    return None


def classify_git(args: list[str], cwd: str) -> Verdict | None:
    if not args:
        return None
    # options globales de git avant la sous-commande (-C dir, -c key=val)
    while args and args[0].startswith("-"):
        if args[0] in ("-C", "-c") and len(args) > 1:
            args = args[2:]
        else:
            args = args[1:]
    if not args:
        return None
    sub, rest = args[0], args[1:]
    if sub == "push":
        flags = [a for a in rest if a.startswith("-")]
        positional = [a for a in rest if not a.startswith("-")]
        if any(f in ("--force", "--force-with-lease", "--force-if-includes") or f.startswith("--force-with-lease=") for f in flags):
            return Verdict("always_pause", "force_push", ALWAYS_PAUSE["force_push"])
        if any(re.fullmatch(r"-[a-zA-Z]*f[a-zA-Z]*", f) for f in flags):
            return Verdict("always_pause", "force_push", ALWAYS_PAUSE["force_push"])
        if any(p.startswith("+") for p in positional):
            return Verdict("always_pause", "force_push", ALWAYS_PAUSE["force_push"])
        if "--delete" in flags or "-d" in flags or any(re.fullmatch(r":\S+", p) for p in positional):
            return Verdict("always_pause", "delete_data", ALWAYS_PAUSE["delete_data"])
        if "--mirror" in flags:
            return Verdict("always_pause", "force_push", ALWAYS_PAUSE["force_push"])
        targets = positional[1:] if len(positional) > 1 else []
        for target in targets:
            dest = target.split(":", 1)[1] if ":" in target else target
            dest = dest.removeprefix("refs/heads/")
            if dest in PROTECTED_BRANCHES or dest.startswith("release/"):
                return Verdict("action", "merge", f"push direct vers la branche protégée `{dest}`")
        if len(positional) <= 1 and current_branch(cwd) in PROTECTED_BRANCHES:
            return Verdict("action", "merge", "push de la branche protégée courante")
        return Verdict("action", "push", "git push")
    if sub == "commit":
        return Verdict("action", "commit", "git commit")
    if sub == "merge":
        branch = current_branch(cwd)
        if branch in PROTECTED_BRANCHES or branch.startswith("release/"):
            return Verdict("action", "merge", f"fusion dans la branche protégée `{branch}`")
        return None
    if sub == "branch" and ("-D" in rest or ("--delete" in rest and "--force" in rest) or any(re.fullmatch(r"-[a-zA-Z]*D[a-zA-Z]*", a) for a in rest)):
        return Verdict("always_pause", "delete_data", ALWAYS_PAUSE["delete_data"])
    if sub == "clean" and any(re.fullmatch(r"-[a-zA-Z]*f[a-zA-Z]*", a) or a == "--force" for a in rest):
        return Verdict("always_pause", "delete_data", ALWAYS_PAUSE["delete_data"])
    if sub in ("filter-branch", "filter-repo", "replace") or (sub == "reflog" and "expire" in rest) or (sub == "gc" and any(a.startswith("--prune") for a in rest)):
        return Verdict("always_pause", "rewrite_shared_history", ALWAYS_PAUSE["rewrite_shared_history"])
    if sub == "credential" or (sub == "config" and any("credential" in a for a in rest)):
        return Verdict("always_pause", "credentials", ALWAYS_PAUSE["credentials"])
    return None


def classify_gh(args: list[str]) -> Verdict | None:
    joined = " ".join(args[:2])
    if joined == "pr merge":
        return Verdict("action", "merge", "gh pr merge")
    if joined == "pr create":
        return Verdict("action", "open_pr", "gh pr create")
    if joined in ("pr comment", "pr review", "issue comment", "issue create", "issue close", "pr close"):
        return Verdict("action", "external_message", f"gh {joined}")
    if joined in ("release create", "release upload", "release edit"):
        return Verdict("action", "deploy", "publication d'une release GitHub")
    if joined in ("repo delete", "release delete") or (joined.startswith("repo") and "--delete" in args):
        return Verdict("always_pause", "delete_data", ALWAYS_PAUSE["delete_data"])
    if args[:1] == ["auth"] or joined == "secret set":
        return Verdict("always_pause", "credentials", ALWAYS_PAUSE["credentials"])
    if args[:1] == ["api"]:
        method = None
        for index, arg in enumerate(args):
            if arg in ("-X", "--method") and index + 1 < len(args):
                method = args[index + 1].upper()
            if arg in ("-f", "-F", "--field", "--raw-field", "--input"):
                method = method or "POST"
        if method and method != "GET":
            return Verdict("action", "external_message", f"gh api {method}")
    return None


def classify_rm(args: list[str], cwd: str) -> Verdict | None:
    recursive = any(a in ("--recursive",) or re.fullmatch(r"-[a-zA-Z]*[rR][a-zA-Z]*", a) for a in args if a.startswith("-"))
    if not recursive:
        return None
    targets = [a for a in args if not a.startswith("-")]
    if not targets:
        return None
    for target in targets:
        cleaned = target.strip("'\"")
        if ".." in cleaned.split("/"):
            return Verdict("always_pause", "delete_data", ALWAYS_PAUSE["delete_data"])
        if cleaned.startswith(("/tmp/", "/private/tmp/", "$TMPDIR", "${TMPDIR")):
            continue
        normalized = cleaned.rstrip("/")
        if not normalized.startswith("/") and os.path.basename(normalized) in SAFE_DELETE_BASENAMES:
            continue
        return Verdict("always_pause", "delete_data", ALWAYS_PAUSE["delete_data"])
    return None


def classify_credentials(head: str, args: list[str]) -> Verdict | None:
    first = args[0] if args else ""
    second = args[1] if len(args) > 1 else ""
    rules = {
        "aws": first == "configure" or (first == "sso" and second == "login"),
        "az": first == "login" or (first == "account" and second == "set"),
        "gcloud": first == "auth",
        "op": first in ("signin", "read", "item", "inject", "run"),
        "vault": first in ("login", "read", "kv", "write", "token"),
        "docker": first == "login",
        "npm": first in ("login", "adduser", "token"),
        "yarn": first == "login",
        "heroku": first in ("login", "authorizations"),
        "vercel": first == "login",
        "flyctl": first == "auth",
        "fly": first == "auth",
        "wrangler": first == "login",
        "doppler": first in ("login", "secrets"),
        "gpg": any(a.startswith("--export-secret") for a in args),
        "ssh-add": True,
        "security": first in ("find-generic-password", "find-internet-password"),
    }
    if rules.get(head):
        return Verdict("always_pause", "credentials", ALWAYS_PAUSE["credentials"])
    return None


def classify_deploy(head: str, args: list[str], lowered: str) -> Verdict | None:
    first = args[0] if args else ""
    second = args[1] if len(args) > 1 else ""
    table = {
        "terraform": first in ("apply", "destroy", "import", "taint"),
        "tofu": first in ("apply", "destroy"),
        "kubectl": first in ("apply", "delete", "rollout", "scale", "patch", "create", "replace", "drain", "cordon", "set"),
        "helm": first in ("install", "upgrade", "uninstall", "rollback", "delete"),
        "vercel": first in ("deploy", "--prod", "promote", "rollback") or "--prod" in args,
        "netlify": first == "deploy",
        "fly": first in ("deploy", "scale", "secrets", "machine"),
        "flyctl": first in ("deploy", "scale", "secrets", "machine"),
        "serverless": first in ("deploy", "remove"),
        "sls": first in ("deploy", "remove"),
        "cdk": first in ("deploy", "destroy"),
        "pulumi": first in ("up", "destroy", "refresh"),
        "gcloud": first in ("run", "app", "functions", "compute", "container") and "deploy" in args,
        "az": first in ("webapp", "functionapp", "containerapp", "aks", "vm") and second in ("up", "deploy", "create", "delete", "restart"),
        "aws": "deploy" in args or (first == "s3" and second == "sync" and "--delete" in args) or (first == "lambda" and second.startswith("update-function")),
        "heroku": first in ("releases:rollback", "ps:scale", "config:set", "container:release", "pipelines:promote"),
        "cap": "deploy" in args,
        "ansible-playbook": True,
        "wrangler": first in ("deploy", "publish"),
        "firebase": first == "deploy",
        "eb": first == "deploy",
        "railway": first in ("up", "deploy"),
        "docker": first == "push",
        "npm": first == "publish",
        "pnpm": first == "publish",
        "yarn": first == "publish" or (first == "npm" and second == "publish"),
        "cargo": first == "publish",
        "gem": first == "push",
        "twine": first == "upload",
        "poetry": first == "publish",
        "make": first == "deploy" or any(a in ("deploy", "release", "publish") for a in args),
        "just": first in ("deploy", "release", "publish"),
        "mise": first == "run" and second in ("deploy", "release", "publish"),
        "task": first in ("deploy", "release", "publish"),
    }
    if table.get(head):
        return Verdict("action", "deploy", f"{head} {first}".strip() + " (déploiement ou publication)")
    if head in ("npm", "pnpm", "yarn", "bun") and first == "run" and second in ("deploy", "release", "publish", "deploy:prod", "deploy:production"):
        return Verdict("action", "deploy", f"{head} run {second}")
    if DEPLOY_SCRIPT.search(head) or (head in ("bash", "sh", "python", "python3", "node") and args and DEPLOY_SCRIPT.search(args[0])):
        return Verdict("action", "deploy", "script de déploiement")
    return None


def classify_install(head: str, args: list[str], segment: str) -> Verdict | None:
    first = args[0] if args else ""
    if head in ("npm", "pnpm", "yarn", "bun"):
        if any(a in ("-g", "--global") for a in args) or (head == "yarn" and first == "global"):
            return Verdict("action", "install_global", f"{head} installation globale")
    if head in ("pip", "pip3", "python", "python3") and "install" in args and any(a in ("--user", "--break-system-packages") for a in args):
        return Verdict("action", "install_global", "pip installation utilisateur")
    if head in ("pipx", "brew", "apt", "apt-get", "dnf", "yum", "pacman", "zypper", "apk", "snap", "choco", "winget", "scoop", "port", "nix-env", "flatpak"):
        if first in ("install", "uninstall", "remove", "upgrade", "add", "del", "reinstall", "purge") or (head == "pacman" and first.startswith("-S")) or (head == "nix-env" and first in ("-i", "--install")):
            return Verdict("action", "install_global", f"{head} {first}")
    if head in ("cargo", "go") and first == "install":
        return Verdict("action", "install_global", f"{head} install")
    if head == "gem" and first == "install" and "--user-install" not in args:
        return Verdict("action", "install_global", "gem install")
    return None


def protected_path_write(segment: str, words: list[str], cwd: str, protected: list[str], trust_root: str) -> Verdict | None:
    if not protected and "trust.yaml" not in segment:
        return None
    normalized_words = [normalize_path(w, cwd, trust_root) for w in words]
    trust_candidates = (".azdone/trust.yaml", ".azdone/trust-ledger.md")
    all_protected = list(protected) + [".azdone/trust.yaml"]
    hits = [w for w in normalized_words if any(_path_matches(w, p) for p in all_protected)]
    if not hits:
        return None
    head = os.path.basename(words[0]) if words else ""
    has_redirect = re.search(r"(^|[^<>])>{1,2}\s*\S", segment) is not None
    is_read_only = head in READ_ONLY_COMMANDS and not has_redirect and not (head in ("sed", "perl") and any(a.startswith("-i") for a in words))
    if head == "git" and len(words) > 1 and words[1] in ("diff", "show", "log", "status", "blame", "grep", "ls-files"):
        is_read_only = True
    if is_read_only:
        return None
    if any(_path_matches(h, trust_candidates[0]) for h in hits):
        return Verdict("always_pause", "trust_file", ALWAYS_PAUSE["trust_file"])
    return Verdict("protected", "protected_path", f"écriture dans un chemin protégé ({hits[0]})")


def normalize_path(word: str, cwd: str, trust_root: str) -> str:
    cleaned = word.strip("'\"").split("=", 1)[-1] if word.startswith("--") else word.strip("'\"")
    if cleaned.startswith("/") and trust_root:
        root = trust_root.rstrip("/") + "/"
        if cleaned.startswith(root):
            return cleaned[len(root):]
        if cwd and cleaned.startswith(cwd.rstrip("/") + "/"):
            rel = cleaned[len(cwd.rstrip("/")) + 1:]
            rel_root = os.path.relpath(cwd, trust_root)
            return rel if rel_root == "." else os.path.normpath(os.path.join(rel_root, rel))
    if cleaned.startswith("./"):
        cleaned = cleaned[2:]
    return cleaned


def _path_matches(word: str, protected: str) -> bool:
    protected = protected.strip().lstrip("./")
    word = word.lstrip("./")
    if not protected or not word:
        return False
    if protected.endswith("/"):
        return word == protected.rstrip("/") or word.startswith(protected)
    return word == protected or word.startswith(protected + "/")


def current_branch(cwd: str) -> str:
    if not cwd or not os.path.isdir(cwd):
        return ""
    try:
        result = subprocess.run(
            ["git", "-C", cwd, "symbolic-ref", "--short", "-q", "HEAD"],
            capture_output=True, text=True, timeout=3, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    return result.stdout.strip() if result.returncode == 0 else ""


# --------------------------------------------------------------------------- décision

def decide(verdict: Verdict, policy: dict, trust_file: str, cwd: str = "") -> str | None:
    """Retourne None pour autoriser, sinon la raison du refus."""
    hint = " Voir /azd-setup ou éditer .azdone/trust.yaml."
    if verdict.kind == "always_pause":
        return (f"Action toujours-pause : {verdict.reason}. Non contournable, même avec actions.* en auto "
                f"ou autonomy: full. Un humain exécute cette commande lui-même s'il la veut.")
    if verdict.kind == "protected":
        return f"{verdict.reason} : ces chemins passent en ask quel que soit le niveau.{hint}"
    if verdict.action == "record_run":
        return None
    level = str(policy.get("autonomy", "assisted")).strip()
    defaults = LEVEL_DEFAULTS.get(level, LEVEL_DEFAULTS["assisted"])
    actions = policy.get("actions") if isinstance(policy.get("actions"), dict) else {}
    value = str(actions.get(verdict.action, defaults.get(verdict.action, "ask"))).strip().lower()
    if value == "auto":
        return None
    if value == "conditional":
        problem = check_witness(policy, trust_file, cwd)
        if problem is None:
            return None
        return (f"Action '{verdict.action}' est 'conditional' ({verdict.reason}) mais le témoin "
                f".azdone/conditions-ok ne satisfait pas la politique : {problem}.{hint}")
    return f"Action '{verdict.action}' est '{value}' dans la politique de confiance ({verdict.reason}).{hint}"


def read_witness(trust_file: str) -> dict | None:
    witness = os.path.join(os.path.dirname(trust_file), "conditions-ok")
    try:
        if not os.path.isfile(witness):
            return None
        age = time.time() - os.path.getmtime(witness)
        with open(witness, encoding="utf-8") as handle:
            lines = handle.read().splitlines()
    except (OSError, UnicodeDecodeError):
        return None
    data: dict = {"_age": age}
    for line in lines:
        key, sep, val = line.partition(":")
        if sep:
            data[key.strip()] = val.strip()
    return data


def check_witness(policy: dict, trust_file: str, cwd: str) -> str | None:
    """None si le témoin satisfait `conditions:`, sinon la première condition violée."""
    witness = read_witness(trust_file)
    if witness is None:
        return "aucun témoin (la review indépendante l'écrit sur accept)"
    if witness["_age"] >= WITNESS_MAX_AGE_SECONDS:
        return "témoin périmé (plus de 30 minutes)"
    conditions = policy.get("conditions") if isinstance(policy.get("conditions"), dict) else {}
    head = current_commit(cwd)
    if head and witness.get("commit") and not head.startswith(witness["commit"]) and not witness["commit"].startswith(head):
        return f"témoin écrit pour le commit {witness['commit'][:12]}, HEAD est {head[:12]}"
    if _truthy(conditions.get("require_green_ci", True)) and witness.get("ci") != "green":
        return f"ci: {witness.get('ci', 'absent')} (require_green_ci)"
    if _truthy(conditions.get("require_independent_review", True)):
        if witness.get("review") != "accept":
            return f"review: {witness.get('review', 'absent')} (require_independent_review)"
        if not witness.get("reviewer_id") or witness.get("reviewer_id") == witness.get("author_id"):
            return "reviewer_id absent ou égal à author_id (require_independent_review)"
    ceiling = str(conditions.get("risk_ceiling", "standard")).strip().lower()
    risk = str(witness.get("risk", "critical")).strip().lower()
    if RISK_ORDER.get(risk, 2) > RISK_ORDER.get(ceiling, 1):
        return f"risk: {risk} dépasse risk_ceiling: {ceiling}"
    for key, limit_key in (("files_changed", "max_files_changed"), ("lanes", "max_lanes")):
        limit = conditions.get(limit_key)
        if isinstance(limit, int) and limit > 0:
            try:
                actual = int(witness.get(key, "0"))
            except ValueError:
                return f"{key} illisible dans le témoin"
            if actual > limit:
                return f"{key}: {actual} dépasse {limit_key}: {limit}"
    return None


def _truthy(value) -> bool:
    return value is True or str(value).strip().lower() in ("true", "yes", "1")


def current_commit(cwd: str) -> str:
    if not cwd or not os.path.isdir(cwd):
        return ""
    try:
        result = subprocess.run(["git", "-C", cwd, "rev-parse", "HEAD"], capture_output=True, text=True, timeout=3, check=False)
    except (OSError, subprocess.SubprocessError):
        return ""
    return result.stdout.strip() if result.returncode == 0 else ""


def emit_deny(fmt: str, reason: str) -> None:
    if fmt == "claude":
        payload = {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                          "permissionDecisionReason": reason}}
    else:
        payload = {"permission": "deny", "user_message": reason, "agent_message": reason}
    sys.stdout.write(json.dumps(payload, ensure_ascii=False))
    sys.stdout.flush()


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] in ("record", "witness", "status"):
        return run_subcommand(sys.argv[1:])
    fmt, command, cwd, file_path = read_payload()
    trust_file = find_trust_file(cwd)
    if not trust_file:
        return 0
    try:
        with open(trust_file, encoding="utf-8") as handle:
            policy = parse_trust_yaml(handle.read())
    except (OSError, UnicodeDecodeError) as error:
        emit_deny(fmt, f"trust.yaml illisible ({error}) : refus fail-closed.")
        return 0
    if str(policy.get("enforcement", "declared")).strip().lower() != "enforced":
        return 0
    protected = [str(p) for p in policy.get("protected_paths")] if isinstance(policy.get("protected_paths"), list) else []
    trust_root = os.path.dirname(os.path.dirname(os.path.abspath(trust_file)))
    if file_path:
        verdict = classify_file_write(file_path, cwd, protected, trust_root)
        reason = decide(verdict, policy, trust_file, cwd) if verdict else None
        if reason:
            emit_deny(fmt, reason)
        return 0
    if not command.strip():
        return 0
    if PIPE_TO_SHELL.search(command):
        reason = decide(Verdict("action", "install_global", "script distant exécuté dans un shell"), policy, trust_file, cwd)
        if reason:
            emit_deny(fmt, reason)
            return 0
    for segment in split_segments(command):
        verdict = classify(segment, cwd, protected, trust_root)
        if verdict is None:
            continue
        reason = decide(verdict, policy, trust_file, cwd)
        if reason:
            emit_deny(fmt, reason)
            return 0
    return 0


# --------------------------------------------------------------------------- sous-commandes

def run_subcommand(argv: list[str]) -> int:
    import argparse

    parser = argparse.ArgumentParser(prog="azd-trust-guard.py", description="Journal de confiance AZDone.")
    sub = parser.add_subparsers(dest="command", required=True)
    witness = sub.add_parser("witness", help="écrire .azdone/conditions-ok après une review acceptée")
    witness.add_argument("--commit", required=True)
    witness.add_argument("--ci", required=True, choices=("green", "red", "unknown"))
    witness.add_argument("--review", required=True, choices=("accept", "return-to-build"))
    witness.add_argument("--reviewer-id", required=True)
    witness.add_argument("--author-id", required=True)
    witness.add_argument("--risk", required=True, choices=("rapid", "standard", "critical"))
    witness.add_argument("--files-changed", type=int, required=True)
    witness.add_argument("--lanes", type=int, default=0)
    witness.add_argument("--repo", default="")
    record = sub.add_parser("record", help="journaliser un run et appliquer la confiance gagnée")
    record.add_argument("--run-id", required=True)
    record.add_argument("--risk", required=True, choices=("rapid", "standard", "critical"))
    record.add_argument("--verdict", required=True, choices=("verified", "partial", "blocked", "failed"))
    record.add_argument("--rollback", action="store_true")
    record.add_argument("--override", default="")
    record.add_argument("--actions", default="")
    record.add_argument("--repo", default="")
    status = sub.add_parser("status", help="afficher le niveau, la série et le témoin")
    status.add_argument("--repo", default="")
    args = parser.parse_args(argv)

    repo = os.path.abspath(args.repo or os.getcwd())
    trust_file = find_trust_file(repo)
    if not trust_file:
        print("aucun .azdone/trust.yaml trouvé ; lancez /azd-setup", file=sys.stderr)
        return 2
    azdone_dir = os.path.dirname(trust_file)
    with open(trust_file, encoding="utf-8") as handle:
        policy = parse_trust_yaml(handle.read())

    if args.command == "witness":
        path = os.path.join(azdone_dir, "conditions-ok")
        if args.review != "accept":
            if os.path.exists(path):
                os.remove(path)
            print(f"témoin supprimé (review: {args.review})")
            return 0
        stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        values = {"commit": args.commit, "ci": args.ci, "review": args.review, "reviewer_id": args.reviewer_id,
                  "author_id": args.author_id, "risk": args.risk, "files_changed": str(args.files_changed),
                  "lanes": str(args.lanes), "written_at": stamp}
        with open(path, "w", encoding="utf-8") as handle:
            handle.write("".join(f"{key}: {values[key]}\n" for key in WITNESS_KEYS))
        problem = check_witness(policy, trust_file, repo)
        print(f"témoin écrit : {path}")
        print("conditions : satisfaites" if problem is None else f"conditions : non satisfaites ({problem})")
        return 0

    if args.command == "status":
        level = str(policy.get("autonomy", "assisted"))
        streak = ledger_streak(policy, azdone_dir)
        witness_data = read_witness(trust_file)
        problem = check_witness(policy, trust_file, repo)
        print(f"autonomy: {level}")
        print(f"ceiling: {policy.get('ceiling', 'full')}")
        print(f"enforcement: {policy.get('enforcement', 'declared')}")
        print(f"série verified: {streak}")
        print("témoin: " + ("absent" if witness_data is None else ("valide" if problem is None else f"invalide ({problem})")))
        return 0

    return record_run(args, policy, trust_file, azdone_dir)


def ledger_path(policy: dict, azdone_dir: str) -> str:
    earn = policy.get("earn") if isinstance(policy.get("earn"), dict) else {}
    configured = str(earn.get("ledger", ".azdone/trust-ledger.md"))
    root = os.path.dirname(azdone_dir)
    return configured if os.path.isabs(configured) else os.path.join(root, configured)


def ledger_rows(path: str) -> list[list[str]]:
    rows: list[list[str]] = []
    try:
        with open(path, encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line.startswith("|") or line.startswith("| ---") or line.startswith("| date"):
                    continue
                rows.append([cell.strip() for cell in line.strip("|").split("|")])
    except OSError:
        return []
    return rows


def ledger_streak(policy: dict, azdone_dir: str) -> int:
    streak = 0
    for row in reversed(ledger_rows(ledger_path(policy, azdone_dir))):
        if len(row) < 10:
            continue
        event = row[9]
        if event.startswith(("promotion:", "demotion:")):
            break
        if event != "run":
            continue
        if row[3] == "verified" and row[5] in ("non", "no", "false", ""):
            streak += 1
        else:
            break
    return streak


def record_run(args, policy: dict, trust_file: str, azdone_dir: str) -> int:
    path = ledger_path(policy, azdone_dir)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    existing = open(path, encoding="utf-8").read() if os.path.isfile(path) else ""
    if "| date |" not in existing:
        with open(path, "a", encoding="utf-8") as handle:
            if not existing.strip():
                handle.write("# Trust ledger AZDone\n\n")
            handle.write(LEDGER_HEADER + "\n" + LEDGER_SEPARATOR + "\n")
    level = str(policy.get("autonomy", "assisted")).strip()
    date = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    rollback = "oui" if args.rollback else "non"
    override = args.override.replace("|", "/") or "-"
    actions = args.actions.replace("|", "/") or "-"
    earn = policy.get("earn") if isinstance(policy.get("earn"), dict) else {}
    enabled = _truthy(earn.get("enabled", True))
    promote_after = int(earn.get("promote_after", 5) or 5)
    demote_on = earn.get("demote_on") if isinstance(earn.get("demote_on"), list) else ["failed", "rollback"]

    previous_streak = ledger_streak(policy, azdone_dir)
    if args.verdict == "verified" and not args.rollback:
        streak = previous_streak + 1
    else:
        streak = 0
    rows = [f"| {date} | {args.run_id} | {args.risk} | {args.verdict} | {actions} | {rollback} | {override} | {level} | {streak} | run |"]
    if args.override:
        rows.append(f"| {date} | {args.run_id} | {args.risk} | {args.verdict} | {actions} | {rollback} | {override} | {level} | {streak} | override-session |")

    new_level = level
    ceiling = str(policy.get("ceiling", "full")).strip()
    if enabled and level in LEVEL_ORDER:
        index = LEVEL_ORDER.index(level)
        ceiling_index = LEVEL_ORDER.index(ceiling) if ceiling in LEVEL_ORDER else len(LEVEL_ORDER) - 1
        should_demote = (args.verdict in demote_on) or (args.rollback and "rollback" in demote_on)
        if should_demote and index > 0:
            new_level = LEVEL_ORDER[index - 1]
            rows.append(f"| {date} | {args.run_id} | {args.risk} | {args.verdict} | - | {rollback} | - | {new_level} | 0 | demotion:{level}->{new_level} |")
        elif streak >= promote_after and index < ceiling_index:
            new_level = LEVEL_ORDER[index + 1]
            rows.append(f"| {date} | {args.run_id} | {args.risk} | {args.verdict} | - | {rollback} | - | {new_level} | 0 | promotion:{level}->{new_level} |")
    rows = [row for row in rows if row]
    with open(path, "a", encoding="utf-8") as handle:
        handle.write("\n".join(rows) + "\n")
    if new_level != level:
        rewrite_autonomy_line(trust_file, new_level)
    print(f"ledger: {path}")
    print(f"série verified: {streak}")
    print(f"autonomy: {level} -> {new_level}" if new_level != level else f"autonomy: {level}")
    return 0


def rewrite_autonomy_line(trust_file: str, new_level: str) -> None:
    """Ne réécrit que la ligne `autonomy:`, jamais le reste du fichier."""
    with open(trust_file, encoding="utf-8") as handle:
        lines = handle.read().splitlines(keepends=True)
    for index, line in enumerate(lines):
        if re.match(r"^autonomy:\s*", line):
            comment = ""
            if "#" in line:
                comment = "  #" + line.split("#", 1)[1].rstrip("\n")
            lines[index] = f"autonomy: {new_level}{comment}\n"
            break
    with open(trust_file, "w", encoding="utf-8") as handle:
        handle.writelines(lines)


if __name__ == "__main__":
    sys.exit(main())
