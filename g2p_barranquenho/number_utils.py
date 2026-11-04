"""Barranquenho number verbalization — the pre-lattice normalizer stage.

Numbers written as digits carry no orthography the grapheme-to-phoneme lattice
can read, so numeric tokens are spelled out into Barranquenho words *before*
transcription. This mirrors the architecture tugaphone uses for Portuguese
(``tugaphone.number_utils`` run as the orthography2ipa ``normalizer``): a
:class:`BarranquenhoNumberParser` turns one numeric token into words, and
:func:`normalize_numbers` rewrites every numeric token in running text, leaving
non-numeric tokens untouched. :meth:`BarranquenhoG2PPlugin.transcribe` calls it
first, so the spelled-out words then flow through the rescorer lattice like any
other word.

Attestation
-----------
Navas Sánchez-Élez (2011), *El barranqueño*, documents **no numeral paradigm** —
numerals surface only incidentally in aspiration examples and transcribed oral
texts. So most forms here are **derived**, not cited:

* **Attested** (:data:`ATTESTED`) — the lexeme appears in Navas (2011) or the
  Dicionário / dict data: 2 *douh*/*duah* (Navas *doih*~*doi*~*dous* / *duah*),
  3 *treh*, 4 *quatru* (*quatro*), 5 *cincu* (*cinco*), 6 *seih*, 7 *seti*
  (*sete*), 9 *novi* (*nove*), 10 *deh*, 12 *dozi* (*doze*), 14 *catorzi*,
  20 *binti* (*vinte*), 100 *cien*, 1000 *mil*, ordinal 1st *primeiru*.
* **Derived** (:data:`DERIVED`) — reconstructed from the Portuguese/Spanish
  numeral by the Convenção Ortográfica do Barranquenho (June 2025) spelling
  rules: final unstressed ``-o → -u`` and ``-e → -i``; coda ``-s`` written as
  the aspiration ``-h`` (*douh*, *treh*, plural *-uh*); ``v → b`` (*binti*).
  These are the engine's best reconstruction, marked so a reviewer can tell them
  from a citation.

Conjunction: Barranquenho joins numeral groups with **e** ("and") — attested in
Navas's *"vinte e tal"* (p. 1714 of the text dump). This is the Portuguese-side
copulative, unlike Mirandese *i*.
"""
from typing import Dict, List, Optional, Tuple

LANG = "ext-PT-x-barrancos"

#: copulative conjunction ("and"), Portuguese-side. ATTESTED (*vinte e tal*).
_AND = "e"

#: decimal separator word. Portuguese *vírgula* under the regular ``v→b``
#: correspondence. DERIVED.
_DECIMAL_WORD = "birgula"

#: sign word for negatives. DERIVED (*menos*).
_MINUS_WORD = "menoh"

# ---------------------------------------------------------------------------
# Numeral tables, spelled in Convenção 2025 orthography.
# ---------------------------------------------------------------------------

#: units 0-9, masculine.
_UNITS_M: Dict[int, str] = {
    0: "zeru",      # DERIVED
    1: "un",        # DERIVED
    2: "douh",      # ATTESTED (Navas doih~doi~dous)
    3: "treh",      # ATTESTED
    4: "quatru",    # ATTESTED (Navas quatro)
    5: "cincu",     # ATTESTED (Navas cinco)
    6: "seih",      # ATTESTED
    7: "seti",      # ATTESTED (Navas sete)
    8: "oitu",      # DERIVED
    9: "novi",      # ATTESTED (Navas nove)
}

#: feminine overrides for the gendered units.
_UNITS_F: Dict[int, str] = {
    1: "ũa",        # DERIVED
    2: "duah",      # ATTESTED (Navas duah~dua)
}

#: 10-19.
_TEENS: Dict[int, str] = {
    10: "deh",          # ATTESTED (Navas deh; also Sp. diez)
    11: "onzi",         # DERIVED
    12: "dozi",         # ATTESTED (Navas doze)
    13: "trezi",        # DERIVED
    14: "catorzi",      # ATTESTED
    15: "quinzi",       # DERIVED
    16: "dezaseih",     # DERIVED
    17: "dezaseti",     # DERIVED
    18: "dezoitu",      # DERIVED
    19: "dezanovi",     # DERIVED
}

#: tens 20-90. 20 ATTESTED (Navas vinte); the rest DERIVED.
_TENS: Dict[int, str] = {
    20: "binti",        # ATTESTED (Navas vinte)
    30: "trinta",       # DERIVED
    40: "quarenta",     # DERIVED
    50: "cinquenta",    # DERIVED
    60: "sessenta",     # DERIVED
    70: "setenta",      # DERIVED
    80: "oitenta",      # DERIVED
    90: "nobenta",      # DERIVED
}

