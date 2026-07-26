import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PublicDocumentationTests(unittest.TestCase):
    def test_required_public_documents_exist(self) -> None:
        required = (
            "README.md",
            "README.en.md",
            "CONTRIBUTING.md",
            "SECURITY.md",
            "SUPPORT.md",
            "CODE_OF_CONDUCT.md",
            "CHANGELOG.md",
            "docs/demarrage-rapide.md",
            "docs/installation.md",
            "docs/architecture.md",
            "docs/reference-skills.md",
            "docs/validation.md",
        )
        missing = [path for path in required if not (ROOT / path).is_file()]
        self.assertEqual([], missing)

    def test_readme_is_honest_about_runtime_pilot_and_license(self) -> None:
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        for token in (
            "Aucun runtime AZDone",
            "Pilot 0",
            "ne revendique ni supériorité",
            "public ne signifie pas encore open source",
        ):
            self.assertIn(token, text)

    def test_reference_lists_every_public_skill(self) -> None:
        reference = (ROOT / "docs/reference-skills.md").read_text(encoding="utf-8")
        skill_names = sorted(
            path.name
            for path in (ROOT / "skills").iterdir()
            if path.is_dir() and re.fullmatch(r"[a-z0-9-]+-azd", path.name)
        )
        self.assertEqual(16, len(skill_names))
        missing = [name for name in skill_names if f"`{name}`" not in reference]
        self.assertEqual([], missing)

    def test_installation_uses_official_project_scopes(self) -> None:
        text = (ROOT / "docs/installation.md").read_text(encoding="utf-8")
        self.assertIn(".agents/skills", text)
        self.assertIn(".claude/skills", text)
        self.assertIn("developers.openai.com/codex/skills", text)
        self.assertIn("code.claude.com/docs/en/skills", text)

    def test_issue_forms_have_required_metadata(self) -> None:
        for path in (
            ROOT / ".github/ISSUE_TEMPLATE/bug_report.yml",
            ROOT / ".github/ISSUE_TEMPLATE/feature_request.yml",
        ):
            text = path.read_text(encoding="utf-8")
            self.assertRegex(text, r"(?m)^name: .+")
            self.assertRegex(text, r"(?m)^description: .+")

    def test_relative_markdown_links_resolve(self) -> None:
        markdown_files = (
            ROOT / "README.md",
            ROOT / "README.en.md",
            ROOT / "CONTRIBUTING.md",
            ROOT / "SECURITY.md",
            ROOT / "SUPPORT.md",
            ROOT / "CODE_OF_CONDUCT.md",
            *(ROOT / "docs").glob("*.md"),
        )
        broken: list[str] = []
        for markdown in markdown_files:
            text = markdown.read_text(encoding="utf-8")
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
                if "://" in target or target.startswith("#"):
                    continue
                clean_target = target.split("#", 1)[0]
                if clean_target and not (markdown.parent / clean_target).resolve().exists():
                    broken.append(f"{markdown.relative_to(ROOT)} -> {target}")
        self.assertEqual([], broken)

    def test_public_surface_has_no_private_machine_paths(self) -> None:
        public_files = (
            ROOT / "README.md",
            ROOT / "README.en.md",
            ROOT / "CONTRIBUTING.md",
            ROOT / "SECURITY.md",
            ROOT / "SUPPORT.md",
            ROOT / "CODE_OF_CONDUCT.md",
            ROOT / "CHANGELOG.md",
            ROOT / "CONTRACTS.md",
            ROOT / "HOW_IT_WORKS.md",
            *(ROOT / "docs").glob("*.md"),
            *(ROOT / "skills").glob("**/*"),
        )
        leaked = []
        for path in public_files:
            if path.is_file() and "/Users/" in path.read_text(encoding="utf-8"):
                leaked.append(str(path.relative_to(ROOT)))
        self.assertEqual([], leaked)


if __name__ == "__main__":
    unittest.main()
