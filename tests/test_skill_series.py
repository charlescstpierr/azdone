import re
import unittest

from _skill_helpers import assert_language_rule, read_skill, read_skill_bundle


class SkillSeriesContractTests(unittest.TestCase):
    def test_entry_skill_routes_the_complete_verified_journey(self) -> None:
        skill_text = read_skill("piloter-workflow-azd")
        bundle = read_skill_bundle("piloter-workflow-azd")

        self.assertRegex(skill_text, r"(?m)^name: piloter-workflow-azd$")
        self.assertNotIn("PROVISIONAL", skill_text)
        assert_language_rule(self, bundle)

        for skill in (
            "clarifier-objectif-azd",
            "inspecter-projet-azd",
            "diagnostiquer-probleme-azd",
            "concevoir-experience-azd",
            "planifier-travail-azd",
            "isoler-travail-azd",
            "construire-solution-azd",
            "prouver-resultat-azd",
            "reviser-qualite-azd",
            "livrer-changement-azd",
            "surveiller-livraison-azd",
            "conserver-apprentissages-azd",
            "ameliorer-workflow-azd",
        ):
            self.assertIn(f"${skill}", bundle)

        for guarantee in (
            "same repository",
            "worktree",
            "subagent",
            "UI",
            "prototype",
            "evidence",
            "resume",
            "authority",
        ):
            self.assertIn(guarantee, bundle)

        self.assertRegex(bundle, re.compile(r"partial|blocked|failed", re.IGNORECASE))
        self.assertIn("au plus une question matérielle", bundle)
        self.assertIn("$inspecter-projet-azd` avant le diagnostic, le design, le plan ou le code", bundle)

    def test_build_skill_is_final_bilingual_and_tdd_first(self) -> None:
        skill_text = read_skill("construire-solution-azd")
        bundle = read_skill_bundle("construire-solution-azd")

        self.assertRegex(skill_text, r"(?m)^name: construire-solution-azd$")
        self.assertNotIn("PROVISIONAL", skill_text)
        assert_language_rule(self, bundle)
        self.assertIn("TDD", bundle)
        self.assertIn("smallest valid change", bundle)
        self.assertIn("Ponytail", bundle)
        self.assertIn("evidence", bundle)
        self.assertIn("safety", bundle)
        self.assertIn("accessibility", bundle)
        self.assertIn("tests", bundle)

    def test_verify_skill_is_evidence_first_and_honest(self) -> None:
        skill_text = read_skill("prouver-resultat-azd")
        bundle = read_skill_bundle("prouver-resultat-azd")

        self.assertRegex(skill_text, r"(?m)^name: prouver-resultat-azd$")
        self.assertNotIn("PROVISIONAL", skill_text)
        assert_language_rule(self, bundle)
        self.assertIn("claim-by-claim evidence matrix", bundle)
        self.assertIn("fresh tests", bundle)
        self.assertIn("lint", bundle)
        self.assertIn("types", bundle)
        self.assertIn("build", bundle)
        self.assertIn("runtime", bundle)
        self.assertIn("visual", bundle)
        self.assertIn("partial", bundle)
        self.assertIn("blocked", bundle)
        self.assertIn("failed", bundle)
        for field in ("claim", "status", "evidence", "freshness", "oracle", "risk"):
            self.assertIn(f"`{field}`", bundle)

    def test_review_skill_is_independent_and_ranked(self) -> None:
        skill_text = read_skill("reviser-qualite-azd")
        bundle = read_skill_bundle("reviser-qualite-azd")

        self.assertRegex(skill_text, r"(?m)^name: reviser-qualite-azd$")
        self.assertNotIn("PROVISIONAL", skill_text)
        assert_language_rule(self, bundle)
        self.assertIn("independent", bundle)
        self.assertIn("correctness", bundle)
        self.assertIn("security", bundle)
        self.assertIn("design", bundle)
        self.assertIn("simplicity", bundle)
        self.assertIn("ranked", bundle)
        self.assertIn("actionable", bundle)
        self.assertIn("return to build", bundle)

    def test_ui_contract_tokens_survive_discovery_design_build_verify_and_review(self) -> None:
        discovery = read_skill_bundle("inspecter-projet-azd")
        design = read_skill_bundle("concevoir-experience-azd")
        build = read_skill_bundle("construire-solution-azd")
        verify = read_skill_bundle("prouver-resultat-azd")
        review = read_skill_bundle("reviser-qualite-azd")
        orchestrate = read_skill_bundle("piloter-workflow-azd")

        self.assertIn("public-contract.json", discovery)
        self.assertIn("exact token/path/selector", discovery)
        self.assertIn("UI acceptance matrix", design)
        self.assertIn("loading, empty, error et success", design)
        self.assertIn("UI acceptance matrix", build)
        self.assertIn("contract-completeness pass", verify)
        self.assertIn("contract-completeness pass", review)
        self.assertIn("UI acceptance matrix", orchestrate)
        for text in (discovery, design, build, verify, review, orchestrate):
            self.assertRegex(text, r"token|selector|attribut")

    def test_discovery_contradictions_survive_into_final_risks_and_blind_spots(self) -> None:
        orchestrate = read_skill_bundle("piloter-workflow-azd")
        verify = read_skill_bundle("prouver-resultat-azd")

        self.assertIn("discovery.contradictions", orchestrate)
        self.assertIn("discovery.blind_spots", orchestrate)
        self.assertIn("sans perte", orchestrate)
        self.assertIn("discovery carryover gate", verify)
        self.assertIn("staleness/divergences de version", verify)
        self.assertIn("blind_spots", verify)
        self.assertIn("risks", verify)
        self.assertIn("path/source", verify)
        self.assertIn("fail", verify)


if __name__ == "__main__":
    unittest.main()
