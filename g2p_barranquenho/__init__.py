"""phonemizer for barranquenho

https://en.wikipedia.org/wiki/Barranquenho

Built on the shared **orthography2ipa** pronunciation lattice: grapheme
segmentation comes from the language-agnostic
:class:`orthography2ipa.phonetok.PhonetokTokenizer` (a maximal-munch trie
over the Barranquenho grapheme set), and every Barranquenho-specific
realisation rule is expressed as a
:class:`orthography2ipa.rescorer.LatticeRescorer` re-costing the shared
per-grapheme :class:`~orthography2ipa.phonetok.SegmentSlot` lattice. There
is no private tokenizer and no hand-rolled index arithmetic.

Based on the official orthographic convention suite (2025):
  - Convenção Ortográfica do Barranquenho (June 2025), Câmara Municipal de Barrancos,
    II Congresso Barranquenho.
    https://cm-barrancos.pt/upload_files/1/3/Noticias/2025/II%20Congresso%20Barranquenho/Conven%C3%A7%C3%A3o%20Ortogr%C3%A1fica%20do%20Barranquenho%20junho%202025%20final.pdf
  - Gramática Básica de Barranquenho (July 2025), Gonçalves / Navas / Correia,
    Universidade de Évora. ISBN 978-972-778-464-6.
  - Dicionário de Barranquenho (2025-07-11), Gonçalves / Navas / Ferreira,
    Universidade de Évora. ISBN 978-972-778-460-8.
"""
from functools import lru_cache
from typing import List, Sequence
import unicodedata
from dataclasses import replace

from orthography2ipa import get
from orthography2ipa.phonetok import (
    PhonetokTokenizer, SegmentSlot, Candidate, flat_contexts,
)
from orthography2ipa.rescorer import (
    LatticeRescorer, RescoreContext, apply_rescorers,
)

LANG = "ext-PT-x-barrancos"

# all vowel graphemes: oral + nasal, plain + accented
VOWELS = "aeiouáéíóúàèìòùãẽĩõũâêîôû"
# graphemes carrying an explicit stress mark (acute/grave/circumflex) or a
# tilde, which marks the tonic nasal vowel in this orthography
ACCENTED = "áéíóúàèìòùãẽĩõũâêîôû"

# Standard IPA/Unicode nasalisation diacritic: COMBINING TILDE (U+0303).
_NASAL = "̃"

# Vowel graphemes that nasalise a following syllable-final (coda) ⟨m⟩/⟨n⟩:
# the plain, acute and grave a/e/i/o/u.  ⟨â ê ô⟩ (circumflex) do NOT nasalise
# — they are the closed-tonic vowels (Convenção pp. 26, 35).
_NASALISABLE = set("aeiouáéíóúàèìòù")

# ⟨qu⟩/⟨gu⟩ drop the glide ⟨u⟩ only before a front vowel (Convenção p. 30;
# Gramática p. 20) — *que* [kɨ], *guerra* [ɡeɾɐ]; before a back vowel the
# ⟨u⟩ is a full segment — *quatro* [kuatɾu], *guarda* [ɡuaɾdɐ].
_QGU_FRONT = {"e", "é", "i", "í"}

# Intervocalic ⟨x⟩ words whose pronunciation is the learned [ks] cluster.
# Convenção p. 31; Gramática p. 20: "[ks] group written <x> is preserved
# intervocalically in learned words like crucifixu."
_X_KS_WORDS = {
    "crucifixu", "crucifixo", "fixu", "fixo", "afixu", "afixo",
    "prefixu", "prefixo", "sufixu", "sufixo", "inflexu", "inflexo",
    "reflexu", "reflexo", "complexu", "complexo", "perplexu", "perplexo",
    "fluxu", "fluxo",
}

