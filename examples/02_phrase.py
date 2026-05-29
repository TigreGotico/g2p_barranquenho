"""Example — transcribe a whole phrase, one word at a time.

Run::

    python examples/02_phrase.py
"""
from g2p_barranquenho import phonemize


def main() -> None:
    phrase = "boca cantá que manhán"
    for word in phrase.split():
        compact = "".join(phonemize(word))
        print(f"{word:10s} {phonemize(word)}  ->  /{compact}/")


if __name__ == "__main__":
    main()
