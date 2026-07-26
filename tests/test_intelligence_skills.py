import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"


def read_skill(name: str) -> str:
    return (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")


class IntelligenceSkillContractTests(unittest.TestCase):
    def test_m02_understand_contract_is_concise_and_bilingual(self) -> None:
        text = read_skill("clarifier-objectif-azd").lower()

        self.assertNotIn("provisional", text)
        self.assertIn("français", text)
        self.assertIn("english", text)
        self.assertIn("outcome contract", text)
        self.assertIn("blind spots", text)
        self.assertIn("blind_spots: []", text)
        self.assertIn("unknowns", text)
        self.assertIn('repository: ""', text)
        self.assertIn('worktree: ""', text)
        self.assertIn("one material question", text)
        self.assertIn("evidence-first", text)
        self.assertNotIn("[TODO:", text)

    def test_m03_discover_contract_is_evidence_first_and_safe(self) -> None:
        text = read_skill("inspecter-projet-azd").lower()

        self.assertNotIn("provisional", text)
        self.assertIn("français", text)
        self.assertIn("english", text)
        self.assertIn("repository", text)
        self.assertIn("primary sources", text)
        self.assertIn("trianguler", text)
        self.assertIn("docs locales / readme", text)
        self.assertIn("manifestes", text)
        self.assertIn("source-cache", text)
        self.assertIn("contradictions", text)
        self.assertIn("staleness", text)
        self.assertIn("namespace", text)
        self.assertIn("collisions", text)
        self.assertIn("prioritized_fix_or_doc", text)
        self.assertIn("capability gap", text)
        self.assertIn("observations locales", text)
        self.assertNotIn("changements locaux", text)
        self.assertIn("prompt injection", text)
        self.assertIn("supply-chain", text)
        self.assertIn("stop when sufficient", text)
        self.assertIn("evidence", text)
        self.assertNotIn("[TODO:", text)

    def test_m04_diagnose_contract_is_root_cause_only(self) -> None:
        text = read_skill("diagnostiquer-probleme-azd").lower()

        self.assertNotIn("provisional", text)
        self.assertIn("français", text)
        self.assertIn("english", text)
        self.assertIn("reproduce", text)
        self.assertIn("isolate", text)
        self.assertIn("hypothesis ledger", text)
        self.assertIn("root cause", text)
        self.assertIn("diagnose-only", text)
        self.assertIn("fresh evidence", text)
        self.assertNotIn("[TODO:", text)


if __name__ == "__main__":
    unittest.main()
