import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"


def read_skill(name: str) -> str:
    return (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower())


class DiagnoseReviewContractTests(unittest.TestCase):
    def assertTokens(self, text: str, tokens: tuple[str, ...]) -> None:
        haystack = normalized(text)
        missing = [token for token in tokens if token.lower() not in haystack]
        self.assertEqual([], missing, f"missing tokens: {missing}")

    def test_diagnose_requires_reproducible_ledger_competing_hypotheses_and_no_fix_boundary(self) -> None:
        text = read_skill("diagnostiquer-probleme-azd")

        self.assertTokens(
            text,
            (
                "diagnosis_ledger",
                "command",
                "environment",
                "expected",
                "actual",
                "hypothèses concurrentes",
                "falsification test",
                "falsified",
                "diagnose-only",
                "Ne pas corriger",
                "Ne pas produire de patch",
            ),
        )
        self.assertRegex(text, r"open \| falsified \| supported \| blocked")

    def test_diagnose_separates_author_and_reviewer_evidence(self) -> None:
        text = read_skill("diagnostiquer-probleme-azd")

        self.assertTokens(text, ("author_id", "reviewer_id", "author_evidence", "reviewer_evidence"))
        self.assertIn("observation indépendante", text)

    def test_review_requires_planted_defects_stable_ids_and_ranked_findings(self) -> None:
        text = read_skill("reviser-qualite-azd")

        self.assertTokens(
            text,
            (
                "planted-defect protocol",
                "defect class",
                "logic",
                "contract",
                "security",
                "test gap",
                "evidence drift",
                "stable finding IDs",
                "SEC-01",
                "TEST-02",
                "ARCH-03",
                "ranked",
                "line_or_selector",
            ),
        )
        self.assertIn("never renumber open findings", text)

    def test_review_keeps_author_and_reviewer_evidence_distinct(self) -> None:
        text = read_skill("reviser-qualite-azd")

        self.assertTokens(text, ("author_id != reviewer_id", "author_evidence", "reviewer_evidence"))
        self.assertIn("distinct from `author_evidence`", text)
        self.assertIn("not a copy of the author's claim", text)


if __name__ == "__main__":
    unittest.main()
