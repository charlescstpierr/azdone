"""Portage multi-hote : install globale, cache de capacites par machine,
detection de multi_agent sous Codex, pointeur permanent.

Decision : docs/decisions/0001-portage-multi-hote-et-etat-par-machine.md.
"""

import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTALL = ROOT / "scripts" / "install.sh"
SETUP_SKILL = ROOT / "skills" / "azd-setup" / "SKILL.md"
CACHE_REFERENCE = ROOT / "skills" / "azd-setup" / "references" / "host-capabilities.md"
MODEL_ROUTING = ROOT / "skills" / "azd" / "references" / "model-routing.md"
GUIDE_MODELS = ROOT / "docs" / "guide" / "04-modeles-et-sous-agents.md"

CACHE_PATH = "~/.azdone/host-capabilities.json"
# Les cles de decision : elles vivent dans .azdone/trust.yaml, versionne et lu
# par le hook, jamais dans un cache hors depot.
DECISION_KEYS = ("autonomy", "ceiling", "enforcement", "models.roles")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class GlobalInstallTests(unittest.TestCase):
    """La portee globale ne doit jamais supprimer de contenu reel."""

    def _run(self, *args: str, home: Path) -> subprocess.CompletedProcess:
        env = dict(os.environ)
        env["HOME"] = str(home)
        return subprocess.run(
            ["bash", str(INSTALL), *args],
            capture_output=True,
            text=True,
            env=env,
        )

    @staticmethod
    def _entries(directory: Path) -> list[str]:
        return sorted(p.name for p in directory.iterdir())

    def test_global_link_install_is_idempotent_and_uses_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)

            first = self._run("claude", "--global", home=home)
            self.assertEqual(0, first.returncode, first.stderr)

            skills = home / ".claude/skills"
            agents = home / ".claude/agents"
            self.assertEqual(20, len(self._entries(skills)))
            self.assertEqual(5, len(self._entries(agents)))
            self.assertTrue(
                all(p.is_symlink() for p in skills.iterdir()),
                "la portee globale par defaut pose des liens, pas des copies",
            )
            self.assertEqual(
                (ROOT / "skills" / "azd").resolve(),
                (skills / "azd").resolve(),
                "le lien doit pointer vers le clone AZDone",
            )

            listing_after_first = self._entries(skills)
            second = self._run("claude", "--global", home=home)
            self.assertEqual(0, second.returncode, second.stderr)
            self.assertEqual(listing_after_first, self._entries(skills))

    def test_global_copy_install_writes_real_directories(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)

            result = self._run("codex", "--global", "--copy", home=home)
            self.assertEqual(0, result.returncode, result.stderr)

            skills = home / ".agents/skills"
            self.assertEqual(20, len(self._entries(skills)))
            self.assertFalse(
                any(p.is_symlink() for p in skills.iterdir()),
                "--copy doit figer une version, donc copier",
            )
            self.assertTrue((skills / "azd" / "SKILL.md").is_file())
            self.assertFalse((home / ".agents/agents").exists())

    def test_global_copy_install_places_subagent_cards_as_files(self) -> None:
        # Les cartes de agents/ sont des fichiers : les copier comme des
        # dossiers echoue et laisse un dossier parasite derriere.
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)

            first = self._run("claude", "--global", "--copy", home=home)
            self.assertEqual(0, first.returncode, first.stderr)

            agents = home / ".claude/agents"
            cards = sorted(p for p in agents.iterdir())
            self.assertEqual(5, len(cards))
            for card in cards:
                self.assertTrue(card.is_file(), f"{card.name} doit etre un fichier")
                self.assertTrue(card.name.endswith(".md"))

            second = self._run("claude", "--global", "--copy", home=home)
            self.assertEqual(0, second.returncode, second.stderr)
            self.assertEqual(cards, sorted(p for p in agents.iterdir()))

    def test_global_install_never_clobbers_a_real_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            foreign = home / ".claude/skills/azd"
            foreign.mkdir(parents=True)
            witness = "skill maison, ne pas toucher\n"
            (foreign / "SKILL.md").write_text(witness, encoding="utf-8")

            result = self._run("claude", "--global", home=home)

            self.assertEqual(1, result.returncode, "un conflit doit sortir en erreur")
            self.assertEqual(
                witness,
                (foreign / "SKILL.md").read_text(encoding="utf-8"),
                "le contenu existant doit survivre au conflit",
            )
            self.assertIn("Rien n'a ete supprime", result.stderr)

    def test_global_install_never_replaces_a_foreign_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            elsewhere = home / "ailleurs"
            elsewhere.mkdir()
            skills = home / ".claude/skills"
            skills.mkdir(parents=True)
            (skills / "azd").symlink_to(elsewhere)

            result = self._run("claude", "--global", home=home)

            self.assertEqual(1, result.returncode)
            self.assertEqual(
                elsewhere,
                Path(os.readlink(skills / "azd")),
                "un lien qui pointe hors du clone AZDone reste intact",
            )

    def test_global_install_does_not_install_the_trust_hook(self) -> None:
        # Le hook lit le .azdone/trust.yaml du projet : il n'a pas de sens
        # dans une configuration personnelle.
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            result = self._run("claude", "--global", home=home)

            self.assertEqual(0, result.returncode, result.stderr)
            self.assertFalse((home / ".claude/hooks").exists())

    def test_codex_global_install_asks_the_human_to_confirm_the_path(self) -> None:
        # La documentation OpenAI ne source que .agents/skills en repo-local :
        # le script ne doit pas presenter la portee globale comme verifiee.
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            result = self._run("codex", "--global", home=home)

            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("Confirmez", result.stdout)
            self.assertIn(".agents/skills", result.stdout)

    def test_global_refuses_a_project_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            result = self._run("claude", str(home), "--global", home=home)
            self.assertEqual(1, result.returncode)

    def test_copy_without_global_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            result = self._run("claude", "--copy", home=home)
            self.assertEqual(1, result.returncode)

    def test_project_scope_is_still_the_documented_default(self) -> None:
        text = read(ROOT / "docs" / "installation.md")
        self.assertIn("--global", text)
        self.assertIn("La portée projet reste le défaut", text)


