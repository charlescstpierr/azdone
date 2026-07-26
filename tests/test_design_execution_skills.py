import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"


def read_skill(name: str) -> str:
    return (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")


class DesignExecutionSkillContractTests(unittest.TestCase):
    def test_m05_design_covers_human_facing_design_gate(self) -> None:
        text = read_skill("concevoir-experience-azd")

        self.assertIn("name: concevoir-experience-azd", text)
        self.assertNotIn("PROVISIONAL", text)
        self.assertIn("Français", text)
        self.assertIn("English", text)

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
            self.assertIn(token, text)

    def test_m06_plan_covers_dependency_and_proof_mapping(self) -> None:
        text = read_skill("planifier-travail-azd")

        self.assertIn("name: planifier-travail-azd", text)
        self.assertNotIn("PROVISIONAL", text)
        self.assertIn("Français", text)
        self.assertIn("English", text)

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
            self.assertIn(token, text)

    def test_m07_branch_lab_covers_isolation_and_safe_integration(self) -> None:
        text = read_skill("isoler-travail-azd")

        self.assertIn("name: isoler-travail-azd", text)
        self.assertNotIn("PROVISIONAL", text)
        self.assertIn("Français", text)
        self.assertIn("English", text)

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
            self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()