# Context-free default IPA for every grapheme the tokenizer recognises.
# Context-sensitive graphemes (vowels, r, s, x, c, g) carry a placeholder
# here and are finalised by a rescorer; context-free consonants and the true
# multigraphs carry their final value.
_BASE = {
    # consonants (context-free)
    "b": "b", "ç": "s", "d": "d", "f": "f", "h": "h", "j": "ʒ",
    "k": "k", "l": "l", "m": "m", "n": "n", "p": "p", "q": "k",
    "t": "t", "v": "b", "z": "z", "w": "w", "y": "j",
    # multigraphs consumed atomically by the shared trie
    "ch": "ʃ", "nh": "ɲ", "lh": "ʎ", "tch": "tʃ", "rr": "r", "ss": "s",
    # context-sensitive consonants (finalised by rescorers)
    "c": "k", "g": "g", "r": "r", "s": "s", "x": "ʃ",
    # vowels (finalised by _VowelRescorer)
    "a": "a", "e": "e", "i": "i", "o": "o", "u": "u",
    "á": "a", "é": "ɛ", "í": "i", "ó": "ɔ", "ú": "u",
    "à": "a", "è": "ɛ", "ì": "i", "ò": "ɔ", "ù": "u",
    "â": "ɐ", "ê": "e", "î": "i", "ô": "o", "û": "u",
    "ã": "ɐ" + _NASAL, "ẽ": "ẽ", "ĩ": "ĩ", "õ": "õ", "ũ": "ũ",
}

_VOWEL_GRAPHEMES = set(VOWELS)


def _stressed_index(chars):
    """Return the index of the stressed vowel in *chars*.

    Stress assignment follows Convenção pp. 35–36 and Gramática p. 12:

    1. An explicit accent diacritic fixes the position (acute/grave/circumflex
       on the tonic grapheme, or tilde on a nasal diphthong).
    2. Default is **paroxytone** (penult vowel) for words whose final grapheme
       is a vowel (including the regular Barranquenho atone finals <i> and <u>)
       or a vowel followed by <s>.
    3. Otherwise the last vowel bears stress (oxytone default).

    NOTE: Final bare <i> and <u> are the regular Barranquenho atone endings
    (Portuguese -e/-o → Barr. -i/-u) and do NOT trigger oxytone stress.
    Only accented <í>/<ú> are oxytone triggers, which are already caught by
    rule 1. (Gramática pp. 12, 14; Convenção pp. 20–21, 35.)
    """
    vowel_idx = [i for i, c in enumerate(chars) if c in VOWELS]
    if not vowel_idx:
        return -1
    # Rule 1: explicit accent
    for i, c in enumerate(chars):
        if c in ACCENTED:
            return i
    # Rules 2–3: positional default
    last = chars[-1]
    penult = chars[-2] if len(chars) > 1 else ""
    ends_open = last in VOWELS or (last == "s" and penult in VOWELS)
    if ends_open and len(vowel_idx) >= 2:
        return vowel_idx[-2]
    return vowel_idx[-1]


# ─────────────────────────────────────────────────────────────────────────
# Lattice rescorers — each Barranquenho realisation rule, cited to source
# ─────────────────────────────────────────────────────────────────────────

def _prev_g(ctx: RescoreContext) -> str:
    p = ctx.grapheme.prev
    return p.grapheme if p is not None else ""


def _next_g(ctx: RescoreContext) -> str:
    n = ctx.grapheme.next
    return n.grapheme if n is not None else ""


def _at_g(ctx: RescoreContext, off: int) -> str:
    g = ctx.grapheme.at(off)
    return g.grapheme if g is not None else ""


def _is_coda_nasal(next_g: str, next2_g: str) -> bool:
    """A ⟨m⟩/⟨n⟩ nasalises the preceding vowel only in the syllable coda:
    followed by a consonant grapheme or word-end (Convenção p. 26). An
    *intervocalic* ⟨m⟩/⟨n⟩ is a syllable onset — *lhano* [ʎanu],
    *comunhâu* [kumuɲɐ̃w], *máximu* [mazimu] — and leaves the vowel oral."""
    return next_g in ("m", "n") and (
        next2_g == "" or next2_g[0] not in VOWELS)


