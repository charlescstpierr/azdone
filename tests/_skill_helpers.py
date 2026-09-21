"""Shared helpers for AZDone skill contract tests.

Chantier R: skill contracts (schema fields, contract tokens, concepts) are
being compacted out of SKILL.md into references/*.md (and, for `azd`,
playbooks/*.md). Tests that assert on those contracts should read the whole
*bundle* for a skill instead of hard-coding SKILL.md, so the suite stays
green whether a given token currently lives in SKILL.md or has already moved
to a reference/playbook.

Not named test_*.py, so `unittest discover -p 'test_*.py'` never picks this
module up as a test module on its own; it is only ever imported.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"

_BUNDLE_SEPARATOR = "\n\n<!-- ---- next file ---- -->\n\n"


def skill_dir(name: str) -> Path:
    return SKILLS / name


def read_skill(name: str) -> str:
    """SKILL.md only.

    Use this for assertions that must stay scoped to SKILL.md itself: the
    `name:` frontmatter, the description and its trigger, Quick start /
    concrete invocation, absence of PROVISIONAL, max length, reference
    depth/existence, absence of scripts, and the pilot's domain-agnostic
    routing anchors.
    """
    return (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")


def read_skill_bundle(name: str) -> str:
    """SKILL.md plus every references/*.md and playbooks/*.md for a skill.

    Schema fields, contract tokens, verdicts, gates and named concepts can
    move out of SKILL.md during compaction (chantier C); assertions on those
    should read this bundle instead of SKILL.md alone.
    """
    skill = SKILLS / name
    parts = [(skill / "SKILL.md").read_text(encoding="utf-8")]
    for subdir in ("references", "playbooks"):
        directory = skill / subdir
        if directory.is_dir():
            for path in sorted(directory.glob("*.md")):
                parts.append(path.read_text(encoding="utf-8"))
    return _BUNDLE_SEPARATOR.join(parts)


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower())


def assert_language_rule(test_case, text: str) -> None:
    """Accept either the pre- or post-compaction language rule.

    Before compaction, skill bodies double every sentence in Français and
    English. After compaction, they carry a single rule: reply in the
    user's language ("langue de l'utilisateur"), with commands, paths,
    identifiers and verdicts identical in both languages. Accepting either
    form keeps this suite green across that change.
    """
    lowered = text.lower()
    has_single_rule = "langue de l'utilisateur" in lowered
    has_bilingual_pair = "français" in lowered and "english" in lowered
    test_case.assertTrue(
        has_single_rule or has_bilingual_pair,
        "expected either the single language rule (\"langue de l'utilisateur\") "
        "or both \"Français\" and \"English\" markers",
    )
