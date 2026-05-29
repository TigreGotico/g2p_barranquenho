"""Example — phonemize single Barranquenho words to IPA.

Run::

    python examples/01_basic.py
"""
from g2p_barranquenho import phonemize


def main() -> None:
    words = ["paraba", "pássaru", "biba", "boca", "que", "aquí"]
    for word in words:
        print(f"{word:10s} {phonemize(word)}")


if __name__ == "__main__":
    main()
