"""Example — the context-sensitive letter x (ʃ / s / z).

Run::

    python examples/04_x_disambiguation.py
"""
from g2p_barranquenho import phonemize


def main() -> None:
    # x resolves differently by surrounding letters; show the realised segment.
    # A phone may carry a leading stress mark, so strip it before matching.
    words = ["peixe", "exato", "texto", "exportar", "auxiliar"]
    for word in words:
        phonemes = phonemize(word)
        bare = [p.lstrip("ˈˌ") for p in phonemes]
        x_seg = next((p for p in bare if p in ("ʃ", "s", "z")), None)
        print(f"{word:10s} {phonemes}   x -> {x_seg}")


if __name__ == "__main__":
    main()
