import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class HandoffCarryoverContractTests(unittest.TestCase):
    def test_shared_contract_defines_lossless_handoff(self):
        text = (ROOT / "CONTRACTS.md").read_text(encoding="utf-8")
        for token in (
            "handoff_carryover",
            "required_fields",
            "carried_fields",
            "transformed_fields",
            "dropped_fields",
            "freshness_boundary",
        ):
            self.assertIn(token, text)

    def test_orchestrator_and_plan_require_handoff(self):
        orchestrator = (
            ROOT / "skills/piloter-workflow-azd/references/run-contract.md"
        ).read_text(encoding="utf-8")
        planning = (
            ROOT / "skills/planifier-travail-azd/references/planning-contract.md"
        ).read_text(encoding="utf-8")
        self.assertIn("handoff_carryover", orchestrator)
        self.assertIn("handoff_inputs", planning)
        self.assertIn("handoff_outputs", planning)

    def test_verify_and_ship_fail_closed_on_evidence_loss(self):
        verify = (ROOT / "skills/prouver-resultat-azd/SKILL.md").read_text(encoding="utf-8")
        ship = (ROOT / "skills/livrer-changement-azd/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("carryover_gate", verify)
        self.assertIn("dropped_fields", verify)
        self.assertIn("handoff_carryover", ship)


if __name__ == "__main__":
    unittest.main()
