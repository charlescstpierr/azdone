import json
import os
import re
import stat
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRUST_EXAMPLE = ROOT / "skills" / "azd-setup" / "references" / "trust.example.yaml"
TRUST_POLICY = ROOT / "skills" / "azd" / "references" / "trust-policy.md"
HOOK = ROOT / "hooks" / "azd-trust-guard.sh"
HOOKS_JSON = ROOT / "hooks" / "hooks.json"
CURSOR_HOOKS_JSON = ROOT / "hooks" / "cursor-hooks.json"

LEVELS = ("guided", "assisted", "autonomous", "full")
ACTIONS = (
    "commit",
    "push",
    "open_pr",
    "merge",
    "deploy",
    "install_global",
    "credentials",
    "external_message",
    "delete_data",
    "rewrite_shared_history",
)
ALWAYS_PAUSE = (
    "force-push sur branche partagée",
    "suppression de données ou de branches non fusionnées",
    "mutation de production sans rollback prouvé",
    "message à un client ou à un tiers",
    "usage ou création de credentials",
    "élargissement de trust.yaml par l'agent lui-même",
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def minimal_yaml_parse(text: str):
    """Small indentation-based YAML subset parser: dict/list nesting, inline
    comments and inline [a, b] lists. Enough to sanity-check trust.example.yaml
    without any third-party dependency."""
    lines = []
    for raw in text.splitlines():
        content = raw.split(" #", 1)[0].rstrip()
        if not content.strip() or content.strip().startswith("#"):
            continue
        indent = len(content) - len(content.lstrip(" "))
        lines.append((indent, content.strip()))

    def parse_block(index: int, indent: int):
        container = None
        while index < len(lines):
            cur_indent, item = lines[index]
            if cur_indent < indent:
                break
            if cur_indent > indent:
                raise ValueError(f"unexpected indent before {item!r}")
            if item.startswith("- "):
                if container is None:
                    container = []
                if not isinstance(container, list):
                    raise ValueError(f"mixed list/dict at {item!r}")
                container.append(item[2:].strip())
                index += 1
                continue
            if ":" not in item:
                raise ValueError(f"expected 'key: value' at {item!r}")
            key, _, value = item.partition(":")
            key, value = key.strip(), value.strip()
            if not key:
                raise ValueError(f"empty key at {item!r}")
            if container is None:
                container = {}
            if not isinstance(container, dict):
                raise ValueError(f"mixed list/dict at {item!r}")
            if value == "":
                if index + 1 < len(lines) and lines[index + 1][0] > indent:
                    child, index = parse_block(index + 1, lines[index + 1][0])
                else:
                    child, index = {}, index + 1
                container[key] = child
            else:
                if value.startswith("[") and value.endswith("]"):
                    value = [v.strip() for v in value[1:-1].split(",") if v.strip()]
                container[key] = value
                index += 1
        return container, index

    if not lines:
        return {}
    root, _ = parse_block(0, lines[0][0])
    return root


def run_hook(payload: dict, trust_file: Path | None = None) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    if trust_file is not None:
        env["AZD_TRUST_FILE"] = str(trust_file)
    return subprocess.run(
        ["bash", str(HOOK)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        env=env,
        timeout=10,
    )


def write_trust_yaml(tmp_path: Path, enforcement: str = "enforced", **actions: str) -> Path:
    defaults = {
        "commit": "auto",
        "push": "ask",
        "open_pr": "ask",
        "merge": "ask",
        "deploy": "ask",
        "install_global": "ask",
        "credentials": "never",
        "external_message": "ask",
        "delete_data": "never",
        "rewrite_shared_history": "never",
    }
    defaults.update(actions)
    azdone_dir = tmp_path / ".azdone"
    azdone_dir.mkdir(parents=True, exist_ok=True)
    lines = [f"enforcement: {enforcement}", "actions:"]
    lines += [f"  {key}: {value}" for key, value in defaults.items()]
    trust_file = azdone_dir / "trust.yaml"
    trust_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return trust_file


def claude_payload(command: str, cwd: str = "/tmp") -> dict:
    return {
        "session_id": "s1",
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "tool_input": {"command": command},
        "cwd": cwd,
    }


def cursor_payload(command: str, cwd: str = "/tmp") -> dict:
    return {
        "hook_event_name": "beforeShellExecution",
        "command": command,
        "cwd": cwd,
        "workspace_roots": [cwd],
        "sandbox": "workspace-write",
        "conversation_id": "c1",
        "generation_id": "g1",
    }


class TrustExampleYamlTests(unittest.TestCase):
    def test_trust_example_is_valid_yaml(self) -> None:
        text = read(TRUST_EXAMPLE)
        try:
            import yaml  # type: ignore
        except ImportError:
            yaml = None

        if yaml is not None:
            data = yaml.safe_load(text)
            self.assertIsInstance(data, dict)
            self.assertIn("actions", data)
            self.assertIn("always_pause", data)
            return

        try:
            data = minimal_yaml_parse(text)
        except ValueError as exc:
            self.skipTest(f"no yaml module and minimal parser failed: {exc}")
            return
        self.assertIsInstance(data, dict)
        self.assertIn("actions", data)


class TrustPolicyVocabularyTests(unittest.TestCase):
    def test_four_levels_present_in_both_files(self) -> None:
        policy = read(TRUST_POLICY)
        example = read(TRUST_EXAMPLE)
        for level in LEVELS:
            self.assertIn(level, policy, f"missing level {level} in trust-policy.md")
        for level in ("guided", "assisted", "autonomous", "full"):
            self.assertIn(level, example, f"missing level {level} in trust.example.yaml")

    def test_ten_actions_present_in_both_files(self) -> None:
        policy = read(TRUST_POLICY)
        example = read(TRUST_EXAMPLE)
        for action in ACTIONS:
            self.assertIn(action, policy, f"missing action {action} in trust-policy.md")
            self.assertIn(f"{action}:", example, f"missing action {action} in trust.example.yaml")

    def test_action_values_present(self) -> None:
        policy = read(TRUST_POLICY)
        for value in ("auto", "conditional", "ask", "never"):
            self.assertIn(value, policy)

    def test_always_pause_list_present_in_both_files(self) -> None:
        policy = read(TRUST_POLICY)
        example = read(TRUST_EXAMPLE)
        for entry in ALWAYS_PAUSE:
            self.assertIn(entry, policy, f"missing always_pause entry in trust-policy.md: {entry}")
            self.assertIn(entry, example, f"missing always_pause entry in trust.example.yaml: {entry}")

    def test_protected_paths_present(self) -> None:
        example = read(TRUST_EXAMPLE)
        for path in (".azdone/trust.yaml", ".github/workflows/", "infra/"):
            self.assertIn(path, example)


class HookClassificationTests(unittest.TestCase):
    def test_declared_allows_git_push(self) -> None:
        with self._tmp() as tmp:
            trust = write_trust_yaml(tmp, enforcement="declared", push="ask")
            result = run_hook(claude_payload("git push"), trust_file=trust)
            self.assertEqual(0, result.returncode)
            self.assertEqual("", result.stdout.strip())

    def test_enforced_push_auto_allows(self) -> None:
        with self._tmp() as tmp:
            trust = write_trust_yaml(tmp, push="auto")
            result = run_hook(claude_payload("git push"), trust_file=trust)
            self.assertEqual(0, result.returncode)
            self.assertEqual("", result.stdout.strip())

    def test_enforced_push_ask_denies(self) -> None:
        with self._tmp() as tmp:
            trust = write_trust_yaml(tmp, push="ask")
            result = run_hook(claude_payload("git push"), trust_file=trust)
            self.assertEqual(0, result.returncode)
            data = json.loads(result.stdout)
            self.assertEqual(
                "deny", data["hookSpecificOutput"]["permissionDecision"]
            )

    def test_enforced_merge_conditional_without_witness_denies(self) -> None:
        with self._tmp() as tmp:
            trust = write_trust_yaml(tmp, merge="conditional")
            result = run_hook(claude_payload("git merge origin/main"), trust_file=trust)
            data = json.loads(result.stdout)
            self.assertEqual("deny", data["hookSpecificOutput"]["permissionDecision"])

    def test_enforced_merge_conditional_with_fresh_witness_allows(self) -> None:
        with self._tmp() as tmp:
            trust = write_trust_yaml(tmp, merge="conditional")
            (trust.parent / "conditions-ok").write_text("ok", encoding="utf-8")
            result = run_hook(claude_payload("gh pr merge 42"), trust_file=trust)
            self.assertEqual(0, result.returncode)
            self.assertEqual("", result.stdout.strip())

    def test_force_push_denies_even_with_everything_auto(self) -> None:
        with self._tmp() as tmp:
            trust = write_trust_yaml(
                tmp,
                push="auto",
                merge="auto",
                deploy="auto",
                install_global="auto",
                open_pr="auto",
            )
            result = run_hook(claude_payload("git push --force origin main"), trust_file=trust)
            data = json.loads(result.stdout)
            self.assertEqual("deny", data["hookSpecificOutput"]["permissionDecision"])

    def test_rm_rf_under_tmp_allows(self) -> None:
        with self._tmp() as tmp:
            trust = write_trust_yaml(tmp)
            result = run_hook(claude_payload("rm -rf /tmp/x"), trust_file=trust)
            self.assertEqual(0, result.returncode)
            self.assertEqual("", result.stdout.strip())

    def test_terraform_apply_with_deploy_ask_denies(self) -> None:
        with self._tmp() as tmp:
            trust = write_trust_yaml(tmp, deploy="ask")
            result = run_hook(claude_payload("terraform apply"), trust_file=trust)
            data = json.loads(result.stdout)
            self.assertEqual("deny", data["hookSpecificOutput"]["permissionDecision"])

    def test_cursor_format_deny_output_shape(self) -> None:
        with self._tmp() as tmp:
            trust = write_trust_yaml(tmp, push="ask")
            result = run_hook(cursor_payload("git push"), trust_file=trust)
            self.assertEqual(0, result.returncode)
            data = json.loads(result.stdout)
            self.assertEqual("deny", data["permission"])
            self.assertIn("user_message", data)
            self.assertIn("agent_message", data)

    def test_claude_format_deny_output_shape(self) -> None:
        with self._tmp() as tmp:
            trust = write_trust_yaml(tmp, push="ask")
            result = run_hook(claude_payload("git push"), trust_file=trust)
            data = json.loads(result.stdout)
            self.assertIn("hookSpecificOutput", data)
            self.assertEqual("deny", data["hookSpecificOutput"]["permissionDecision"])

    def test_harmless_ls_allows_silently(self) -> None:
        with self._tmp() as tmp:
            trust = write_trust_yaml(tmp)
            result = run_hook(claude_payload("ls -la"), trust_file=trust)
            self.assertEqual(0, result.returncode)
            self.assertEqual("", result.stdout.strip())

    def test_cursor_format_is_not_confused_by_its_own_hook_event_name(self) -> None:
        # Cursor payloads also carry hook_event_name; the hook must still treat
        # them as Cursor (snake_case output), not Claude Code.
        with self._tmp() as tmp:
            trust = write_trust_yaml(tmp, deploy="ask")
            result = run_hook(cursor_payload("terraform apply"), trust_file=trust)
            data = json.loads(result.stdout)
            self.assertEqual("deny", data["permission"])
            self.assertNotIn("hookSpecificOutput", data)

    class _tmp:
        def __enter__(self):
            import tempfile

            self._ctx = tempfile.TemporaryDirectory()
            return Path(self._ctx.name)

        def __exit__(self, *exc):
            self._ctx.cleanup()
            return False


class HookManifestTests(unittest.TestCase):
    def test_hooks_json_is_valid_and_points_to_guard_script(self) -> None:
        data = json.loads(read(HOOKS_JSON))
        text = read(HOOKS_JSON)
        self.assertIn("azd-trust-guard.sh", text)
        self.assertIn("PreToolUse", data["hooks"])

    def test_cursor_hooks_json_is_valid_and_points_to_guard_script(self) -> None:
        data = json.loads(read(CURSOR_HOOKS_JSON))
        text = read(CURSOR_HOOKS_JSON)
        self.assertIn("azd-trust-guard.sh", text)
        self.assertIn("beforeShellExecution", data["hooks"])

    def test_guard_script_has_valid_bash_syntax(self) -> None:
        result = subprocess.run(["bash", "-n", str(HOOK)], capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stderr)


class SkillPackagingTests(unittest.TestCase):
    def test_no_executable_file_under_azd_setup_skill(self) -> None:
        skill_dir = ROOT / "skills" / "azd-setup"
        executables = []
        for path in skill_dir.rglob("*"):
            if path.is_file() and (path.stat().st_mode & stat.S_IXUSR):
                executables.append(str(path.relative_to(ROOT)))
        self.assertEqual([], executables)


if __name__ == "__main__":
    unittest.main()
