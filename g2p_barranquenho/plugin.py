"""Integration wrapper exposing the Barranquenho engine to the wider toolchain.

Barranquenho phonology lives in the shared ``ext-PT-x-barrancos`` spec; this
class adapts the package's ``transcribe``/``phonemize`` surface to the string
methods other components expect. It is an engine built ON orthography2ipa, not
a plugin discovered by it.
"""
from typing import List, Optional

from orthography2ipa import WordContext

from g2p_barranquenho import phonemize, transcribe


class BarranquenhoG2PPlugin:
    """String-returning G2P adapter for Barranquenho (ext-PT-x-barrancos)."""

    @property
    def language_codes(self) -> List[str]:
        return ["ext-PT-x-barrancos"]

    def transcribe(self, text: str) -> str:
        """Transcribe *text* to an IPA string.

        The whole utterance is transcribed together so cross-word sandhi (coda
        aspiration and deletion, article/conjunction destressing, elision)
        applies; word boundaries surface as spaces.
        """
        return transcribe(text)

    def transcribe_word(self, word: str, context: Optional[WordContext] = None) -> str:
        """Transcribe a single *word* to an IPA string (no cross-word sandhi)."""
        return "".join(phonemize(word))
