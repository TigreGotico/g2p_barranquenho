"""
phonemizer for barranquenho

https://en.wikipedia.org/wiki/Barranquenho

based on https://cm-barrancos.pt/upload_files/1/3/Noticias/2025/II%20Congresso%20Barranquenho/Conven%C3%A7%C3%A3o%20Ortogr%C3%A1fica%20do%20Barranquenho%20junho%202025%20final.pdf
"""

# all vowel graphemes: oral + nasal, plain + accented
VOWELS = "aeiouáéíóúàèìòùãẽĩõũâêîôû"
# graphemes carrying an explicit stress mark (acute/grave/circumflex) or a
# tilde, which marks the tonic nasal vowel in this orthography
ACCENTED = "áéíóúàèìòùãẽĩõũâêîôû"


def _stressed_index(chars):
    """Index of the stressed vowel grapheme.

    An explicit accent fixes the stress. Otherwise the Portuguese default
    applies: the penultimate vowel for words ending in a vowel (optionally
    followed by ``s``), the last vowel otherwise.
    """
    vowel_idx = [i for i, c in enumerate(chars) if c in VOWELS]
    if not vowel_idx:
        return -1
    for i, c in enumerate(chars):
        if c in ACCENTED:
            return i
    last = chars[-1]
    penult = chars[-2] if len(chars) > 1 else ""
    ends_open = last in VOWELS or (last == "s" and penult in VOWELS)
    if ends_open and len(vowel_idx) >= 2:
        return vowel_idx[-2]
    return vowel_idx[-1]


