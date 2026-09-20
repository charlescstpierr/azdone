import unittest

from _skill_helpers import assert_language_rule, read_skill, read_skill_bundle


class AppVerificationSkillTests(unittest.TestCase):
    def test_skill_exists_with_expected_name_and_description(self) -> None:
        skill_text = read_skill("verifier-application-azd")

        self.assertRegex(skill_text, r"(?m)^name: verifier-application-azd$")
        self.assertNotIn("PROVISIONAL", skill_text)
        self.assertIn("Utiliser", skill_text)

    def test_three_modes_are_present(self) -> None:
        bundle = read_skill_bundle("verifier-application-azd")

        for mode in ("generer", "executer", "maintenir"):
            self.assertIn(f"`{mode}`", bundle)

    def test_bundle_covers_the_required_contract_tokens(self) -> None:
        bundle = read_skill_bundle("verifier-application-azd")
        assert_language_rule(self, bundle)
        self.assertNotIn("TODO", bundle)

        for contract in (
            "app_verification",
            "verifier-<app>",
            ".azdone/proofs/",
            "Jamais contre la production",
            "statut: never",
        ):
            self.assertIn(contract, bundle)

    def test_prove_skill_invokes_verify_application_executer(self) -> None:
        bundle = read_skill_bundle("prouver-resultat-azd")
        self.assertIn("$verifier-application-azd executer", bundle)

    def test_visual_proof_reference_exists_and_covers_the_manifest_schema(self) -> None:
        from pathlib import Path

        root = Path(__file__).resolve().parents[1]
        path = root / "skills/verifier-application-azd/references/preuve-visuelle.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")

        for token in ("manifest.json", "report.md", "redacted", "test_start", "assertion"):
            self.assertIn(token, text)

    def test_prove_bundle_cites_the_visual_proof_reference(self) -> None:
        bundle = read_skill_bundle("prouver-resultat-azd")
        self.assertIn("preuve-visuelle", bundle)

    def test_init_skill_invokes_verify_application_generer(self) -> None:
        bundle = read_skill_bundle("initialiser-projet-azd")
        self.assertIn("$verifier-application-azd generer", bundle)

    def test_reference_skills_doc_cites_the_new_skill(self) -> None:
        from pathlib import Path

        root = Path(__file__).resolve().parents[1]
        text = (root / "docs/reference-skills.md").read_text(encoding="utf-8")
        self.assertIn("verifier-application-azd", text)

    def test_prove_bundle_carries_the_app_verification_block(self) -> None:
        bundle = read_skill_bundle("prouver-resultat-azd")
        self.assertIn("app_verification", bundle)

    def test_watch_bundle_cites_verify_application_skill(self) -> None:
        bundle = read_skill_bundle("surveiller-livraison-azd")
        self.assertIn("verifier-application-azd", bundle)


if __name__ == "__main__":
    unittest.main()
