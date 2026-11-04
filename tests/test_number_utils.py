"""Tests for g2p_barranquenho.number_utils — Barranquenho number verbalization.

Navas Sánchez-Élez (2011) documents no numeral paradigm, so most expected forms
are DERIVED by the Convenção Ortográfica do Barranquenho (2025) spelling rules
(final ``-o→-u``/``-e→-i``, coda ``-s→-h``, ``v→b``); the lexemes marked
ATTESTED appear in Navas (2011) or the dict data. See the module docstring.
"""
import pytest

from g2p_barranquenho import transcribe
from g2p_barranquenho.number_utils import (
    BarranquenhoNumberParser, normalize_numbers, ATTESTED, DERIVED,
)


@pytest.fixture(scope="module")
def parser():
    return BarranquenhoNumberParser()


class TestCardinals:
    @pytest.mark.parametrize("n,expected", [
        (0, "zeru"), (1, "un"), (2, "douh"), (3, "treh"), (4, "quatru"),
        (5, "cincu"), (6, "seih"), (7, "seti"), (8, "oitu"), (9, "novi"),
        (10, "deh"), (12, "dozi"), (14, "catorzi"), (16, "dezaseih"),
        (20, "binti"), (30, "trinta"), (100, "cien"), (1000, "mil"),
    ])
    def test_base(self, parser, n, expected):
        assert parser.cardinal(n) == expected

    def test_attested_lexemes_present(self, parser):
        # spot-check the forms Navas actually attests
        for n, form in [(2, "douh"), (3, "treh"), (6, "seih"), (10, "deh"),
                        (14, "catorzi"), (20, "binti")]:
            assert parser.cardinal(n) == form
            assert form in ATTESTED


class TestGender:
    def test_one(self, parser):
        assert parser.cardinal(1, "masculine") == "un"
        assert parser.cardinal(1, "feminine") == "ũa"

    def test_two(self, parser):
        # douh / duah — Navas attests doih~doi~dous / duah~dua
        assert parser.cardinal(2, "masculine") == "douh"
        assert parser.cardinal(2, "feminine") == "duah"


class TestCompounds:
    @pytest.mark.parametrize("n,expected", [
        (21, "binti e un"),
        (42, "quarenta e douh"),
        (101, "cien e un"),
        (256, "duzentuh e cinquenta e seih"),
        (999, "novecentuh e nobenta e novi"),
        (2025, "douh mil e binti e cincu"),
    ])
    def test_compound(self, parser, n, expected):
        # conjunction is "e" (Portuguese-side), attested in "vinte e tal"
        assert parser.cardinal(n) == expected

    def test_million(self, parser):
        assert parser.cardinal(1_000_000) == "un milhon"


class TestEdgeCases:
    def test_zero(self, parser):
        assert parser.cardinal(0) == "zeru"

    def test_teens_synthetic(self, parser):
        for n in range(11, 16):
            assert " " not in parser.cardinal(n)

    def test_negative(self, parser):
        assert parser.pronounce_token("-4") == "menoh quatru"


class TestOrdinals:
    def test_first_attested(self, parser):
        assert parser.ordinal(1) == "primeiru"
        assert "primeiru" in ATTESTED

    @pytest.mark.parametrize("n,expected", [
        (2, "segundu"), (3, "terceiru"), (4, "quartu"), (5, "quintu"),
        (8, "oitabu"), (10, "decimu"),
    ])
    def test_ordinal_derived(self, parser, n, expected):
        assert parser.ordinal(n) == expected

    def test_feminine_agreement(self, parser):
        assert parser.ordinal(1, "feminine") == "primeira"
        assert parser.ordinal(4, "feminine") == "quarta"

    def test_out_of_range(self, parser):
        with pytest.raises(ValueError):
            parser.ordinal(11)


class TestDecimal:
    def test_decimal(self, parser):
        assert parser.pronounce_token("3,5") == "treh birgula cincu"
        assert parser.pronounce_token("3.5") == "treh birgula cincu"


class TestNormalizeNumbers:
    def test_cardinal_context(self):
        assert normalize_numbers("tenho 3 gatu") == "tenho treh gatu"

    def test_compound_context(self):
        assert normalize_numbers("20 anu") == "binti anu"

    def test_ordinal_marker_fem(self):
        assert normalize_numbers("la casa 1ª") == "la casa primeira"

    def test_ordinal_marker_masc(self):
        assert normalize_numbers("o 2º dia") == "o segundu dia"

    def test_punctuation_preserved(self):
        assert normalize_numbers("(3) gatu, 2!") == "(treh) gatu, douh!"

    def test_non_numeric_untouched(self):
        # regression: digit-free text returned byte-for-byte
        text = "o barranquenhu ehtá bibu na feira de Barrancoh"
        assert normalize_numbers(text) == text

    def test_ordinal_out_of_range_left_alone(self):
        assert normalize_numbers("99º") == "99º"


class TestAttestation:
    def test_sets_disjoint(self):
        assert ATTESTED.isdisjoint(DERIVED)


class TestTranscribeIntegration:
    def test_numbers_expanded_by_default(self):
        # "3" becomes *treh* and is transcribed by the lattice
        assert transcribe("3") == transcribe("treh")

    def test_expand_off_matches_bare(self):
        # regression: with expansion off, digit-free text is unchanged
        assert transcribe("boca", expand_numbers=False) == transcribe(
            "boca", expand_numbers=True)
