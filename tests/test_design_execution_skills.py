import unittest

from _skill_helpers import assert_language_rule, read_skill, read_skill_bundle


class DesignExecutionSkillContractTests(unittest.TestCase):
    def test_m05_design_covers_human_facing_design_gate(self) -> None:
        skill_text = read_skill("concevoir-experience-azd")
        bundle = read_skill_bundle("concevoir-experience-azd")

        self.assertIn("name: concevoir-experience-azd", skill_text)
        self.assertNotIn("PROVISIONAL", skill_text)
        assert_language_rule(self, bundle)

        for token in (
            "web",
            "mobile",
            "desktop",
            "CLI",
            "TUI",
            "IDE",
            "chat",
            "report",
            "notification",
            "professional prototype",
            "accessibility",
            "human authority",
            "evidence-first",
        ):
            self.assertIn(token, bundle)

    def test_m06_plan_covers_dependency_and_proof_mapping(self) -> None:
        skill_text = read_skill("planifier-travail-azd")
        bundle = read_skill_bundle("planifier-travail-azd")

        self.assertIn("name: planifier-travail-azd", skill_text)
        self.assertNotIn("PROVISIONAL", skill_text)
        assert_language_rule(self, bundle)

        for token in (
            "dependency graph",
            "requirement-to-proof",
            "ownership",
            "overlap",
            "rollback",
            "no vague steps",
            "frozen",
            "evidence",
            "ordering",
        ):
            self.assertIn(token, bundle)

    def test_m07_branch_lab_covers_isolation_and_safe_integration(self) -> None:
        skill_text = read_skill("isoler-travail-azd")
        bundle = read_skill_bundle("isoler-travail-azd")

        self.assertIn("name: isoler-travail-azd", skill_text)
        self.assertNotIn("PROVISIONAL", skill_text)
        assert_language_rule(self, bundle)

        for token in (
            "same repository",
            "worktree",
            "subagent briefs",
            "agent_id",
            "execution_status",
            "subagents-unavailable",
            "Ne jamais présenter un plan de délégation comme une exécution observée",
            "leases",
            "checkpoints",
            "no shared worktree",
            "dirty-worktree safety",
            "frozen evaluator",
            "safe integration",
            "native Git",
            "evidence",
        ):
            self.assertIn(token, bundle)


if __name__ == "__main__":
    unittest.main()
