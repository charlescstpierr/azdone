import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"


def read_skill(name: str) -> str:
    return (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")


class SkillSeriesContractTests(unittest.TestCase):
    def test_entry_skill_routes_the_complete_verified_journey(self) -> None:
        text = read_skill("piloter-workflow-azd")

        self.assertRegex(text, r"(?m)^name: piloter-workflow-azd$")
        self.assertNotIn("PROVISIONAL", text)
        self.assertIn("Français", text)
        self.assertIn("English", text)

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
            self.assertIn(f"${skill}", text)

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
            self.assertIn(guarantee, text)

        self.assertRegex(text, re.compile(r"partial|blocked|failed", re.IGNORECASE))
        self.assertIn("au plus une question matérielle", text)
        self.assertIn("$inspecter-projet-azd` avant le diagnostic, le design, le plan ou le code", text)

    def test_build_skill_is_final_bilingual_and_tdd_first(self) -> None:
        text = read_skill("construire-solution-azd")

        self.assertRegex(text, r"(?m)^name: construire-solution-azd$")
        self.assertNotIn("PROVISIONAL", text)
        self.assertIn("Français", text)
        self.assertIn("English", text)
        self.assertIn("TDD", text)
        self.assertIn("smallest valid change", text)
        self.assertIn("Ponytail", text)
        self.assertIn("evidence", text)
        self.assertIn("safety", text)
        self.assertIn("accessibility", text)
        self.assertIn("tests", text)

    def test_verify_skill_is_evidence_first_and_honest(self) -> None:
        text = read_skill("prouver-resultat-azd")

        self.assertRegex(text, r"(?m)^name: prouver-resultat-azd$")
        self.assertNotIn("PROVISIONAL", text)
        self.assertIn("Français", text)
        self.assertIn("English", text)
        self.assertIn("claim-by-claim evidence matrix", text)
        self.assertIn("fresh tests", text)
        self.assertIn("lint", text)
        self.assertIn("types", text)
        self.assertIn("build", text)
        self.assertIn("runtime", text)
        self.assertIn("visual", text)
        self.assertIn("partial", text)
        self.assertIn("blocked", text)
        self.assertIn("failed", text)
        for field in ("claim", "status", "evidence", "freshness", "oracle", "risk"):
            self.assertIn(f"`{field}`", text)

    def test_review_skill_is_independent_and_ranked(self) -> None:
        text = read_skill("reviser-qualite-azd")

        self.assertRegex(text, r"(?m)^name: reviser-qualite-azd$")
        self.assertNotIn("PROVISIONAL", text)
        self.assertIn("Français", text)
        self.assertIn("English", text)
        self.assertIn("independent", text)
        self.assertIn("correctness", text)
        self.assertIn("security", text)
        self.assertIn("design", text)
        self.assertIn("simplicity", text)
        self.assertIn("ranked", text)
        self.assertIn("actionable", text)
        self.assertIn("return to build", text)

    def test_ui_contract_tokens_survive_discovery_design_build_verify_and_review(self) -> None:
        discovery = read_skill("inspecter-projet-azd")
        design = read_skill("concevoir-experience-azd")
        build = read_skill("construire-solution-azd")
        verify = read_skill("prouver-resultat-azd")
        review = read_skill("reviser-qualite-azd")
        orchestrate = read_skill("piloter-workflow-azd")

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
        orchestrate = read_skill("piloter-workflow-azd")
        verify = read_skill("prouver-resultat-azd")

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
