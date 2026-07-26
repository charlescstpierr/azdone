import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"


def read_skill(name: str) -> str:
    return (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")


def read_reference(skill: str, reference: str) -> str:
    return (SKILLS / skill / "references" / reference).read_text(encoding="utf-8")


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower())


class ReferenceBestPracticeRegressionTests(unittest.TestCase):
    def assertTokens(self, text: str, tokens: tuple[str, ...]) -> None:
        haystack = normalized(text)
        missing = [token for token in tokens if token.lower() not in haystack]
        self.assertEqual(missing, [], f"missing tokens: {missing}")

    def test_resume_context_schema_is_shared_and_routed_by_plan_branch_lab_and_ship(self) -> None:
        expected_fields = (
            "resume_context",
            "base_commit",
            "branch",
            "worktree",
            "current_step",
            "remaining_work",
            "failed_approaches",
            "resume_commands",
            "next_safe_action",
            "blockers",
        )

        self.assertTokens(read_reference("piloter-workflow-azd", "run-contract.md"), expected_fields)
        for skill in ("planifier-travail-azd", "isoler-travail-azd", "livrer-changement-azd"):
            with self.subTest(skill=skill):
                self.assertTokens(read_skill(skill), expected_fields)

    def test_orchestrate_terminal_contract_uses_canonical_next_safe_action_not_vague_next(self) -> None:
        skill_text = read_skill("piloter-workflow-azd")
        contract_text = read_reference("piloter-workflow-azd", "run-contract.md")
        combined = normalized(f"{skill_text}\n{contract_text}")

        self.assertIn("next_safe_action", combined)
        for status in ("partial", "blocked"):
            with self.subTest(status=status):
                self.assertRegex(
                    combined,
                    re.compile(rf"{status}[^.]*next_safe_action", re.IGNORECASE),
                )
        for status in ("verified", "failed"):
            with self.subTest(status=status):
                self.assertRegex(
                    combined,
                    re.compile(rf"{status}[^.]*next_safe_action[^.]*none", re.IGNORECASE),
                )
        self.assertNotRegex(skill_text, re.compile(r"`next`", re.IGNORECASE))
        self.assertNotRegex(contract_text, re.compile(r"^\s*next\s*:", re.IGNORECASE | re.MULTILINE))

    def test_progress_snapshot_schema_is_visible_to_orchestrate_ship_and_operate(self) -> None:
        expected_fields = (
            "progress_snapshot",
            "phase",
            "status",
            "done",
            "total",
            "blocked_by",
            "last_checked_at",
            "next_check",
        )

        for skill in ("piloter-workflow-azd", "livrer-changement-azd", "surveiller-livraison-azd"):
            with self.subTest(skill=skill):
                self.assertTokens(read_skill(skill), expected_fields)

    def test_evidence_graph_contract_preserves_claim_source_artifact_oracle_and_drift_edges(self) -> None:
        expected_fields = (
            "evidence_graph",
            "claim",
            "source",
            "artifact",
            "oracle",
            "supports",
            "contradicts",
            "derived_from",
            "supersedes",
            "stale",
            "superseded",
            "contradicted",
            "revalidation_condition",
        )

        for skill in ("prouver-resultat-azd", "conserver-apprentissages-azd"):
            with self.subTest(skill=skill):
                self.assertTokens(read_skill(skill), expected_fields)

    def test_branch_lab_preflights_existing_isolation_before_dispatching_parallel_work(self) -> None:
        expected_fields = (
            "isolation_preflight",
            "existing_isolation",
            "submodule_guard",
            "native_tool_used",
            "directory_ignored",
            "baseline_ready",
            "brief_path",
            "review_package_path",
            "dispatch_scope",
            "expected_output",
        )

        self.assertTokens(read_skill("isoler-travail-azd"), expected_fields)

    def test_design_reviews_specs_with_placeholder_ambiguity_scope_and_authority_checks(self) -> None:
        expected_fields = (
            "spec_review",
            "placeholder_scan",
            "ambiguity_scan",
            "scope_check",
            "authority-aware",
            "selected_direction",
        )

        self.assertTokens(read_skill("concevoir-experience-azd"), expected_fields)

    def test_discovery_runs_generic_environment_preflight_before_reporting_ready_warn_or_blocked(self) -> None:
        expected_fields = (
            "environment_preflight",
            "repository_root",
            "git_state",
            "required_tools",
            "native_capabilities",
            "conflicts",
            "ready",
            "warn",
            "blocked",
        )

        self.assertTokens(read_skill("inspecter-projet-azd"), expected_fields)

    def test_plan_staffing_guidance_names_role_optional_model_hints_and_expected_output(self) -> None:
        expected_fields = (
            "staffing",
            "role",
            "model_hint",
            "reasoning_effort",
            "expected_output",
        )

        self.assertTokens(read_skill("planifier-travail-azd"), expected_fields)


if __name__ == "__main__":
    unittest.main()