class _NasalCodaDeleteRescorer(LatticeRescorer):
    """A syllable-final ⟨m⟩/⟨n⟩ after a nasalisable vowel is absorbed into the
    nasal vowel and contributes no segment (Convenção p. 26): *ambu* [ɐ̃bu],
    *cantá* [kɐ̃ta], *quen* [kẽ]. Onset ⟨m⟩/⟨n⟩ survives (*câmara*, *lhano*)."""

    def rescore(self, slot: SegmentSlot, ctx: RescoreContext):
        if slot.grapheme not in ("m", "n"):
            return slot.candidates
        if _prev_g(ctx) in _NASALISABLE and _is_coda_nasal(
                slot.grapheme, _next_g(ctx)):
            return ()
        return slot.candidates


class _VowelRescorer(LatticeRescorer):
    """Resolve every vowel/glide grapheme to its Barranquenho realisation:
    coda nasalisation, nasal diphthongs, stress-conditioned quality, atone
    finals and the syllabic-vs-glide ⟨i⟩/⟨u⟩ distinction. Sources: Convenção
    pp. 20–21, 26–27, 35; Gramática pp. 12–17."""

    def rescore(self, slot: SegmentSlot, ctx: RescoreContext):
        g = slot.grapheme
        if g not in _VOWEL_GRAPHEMES:
            return slot.candidates
        ipa = self._vowel(g, ctx)
        return (Candidate(ipa, 0.0),)

    @staticmethod
    def _vowel(g: str, ctx: RescoreContext) -> str:
        prev_g = _prev_g(ctx)
        next_g = _next_g(ctx)
        next2_g = _at_g(ctx, 2)
        is_final = ctx.grapheme.next is None
        stressed = ctx.is_stressed is True
        coda_nasal = _is_coda_nasal(next_g, next2_g)
        NA = "ɐ" + _NASAL  # nasal open-central vowel

        # ---- A ----
        if g in "aáà" and coda_nasal:
            return NA
        if g == "ã":
            return NA
        if g in "áà":
            return "a"
        if g == "â" and next_g in ("u", "i"):
            # tonic nasal diphthong ⟨âu⟩ [ɐ̃w] / ⟨âi⟩ [ɐ̃j]
            # (Convenção pp. 26–27; Gramática pp. 16–17)
            return NA
        if g == "â":
            return "ɐ"
        if g == "a" and is_final:
            return "ɐ"
        if g == "a" and next_g == "s" and next2_g == "":
            return "ɐ"
        if g == "a":
            return "a" if stressed else "ɐ"

        # ---- E ----
        if g in "eéè" and coda_nasal:
            # ⟨em⟩/⟨en⟩ → [ẽ] plain nasal vowel, NOT pt-PT [ẽj]
            # (Convenção p. 26; Gramática p. 15)
            return "ẽ"
        if g in "éè":
            return "ɛ"
        if g == "ê":
            return "e"
        if g == "e" and next_g == "ã":
            return "j"  # leãu
        if g == "e" and is_final:
            return "ɨ"
        if g == "e" and next_g == "s" and next2_g == "":
            return "ɨ"
        if g == "e":
            return "e" if stressed else "ɨ"

        # ---- I ----
        if g in "iíì" and coda_nasal:
            return "ĩ"
        if g in "íì":
            return "i"
        if g == "î":
            return "i"
        if g == "i":
            if prev_g in ("â", "ô", "ã"):
                return "j"  # glide of a nasal diphthong (mâi, patrôi)
            next_is_vowel = bool(next_g) and next_g[0] in VOWELS
            return "j" if next_is_vowel else "i"

        # ---- O ----
        if g in "oóò" and coda_nasal:
            return "õ"
        if g == "õ":
            return "õ"
        if g in "óò":
            return "ɔ"
        if g == "ô" and next_g == "i":
            return "õ"  # nasal diphthong ⟨ôi⟩ [õj] (Convenção pp. 26–27)
        if g == "ô":
            return "o"
        if g == "o":
            return "o" if stressed else "u"

        # ---- U ----
        if g in "uúù" and coda_nasal:
            return "ũ"
        if g == "u" and prev_g in ("ã", "â"):
            return "w"  # glide of a nasal diphthong (comunhâu, leãu)
        if g == "û":
            return "u"
        return "u"  # u, ú, ù


