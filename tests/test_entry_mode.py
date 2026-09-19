import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AZD_SKILL = ROOT / "skills" / "azd"
AGENTS_DIR = ROOT / "agents"

PLAYBOOKS = [
    "changement-code.md",
    "correction-bug.md",
    "investigation.md",
    "surface-humaine.md",
    "release.md",
    "run-autonome.md",
    "reprise-de-session.md",
    "babysit-pr.md",
]

AGENT_FILES = [
    "azd-scout.md",
    "azd-builder.md",
    "azd-verifier.md",
    "azd-reviewer.md",
    "azd-watcher.md",
]

READONLY_AGENTS = ["azd-scout.md", "azd-reviewer.md", "azd-watcher.md"]

AGENT_ROLE_WORDS = ["azd-scout", "azd-builder", "azd-verifier", "azd-reviewer", "azd-watcher"]

EM_DASH = "—"

# Style rule (no em dash) extended to every path this work touched. hooks/azd-trust-guard.sh
# and hooks/azd-trust-guard.py are excluded: they are owned by a parallel, in-flight
# workstream rewriting the hook (same reason tests/test_trust_policy.py is allowed to be
# red in the meantime); they are not edited here.
EM_DASH_SCAN_ROOTS = [
    AZD_SKILL,
    ROOT / "skills" / "azd-setup",
    AGENTS_DIR,
    ROOT / "hooks",
    ROOT / "scripts",
    ROOT / "docs" / "guide",
]
EM_DASH_EXCLUDED_FILES = {
    ROOT / "hooks" / "azd-trust-guard.sh",
    ROOT / "hooks" / "azd-trust-guard.py",
}
CHANGELOG_PATH = ROOT / "CHANGELOG.md"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return {}
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        # strip trailing inline comments (e.g. "mode: true  # Cursor : mode collant")
        value = value.split("#", 1)[0]
        values[key.strip()] = value.strip().strip('"')
    return values