class HostCapabilitiesCacheTests(unittest.TestCase):
    """Le cache hors depot ne contient que des faits sondes."""

    def test_reference_exists_and_is_linked_from_the_skill(self) -> None:
        self.assertTrue(CACHE_REFERENCE.is_file())
        self.assertIn("(references/host-capabilities.md)", read(SETUP_SKILL))

    def test_setup_reads_the_cache_before_probing(self) -> None:
        text = read(SETUP_SKILL)
        self.assertIn(CACHE_PATH, text)
        self.assertIn("ignoré en silence", text)

    def test_setup_announces_every_write_outside_the_repository(self) -> None:
        self.assertIn("n'est jamais silencieuse", read(SETUP_SKILL))

    def test_no_decision_key_may_enter_the_cache(self) -> None:
        reference = read(CACHE_REFERENCE)
        for key in DECISION_KEYS:
            self.assertIn(key, reference, f"{key} doit etre nomme comme interdit")
        self.assertIn("jamais", reference)
        self.assertIn("trust.yaml", reference)

    def test_setup_forbids_writing_a_decision_into_the_cache(self) -> None:
        text = read(SETUP_SKILL)
        self.assertIn("Ne jamais écrire une décision", text)

    def test_cache_staleness_is_bounded(self) -> None:
        self.assertIn("30 jours", read(CACHE_REFERENCE))
        self.assertIn("30 jours", read(SETUP_SKILL))

    def test_cache_is_documented_for_removal(self) -> None:
        self.assertIn("host-capabilities.json", read(ROOT / "docs" / "installation.md"))


class CodexSubagentTests(unittest.TestCase):
    """multi_agent se detecte et se documente, il ne s'ecrit jamais."""

    def test_setup_detects_the_flag_read_only(self) -> None:
        text = read(SETUP_SKILL)
        self.assertIn("multi_agent = true", text)
        self.assertIn("~/.codex/config.toml", text)
        self.assertIn("lecture seule", text)

    def test_setup_never_writes_the_global_codex_config(self) -> None:
        text = read(SETUP_SKILL)
        self.assertIn("Ne jamais écrire dans `~/.codex/config.toml`", text)
        self.assertIn("install_global", text)

    def test_routing_and_guide_agree_on_the_fallback(self) -> None:
        for path in (MODEL_ROUTING, GUIDE_MODELS):
            text = read(path)
            self.assertIn("multi_agent", text, f"{path.name} ignore multi_agent")
            self.assertIn(
                "subagents-unavailable",
                text,
                f"{path.name} doit garder le repli explicite",
            )

    def test_the_flag_is_not_presented_as_a_proof(self) -> None:
        # Presence du flag = fait lisible. Sous-agents reellement livres =
        # non prouve : le run doit pouvoir retomber et le dire.
        self.assertIn("ne les prouve pas", read(GUIDE_MODELS))
        self.assertIn(
            "Le flag rend les sous-agents natifs possibles, il ne les prouve pas",
            read(SETUP_SKILL),
        )
        self.assertIn("retombe sur `subagents-unavailable`", read(SETUP_SKILL))


class PermanentPointerTests(unittest.TestCase):
    """Fichier de controle du projet d'abord, global sur demande explicite."""

    def test_pointer_covers_the_three_hosts(self) -> None:
        self.assertIn("Sur les trois hôtes", read(SETUP_SKILL))

    def test_project_control_file_comes_first(self) -> None:
        self.assertIn("Le fichier du projet passe toujours en premier", read(SETUP_SKILL))

    def test_global_control_file_needs_an_explicit_request(self) -> None:
        text = read(SETUP_SKILL)
        self.assertIn("~/.codex/AGENTS.md", text)
        self.assertIn("explicitement dans le tour courant", text)

    def test_the_single_control_file_rule_survives(self) -> None:
        self.assertIn("Ne jamais créer de second fichier de contrôle", read(SETUP_SKILL))


if __name__ == "__main__":
    unittest.main()
