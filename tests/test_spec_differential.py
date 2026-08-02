"""Consistency check between the engine and the orthography2ipa spec.

The engine is spec-driven, so its outputs must be spec-valid. Two guards:

- the primary digraph realisations are declared candidates in the spec's
  grapheme table (nh→ɲ, ch→ʃ, lh→ʎ, tch→tʃ);
- a probe word containing each digraph actually surfaces that phone (a phone may
  carry a leading stress mark, which is stripped before matching).
"""
import pytest

from orthography2ipa import get

from g2p_barranquenho import phonemize


@pytest.fixture(scope="module")
def spec():
    return get("ext-PT-x-barrancos")


_DIGRAPHS = [
    ("nh", "ɲ", "nhada"),
    ("ch", "ʃ", "chave"),
    ("lh", "ʎ", "lhano"),
    ("tch", "tʃ", "tchapa"),
]


class TestDigraphsInSpec:
    """The primary digraph outputs must be spec-valid candidates."""

    @pytest.mark.parametrize("digraph,ipa,_probe", _DIGRAPHS)
    def test_output_declared_in_spec(self, spec, digraph, ipa, _probe):
        candidates = spec.graphemes.get(digraph, [])
        assert ipa in candidates, f"{ipa!r} not in spec.graphemes[{digraph!r}]: {candidates}"


class TestDigraphsRealised:
    """A probe word surfaces the digraph's phone (ignoring any stress mark)."""

    @pytest.mark.parametrize("digraph,ipa,probe", _DIGRAPHS)
    def test_probe_contains_phone(self, digraph, ipa, probe):
        # the affricate tʃ surfaces as two adjacent chars in a flat IPA string,
        # so match the digraph's phones as a substring of the joined output
        joined = "".join(phonemize(probe)).replace("ˈ", "").replace("ˌ", "")
        assert ipa in joined, f"{probe!r} -> {phonemize(probe)} missing {ipa!r}"
