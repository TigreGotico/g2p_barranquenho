"""Tests for BarranquenhoG2PPlugin.

Validates:
- the engine exposes the surface downstream code relies on
- language_codes declares the correct BCP-47 extension tag
- transcribe() joins phonemize() word outputs into a plain IPA string
- transcribe_word() equals transcribe() for a single-word input
- transcribe preserves punctuation tokens that produce no phonemes
"""
import pytest


from g2p_barranquenho import phonemize
from g2p_barranquenho.plugin import BarranquenhoG2PPlugin


@pytest.fixture(scope="module")
def plugin():
    return BarranquenhoG2PPlugin()


class TestInterface:
    def test_implements_shared_base(self, plugin):
        # An engine built ON orthography2ipa, not a plugin TO it — nothing there
        # discovers or calls this. The surface is what matters, not inheritance.
        for method in ("transcribe", "transcribe_word"):
            assert callable(getattr(plugin, method))

    def test_language_codes_contains_barrancos(self, plugin):
        assert "ext-PT-x-barrancos" in plugin.language_codes


class TestTranscribe:
    def test_single_word(self, plugin):
        expected = "".join(phonemize("paraba"))
        assert plugin.transcribe("paraba") == expected

    def test_multi_word_space_separated(self, plugin):
        result = plugin.transcribe("boca cantá")
        words = result.split()
        assert len(words) == 2
        assert words[0] == "".join(phonemize("boca"))
        assert words[1] == "".join(phonemize("cantá"))

    def test_transcribe_returns_string(self, plugin):
        out = plugin.transcribe("paraba")
        assert isinstance(out, str)

    def test_non_phonemic_token_passed_through(self, plugin):
        # a comma or period produces no phonemes and should survive verbatim
        out = plugin.transcribe(",")
        assert out == ","


class TestTranscribeWord:
    def test_returns_string(self, plugin):
        out = plugin.transcribe_word("paraba")
        assert isinstance(out, str)

    def test_equals_phonemize_joined(self, plugin):
        word = "pássaru"
        assert plugin.transcribe_word(word) == "".join(phonemize(word))

    def test_equals_transcribe_single_word(self, plugin):
        word = "manhán"
        assert plugin.transcribe_word(word) == plugin.transcribe(word)

    def test_accepts_word_context_none(self, plugin):
        # context=None must not raise
        out = plugin.transcribe_word("boca", context=None)
        assert out == "".join(phonemize("boca"))
