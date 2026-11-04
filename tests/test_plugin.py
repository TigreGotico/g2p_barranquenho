"""Tests for BarranquenhoG2PPlugin, the string-returning integration adapter.

Validates:
- the engine exposes the surface downstream code relies on
- language_codes declares the correct BCP-47 extension tag
- transcribe() phonemises a whole utterance (with cross-word sandhi)
- transcribe_word() equals the joined phonemize() list for one word
"""
import pytest

from g2p_barranquenho import phonemize, transcribe
from g2p_barranquenho.plugin import BarranquenhoG2PPlugin


@pytest.fixture(scope="module")
def plugin():
    return BarranquenhoG2PPlugin()


class TestInterface:
    def test_exposes_transcribe_methods(self, plugin):
        # An engine built ON orthography2ipa, not a plugin TO it — nothing there
        # discovers or calls this. The surface is what matters, not inheritance.
        for method in ("transcribe", "transcribe_word"):
            assert callable(getattr(plugin, method))

    def test_language_codes_contains_barrancos(self, plugin):
        assert "ext-PT-x-barrancos" in plugin.language_codes


class TestTranscribe:
    def test_returns_string(self, plugin):
        assert isinstance(plugin.transcribe("paraba"), str)

    def test_matches_module_transcribe(self, plugin):
        text = "Comprámos pão e vinho na feira de Barrancos."
        assert plugin.transcribe(text) == transcribe(text)

    def test_applies_sandhi_across_words(self, plugin):
        # the whole utterance elides across the word boundary (que o -> [k o])
        per_word = " ".join("".join(phonemize(w)) for w in "que o".split())
        assert plugin.transcribe("que o") != per_word


class TestTranscribeWord:
    def test_returns_string(self, plugin):
        assert isinstance(plugin.transcribe_word("paraba"), str)

    def test_equals_phonemize_joined(self, plugin):
        word = "pássaru"
        assert plugin.transcribe_word(word) == "".join(phonemize(word))

    def test_accepts_word_context_none(self, plugin):
        out = plugin.transcribe_word("boca", context=None)
        assert out == "".join(phonemize("boca"))
