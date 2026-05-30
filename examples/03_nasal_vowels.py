"""Example — nasal vowels: a vowel before m/n swallows it and nasalises.

Run::

    python examples/03_nasal_vowels.py
"""
from g2p_barranquenho import phonemize


def main() -> None:
    # A vowel before m/n nasalises and absorbs that consonant.
    nasal_marks = ("͂", "̃")  # combining marks used by nasal segments
    words = ["ambu", "cantá", "manhán", "leãu"]
    for word in words:
        phonemes = phonemize(word)
        nasal = [p for p in phonemes if any(m in p for m in nasal_marks)]
        print(f"{word:10s} {phonemes}   nasal segments: {nasal}")


if __name__ == "__main__":
    main()
