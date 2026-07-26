import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"


def read_skill(name: str) -> str:
    return (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")


class DeliveryAndLearningSkillTests(unittest.TestCase):
    def test_ship_integrates_verifies_documents_and_respects_authority(self) -> None:
        text = read_skill("livrer-changement-azd")

        self.assertRegex(text, r"(?m)^name: livrer-changement-azd$")
        self.assertNotIn("PROVISIONAL", text)
        self.assertIn("Français", text)
        self.assertIn("English", text)
        self.assertNotIn("TODO", text)

        for contract in (
            "dependency order",
            "integrated result",
            "fresh verification",
            "release notes",
            "remaining risks",
            "push",
            "pull request",
            "merge",
            "deploy",
            "explicit authority",
            "authority-request",
        ):
            self.assertIn(contract, text)

        self.assertRegex(text, re.compile(r"partial|blocked|failed", re.IGNORECASE))

    def test_operate_observes_canaries_and_recovers_under_authority(self) -> None:
        text = read_skill("surveiller-livraison-azd")

        self.assertRegex(text, r"(?m)^name: surveiller-livraison-azd$")
        self.assertNotIn("PROVISIONAL", text)
        self.assertIn("Français", text)
        self.assertIn("English", text)
        self.assertNotIn("TODO", text)

        for contract in (
            "canary",
            "monitor",
            "incident",
            "rollback",
            "baseline",
            "logs",
            "metrics",
            "traces",
            "explicit authority",
            "authority-request",
            "production",
            "evidence",
        ):
            self.assertIn(contract, text)

        self.assertRegex(text, re.compile(r"partial|blocked|failed", re.IGNORECASE))

    def test_learn_records_scoped_falsifiable_and_governed_knowledge(self) -> None:
        text = read_skill("conserver-apprentissages-azd")

        self.assertRegex(text, r"(?m)^name: conserver-apprentissages-azd$")
        self.assertNotIn("PROVISIONAL", text)
        self.assertIn("Français", text)
        self.assertIn("English", text)
        self.assertNotIn("TODO", text)

        for contract in (
            "provenance",
            "source run",
            "scope",
            "confidence",
            "counterexample",
            "expiry",
            "conflict",
            "insufficient-evidence",
            "future decision",
            "secrets",
        ):
            self.assertIn(contract, text)

        self.assertRegex(text, re.compile(r"anecdote|single preference", re.IGNORECASE))
        self.assertRegex(text, re.compile(r"never.*universal", re.IGNORECASE))

    def test_evolve_uses_isolated_protected_evaluation_without_reward_hacking(self) -> None:
        text = read_skill("ameliorer-workflow-azd")

        self.assertRegex(text, r"(?m)^name: ameliorer-workflow-azd$")
        self.assertNotIn("PROVISIONAL", text)
        self.assertIn("Français", text)
        self.assertIn("English", text)
        self.assertNotIn("TODO", text)

        for contract in (
            "falsifiable hypothesis",
            "isolated worktree",
            "candidate branch",
            "frozen evaluator",
            "train",
            "eval",
            "hidden oracle",
            "protected regressions",
            "correctness",
            "cost",
            "latency",
            "interruptions",
            "reward hacking",
            "keep",
            "discard",
            "rollback",
            "human-gate",
            "authority policy",
        ):
            self.assertIn(contract, text)

        self.assertRegex(text, re.compile(r"incomplete|interrupted", re.IGNORECASE))
        self.assertRegex(text, re.compile(r"cannot|must not|never", re.IGNORECASE))


if __name__ == "__main__":
    unittest.main()
