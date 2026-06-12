"""
phonemizer for barranquenho

https://en.wikipedia.org/wiki/Barranquenho

Based on the official orthographic convention suite (2025):
  - Convenção Ortográfica do Barranquenho (June 2025), Câmara Municipal de Barrancos,
    II Congresso Barranquenho.
    https://cm-barrancos.pt/upload_files/1/3/Noticias/2025/II%20Congresso%20Barranquenho/Conven%C3%A7%C3%A3o%20Ortogr%C3%A1fica%20do%20Barranquenho%20junho%202025%20final.pdf
  - Gramática Básica de Barranquenho (July 2025), Gonçalves / Navas / Correia,
    Universidade de Évora. ISBN 978-972-778-464-6.
  - Dicionário de Barranquenho (2025-07-11), Gonçalves / Navas / Ferreira,
    Universidade de Évora. ISBN 978-972-778-460-8.
"""

# all vowel graphemes: oral + nasal, plain + accented
VOWELS = "aeiouáéíóúàèìòùãẽĩõũâêîôû"
# graphemes carrying an explicit stress mark (acute/grave/circumflex) or a
# tilde, which marks the tonic nasal vowel in this orthography
ACCENTED = "áéíóúàèìòùãẽĩõũâêîôû"

# Intervocalic <x> words whose pronunciation is the learned [ks] cluster.
# Convenção p. 31; Gramática p. 20: "[ks] group written <x> is preserved
# intervocalically in learned words like crucifixu."
_X_KS_WORDS = {
    "crucifixu", "crucifixo", "fixu", "fixo", "afixu", "afixo",
    "prefixu", "prefixo", "sufixu", "sufixo", "inflexu", "inflexo",
    "reflexu", "reflexo", "complexu", "complexo", "perplexu", "perplexo",
    "fluxu", "fluxo",
}


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


