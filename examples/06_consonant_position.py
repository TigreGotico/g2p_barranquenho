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
        bare = [p.lstrip("ˈˌ") for p in phonemes]  # a phone may lead with stress
        rhotics = [p for p in bare if p in ("r", "ɾ")]
        sibilants = [p for p in bare if p in ("s", "z", "s̺", "z̺")]
        print(f"{word:10s} {phonemes}   r/ɾ={rhotics}  s/z={sibilants}")


if __name__ == "__main__":
    main()
