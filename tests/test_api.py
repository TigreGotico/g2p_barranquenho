"""Public API contract for g2p_barranquenho.

Pins the stable surface downstream code relies on:
- ``phonemize(word) -> list[str]``; joining the list is the word's IPA string
- ``transcribe(text) -> str`` phonemises a whole utterance with cross-word sandhi
- ``normalize`` is caller-side text folding only (no phonology)
"""
from g2p_barranquenho import LANG, normalize, phonemize, transcribe


class TestPhonemize:
    def test_returns_list_of_str(self):
        out = phonemize("boca")
        assert isinstance(out, list) and all(isinstance(p, str) for p in out)

    def test_join_is_word_ipa(self):
        # joining the phone list reproduces the single-word transcription
        assert "".join(phonemize("bonita")) == transcribe("bonita")

    def test_nasal_vowel_is_one_phone(self):
        # a coda m/n is absorbed into the nasal vowel: one list item, not two
        bare = [p.lstrip("ˈˌ") for p in phonemize("ambu")]
        assert "ɐ̃" in bare

    def test_stress_is_marked(self):
        # spec-driven output carries lexical stress (the old rule cascade did not)
        assert any("ˈ" in p for p in phonemize("bonita"))

    def test_empty_input(self):
        assert phonemize("") == []


class TestTranscribe:
    def test_returns_str(self):
        assert isinstance(transcribe("boca cantá"), str)

    def test_applies_cross_word_sandhi(self):
        # a whole utterance elides across the word boundary (que o -> [k o]),
        # which phonemising each word in isolation cannot see
        whole = transcribe("que o")
        per_word = " ".join("".join(phonemize(w)) for w in "que o".split())
        assert whole != per_word

    def test_case_insensitive(self):
        assert transcribe("BOCA") == transcribe("boca")


class TestNormalize:
    def test_folds_case_and_form(self):
        assert normalize("BÔA") == "bôa"

    def test_idempotent(self):
        once = normalize("Ehtá")
        assert normalize(once) == once


def test_lang_code():
    assert LANG == "ext-PT-x-barrancos"