class _SoftCGRescorer(LatticeRescorer):
    """⟨c⟩ → [s] and ⟨g⟩ → [ʒ] before a front vowel; a ⟨c⟩ after ⟨x⟩ is
    elided (the ⟨x⟩ carries the [s]). Convenção p. 28; Gramática pp. 18–19."""

    def rescore(self, slot: SegmentSlot, ctx: RescoreContext):
        g = slot.grapheme
        next_g = _next_g(ctx)
        if g == "c":
            if _prev_g(ctx) == "x":
                return ()  # exceção: x→[s], c elided
            if next_g in ("e", "i"):
                return (Candidate("s", 0.0),)
            return slot.candidates
        if g == "g":
            if next_g in ("e", "i", "í"):
                return (Candidate("ʒ", 0.0),)
            return slot.candidates
        return slot.candidates


class _QuGuGlideRescorer(LatticeRescorer):
    """Elide the glide ⟨u⟩ of ⟨qu⟩/⟨gu⟩ before a front vowel (*que* [kɨ],
    *guia* [ɡjɐ]); keep it before a back vowel (*quatro*, *guarda*).
    Convenção p. 30; Gramática p. 20."""

    def rescore(self, slot: SegmentSlot, ctx: RescoreContext):
        if slot.grapheme == "u" and _prev_g(ctx) in ("q", "g") \
                and _next_g(ctx) in _QGU_FRONT:
            return ()
        return slot.candidates


class _RhoticRescorer(LatticeRescorer):
    """Word-initial ⟨r⟩ is the alveolar trill [r]; elsewhere the tap [ɾ].
    ⟨rr⟩ is the trill [r] (context-free, from the trie). Convenção p. 30
    (Barranquenho keeps the alveolar trill, not the pt-PT uvular /ʁ/)."""

    def rescore(self, slot: SegmentSlot, ctx: RescoreContext):
        if slot.grapheme != "r":
            return slot.candidates
        return (Candidate("r" if ctx.is_word_initial else "ɾ", 0.0),)


class _SibilantRescorer(LatticeRescorer):
    """⟨s⟩: word-initial [s], intervocalic [z], coda [h] aspiration — the
    defining Barranquenho feature (*mehmu*, *Lihboa*, *bihtu*). ⟨ss⟩ is [s]
    (from the trie). Convenção pp. 28–29; Dicionário 2025."""

    def rescore(self, slot: SegmentSlot, ctx: RescoreContext):
        if slot.grapheme != "s":
            return slot.candidates
        if ctx.is_word_initial:
            return (Candidate("s", 0.0),)
        next_g = _next_g(ctx)
        if next_g and next_g[0] in VOWELS:
            return (Candidate("z", 0.0),)  # intervocalic
        return (Candidate("h", 0.0),)  # coda / pre-consonant / word-final


