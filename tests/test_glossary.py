"""Tests pour docs/glossaire.md : couverture des concepts et contraintes de forme."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GLOSSARY = ROOT / "docs" / "glossaire.md"

REQUIRED_NAMES = [
    "Boussole",
    "Atlas",
    "Language Pack",
    "Route Pack",
    "System Success Map",
    "Project Decision Graph",
    "Readiness Forecast",
    "Proof Contract",
    "Wayfinder",
    "Bootstrap Council",
    "Opportunity Radar",
    "Dreamer",
    "Destroyer",
    "Investor",
    "Ponytail",
    "Decision Stack",
    "Opportunity Inbox",
    "zero-assumption gate",
    "conditions-ok",
    "trust-ledger",
    "feature map",
    "context packet",
    "playbook",
    "lane",
    "frozen evaluator",
]

EM_DASH = "—"


class GlossaryTests(unittest.TestCase):
    def test_glossary_exists(self) -> None:
        self.assertTrue(GLOSSARY.is_file())

    def test_every_required_name_is_bold(self) -> None:
        text = GLOSSARY.read_text(encoding="utf-8")
        missing = [name for name in REQUIRED_NAMES if f"**{name}**" not in text]
        self.assertEqual([], missing)

    def test_glossary_is_at_most_140_lines(self) -> None:
        lines = GLOSSARY.read_text(encoding="utf-8").splitlines()
        self.assertLessEqual(len(lines), 140)

    def test_glossary_has_no_em_dash(self) -> None:
        text = GLOSSARY.read_text(encoding="utf-8")
        self.assertNotIn(EM_DASH, text)


if __name__ == "__main__":
    unittest.main()
