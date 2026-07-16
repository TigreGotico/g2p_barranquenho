"""Grapheme-to-phoneme converter for Barranquenho (``ext-PT-x-barrancos``).

Barranquenho is an Ibero-Romance variety spoken in Barrancos, Portugal, sharing
features with the Extremaduran and Andalusian varieties of Spanish.
https://en.wikipedia.org/wiki/Barranquenho

The phonology lives in the shared **orthography2ipa** language spec
``ext-PT-x-barrancos``: its grapheme table, allophone rules, stress model and
cross-word sandhi describe every Barranquenho realisation. This package is a
thin caller-side wrapper around :class:`orthography2ipa.G2P` driven by that
spec — it owns text handling (normalisation, tokenisation into the shapes the
spec expects) and the stable ``phonemize``/``transcribe`` surface, not the
phonological rules. Improving a rule means editing the spec upstream, which
every downstream consumer then shares.

Sources behind the spec (page-pinned in the spec's own ``sources`` array):

  - Convenção Ortográfica do Barranquenho (June 2025), Câmara Municipal de
    Barrancos, II Congresso Barranquenho.
  - Gramática Básica de Barranquenho (July 2025), Gonçalves / Navas / Correia,
    Universidade de Évora. ISBN 978-972-778-464-6.
  - Dicionário de Barranquenho (2025), Gonçalves / Navas / Ferreira,
    Universidade de Évora. ISBN 978-972-778-460-8.
  - Navas Sánchez-Élez, M. V. (2011), *El barranqueño: un modelo de lenguas en
    contacto*, Editorial Complutense — the phonetic descriptions the spec cites.
"""
import unicodedata
from functools import lru_cache
from typing import Callable, List, Optional

from orthography2ipa import G2P

from g2p_barranquenho.number_utils import (
    normalize_numbers, BarranquenhoNumberParser,
)

LANG = "ext-PT-x-barrancos"

# Modifier letters and suprasegmentals that bind to the preceding base phone
# when a transcription string is split back into a phone list.
_BINDING = "ːʲʷˠˤ͡"
# Stress marks bind to the following phone (they precede the stressed syllable).
_STRESS = "ˈˌ"


def normalize(text: str) -> str:
    """Caller-side text normalisation applied before phonemisation.

    Barranquenho orthography is case-insensitive for pronunciation and the spec
    is written in NFC, lower case. This folds input to that shape; it performs
    no phonological work (which belongs to the spec).
    """
    return unicodedata.normalize("NFC", text).lower()


@lru_cache(maxsize=1)
def _engine() -> G2P:
    """The shared, spec-driven Barranquenho engine (built once)."""
    return G2P(LANG)


def _split_phones(ipa: str) -> List[str]:
    """Split an IPA string into a phone list that re-joins to the original.

    Combining diacritics and suprasegmental modifiers bind to the preceding
    base phone (so a nasal vowel ``ɐ̃`` is one item); a stress mark binds to the
    phone that follows it. ``"".join(_split_phones(s)) == s``.
    """
    phones: List[str] = []
    for ch in ipa:
        if unicodedata.combining(ch) or ch in _BINDING:
            if phones:
                phones[-1] += ch
            else:
                phones.append(ch)
        elif ch in _STRESS:
            phones.append(ch)
        elif phones and phones[-1] and phones[-1][-1] in _STRESS:
            phones[-1] += ch
        else:
            phones.append(ch)
    return phones


def transcribe(text: str, *, normalizer: Optional[Callable[[str], str]] = normalize,
               expand_numbers: bool = True) -> str:
    """Transcribe Barranquenho *text* to a single IPA string.

    A full utterance is transcribed as a whole so the spec's cross-word sandhi
    applies (coda-/s/ aspiration and deletion, article and conjunction
    destressing, elision). Word boundaries surface as spaces. Pass
    ``normalizer=None`` to feed *text* to the spec verbatim.

    When *expand_numbers* is true (the default), numeric tokens are spelled out
    into Barranquenho words by
    :func:`~g2p_barranquenho.number_utils.normalize_numbers` first — the
    normalizer stage, before the lattice — so digits are transcribed as words.
    Pass ``expand_numbers=False`` to leave digits untouched.
    """
    if expand_numbers:
        text = normalize_numbers(text)
    if normalizer is not None:
        text = normalizer(text)
    return _engine().transcribe(text)


def phonemize(word: str) -> List[str]:
    """Return the IPA phone list for a single Barranquenho *word*.

    Delegates to the ``ext-PT-x-barrancos`` spec via :class:`orthography2ipa.G2P`
    and splits the result into phones (nasal vowels stay a single item; a stress
    mark leads the phone that carries it). ``"".join(phonemize(word))`` is the
    word's IPA string. For multi-word input use :func:`transcribe`, which also
    applies cross-word sandhi.
    """
    ipa = _engine().transcribe_word(normalize(word))
    return _split_phones(ipa)


if __name__ == "__main__":
    for w in "paraba, pássaru, biba, cahtelu, boca, ambu, cantá, manhán, que, aqui".split(", "):
        print(f"{w:10s} {phonemize(w)}  ->  /{''.join(phonemize(w))}/")
    print()
    print(transcribe("O tempu não ehtá nada bom agora."))
