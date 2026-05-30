"""Example — position-sensitive r and s, and doubled consonants.

Run::

    python examples/06_consonant_position.py
"""
from g2p_barranquenho import phonemize


def main() -> None:
    # r: initial r vs medial ɾ; s: initial s vs medial z; ss/rr collapse.
    words = ["rato", "paraba", "saku", "pássaru"]
    for word in words:
        phonemes = phonemize(word)
        rhotics = [p for p in phonemes if p in ("r", "ɾ")]
        sibilants = [p for p in phonemes if p in ("s", "z")]
        print(f"{word:10s} {phonemes}   r/ɾ={rhotics}  s/z={sibilants}")


if __name__ == "__main__":
    main()