class EntryModeSkillTests(unittest.TestCase):
    maxDiff = None

    def test_skill_md_exists(self) -> None:
        self.assertTrue((AZD_SKILL / "SKILL.md").is_file())

    def test_frontmatter_has_required_entry_mode_fields(self) -> None:
        text = read_text(AZD_SKILL / "SKILL.md")
        fm = frontmatter(text)
        self.assertEqual("azd", fm.get("name"))
        self.assertEqual("true", fm.get("disable-model-invocation"))
        self.assertEqual("true", fm.get("mode"))

    def test_skill_md_stays_within_120_lines(self) -> None:
        text = read_text(AZD_SKILL / "SKILL.md")
        line_count = len(text.splitlines())
        self.assertLessEqual(line_count, 120, f"SKILL.md has {line_count} lines")

    def test_eight_playbooks_exist_are_short_and_carry_predicate_and_skill(self) -> None:
        failures = []
        skill_ref = re.compile(r"\$[a-z][a-z0-9-]*-azd\b")

        for name in PLAYBOOKS:
            path = AZD_SKILL / "playbooks" / name
            if not path.is_file():
                failures.append(f"{name}: missing playbook file")
                continue
            text = read_text(path)
            line_count = len(text.splitlines())
            if line_count > 35:
                failures.append(f"{name}: {line_count} lines exceeds 35")
            if not skill_ref.search(text):
                failures.append(f"{name}: does not cite a $...-azd skill")
            if "Prédicat" not in text:
                failures.append(f"{name}: missing 'Prédicat'")

        self.assertEqual([], failures)

    def test_skill_md_references_every_playbook_by_path(self) -> None:
        text = read_text(AZD_SKILL / "SKILL.md")
        failures = []
        for name in PLAYBOOKS:
            if f"playbooks/{name}" not in text:
                failures.append(f"SKILL.md does not reference playbooks/{name}")
        self.assertEqual([], failures)

    def test_skill_md_mentions_trust_policy_and_agent_roles(self) -> None:
        text = read_text(AZD_SKILL / "SKILL.md")
        failures = []

        if ".azdone/trust.yaml" not in text:
            failures.append("missing .azdone/trust.yaml")

        for token in ["auto", "conditional", "ask", "never"]:
            if not re.search(rf"`{token}`", text):
                failures.append(f"missing action level token: {token}")

        if "always_pause" not in text and "toujours-pause" not in text.lower():
            failures.append("missing always_pause / toujours-pause")

        for role in AGENT_ROLE_WORDS:
            if role not in text:
                failures.append(f"missing agent role mention: {role}")

        self.assertEqual([], failures)

    def test_context_packet_reference_stays_within_60_lines(self) -> None:
        path = AZD_SKILL / "references" / "context-packet.md"
        self.assertTrue(path.is_file())
        line_count = len(read_text(path).splitlines())
        self.assertLessEqual(line_count, 60, f"context-packet.md has {line_count} lines")

    def test_model_routing_reference_contains_verified_cli_forms(self) -> None:
        path = AZD_SKILL / "references" / "model-routing.md"
        self.assertTrue(path.is_file())
        text = read_text(path)
        for token in ["codex exec", "claude -p", "agent -p", "adapter-unavailable"]:
            self.assertIn(token, text, f"model-routing.md missing {token!r}")

    def test_language_rule_is_present_in_skill_md(self) -> None:
        text = read_text(AZD_SKILL / "SKILL.md")
        self.assertIn("langue de l'utilisateur", text)

    def test_no_em_dash_anywhere_in_azd_entry_mode_files(self) -> None:
        failures = []
        seen: set[Path] = set()
        for root in EM_DASH_SCAN_ROOTS:
            for path in root.rglob("*"):
                if not path.is_file() or path in seen or path in EM_DASH_EXCLUDED_FILES:
                    continue
                if "__pycache__" in path.parts:
                    continue
                seen.add(path)
                try:
                    text = read_text(path)
                except UnicodeDecodeError:
                    continue  # binary file, not source text
                if EM_DASH in text:
                    failures.append(str(path.relative_to(ROOT)))

        if CHANGELOG_PATH.is_file():
            for lineno, line in enumerate(read_text(CHANGELOG_PATH).splitlines(), start=1):
                if "0.1.0-preview" in line:
                    continue
                if EM_DASH in line:
                    failures.append(f"CHANGELOG.md:{lineno}")

        self.assertEqual([], failures)


class SubagentDefinitionTests(unittest.TestCase):
    maxDiff = None

    def test_all_five_agent_files_exist(self) -> None:
        for name in AGENT_FILES:
            self.assertTrue((AGENTS_DIR / name).is_file(), f"missing agents/{name}")

    def test_agent_frontmatter_has_name_description_model(self) -> None:
        failures = []
        for name in AGENT_FILES:
            path = AGENTS_DIR / name
            fm = frontmatter(read_text(path))
            for key in ("name", "description", "model"):
                if not fm.get(key):
                    failures.append(f"{name}: missing {key}")
        self.assertEqual([], failures)

    def test_readonly_agents_declare_readonly_true(self) -> None:
        failures = []
        for name in READONLY_AGENTS:
            fm = frontmatter(read_text(AGENTS_DIR / name))
            if fm.get("readonly") != "true":
                failures.append(f"{name}: readonly is not true")
        self.assertEqual([], failures)

    def test_model_tiers_match_design(self) -> None:
        expected = {
            "azd-scout.md": "haiku",
            "azd-builder.md": "sonnet",
            "azd-verifier.md": "sonnet",
            "azd-reviewer.md": "opus",
            "azd-watcher.md": "haiku",
        }
        failures = []
        for name, model in expected.items():
            fm = frontmatter(read_text(AGENTS_DIR / name))
            if fm.get("model") != model:
                failures.append(f"{name}: expected model {model}, got {fm.get('model')}")
        self.assertEqual([], failures)


if __name__ == "__main__":
    unittest.main()
