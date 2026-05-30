"""Example — the context-sensitive letter x (ʃ / s / z).

Run::

    python examples/04_x_disambiguation.py
"""
from g2p_barranquenho import phonemize


def main() -> None:
    # x resolves differently by surrounding letters; show the realised segment.
    words = ["peixe", "exato", "texto", "exportar", "auxiliar"]
    for word in words:
        phonemes = phonemize(word)
        x_seg = next((p for p in phonemes if p in ("ʃ", "s", "z")), None)
        print(f"{word:10s} {phonemes}   x -> {x_seg}")


if __name__ == "__main__":
    main()
