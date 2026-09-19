import re
import unittest

from _skill_helpers import assert_language_rule, read_skill, read_skill_bundle


class DeliveryAndLearningSkillTests(unittest.TestCase):
    def test_ship_integrates_verifies_documents_and_respects_authority(self) -> None:
        skill_text = read_skill("livrer-changement-azd")
        bundle = read_skill_bundle("livrer-changement-azd")

        self.assertRegex(skill_text, r"(?m)^name: livrer-changement-azd$")
        self.assertNotIn("PROVISIONAL", skill_text)
        assert_language_rule(self, bundle)
        self.assertNotIn("TODO", bundle)

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
            self.assertIn(contract, bundle)

        self.assertRegex(bundle, re.compile(r"partial|blocked|failed", re.IGNORECASE))

    def test_operate_observes_canaries_and_recovers_under_authority(self) -> None:
        skill_text = read_skill("surveiller-livraison-azd")
        bundle = read_skill_bundle("surveiller-livraison-azd")

        self.assertRegex(skill_text, r"(?m)^name: surveiller-livraison-azd$")
        self.assertNotIn("PROVISIONAL", skill_text)
        assert_language_rule(self, bundle)
        self.assertNotIn("TODO", bundle)

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
            self.assertIn(contract, bundle)

        self.assertRegex(bundle, re.compile(r"partial|blocked|failed", re.IGNORECASE))

    def test_learn_records_scoped_falsifiable_and_governed_knowledge(self) -> None:
        skill_text = read_skill("conserver-apprentissages-azd")
        bundle = read_skill_bundle("conserver-apprentissages-azd")

        self.assertRegex(skill_text, r"(?m)^name: conserver-apprentissages-azd$")
        self.assertNotIn("PROVISIONAL", skill_text)
        assert_language_rule(self, bundle)
        self.assertNotIn("TODO", bundle)

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
            self.assertIn(contract, bundle)

        self.assertRegex(bundle, re.compile(r"anecdote|single preference", re.IGNORECASE))
        self.assertRegex(bundle, re.compile(r"never.*universal", re.IGNORECASE))

    def test_evolve_uses_isolated_protected_evaluation_without_reward_hacking(self) -> None:
        skill_text = read_skill("ameliorer-workflow-azd")
        bundle = read_skill_bundle("ameliorer-workflow-azd")

        self.assertRegex(skill_text, r"(?m)^name: ameliorer-workflow-azd$")
        self.assertNotIn("PROVISIONAL", skill_text)
        assert_language_rule(self, bundle)
        self.assertNotIn("TODO", bundle)

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
            self.assertIn(contract, bundle)

        self.assertRegex(bundle, re.compile(r"incomplete|interrupted", re.IGNORECASE))
        self.assertRegex(bundle, re.compile(r"cannot|must not|never", re.IGNORECASE))


if __name__ == "__main__":
    unittest.main()
