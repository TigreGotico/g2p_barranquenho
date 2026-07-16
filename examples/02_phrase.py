"""Example — transcribe a whole utterance with cross-word sandhi.

``transcribe`` phonemises the sentence as a whole, so the spec's sandhi applies
across word boundaries: coda-/s/ aspiration and deletion, and the destressing of
articles and the conjunction ``e``. Contrast this with phonemising each word in
isolation, which cannot see its neighbours.

Run::

    python examples/02_phrase.py
"""
from g2p_barranquenho import phonemize, transcribe


def main() -> None:
    sentence = "Comprámos pão e vinho na feira de Barrancos."
    print("sentence :", sentence)
    print("sandhi   :", transcribe(sentence))
    print("per-word :", " ".join("".join(phonemize(w)) for w in sentence.split()))


if __name__ == "__main__":
    main()
