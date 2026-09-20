import re
import unittest

from _skill_helpers import assert_language_rule, normalized, read_skill, read_skill_bundle


class StructureSkillTests(unittest.TestCase):
    def test_skill_exists_with_expected_name_and_description(self) -> None:
        skill_text = read_skill("structurer-code-azd")

        self.assertRegex(skill_text, r"(?m)^name: structurer-code-azd$")
        self.assertNotIn("PROVISIONAL", skill_text)
        self.assertIn("Utiliser", skill_text)

    def test_bundle_covers_the_required_contract_tokens(self) -> None:
        bundle = read_skill_bundle("structurer-code-azd")
        assert_language_rule(self, bundle)
        self.assertNotIn("TODO", bundle)

        for token in (
            "data_shapes",
            "boundaries",
            "invariants",
            "adr_path",
            "verifiable_units",
            "machine à états",
            "supprimer avant d'ajouter",
        ):
            self.assertIn(token, bundle, token)

    def test_principles_reference_has_ten_titles(self) -> None:
        from pathlib import Path

        root = Path(__file__).resolve().parents[1]
        path = root / "skills/structurer-code-azd/references/principes-structure.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")

        titles = re.findall(r"(?m)^## \d+\.", text)
        self.assertEqual(10, len(titles))

    def test_pilot_cites_the_new_skill_as_conditional(self) -> None:
        bundle = read_skill_bundle("piloter-workflow-azd")

        self.assertIn("$structurer-code-azd", bundle)
        self.assertRegex(
            bundle, r"Appeler `?\$structurer-code-azd`? seulement lorsqu"
        )

    def test_pilot_conditional_rule_does_not_break_the_design_regex(self) -> None:
        # Chantier C froze this regex against piloter-workflow-azd/SKILL.md
        # for concevoir-experience-azd; the new conditional rule for
        # structurer-code-azd must never collide with it.
        skill_text = read_skill("piloter-workflow-azd")

        self.assertRegex(
            skill_text, r"Appeler `?\$concevoir-experience-azd`? seulement lorsqu"
        )
        self.assertIn(
            "Pour une sortie textuelle stable sans décision de design, omettre cette étape",
            skill_text,
        )

    def test_build_skill_cites_structure_skill(self) -> None:
        bundle = read_skill_bundle("construire-solution-azd")
        self.assertIn("structurer-code-azd", bundle)

    def test_reference_skills_doc_cites_the_new_skill(self) -> None:
        from pathlib import Path

        root = Path(__file__).resolve().parents[1]
        text = (root / "docs/reference-skills.md").read_text(encoding="utf-8")
        self.assertIn("structurer-code-azd", text)

    def test_trigger_sentence_is_identical_across_the_six_sources(self) -> None:
        from pathlib import Path

        root = Path(__file__).resolve().parents[1]
        trigger = (
            "lorsqu'un changement traverse une frontière de module, "
            "ajoute de l'état ou une forme de donnée, ou laisse le choix "
            "entre plusieurs structures"
        )
        sources = (
            "skills/structurer-code-azd/SKILL.md",
            "skills/piloter-workflow-azd/SKILL.md",
            "skills/azd/SKILL.md",
            "skills/azd/playbooks/changement-code.md",
            "docs/reference-skills.md",
            "docs/parcours.md",
        )
        for relative_path in sources:
            text = (root / relative_path).read_text(encoding="utf-8")
            # Markdown hard-wraps long lines; compare on whitespace-normalized
            # text so a line break inside the sentence does not fail this
            # otherwise byte-for-byte check against each raw file.
            self.assertIn(trigger, normalized(text), relative_path)
            self.assertNotIn("touche plus de trois fichiers", text, relative_path)


if __name__ == "__main__":
    unittest.main()
