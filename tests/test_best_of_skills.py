import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"


def skill_path(name: str) -> Path:
    return SKILLS / name / "SKILL.md"


def read_skill(name: str) -> str:
    return skill_path(name).read_text(encoding="utf-8")


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower())


class BestOfSkillRegressionTests(unittest.TestCase):
    def assertConcepts(self, text: str, concept_groups: tuple[tuple[str, ...], ...]) -> None:
        haystack = normalized(text)
        missing = [
            " / ".join(group)
            for group in concept_groups
            if not any(option.lower() in haystack for option in group)
        ]
        self.assertEqual(missing, [], f"missing concepts: {missing}")

    def test_m01_routes_wayfinder_and_domain_model_modes_through_existing_skills(self) -> None:
        text = read_skill("piloter-workflow-azd")

        self.assertConcepts(
            text,
            (
                ("$clarifier-objectif-azd",),
                ("$planifier-travail-azd",),
                ("wayfinder",),
                ("domain model", "modèle de domaine"),
                ("destination",),
                ("fog", "brouillard"),
                ("frontier", "frontière"),
            ),
        )

    def test_m01_routes_by_capability_and_keeps_design_conditional(self) -> None:
        text = read_skill("piloter-workflow-azd")

        self.assertConcepts(
            text,
            (
                ("code-change",),
                ("investigation",),
                ("human-surface",),
                ("release-ops",),
                ("skill-mutation",),
                ("seulement lorsqu", "only when"),
                ("sortie textuelle stable", "stable textual output"),
                ("omettre cette étape", "skip design"),
                ("host compatible", "compatible host"),
                ("harness externe", "external harness"),
            ),
        )

    def test_m02_asks_one_adaptive_question_per_round_with_confidence_zero_assumption_and_domain_model(self) -> None:
        text = read_skill("clarifier-objectif-azd")

        self.assertConcepts(
            text,
            (
                ("adaptive", "adaptatif"),
                ("per round", "par round", "chaque round"),
                ("one material question", "une question matérielle"),
                ("confidence", "confiance"),
                ("zero-assumption", "zéro hypothèse", "zero assumption"),
                ("domain model", "modèle de domaine"),
                ("vocabulary", "vocabulaire"),
                ("entities", "entités"),
                ("invariants",),
                ("fail closed", "blocked"),
            ),
        )
        self.assertRegex(text, r"(?is)confidence:\s*(low|medium|high)")
        self.assertNotIn("confidence >=", text.lower())

    def test_m06_wayfinder_mode_covers_destination_fog_frontier_decisions_tracker_fallback_and_resume(self) -> None:
        text = read_skill("planifier-travail-azd")

        self.assertConcepts(
            text,
            (
                ("wayfinder",),
                ("destination",),
                ("fog", "brouillard", "unknown terrain"),
                ("frontier", "frontière"),
                ("decision ticket", "ticket de décision"),
                ("tracker fallback", "fallback tracker", "tracker de secours", "tracker existant si", "sinon créer"),
                ("resume", "reprise"),
                ("blocked", "partial", "failed"),
            ),
        )

    def test_m06_devex_mode_is_surface_specific_for_cli_api_and_sdk_contracts(self) -> None:
        text = read_skill("planifier-travail-azd")

        self.assertConcepts(
            text,
            (
                ("devex", "developer experience"),
                ("surface: cli | api | sdk | none", "surface"),
                ("for cli/api/sdk", "pour cli/api/sdk", "lorsque ces surfaces changent", "alors que ces surfaces changent"),
                ("cli",),
                ("api",),
                ("sdk",),
                ("flags",),
                ("stdout",),
                ("stderr",),
                ("exit code", "exit codes", "codes de sortie"),
                ("config precedence", "precedence de config", "priorité de config"),
            ),
        )

    def test_series_uses_surface_specific_overlays_for_any_kind_of_output(self) -> None:
        text = "\n".join(
            (
                read_skill("piloter-workflow-azd"),
                read_skill("planifier-travail-azd"),
                read_skill("prouver-resultat-azd"),
            )
        )

        self.assertConcepts(
            text,
            (
                ("surface-specific", "par surface", "surface existe", "surfaces changent"),
                ("web",),
                ("mobile",),
                ("backend", "service"),
                ("data", "migration"),
                ("infrastructure", "infra"),
                ("library", "sdk", "bibliothèque"),
                ("cli/tui", "cli", "tui"),
                ("docs", "documentation"),
                ("verification overlay", "overlay de vérification", "contrat de vérification"),
            ),
        )

    def test_m05_design_requires_ascii_wireframes_for_cli_tui_surfaces(self) -> None:
        text = read_skill("concevoir-experience-azd")

        self.assertConcepts(
            text,
            (
                ("cli",),
                ("tui",),
                ("ascii wireframe", "wireframe ascii", "maquette ascii"),
                ("transcript", "rendu textuel"),
            ),
        )

    def test_m05_design_compares_three_directions_for_material_decisions(self) -> None:
        text = read_skill("concevoir-experience-azd")

        self.assertConcepts(
            text,
            (
                ("exactly three directions", "trois directions"),
                ("material decision", "décision matérielle", "incertitude matérielle"),
                ("selected_direction", "direction retenue"),
                ("human authority", "autorité humaine"),
            ),
        )

    def test_m06_plan_freezes_exact_commands_and_paths_before_execution(self) -> None:
        text = read_skill("planifier-travail-azd")

        self.assertConcepts(
            text,
            (
                ("frozen", "gelé"),
                ("exact command", "commandes exactes", "commands exactes"),
                ("repo-local paths", "paths repo-locaux", "chemins repo-locaux"),
                ("requirement-to-proof",),
                ("no vague steps",),
            ),
        )
        self.assertRegex(text, r"(?is)(commands|commandes):\s*\[")
        self.assertRegex(text, r"(?is)(paths|chemins):\s*\[")

    def test_m07_branch_lab_requires_host_observed_agents_and_fresh_agent_per_task_when_relevant(self) -> None:
        text = read_skill("isoler-travail-azd")

        self.assertConcepts(
            text,
            (
                ("host-observed", "observée par le host", "observable"),
                ("real subagent", "subagents natifs", "vrais agents"),
                ("fresh agent per task", "agent frais par tâche", "new agent per task"),
                ("agent_id",),
                ("execution_status",),
                ("do not simulate", "ne jamais simuler"),
            ),
        )

    def test_m10_review_runs_spec_compliance_then_code_quality_with_distinct_people(self) -> None:
        text = read_skill("reviser-qualite-azd")

        self.assertConcepts(
            text,
            (
                ("spec-compliance", "contract-completeness", "conformité spec", "contract/spec compliance"),
                ("code-quality", "qualité du code", "quality/correctness"),
                ("author_id != reviewer_id", "author et reviewer sont identiques"),
                ("distinct", "indépendant"),
                ("reviewer_id",),
                ("author_id",),
            ),
        )
        self.assertRegex(text, r"(?is)(spec-compliance|contract-completeness|contract/spec compliance).*(code-quality|qualité du code|quality/correctness)")

    def test_m09_verify_covers_terminal_checks_only_when_cli_tui_surface_exists(self) -> None:
        text = read_skill("prouver-resultat-azd")

        self.assertConcepts(
            text,
            (
                ("when the surface exists", "lorsque la surface existe", "si la surface existe"),
                ("cli",),
                ("tui",),
                ("small terminal", "petit terminal", "80x24", "terminal étroit"),
                ("interruption", "interrupt", "sigint"),
                ("stdout",),
                ("stderr",),
                ("exit code", "codes de sortie"),
            ),
        )

    def test_m13_learn_treats_memory_as_optional_not_a_runtime_dependency(self) -> None:
        text = read_skill("conserver-apprentissages-azd")

        self.assertConcepts(
            text,
            (
                ("optional memory", "mémoire optionnelle", "memory optional"),
                ("no memory dependency", "sans dépendance mémoire", "not depend on memory", "no daemon, database, or durable service"),
                ("memory_authority",),
                ("local | durable | none",),
                ("persisted_paths",),
            ),
        )

    def test_m14_evolve_keeps_evaluation_protected_before_scoring_or_promotion(self) -> None:
        text = read_skill("ameliorer-workflow-azd")

        self.assertConcepts(
            text,
            (
                ("frozen evaluator",),
                ("hidden oracle",),
                ("protected regressions",),
                ("outside_candidate_write_scope",),
                ("reward hacking",),
                ("incomplete or interrupted",),
                ("before scoring", "before comparing", "avant l'essai"),
                ("keep | discard | rollback | human-gate",),
            ),
        )


if __name__ == "__main__":
    unittest.main()
