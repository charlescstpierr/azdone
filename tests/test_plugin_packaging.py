import json
import re
import stat
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class PluginManifestTests(unittest.TestCase):
    def test_manifests_and_marketplace_are_valid_json(self) -> None:
        for path in (
            ROOT / ".claude-plugin/plugin.json",
            ROOT / ".claude-plugin/marketplace.json",
            ROOT / ".cursor-plugin/plugin.json",
        ):
            self.assertTrue(path.is_file(), f"missing manifest: {path}")
            _load_json(path)  # raises on invalid JSON

    def test_manifest_names_are_azdone(self) -> None:
        claude = _load_json(ROOT / ".claude-plugin/plugin.json")
        cursor = _load_json(ROOT / ".cursor-plugin/plugin.json")
        marketplace = _load_json(ROOT / ".claude-plugin/marketplace.json")
        self.assertEqual("azdone", claude["name"])
        self.assertEqual("azdone", cursor["name"])
        self.assertEqual("azdone", marketplace["name"])
        plugin_names = [plugin.get("name") for plugin in marketplace.get("plugins", [])]
        self.assertIn("azdone", plugin_names)

    def test_manifests_share_version_present_in_changelog(self) -> None:
        claude = _load_json(ROOT / ".claude-plugin/plugin.json")
        cursor = _load_json(ROOT / ".cursor-plugin/plugin.json")
        version = claude.get("version")
        self.assertTrue(version, "claude plugin.json must declare a version")
        self.assertEqual(version, cursor.get("version"))
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn(version, changelog)

    def test_manifests_never_invent_a_license(self) -> None:
        # The project has not chosen a reuse license yet: the manifests must
        # not fabricate one (see README.md "Licence").
        claude = _load_json(ROOT / ".claude-plugin/plugin.json")
        cursor = _load_json(ROOT / ".cursor-plugin/plugin.json")
        self.assertNotIn("license", claude)
        self.assertNotIn("license", cursor)

    def test_declared_paths_exist_when_parallel_workstream_is_ready(self) -> None:
        # hooks/ and agents/ are written by other, parallel workstreams
        # (chantiers T and E). Only assert their contents once hooks/ exists,
        # so this suite stays green while that work is still in flight.
        hooks_dir = ROOT / "hooks"
        if not hooks_dir.is_dir():
            self.skipTest(
                "hooks/ does not exist yet (owned by a parallel workstream); "
                "skipping hooks/agents path checks until it lands"
            )
        for relative in ("hooks/hooks.json", "hooks/cursor-hooks.json"):
            self.assertTrue((ROOT / relative).is_file(), f"missing {relative}")
        self.assertTrue((ROOT / "agents").is_dir(), "missing agents/ directory")


class InstallScriptTests(unittest.TestCase):
    def setUp(self) -> None:
        self.script = ROOT / "scripts/install.sh"
        self.assertTrue(self.script.is_file(), "scripts/install.sh must exist")
        self.text = self.script.read_text(encoding="utf-8")

    def test_is_executable(self) -> None:
        mode = self.script.stat().st_mode
        self.assertTrue(mode & stat.S_IXUSR, "scripts/install.sh must be executable")

    def test_uses_strict_mode(self) -> None:
        self.assertIn("set -euo pipefail", self.text)

    def test_never_force_removes(self) -> None:
        self.assertNotIn("rm -rf", self.text)

    def test_passes_bash_syntax_check(self) -> None:
        result = subprocess.run(
            ["bash", "-n", str(self.script)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stderr)


class GuideTests(unittest.TestCase):
    EXPECTED_PAGES = (
        "README.md",
        "01-installation.md",
        "02-azd.md",
        "03-confiance.md",
        "04-modeles-et-sous-agents.md",
        "05-comprendre-et-concevoir.md",
        "06-construire-prouver-livrer.md",
        "07-run-autonome.md",
        "08-recettes-et-pieges.md",
    )

    def test_guide_has_every_page(self) -> None:
        guide_dir = ROOT / "docs/guide"
        missing = [name for name in self.EXPECTED_PAGES if not (guide_dir / name).is_file()]
        self.assertEqual([], missing)

    def test_guide_relative_links_resolve(self) -> None:
        guide_dir = ROOT / "docs/guide"
        broken: list[str] = []
        for markdown in guide_dir.glob("*.md"):
            text = markdown.read_text(encoding="utf-8")
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
                if "://" in target or target.startswith("#"):
                    continue
                clean_target = target.split("#", 1)[0]
                if clean_target and not (markdown.parent / clean_target).resolve().exists():
                    broken.append(f"{markdown.relative_to(ROOT)} -> {target}")
        self.assertEqual([], broken)


class ReadmeMentionsEntryLayerTests(unittest.TestCase):
    def test_readmes_mention_entry_layer_and_trust_file(self) -> None:
        for name in ("README.md", "README.en.md"):
            text = (ROOT / name).read_text(encoding="utf-8")
            self.assertIn("/azd", text, f"{name} must mention /azd")
            self.assertIn("/azd-setup", text, f"{name} must mention /azd-setup")
            self.assertIn("trust.yaml", text, f"{name} must mention trust.yaml")


if __name__ == "__main__":
    unittest.main()
