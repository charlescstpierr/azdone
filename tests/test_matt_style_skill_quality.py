import os
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"


def skill_dirs() -> list[Path]:
    return sorted(
        path
        for path in SKILLS.iterdir()
        if path.is_dir() and re.fullmatch(r"[a-z0-9-]+-azd", path.name)
    )


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
        values[key.strip()] = value.strip().strip('"')
    return values


def default_prompt(openai_yaml: Path) -> str:
    match = re.search(r'(?m)^\s*default_prompt:\s*"(.*)"\s*$', read_text(openai_yaml))
    if not match:
        return ""
    return match.group(1)


class MattStyleSkillQualityTests(unittest.TestCase):
    maxDiff = None

    def test_all_16_azdone_skill_directories_are_present(self) -> None:
        self.assertEqual(16, len(skill_dirs()))

    def test_descriptions_explain_capability_and_use_when_trigger(self) -> None:
        failures = []

        for skill in skill_dirs():
            description = frontmatter(read_text(skill / "SKILL.md")).get("description", "")
            if not description:
                failures.append(f"{skill.name}: missing description")
                continue
            if len(description) > 1024:
                failures.append(f"{skill.name}: description exceeds 1024 chars")
            if "Use when" not in description and "Utiliser" not in description:
                failures.append(f"{skill.name}: description must include an explicit use trigger")
            if len(description.split()) < 10:
                failures.append(f"{skill.name}: description is too thin to explain capability")

        self.assertEqual([], failures)

    def test_skill_markdown_stays_concise_or_splits_reference_material(self) -> None:
        failures = []

        for skill in skill_dirs():
            skill_md = skill / "SKILL.md"
            line_count = len(read_text(skill_md).splitlines())
            has_reference_split = (skill / "references").is_dir()
            line_limit = 120 if has_reference_split else 100
            if line_count > line_limit:
                split_note = "with references/ split" if has_reference_split else "without references/ split"
                failures.append(f"{skill.name}: {line_count} lines exceeds {line_limit} {split_note}")

        self.assertEqual([], failures)

    def test_each_skill_has_quick_start_or_concrete_invocation_example(self) -> None:
        failures = []

        for skill in skill_dirs():
            text = read_text(skill / "SKILL.md")
            skill_name = frontmatter(text).get("name", skill.name)
            has_quick_start = re.search(r"(?im)^##\s+quick[- ]start\b", text) is not None
            has_example = re.search(r"(?im)^##\s+(examples?|exemples?)\b", text) is not None
            has_concrete_example = re.search(
                rf"(?is)(^##\s+(examples?|exemples?)\b|\b(example|exemple)\b.*\${re.escape(skill_name)})",
                text,
            ) is not None
            if not (has_quick_start or has_example or has_concrete_example):
                failures.append(f"{skill.name}: missing Quick start or concrete example")

        self.assertEqual([], failures)

    def test_openai_default_prompt_uses_exact_skill_name(self) -> None:
        failures = []

        for skill in skill_dirs():
            name = frontmatter(read_text(skill / "SKILL.md")).get("name", skill.name)
            prompt = default_prompt(skill / "agents" / "openai.yaml")
            if f"${name}" not in prompt:
                failures.append(f"{skill.name}: default_prompt does not include exact ${name}")

        self.assertEqual([], failures)

    def test_references_are_one_level_deep_and_existing(self) -> None:
        failures = []

        for skill in skill_dirs():
            text = read_text(skill / "SKILL.md")
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
                if re.match(r"^[a-z]+://", target) or target.startswith("#"):
                    continue
                target_path = Path(target)
                if target_path.is_absolute() or ".." in target_path.parts:
                    failures.append(f"{skill.name}: unsafe reference {target}")
                    continue
                if len(target_path.parts) > 2:
                    failures.append(f"{skill.name}: reference too deep {target}")
                if not (skill / target_path).exists():
                    failures.append(f"{skill.name}: missing reference {target}")

        self.assertEqual([], failures)

    def test_skills_do_not_add_runtime_scripts_or_executables(self) -> None:
        failures = []

        allowed = {"SKILL.md", "agents/openai.yaml"}
        for skill in skill_dirs():
            for path in skill.rglob("*"):
                if not path.is_file():
                    continue
                relative = path.relative_to(skill).as_posix()
                if relative in allowed or relative.startswith("references/"):
                    continue
                failures.append(f"{skill.name}: unexpected runtime artifact {relative}")
                if os.access(path, os.X_OK):
                    failures.append(f"{skill.name}: executable artifact {relative}")

        self.assertEqual([], failures)

    def test_routing_remains_domain_agnostic_and_m05_is_conditional(self) -> None:
        m01 = read_text(SKILLS / "piloter-workflow-azd" / "SKILL.md")
        m02 = read_text(SKILLS / "clarifier-objectif-azd" / "SKILL.md")
        m03 = read_text(SKILLS / "inspecter-projet-azd" / "SKILL.md")
        m06 = read_text(SKILLS / "planifier-travail-azd" / "SKILL.md")

        domain_terms = (
            ("product", "produit"),
            ("backend",),
            ("infra",),
            ("data",),
            ("mobile",),
            ("desktop",),
            ("web",),
            ("CLI",),
            ("docs",),
        )

        for skill_name, text in (
            ("clarifier-objectif-azd", m02),
            ("inspecter-projet-azd", m03),
            ("planifier-travail-azd", m06),
        ):
            self.assertIn("domain-agnostic", text, skill_name)
            for aliases in domain_terms:
                self.assertTrue(
                    any(alias in text for alias in aliases),
                    f"{skill_name}: missing domain alias from {aliases}",
                )

        self.assertIn("$concevoir-experience-azd", m01)
        self.assertRegex(m01, r"Appeler `?\$concevoir-experience-azd`? seulement lorsqu")
        self.assertIn("Pour une sortie textuelle stable sans décision de design, omettre cette étape", m01)
        self.assertIn("contrat DevEx CLI/API/SDK seulement si pertinent", m06)


if __name__ == "__main__":
    unittest.main()