#: hundreds. 100 *cien* ATTESTED (Navas, Spanish-leaning); 200-900 DERIVED on
#: the Portuguese *-centos* pattern with the coda-``s`` aspiration (*-centuh*).
_HUNDRED_ONE = "cien"        # ATTESTED (exactly 100 and compound head)
_HUNDREDS: Dict[int, str] = {
    200: "duzentuh",        # DERIVED
    300: "trezentuh",       # DERIVED
    400: "quatrucentuh",    # DERIVED
    500: "quinhentuh",      # DERIVED
    600: "seiscentuh",      # DERIVED
    700: "setecentuh",      # DERIVED
    800: "oitocentuh",      # DERIVED
    900: "novecentuh",      # DERIVED
}

#: scale words. *mil* ATTESTED (Navas *cinco mil rei*); millions DERIVED.
_THOUSAND = "mil"                       # ATTESTED
_MILLION = ("milhon", "milhoneh")       # DERIVED
_BILLION = ("bilhon", "bilhoneh")       # DERIVED

#: ordinals 1-10, masculine. Only 1st (*primeiru*) is attested (Navas
#: *primeiro*); the rest are DERIVED — Navas documents no ordinal series.
_ORDINALS_M: Dict[int, str] = {
    1: "primeiru",     # ATTESTED (Navas primeiro)
    2: "segundu",      # DERIVED
    3: "terceiru",     # DERIVED
    4: "quartu",       # DERIVED
    5: "quintu",       # DERIVED
    6: "sestu",        # DERIVED
    7: "setimu",       # DERIVED
    8: "oitabu",       # DERIVED
    9: "nonu",         # DERIVED
    10: "decimu",      # DERIVED
}

#: lexemes attested in Navas (2011) / dict, regardless of exact surface spelling.
ATTESTED = {
    "douh", "duah", "treh", "quatru", "cincu", "seih", "seti", "novi",
    "deh", "dozi", "catorzi", "binti", "cien", "mil", "primeiru",
}
#: forms reconstructed by the Convenção 2025 spelling rules.
DERIVED = {
    "zeru", "un", "ũa", "oitu", "onzi", "trezi", "quinzi", "dezaseih",
    "dezaseti", "dezoitu", "dezanovi", "trinta", "quarenta", "cinquenta",
    "sessenta", "setenta", "oitenta", "nobenta", "duzentuh", "trezentuh",
    "quatrucentuh", "quinhentuh", "seiscentuh", "setecentuh", "oitocentuh",
    "novecentuh", "milhon", "milhoneh", "bilhon", "bilhoneh", "segundu",
    "terceiru", "quartu", "quintu", "sestu", "setimu", "oitabu", "nonu",
    "decimu", "birgula", "menoh",
}


