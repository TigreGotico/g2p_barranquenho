"""G2PPlugin wrapper for Barranquenho.

Wraps the rule-based ``phonemize()`` function in the shared
``orthography2ipa.g2p_plugin.G2PPlugin`` base class so it integrates with
the broader orthography2ipa toolchain.  The ``phonemize()`` function remains
the stable public API; this class is the integration layer.
"""
from typing import List, Optional

from orthography2ipa.g2p_plugin import G2PPlugin, WordContext

from g2p_barranquenho import phonemize


class BarranquenhoG2PPlugin(G2PPlugin):
    """Rule-based G2P for Barranquenho (ext-PT-x-barrancos)."""

    @property
    def language_codes(self) -> List[str]:
        return ["ext-PT-x-barrancos"]

    def transcribe(self, text: str) -> str:
        """Transcribe *text* to IPA.

        Each whitespace-separated token is transcribed individually via
        ``phonemize()``.  Non-alphabetic tokens that produce no phonemes are
        passed through unchanged so punctuation is preserved as-is.
        """
        tokens = text.split()
        parts = []
        for token in tokens:
            phones = phonemize(token)
            if phones:
                parts.append("".join(phones))
            else:
                parts.append(token)
        return " ".join(parts)

    def transcribe_word(self, word: str, context: Optional[WordContext] = None) -> str:
        """Transcribe a single *word* to an IPA string."""
        return "".join(phonemize(word))