def phonemize(word: str):
    vowels = "aeiouáéíóúàèìòùãẽĩõũâêîôû"
    has_stress = any(c in word for c in "áéíóúàèìòùãẽĩõũâêîôû")
    chars = list(word.lower())
    stress_idx = _stressed_index(chars)
    phonemes = [None] * len(chars)

    # first pass - special digraphs
    # tch ch nh lh qu gu
    for idx, char in enumerate(chars):
        next_char = chars[idx + 1] if idx < len(chars) - 1 else ""
        next_next_char = chars[idx + 2] if idx < len(chars) - 2 else ""
        if char is None:
            continue
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

    # second pass - individual graphemes
    final_idx = len(chars) - 1
    for idx, char in enumerate(chars):
        if char is None:
            continue
        prev_prev_char = chars[idx - 2] if idx > 1 else ""
        prev_char = chars[idx - 1] if idx > 0 else ""
        next_char = chars[idx + 1] if idx < len(chars) - 1 else ""

        # vowels
        # A
        if char in "áàa" and (next_char == "m" or next_char == "n"):  # nasal diphtong
            phonemes[idx] = "ɐ͂"
            chars[idx + 1] = None
        elif char in "ã":   # nasal
            phonemes[idx] = "ɐ͂"
        elif char in "áà":  # stress
            phonemes[idx] = "a"
        elif char == "â":  # closed
            phonemes[idx] = "ɐ"
        elif char == "a" and idx == final_idx:  # -a
            phonemes[idx] = "ɐ"
        elif char == "a" and idx == final_idx - 1 and next_char == "s": # -as
            phonemes[idx] = "ɐ"
        elif char == "a":
            # stressed bare ``a`` is the open central [a]; unstressed ``a``
            # reduces to the near-open central [ɐ]
            phonemes[idx] = "a" if idx == stress_idx else "ɐ"
        # E
        elif char in "éèe" and (next_char == "m" or next_char == "n"): # nasal
            phonemes[idx] = "ẽj"
            chars[idx + 1] = None
        elif char in "éè": # stress
            phonemes[idx] = "ɛ"
        elif char == "ê": #  closed
            phonemes[idx] = "e"
        elif char == "e" and idx == final_idx: # e caduc
            phonemes[idx] = "ɨ"
        elif char == "e" and idx == final_idx - 1 and next_char == "s": # e caduc
            phonemes[idx] = "ɨ"
        elif char == "e" and next_char == "ã":
            phonemes[idx] = "j" #  "leãu"
        elif char == "e":
            # stressed bare ``e`` is the close-mid [e]; unstressed ``e``
            # reduces to the central [ɨ] (e caduc). Word-final and the
            # pre-final ``-es`` cases are already handled above.
            phonemes[idx] = "e" if idx == stress_idx else "ɨ"
        # I
        elif char in "íìi" and (next_char == "m" or next_char == "n"): # nasal
            phonemes[idx] = "ĩ"
            chars[idx + 1] = None
        elif char in "íìi":
            phonemes[idx] = "j"
        # O
        if char in "óòo" and (next_char == "m" or next_char == "n"):  # nasal diphtong
            phonemes[idx] = "õ"
            chars[idx + 1] = None
        elif char in "õ":   # nasal
            phonemes[idx] = "õ"
        elif char in "óò":  # stress
            phonemes[idx] = "ɔ"
        elif char == "ô":  # closed
            phonemes[idx] = "o"
        elif char == "o":
            # stressed bare ``o`` is the close-mid [o]; unstressed ``o``
            # raises to [u], the consistent European-Portuguese reduction
            # retained in Barranquenho
            phonemes[idx] = "o" if idx == stress_idx else "u"
        # U
        elif char in "úùu" and (next_char == "m" or next_char == "n"):  # nasal diphtong
            phonemes[idx] = "ũ"
            chars[idx + 1] = None
        elif char == "u" and prev_char == "ã": # diphtong ãu
            phonemes[idx] = "w"
        elif char in "úùu":
            phonemes[idx] = "u"

        # consonants
        elif char == "b":
            phonemes[idx] = "b"
        elif char == "c":
            if next_char in ["e", "i"]:
                phonemes[idx] = "s"
            else:
                phonemes[idx] = "k"
        elif char == "ç":
            phonemes[idx] = "s"
        elif char == "d":
            phonemes[idx] = "d"
        elif char == "f":
            phonemes[idx] = "f"
        elif char == "g":
            if next_char in ["e", "i", "í"]:
                phonemes[idx] = "ʒ"
            else:
                phonemes[idx] = "g"
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
        elif char == "q" or char == "k":  # K is never used in barranquenho, only for estrangeirisms
            phonemes[idx] = "k"
        elif char == "r":
            if next_char == "r":
                phonemes[idx] = "r"
                chars[idx + 1] = None
            else:
                phonemes[idx] = "r" if idx == 0 else "ɾ"
        elif char == "s":
            if next_char == "s":
                chars[idx + 1] = None
                phonemes[idx] = "s"
            elif idx == 0:
                phonemes[idx] = "s"
            else:
                phonemes[idx] = "z"
        elif char == "t":
            phonemes[idx] = "t"
        elif char == "v":  # NOT USED in barranquenho, it's always written B never V
            phonemes[idx] = "b"
        elif char == "x":
            if idx == 0:
                phonemes[idx] = "ʃ"
            else:
                # disambiguation based on pt-PT rules, lots of edge-cases and no formal rule!

                # n/m-x
                if idx == 0 or prev_char in ["n", "m"]:
                    # enxofre, enxame, enxuto
                    phonemes[idx] = "ʃ"

                # x-c
                elif next_char == "c":
                    #  exceção
                    phonemes[idx] = "s"
                    chars[idx+1] = None

                # vowel-vowel-x
                elif (prev_prev_char in vowels and prev_char in vowels):
                    if prev_prev_char == "a" and prev_char == "u":
                        # auxiliar
                        phonemes[idx] = "s"
                    else:
                        # ameixa, peixe, caixa, abaixo
                        phonemes[idx] = "ʃ"

                # vowel-x-vowel
                elif prev_char in vowels and next_char in vowels:
                    if prev_char in ["ó", "á"] and next_char == "i":
                        # próximo, máximo
                        phonemes[idx] = "s"
                    else:
                        # exame, exato, êxodo, exercício, exemplo e exagero.
                        phonemes[idx] =  "z"

                # x-p/t
                elif next_char in ["p", "t"]:
                    # expressar, explorar, experiência, texto, externo, sexta
                    phonemes[idx] = "s"

                # default
                else:
                    phonemes[idx] =  "ʃ"

        elif char == "z":
            phonemes[idx] = "z"

    phonemes = [p for p in phonemes if p]
    return [p for p in phonemes if p]


if __name__ == "__main__":
    for w in "paraba, pássaru, biba, cahtelu, boca, ambu, cantá, manhán, que, aquí".split(", "):
        phonemes = phonemize(w)
        print(w, phonemes)
