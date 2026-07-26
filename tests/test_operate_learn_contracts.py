import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def read_skill(name: str) -> str:
    return read(f"skills/{name}/SKILL.md")


class OperateLearnContractTests(unittest.TestCase):
    def test_operate_requires_incident_canary_rollback_evidence_and_fail_closed_capabilities(self) -> None:
        text = read_skill("surveiller-livraison-azd")

        for token in (
            "host_capabilities",
            "observability",
            "traffic_control",
            "deploy_control",
            "rollback_control",
            "fail closed",
            "capability_gap",
            "incident_evidence",
            "canary_evidence",
            "rollback_evidence",
            "baseline_refs",
            "active_version_proof",
            "authority_artifact",
            "redacted",
        ):
            self.assertIn(token, text)

        self.assertRegex(text, re.compile(r"missing.*blocked", re.IGNORECASE | re.DOTALL))
        self.assertRegex(text, re.compile(r"incident.*timeline.*impact", re.IGNORECASE | re.DOTALL))
        self.assertRegex(text, re.compile(r"canary.*step.*baseline", re.IGNORECASE | re.DOTALL))
        self.assertRegex(text, re.compile(r"rollback.*active_version_proof", re.IGNORECASE | re.DOTALL))

    def test_learn_is_restart_safe_branch_scoped_provenance_drift_redaction_and_fail_closed(self) -> None:
        text = read_skill("conserver-apprentissages-azd")
        details = read("skills/conserver-apprentissages-azd/references/learn-details.md")

        for token in (
            "branch_scope",
            "repo",
            "branch",
            "base_commit",
            "head_commit",
            "restart_safe_retrieval",
            "retrieval_key",
            "learning_store",
            "resume",
            "provenance",
            "drift",
            "redaction",
            "redaction_log",
            "host_capabilities",
            "fail closed",
            "capability_gap",
            "no daemon",
            "no database",
        ):
            self.assertIn(token, text)

        self.assertRegex(text, re.compile(r"branch_scope.*must match", re.IGNORECASE | re.DOTALL))
        self.assertRegex(text, re.compile(r"missing.*capability.*local-only|local-only.*missing.*capability", re.IGNORECASE | re.DOTALL))
        self.assertIn("Restart-safe branch-scoped retrieval", details)
        self.assertIn("Redaction and provenance", details)

    def test_agent_cards_advertise_fail_closed_contracts(self) -> None:
        operate = read("skills/surveiller-livraison-azd/agents/openai.yaml")
        learn = read("skills/conserver-apprentissages-azd/agents/openai.yaml")

        self.assertIn("fail-closed", operate)
        self.assertIn("evidence", operate)
        self.assertIn("fail-closed", learn)
        self.assertIn("branch-scoped", learn)


if __name__ == "__main__":
    unittest.main()
