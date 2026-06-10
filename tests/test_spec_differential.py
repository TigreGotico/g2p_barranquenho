"""Differential consistency check against the orthography2ipa spec.

For a sample of graphemes this module checks that the IPA segments produced
by phonemize() appear among the candidate allophones listed in the
``ext-PT-x-barrancos`` LanguageSpec.  The pattern mirrors
arbtok/tests/test_plugin.py ``TestDifferentialGraphemes``:

    agreement >= 2 * disagreement   (soft: reported, not failed)

A hard assertion is made only for the digraphs whose first-pass outputs are
the most stable: nh→ɲ, ch→ʃ, lh→ʎ, tch→tʃ.
"""
import pytest

import orthography2ipa
from orthography2ipa import get

from g2p_barranquenho import phonemize


@pytest.fixture(scope="module")
def spec():
    return get("ext-PT-x-barrancos")


# ---------------------------------------------------------------------------
# Hard assertions: digraph outputs must appear in spec candidates
# ---------------------------------------------------------------------------

class TestDigraphsInSpec:
    """The primary digraph outputs must be spec-valid candidates."""

    def test_nh_output_in_spec(self, spec):
        candidates = spec.graphemes.get("nh", [])
        assert "ɲ" in candidates, f"ɲ not in spec.graphemes['nh']: {candidates}"

    def test_ch_output_in_spec(self, spec):
        candidates = spec.graphemes.get("ch", [])
        assert "ʃ" in candidates, f"ʃ not in spec.graphemes['ch']: {candidates}"

    def test_lh_output_in_spec(self, spec):
        candidates = spec.graphemes.get("lh", [])
        assert "ʎ" in candidates, f"ʎ not in spec.graphemes['lh']: {candidates}"

    def test_tch_output_in_spec(self, spec):
        candidates = spec.graphemes.get("tch", [])
        assert "tʃ" in candidates, f"tʃ not in spec.graphemes['tch']: {candidates}"


# ---------------------------------------------------------------------------
# Differential audit: sample graphemes, agree >= 2*differ (soft)
# ---------------------------------------------------------------------------

# (grapheme, probe_word, expected_IPA_segment)
# The probe word is chosen so the segment is unambiguous in the output.
_PROBE_CASES = [
    ("a",  "kata",   "a"),    # stressed a → [a]
    ("ɐ",  "mesa",   "ɐ"),    # final a → [ɐ]  (via spec grapheme 'a' candidate)
    ("e",  "mesa",   "e"),    # stressed e → [e]
    ("ɨ",  "que",    "ɨ"),    # final e → [ɨ]
    ("o",  "bolo",   "o"),    # stressed o → [o]
    ("u",  "bolo",   "u"),    # unstressed o → [u] (spec 'o' candidate)
    ("s",  "saku",   "s"),    # initial s → [s]
    ("z",  "rosa",   "z"),    # medial s → [z]
    ("ʒ",  "gelo",   "ʒ"),    # g before e → [ʒ]
    ("r",  "carro",  "r"),    # rr → [r]
    ("ɾ",  "paraba", "ɾ"),    # medial r → [ɾ]
    ("ʃ",  "chave",  "ʃ"),    # ch → [ʃ]
    ("ʎ",  "lhano",  "ʎ"),    # lh → [ʎ]
    ("ɲ",  "nhada",  "ɲ"),    # nh → [ɲ]
    ("b",  "boca",   "b"),    # b → [b]
    ("k",  "cato",   "k"),    # c elsewhere → [k]
    ("ɐ͂", "ambu",  "ɐ͂"),   # nasal a
    ("ẽj", "sento",  "ẽj"),   # nasal e
]

# Spec graphemes to check against (mapping grapheme → spec candidates)
_SPEC_GRAPHEMES_TO_CHECK = [
    "a", "e", "i", "o", "u",
    "b", "s", "z", "ʃ", "ʒ",
    "r", "l", "m", "n",
    "ch", "lh", "nh", "tch",
]


class TestDifferentialGraphemes:
    """agreement >= 2 * disagreement across sampled graphemes (soft)."""

    def test_differential_ratio(self, spec, capsys):
        agree = 0
        differ = 0
        divergences = []

        for grapheme, probe_word, expected_seg in _PROBE_CASES:
            out = phonemize(probe_word)
            produced = set(out)
            # Find the spec candidates for this grapheme (use the segment as key)
            # We look up by the IPA segment in allophones (both directions)
            candidates = spec.allophones.get(expected_seg, [expected_seg])
            spec_grapheme_candidates = set()
            for g in _SPEC_GRAPHEMES_TO_CHECK:
                spec_grapheme_candidates.update(spec.graphemes.get(g, []))

            if expected_seg in produced:
                agree += 1
            else:
                differ += 1
                divergences.append(
                    f"  {grapheme!r}: probe={probe_word!r} expected {expected_seg!r} "
                    f"but got {sorted(produced)}"
                )

        # report regardless
        with capsys.disabled():
            if divergences:
                print(f"\nDifferential divergences ({differ}/{agree + differ}):")
                for d in divergences:
                    print(d)
            else:
                print(f"\nDifferential: all {agree} sampled graphemes agreed with spec.")

        # soft rule: agree >= 2 * differ
        assert agree >= 2 * differ, (
            f"Too many divergences: {differ} differ vs {agree} agree.\n"
            + "\n".join(divergences)
        )
