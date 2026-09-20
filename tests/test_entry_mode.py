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
    "prototype.md",
    "surface-humaine.md",
    "release.md",
    "run-autonome.md",
    "reprise-de-session.md",
    "babysit-pr.md",
]

TRUST_SETUP_DIR = ROOT / "skills" / "azd-setup"
TRUST_POLICY = AZD_SKILL / "references" / "trust-policy.md"
TRUST_EXAMPLE = TRUST_SETUP_DIR / "references" / "trust.example.yaml"
MODEL_ROUTING = AZD_SKILL / "references" / "model-routing.md"
RUN_AUTONOME = AZD_SKILL / "playbooks" / "run-autonome.md"

VALID_AGENT_MODELS = {"haiku", "sonnet", "opus", "inherit"}
TOOLS_TOKEN = re.compile(r"^[A-Za-z][A-Za-z0-9]*(\([^)]*\))?$")

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
    ROOT / ".github" / "workflows",
]
EM_DASH_EXCLUDED_FILES = {
    ROOT / "hooks" / "azd-trust-guard.sh",
    ROOT / "hooks" / "azd-trust-guard.py",
}
CHANGELOG_PATH = ROOT / "CHANGELOG.md"
EM_DASH_SCAN_FILES = [
    ROOT / "docs" / "parcours.md",
    ROOT / "skills" / "verifier-application-azd" / "references" / "preuve-visuelle.md",
]


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

    def test_nine_playbooks_exist_are_short_and_carry_predicate_and_skill(self) -> None:
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

        for path in EM_DASH_SCAN_FILES:
            if path.is_file() and EM_DASH in read_text(path):
                failures.append(str(path.relative_to(ROOT)))

        self.assertEqual([], failures)

    def test_record_and_witness_cited_in_azd_skill(self) -> None:
        text = read_text(AZD_SKILL / "SKILL.md")
        self.assertIn("record", text)
        self.assertIn("witness", text)

    def test_decisions_tsv_header_with_tabs_in_run_autonome(self) -> None:
        self.assertTrue(RUN_AUTONOME.is_file())
        text = read_text(RUN_AUTONOME)
        header = "ts\trun_id\titeration\tdecision\talternative_rejetee\tpreuve\tpredicat_avance"
        self.assertIn(header, text)

    def test_ecriture_humaine_reference_exists_and_stays_short(self) -> None:
        path = AZD_SKILL / "references" / "ecriture-humaine.md"
        self.assertTrue(path.is_file())
        text = read_text(path)
        line_count = len(text.splitlines())
        self.assertLessEqual(line_count, 100, f"ecriture-humaine.md has {line_count} lines")

        tell_bullets = re.findall(r"(?m)^\d+\.\s", text)
        self.assertGreaterEqual(len(tell_bullets), 20, "expected at least 20 numbered tells")

    def test_ecriture_humaine_is_cited_by_deliver_and_retain_bundles(self) -> None:
        from _skill_helpers import read_skill_bundle

        for name in ("livrer-changement-azd", "conserver-apprentissages-azd"):
            bundle = read_skill_bundle(name)
            self.assertIn("ecriture-humaine", bundle, f"{name} bundle does not cite ecriture-humaine.md")


class TrustAndModelDocTests(unittest.TestCase):
    maxDiff = None

    def test_spawn_agent_present_in_trust_policy_and_example(self) -> None:
        failures = []
        for path in (TRUST_POLICY, TRUST_EXAMPLE):
            self.assertTrue(path.is_file(), f"missing {path}")
            if "spawn_agent" not in read_text(path):
                failures.append(f"{path.name}: missing spawn_agent")
        self.assertEqual([], failures)

    def test_cli_adapter_slug_grammar_and_panels_documented(self) -> None:
        failures = []
        grammar = "cli:<adaptateur>:<slug>"
        for path in (MODEL_ROUTING, TRUST_EXAMPLE):
            self.assertTrue(path.is_file(), f"missing {path}")
            text = read_text(path)
            if grammar not in text:
                failures.append(f"{path.name}: missing grammar {grammar!r}")
            if "panels" not in text:
                failures.append(f"{path.name}: missing 'panels'")
        self.assertEqual([], failures)

    def test_azd_setup_asks_and_outputs_ceiling(self) -> None:
        text = read_text(TRUST_SETUP_DIR / "SKILL.md")
        failures = []
        if "question" not in text.lower() or "`ceiling`" not in text:
            failures.append("azd-setup SKILL.md does not ask a ceiling question")
        if "ceiling:" not in text:
            failures.append("azd-setup SKILL.md output block missing ceiling:")
        if text.count("ceiling") < 2:
            failures.append("ceiling must appear in both the question and the output block")
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

    def test_agent_model_is_valid_and_tools_syntax_is_name_or_name_pattern(self) -> None:
        failures = []
        for name in AGENT_FILES:
            fm = frontmatter(read_text(AGENTS_DIR / name))
            model = fm.get("model")
            if model not in VALID_AGENT_MODELS:
                failures.append(f"{name}: model {model!r} not in {sorted(VALID_AGENT_MODELS)}")
            tools = fm.get("tools")
            if tools:
                for token in tools.split(","):
                    token = token.strip()
                    if not TOOLS_TOKEN.match(token):
                        failures.append(f"{name}: tools token {token!r} does not match Name or Name(pattern)")
        self.assertEqual([], failures)


if __name__ == "__main__":
    unittest.main()