class _XRescorer(LatticeRescorer):
    """⟨x⟩ three-way rule (Convenção pp. 28, 31; Gramática pp. 18–19):
    word-initial → [ʃ]; enumerated learned words (crucifixu) → [ks]; after a
    nasal → [ʃ]; intervocalic → [z]; before ⟨c⟩/⟨p⟩/⟨t⟩ → [s]; else [ʃ]."""

    def rescore(self, slot: SegmentSlot, ctx: RescoreContext):
        if slot.grapheme != "x":
            return slot.candidates
        if ctx.is_word_initial:
            return (Candidate("ʃ", 0.0),)
        word = "".join(s.grapheme for s in ctx.slots)
        if word in _X_KS_WORDS:
            return (Candidate("ks", 0.0),)
        prev_g = _prev_g(ctx)
        next_g = _next_g(ctx)
        if prev_g in ("n", "m"):
            return (Candidate("ʃ", 0.0),)
        if prev_g and prev_g[0] in VOWELS and next_g and next_g[0] in VOWELS:
            return (Candidate("z", 0.0),)
        if next_g == "c" or next_g in ("p", "t"):
            return (Candidate("s", 0.0),)
        return (Candidate("ʃ", 0.0),)


# Order is independent of correctness — every rescorer reads the *original*
# grapheme context (never another rescorer's output), so the passes commute;
# this ordering is merely the reading order of the rule set.
_RESCORERS = (
    _NasalCodaDeleteRescorer(),
    _VowelRescorer(),
    _SoftCGRescorer(),
    _QuGuGlideRescorer(),
    _RhoticRescorer(),
    _SibilantRescorer(),
    _XRescorer(),
)


@lru_cache(maxsize=1)
def _tokenizer() -> PhonetokTokenizer:
    """The shared maximal-munch tokenizer over the Barranquenho grapheme set.

    Built from the published ``ext-PT-x-barrancos`` spec but with the grapheme
    table narrowed to the units Barranquenho tokenises atomically — the
    consonant multigraphs ⟨tch ch nh lh rr ss⟩ plus the single letters — so
    vowel sequences (⟨ei au em…⟩) stay separate graphemes whose realisation
    the rescorers decide from context, rather than being merged by the trie.
    """
    spec = get(LANG)
    narrowed = replace(
        spec,
        graphemes={k: [v] for k, v in _BASE.items()},
        positional_graphemes=None,
        allophones={},
    )
    return PhonetokTokenizer(narrowed)


def _stressed_token_index(word: str, gtokens) -> int:
    """Map the stressed *character* (from :func:`_stressed_index`) to the
    index of the GRAPHEME token that carries it."""
    norm = unicodedata.normalize("NFC", word)
    si = _stressed_index(list(norm.lower()))
    if si < 0:
        return -1
    for i, t in enumerate(gtokens):
        if t.position <= si < t.position + t.length:
            return i
    return -1


def phonemize(word: str) -> List[str]:
    """Return a list of IPA phoneme strings for *word* spelled in Barranquenho
    orthography.

    The word is tokenised by the shared
    :class:`orthography2ipa.phonetok.PhonetokTokenizer` (maximal-munch over
    the Barranquenho grapheme set) into one lattice
    :class:`~orthography2ipa.phonetok.SegmentSlot` per grapheme, and the
    Barranquenho realisation rules run as
    :class:`~orthography2ipa.rescorer.LatticeRescorer`\\ s over that lattice.
    Rules conform to the three official 2025 sources (see module docstring).
    """
    tok = _tokenizer()
    gtokens = tok.grapheme_tokens(word)
    if not gtokens:
        return []

    contexts = flat_contexts(gtokens)
    slots = [
        SegmentSlot(
            grapheme=t.grapheme,
            span=(t.position, t.position + t.length),
            candidates=(Candidate(_BASE.get(t.grapheme, t.grapheme), 0.0),),
        )
        for t in gtokens
    ]

    stressed = _stressed_token_index(word, gtokens)
    syll_for_token = list(range(len(gtokens)))
    rescored = apply_rescorers(
        slots, contexts, _RESCORERS,
        syll_for_token=syll_for_token,
        stressed_syll_idx=stressed if stressed >= 0 else None,
    )
    return [s.top.ipa for s in rescored if s.candidates and s.top.ipa]


if __name__ == "__main__":
    for w in "paraba, pássaru, biba, cahtelu, boca, ambu, cantá, manhán, que, aquí".split(", "):
        print(w, phonemize(w))