class BarranquenhoNumberParser:
    """Spell an integer or numeric token into Barranquenho words.

    Recursive over scale groups (units < 100, hundreds, thousands, millions),
    joined by the copulative :data:`_AND`. Gender applies to the units 1 and 2;
    the caller picks, defaulting to masculine.
    """

    def _unit(self, n: int, gender: str) -> str:
        if gender == "feminine" and n in _UNITS_F:
            return _UNITS_F[n]
        return _UNITS_M[n]

    def _under_100(self, n: int, gender: str) -> str:
        if n < 10:
            return self._unit(n, gender)
        if n < 20:
            return _TEENS[n]
        tens, unit = divmod(n, 10)
        base = _TENS[tens * 10]
        if unit == 0:
            return base
        return f"{base} {_AND} {self._unit(unit, gender)}"

    def _under_1000(self, n: int, gender: str) -> str:
        if n < 100:
            return self._under_100(n, gender)
        hundreds, rem = divmod(n, 100)
        head = _HUNDRED_ONE if hundreds == 1 else _HUNDREDS[hundreds * 100]
        if rem == 0:
            return head
        return f"{head} {_AND} {self._under_100(rem, gender)}"

    def _scale(self, n: int, gender: str) -> str:
        if n < 1000:
            return self._under_1000(n, gender)
        if n < 1_000_000:
            thousands, rem = divmod(n, 1000)
            head = _THOUSAND if thousands == 1 \
                else f"{self._under_1000(thousands, 'masculine')} {_THOUSAND}"
            return head if rem == 0 else f"{head} {self._join_rem(rem, gender)}"
        return self._big(n, gender)

    def _big(self, n: int, gender: str) -> str:
        for divisor, (sing, plur) in ((1_000_000_000, _BILLION),
                                      (1_000_000, _MILLION)):
            if n >= divisor:
                count, rem = divmod(n, divisor)
                word = sing if count == 1 else plur
                head = f"{self._under_1000(count, 'masculine')} {word}"
                return head if rem == 0 \
                    else f"{head} {self._join_rem(rem, gender)}"
        return self._under_1000(n, gender)

    def _join_rem(self, rem: int, gender: str) -> str:
        tail = self._scale(rem, gender)
        return f"{_AND} {tail}" if rem < 100 else tail

    # -- public API ------------------------------------------------------
    def cardinal(self, n: int, gender: str = "masculine") -> str:
        """Spell integer *n* as a cardinal."""
        if n < 0:
            return f"{_MINUS_WORD} {self.cardinal(-n, gender)}"
        if n == 0:
            return _UNITS_M[0]
        return self._scale(n, gender)

    def ordinal(self, n: int, gender: str = "masculine") -> str:
        """Spell integer *n* (1-10) as an ordinal.

        Feminine swaps the final ``-u`` for ``-a`` (the regular agreement).
        """
        if n not in _ORDINALS_M:
            raise ValueError(f"ordinal out of supported range 1-10: {n}")
        word = _ORDINALS_M[n]
        if gender == "feminine" and word.endswith("u"):
            return word[:-1] + "a"
        return word

    def decimal(self, whole: int, frac: str, gender: str = "masculine") -> str:
        """Spell a decimal: whole part, *birgula*, then digit-by-digit frac."""
        digits = " ".join(self._unit(int(d), gender) for d in frac)
        return f"{self.cardinal(whole, gender)} {_DECIMAL_WORD} {digits}"

    def year(self, n: int) -> str:
        """Spell a year as a plain cardinal."""
        return self.cardinal(n, "masculine")

    def pronounce_token(self, token: str, gender: str = "masculine",
                        as_ordinal: bool = False) -> Optional[str]:
        """Spell one numeric *token* ("12", "3,5", "-4"), or ``None``."""
        t = token.strip()
        neg = t.startswith("-")
        if neg:
            t = t[1:]
        for sep in (",", "."):
            if sep in t:
                whole_s, _, frac_s = t.partition(sep)
                if whole_s.isdigit() and frac_s.isdigit():
                    out = self.decimal(int(whole_s), frac_s, gender)
                    return f"{_MINUS_WORD} {out}" if neg else out
        if not t.isdigit():
            return None
        n = int(t)
        val = self.ordinal(n, gender) if as_ordinal else self.cardinal(n, gender)
        return f"{_MINUS_WORD} {val}" if neg else val


_ORD_MASC = "º"
_ORD_FEM = "ª"
_ORDINAL_MARKERS = (_ORD_MASC, _ORD_FEM)


def normalize_numbers(text: str, strict: bool = False) -> str:
    """Replace numeric tokens in *text* with their Barranquenho written forms.

    The pre-lattice normalizer stage: it runs on raw orthographic text before
    the rescorer lattice, so spelled-out numbers are then transcribed like any
    other word. Non-numeric tokens are returned untouched. A trailing ordinal
    marker (``º`` masc / ``ª`` fem) triggers an ordinal reading and is consumed.

    :param strict: when true, re-raise a token that fails to verbalize;
        otherwise leave it in place.
    """
    parser = BarranquenhoNumberParser()
    out: List[str] = []
    for word in text.split():
        prefix, core, suffix = _split_affixes(word)
        as_ord = suffix[:1] in _ORDINAL_MARKERS
        gender = "feminine" if suffix[:1] == _ORD_FEM else "masculine"
        emit_suffix = suffix[1:] if as_ord else suffix
        try:
            spelled = parser.pronounce_token(
                core, gender=gender, as_ordinal=as_ord) if core else None
        except Exception:
            if strict:
                raise
            spelled = None
        out.append(f"{prefix}{spelled}{emit_suffix}"
                   if spelled is not None else word)
    return " ".join(out)


def _split_affixes(word: str) -> Tuple[str, str, str]:
    """Split leading/trailing punctuation off a token's numeric core."""
    start, end = 0, len(word)
    while start < end and not (word[start].isdigit() or word[start] == "-"):
        start += 1
    while end > start and not word[end - 1].isdigit():
        end -= 1
    return word[:start], word[start:end], word[end:]
