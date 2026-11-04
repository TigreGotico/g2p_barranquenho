"""Example — build a vocabulary -> IPA lookup table.

Run::

    python examples/05_vocab_table.py
"""
from g2p_barranquenho import phonemize


def main() -> None:
    vocab = ["paraba", "pássaru", "biba", "cahtelu", "boca", "ambu", "que"]
    table = {word: phonemize(word) for word in vocab}

    for word, phonemes in table.items():
        print(f"{word:10s} {''.join(phonemes)}")

    print(f"\n{len(table)} entries, "
          f"{sum(len(p) for p in table.values())} total phonemes")


if __name__ == "__main__":
    main()