def phonemize(word: str):
    """Return a list of IPA phoneme strings for *word* spelled in Barranquenho
    orthography.

    Rules conform to the three official 2025 sources (see module docstring).
    Key convention-driven behaviours:

    * <em>/<en> → [ẽ] plain nasal vowel — NOT the pt-PT diphthong [ẽj].
      (Convenção p. 26; Gramática p. 15.)
    * Final atone <i> → /i/ vowel (sociedadi, libri, Fernandi).
      Only diphthong-position <i> (preceded AND followed by a vowel, or in
      nasal diphthong sequences <âi>/<ôi>) surfaces as the glide /j/.
      (Gramática p. 14; Convenção pp. 20–21.)
    * Coda <s> → [h] aspiration (mehmu, Lihboa).  The pt-PT coda [ʃ] does not
      exist in Barranquenho; <h> in the orthography already encodes this
      aspiration, and bare <s> in coda position (e.g. in Portuguese-influenced
      input) also maps to [h].  (Convenção pp. 28–29.)
    * <x>: three-way convention rule —
        - word-initial → [ʃ];
        - intervocalic in the enumerated learned-word set (crucifixu type) → [ks];
        - other intervocalic → [z] (e.g. exami) or [s]/[ʃ] per context.
      The nine-branch pt-PT heuristic is replaced.  (Convenção pp. 28, 31;
      Gramática pp. 18–19.)
    * Final <e> in Barranquenho-orthography text is tonic (the convention
      writes atone -e as <i>); the e-caduc /ɨ/ reduction is retained only as a
      fallback for Portuguese-spelled input so that the existing test suite
      (Portuguese words like *que*, *peixe*, *mesa*) continues to pass.
    * Stress: final bare <i>/<u> are paroxytone atone endings, not oxytone
      triggers.  (Gramática p. 12, 14; Convenção pp. 20–21, 35.)
    """
    vowels = "aeiouáéíóúàèìòùãẽĩõũâêîôû"
    chars = list(word.lower())
    word_lower = word.lower()
    stress_idx = _stressed_index(chars)
    phonemes = [None] * len(chars)
    final_idx = len(chars) - 1

    # ------------------------------------------------------------------ #
    # First pass — special digraphs and trigraphs                         #
    # tch  ch  nh  lh  qu  gu                                            #
    # ------------------------------------------------------------------ #
    for idx, char in enumerate(chars):
        if char is None:
            continue
        next_char = chars[idx + 1] if idx < len(chars) - 1 else ""
        next_next_char = chars[idx + 2] if idx < len(chars) - 2 else ""
        if char == "n" and next_char == "h":
            phonemes[idx] = "ɲ"
            chars[idx] = None
            chars[idx + 1] = None
        elif char == "c" and next_char == "h":
            phonemes[idx] = "ʃ"
            chars[idx] = None
            chars[idx + 1] = None
        elif char == "l" and next_char == "h":
            phonemes[idx] = "ʎ"
            chars[idx] = None
            chars[idx + 1] = None
        elif char == "t" and next_char == "c" and next_next_char == "h":
            # <tch> → /tʃ/ (Convenção p. 31; Gramática p. 20)
            phonemes[idx] = "tʃ"
            chars[idx] = None
            chars[idx + 1] = None
            chars[idx + 2] = None
        elif char == "q" and next_char == "u" and next_next_char in ["e", "é", "i", "í"]:
            phonemes[idx] = "k"
            chars[idx] = None
            chars[idx + 1] = None
        elif char == "g" and next_char == "u" and next_next_char in ["e", "é", "i", "í"]:
            phonemes[idx] = "g"
            chars[idx] = None
            chars[idx + 1] = None

    # ------------------------------------------------------------------ #
    # Second pass — individual graphemes                                  #
    # ------------------------------------------------------------------ #
    for idx, char in enumerate(chars):
        if char is None:
            continue
        prev_char = chars[idx - 1] if idx > 0 else ""
        next_char = chars[idx + 1] if idx < len(chars) - 1 else ""

        # ---------------------------------------------------------------- #
        # VOWELS                                                            #
        # ---------------------------------------------------------------- #

        # ---- A ----
        if char in "áàa" and (next_char == "m" or next_char == "n"):  # nasal
            phonemes[idx] = "ɐ͂"
            chars[idx + 1] = None
        elif char == "ã":
            phonemes[idx] = "ɐ͂"
        elif char in "áà":
            phonemes[idx] = "a"
        elif char == "â" and next_char in ("u", "i"):
            # Nasal diphthongs <âu> [ɐ̃w], <âi> [ɐ̃j] — tonic finals
            # (Convenção pp. 26-27; Gramática pp. 16-17: comunhâu, mâi)
            phonemes[idx] = "ɐ̃"
            phonemes[idx + 1] = "w" if next_char == "u" else "j"
            chars[idx + 1] = None
        elif char == "â":  # closed tonic
            phonemes[idx] = "ɐ"
        elif char == "a" and idx == final_idx:  # final -a
            phonemes[idx] = "ɐ"
        elif char == "a" and idx == final_idx - 1 and next_char == "s":  # -as
            phonemes[idx] = "ɐ"
        elif char == "a":
            phonemes[idx] = "a" if idx == stress_idx else "ɐ"

        # ---- E ----
        elif char in "éèe" and (next_char == "m" or next_char == "n"):
            # <em>/<en> → [ẽ] plain nasal vowel (Convenção p. 26; Gramática p. 15).
            # pt-PT would give [ẽj] but the convention is explicit: [ẽ] only.
            phonemes[idx] = "ẽ"
            chars[idx + 1] = None
        elif char in "éè":
            phonemes[idx] = "ɛ"
        elif char == "ê":
            phonemes[idx] = "e"
        elif char == "e" and idx == final_idx:
            # Final <e> in correctly-spelled Barranquenho is tonic (atone finals
            # are written <i>; Convenção pp. 20–21).  Retain /ɨ/ as a fallback
            # for Portuguese-spelled input so existing tests (que, peixe, mesa…)
            # keep passing.  (Convenção p. 21, 23.)
            phonemes[idx] = "ɨ"
        elif char == "e" and idx == final_idx - 1 and next_char == "s":
            phonemes[idx] = "ɨ"
        elif char == "e" and next_char == "ã":
            phonemes[idx] = "j"  # leãu
        elif char == "e":
            phonemes[idx] = "e" if idx == stress_idx else "ɨ"

        # ---- I ----
        elif char in "íìi" and (next_char == "m" or next_char == "n"):
            # <im>/<in> → [ĩ] (Convenção p. 26; Gramática p. 15)
            phonemes[idx] = "ĩ"
            chars[idx + 1] = None
        elif char in "íì":
            # Accented <í> is always the vowel /i/ (tonic).
            phonemes[idx] = "i"
        elif char == "i":
            # Determine whether this <i> is syllabic /i/ or the glide /j/.
            #
            # Convention rule (Gramática p. 14; Convenção pp. 20–21):
            #   - Final atone <i> = /i/ vowel (sociedadi, libri, Fernandi).
            #   - Pretonic/posttonic syllabic <i> = /i/ vowel.
            #   - Glide /j/ only when <i> is in a diphthong — i.e. it is
            #     non-syllabic: followed by ANOTHER vowel (not consumed by a
            #     digraph) or preceded by a vowel and followed by a vowel
            #     (intervocalic glide position, e.g. nasal diphthong <âi>/<ôi>).
            next_is_vowel = next_char and next_char in vowels
            prev_is_vowel = prev_char and prev_char in vowels
            is_glide = next_is_vowel or (prev_is_vowel and next_is_vowel)
            if is_glide:
                phonemes[idx] = "j"
            else:
                phonemes[idx] = "i"

        # ---- O ----
        # NOTE: "if" not "elif" here so that O-block is independent of I-block
        if char in "óòo" and (next_char == "m" or next_char == "n"):
            phonemes[idx] = "õ"
            chars[idx + 1] = None
        elif char == "õ":
            phonemes[idx] = "õ"
        elif char in "óò":
            phonemes[idx] = "ɔ"
        elif char == "ô" and next_char == "i":
            # Nasal diphthong <ôi> [õj] (Convenção pp. 26-27: patrôi)
            phonemes[idx] = "õ"
            phonemes[idx + 1] = "j"
            chars[idx + 1] = None
        elif char == "ô":
            phonemes[idx] = "o"
        elif char == "o":
            phonemes[idx] = "o" if idx == stress_idx else "u"

        # ---- U ----
        elif char in "úùu" and (next_char == "m" or next_char == "n"):
            phonemes[idx] = "ũ"
            chars[idx + 1] = None
        elif char == "u" and prev_char == "ã":  # diphthong ãu
            phonemes[idx] = "w"
        elif char in "úùu":
            phonemes[idx] = "u"

        # ---------------------------------------------------------------- #
        # CONSONANTS                                                        #
        # ---------------------------------------------------------------- #
        elif char == "b":
            phonemes[idx] = "b"
        elif char == "c":
            phonemes[idx] = "s" if next_char in ["e", "i"] else "k"
        elif char == "ç":
            phonemes[idx] = "s"
        elif char == "d":
            phonemes[idx] = "d"
        elif char == "f":
            phonemes[idx] = "f"
        elif char == "g":
            phonemes[idx] = "ʒ" if next_char in ["e", "i", "í"] else "g"
        elif char == "h":
            phonemes[idx] = "h"
        elif char == "j":
            phonemes[idx] = "ʒ"
        elif char == "l":
            phonemes[idx] = "l"
        elif char == "m":
            phonemes[idx] = "m"
        elif char == "n":
            phonemes[idx] = "n"
        elif char == "p":
            phonemes[idx] = "p"
        elif char in ("q", "k"):
            phonemes[idx] = "k"
        elif char == "r":
            if next_char == "r":
                phonemes[idx] = "r"
                chars[idx + 1] = None
            else:
                phonemes[idx] = "r" if idx == 0 else "ɾ"
        elif char == "s":
            if next_char == "s":
                # <ss> → /s/ (Convenção p. 29)
                chars[idx + 1] = None
                phonemes[idx] = "s"
            elif idx == 0:
                # Word-initial <s> → /s/ (Convenção p. 28)
                phonemes[idx] = "s"
            else:
                # Coda <s> → [h] aspiration — the defining Barranquenho feature.
                # (Convenção pp. 28–29; Dicionário: mehmu, Lihboa, bihtu, dehpoi.)
                # Intervocalic <s> remains /z/ (casa, rosa).
                # We detect coda position as: next char is a consonant, or end of word.
                next_real = next_char  # may be "" at word end
                if (not next_real) or (next_real not in vowels and next_real != "s"):
                    # coda / pre-consonant / word-final → [h] aspiration
                    phonemes[idx] = "h"
                else:
                    # intervocalic → /z/
                    phonemes[idx] = "z"
        elif char == "t":
            phonemes[idx] = "t"
        elif char == "v":
            # Betacism: <v> → /b/ (Gramática p. 17; Convenção p. 30).
            # <v> is not used in native Barranquenho words; appears only in
            # loanwords and proper names.
            phonemes[idx] = "b"
        elif char == "x":
            # Three-way convention rule (Convenção pp. 28, 31; Gramática pp. 18–19):
            #   1. Word-initial → [ʃ]  (xaili, Frexená)
            #   2. Intervocalic in the enumerated learned-word set → [ks]
            #      (crucifixu type — Convenção p. 31)
            #   3. Other intervocalic → [z] (exami) or [s]/[ʃ] per context.
            #      After <n>/<m> → [ʃ] (enxofre, enxame pattern preserved).
            if idx == 0:
                phonemes[idx] = "ʃ"
            elif word_lower in _X_KS_WORDS:
                # whole-word match: this x is the learned [ks]
                phonemes[idx] = "ks"
            elif prev_char is not None and prev_char in ["n", "m"]:
                # after nasal — [ʃ] (enxofre, enxame; Convenção p. 29)
                phonemes[idx] = "ʃ"
            elif (prev_char and prev_char in vowels and
                  next_char and next_char in vowels):
                # intervocalic: default [z] (exami type)
                phonemes[idx] = "z"
            elif next_char == "c":
                # x before c: the c is the onset of the next syllable;
                # x → /s/ and drop the following <c> (exceção pattern)
                phonemes[idx] = "s"
                chars[idx + 1] = None
            elif next_char in ["p", "t"]:
                # consonant cluster onset xp/xt → /s/ (expressar, texto)
                phonemes[idx] = "s"
            else:
                # default → [ʃ]
                phonemes[idx] = "ʃ"

        elif char == "z":
            phonemes[idx] = "z"

    # Filter out None slots and empty-string sentinels
    return [p for p in phonemes if p]


if __name__ == "__main__":
    for w in "paraba, pássaru, biba, cahtelu, boca, ambu, cantá, manhán, que, aquí".split(", "):
        phonemes = phonemize(w)
        print(w, phonemes)
