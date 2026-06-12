"""Gold test suite for g2p_barranquenho.

Pins the current behaviour of phonemize() per rule, aligned with the official
orthographic convention suite (2025):

  - Convenção Ortográfica do Barranquenho (June 2025) — "Convenção 2025"
  - Gramática Básica de Barranquenho (July 2025), Gonçalves/Navas/Correia — "Gramática 2025"
  - Dicionário de Barranquenho (2025-07-11), Gonçalves/Navas/Ferreira — "Dicionário 2025"

Rule coverage:
- README worked examples (updated to convention-correct outputs)
- Digraphs: nh, ch, lh, tch, qu (e/i), gu (e/i)
- Nasal vowels: a/e/i/o/u before m/n; ã; -ão/-ãu diphthong
  * <em>/<en> → [ẽ] plain (Convenção p. 26; Gramática p. 15)
- Stress-conditioned vowel quality: a (stressed [a] vs unstressed [ɐ])
- Stress-conditioned e: stressed [e], unstressed [ɨ], final [ɨ]
- Stress-conditioned o: stressed [o], unstressed [u]
- Accented vowels: á é ê â ô ó í ú
- Final atone <i> → /i/ vowel (Gramática p. 14; Convenção pp. 20–21)
- Word-final e/a/o reduction
- Coda <s> → [h] aspiration (Convenção pp. 28–29)
- r/rr: initial [r], medial [ɾ], rr→[r]
- s/ss: initial [s], intervocalic [z], coda [h], ss→[s]
- c before e/i → [s]; c elsewhere → [k]
- g before e/i/í → [ʒ]; g elsewhere → [g]
- x: initial [ʃ]; after n/m [ʃ]; intervocalic learned [ks]; intervocalic [z];
     before xc [s]+elide; before p/t [s]; default [ʃ]
  (Convenção pp. 28, 31; Gramática pp. 18–19)
- v is always [b] (betacism: Gramática p. 17; Convenção p. 30)
- Convention-signature headwords from the Dicionário 2025
"""
from g2p_barranquenho import phonemize


# ---------------------------------------------------------------------------
# README / __main__ worked examples
# ---------------------------------------------------------------------------

class TestReadmeExamples:
    """Outputs from the __main__ block, corrected to the convention."""

    def test_paraba(self):
        assert phonemize("paraba") == ["p", "ɐ", "ɾ", "a", "b", "ɐ"]

    def test_passaru(self):
        assert phonemize("pássaru") == ["p", "a", "s", "ɐ", "ɾ", "u"]

    def test_biba(self):
        # <i> is final atone → /i/ vowel, NOT /j/ (Gramática p. 14; Convenção pp. 20–21)
        assert phonemize("biba") == ["b", "i", "b", "ɐ"]

    def test_cahtelu(self):
        assert phonemize("cahtelu") == ["k", "ɐ", "h", "t", "e", "l", "u"]

    def test_boca(self):
        assert phonemize("boca") == ["b", "o", "k", "ɐ"]

    def test_ambu(self):
        assert phonemize("ambu") == ["ɐ͂", "b", "u"]

    def test_canta(self):
        assert phonemize("cantá") == ["k", "ɐ͂", "t", "a"]

    def test_manhan(self):
        assert phonemize("manhán") == ["m", "ɐ", "ɲ", "ɐ͂"]

    def test_que(self):
        assert phonemize("que") == ["k", "ɨ"]

    def test_aqui(self):
        # <í> accented → /i/ vowel (Gramática p. 14; Convenção p. 20)
        assert phonemize("aquí") == ["ɐ", "k", "i"]


# ---------------------------------------------------------------------------
# Digraphs
# ---------------------------------------------------------------------------

class TestDigraphs:
    def test_nh_initial(self):
        out = phonemize("nhada")
        assert out[0] == "ɲ"

    def test_nh_medial(self):
        out = phonemize("manhán")
        assert "ɲ" in out

    def test_ch_initial(self):
        out = phonemize("chave")
        assert out[0] == "ʃ"

    def test_lh_initial(self):
        out = phonemize("lhano")
        assert out[0] == "ʎ"

    def test_tch(self):
        # <tch> → /tʃ/ (Convenção p. 31; Gramática p. 20)
        out = phonemize("tche")
        assert out[0] == "tʃ"

    def test_qu_before_e(self):
        out = phonemize("que")
        assert out == ["k", "ɨ"]

    def test_qu_before_i(self):
        out = phonemize("quito")
        assert out[0] == "k"

    def test_gu_before_e(self):
        out = phonemize("guerra")
        assert out[0] == "g"

    def test_gu_before_i(self):
        out = phonemize("guia")
        assert out[0] == "g"


# ---------------------------------------------------------------------------
# Nasal vowels
# ---------------------------------------------------------------------------

class TestNasalVowels:
    def test_a_before_m(self):
        out = phonemize("ambu")
        assert out[0] == "ɐ͂"
        assert "m" not in out

    def test_a_before_n(self):
        out = phonemize("cantá")
        assert "ɐ͂" in out

    def test_e_before_m(self):
        # <em> → [ẽ] plain nasal vowel (Convenção p. 26; Gramática p. 15).
        # NOT the pt-PT diphthong [ẽj].
        out = phonemize("sento")
        assert "ẽ" in out
        assert "ẽj" not in out

    def test_e_before_n(self):
        # <en> → [ẽ] plain nasal vowel (Convenção p. 26; Gramática p. 15).
        out = phonemize("cento")
        assert "ẽ" in out
        assert "ẽj" not in out

    def test_i_before_n(self):
        out = phonemize("lindo")
        assert "ĩ" in out

    def test_o_before_m(self):
        out = phonemize("bom")
        assert "õ" in out

    def test_u_before_n(self):
        out = phonemize("mundo")
        assert "ũ" in out

    def test_a_tilde(self):
        assert phonemize("ã") == ["ɐ͂"]

    def test_ao_diphthong(self):
        out = phonemize("pão")
        assert "ɐ͂" in out
        assert "w" in out or "u" in out

    def test_leau_diphthong(self):
        out = phonemize("leãu")
        assert "ɐ͂" in out


# ---------------------------------------------------------------------------
# Convention-signature nasal vowel tests (Convenção p. 26; Gramática p. 15)
# ---------------------------------------------------------------------------

class TestConventionNasalEM_EN:
    """<em>/<en> → [ẽ] — the convention is explicit (not a diphthong)."""

    def test_tempu(self):
        # tempu (tempo): t + ẽ + p + u
        out = phonemize("tempu")
        assert out == ["t", "ẽ", "p", "u"]

    def test_tentu(self):
        # tentu (tento): t + ẽ + t + u
        out = phonemize("tentu")
        assert out == ["t", "ẽ", "t", "u"]

    def test_quen(self):
        # quen (quem): k + ẽ  (final -n consumed into nasal vowel)
        out = phonemize("quen")
        assert out == ["k", "ẽ"]


# ---------------------------------------------------------------------------
# Final atone <i> is vowel /i/ — NOT glide /j/
# (Gramática p. 14; Convenção pp. 20–21)
# ---------------------------------------------------------------------------

class TestFinalAtoneI:
    def test_sociedadi(self):
        # sociedadi (sociedade): final -i is /i/ vowel
        out = phonemize("sociedadi")
        assert out[-1] == "i"

    def test_libri(self):
        # libri (livre): l + i + b + ɾ + i
        out = phonemize("libri")
        assert out == ["l", "i", "b", "ɾ", "i"]

    def test_Fernandi(self):
        # Fernandi (Fernando): final -i is /i/ vowel
        out = phonemize("fernandi")
        assert out[-1] == "i"


# ---------------------------------------------------------------------------
# Coda <s> → [h] aspiration (Convenção pp. 28–29; Dicionário: mehmu, Lihboa)
# ---------------------------------------------------------------------------

class TestCodaS:
    def test_mehmu_h_already_written(self):
        # mehmu (mesmo): m + e + h + m + u  — aspiration already in spelling
        out = phonemize("mehmu")
        assert out == ["m", "e", "h", "m", "u"]

    def test_coda_s_becomes_h(self):
        # When a Portuguese-spelled word reaches the engine, coda <s> → [h].
        # e.g. "mesmo" spelled Portuguese-style: m + e + h + m + u
        # Use a clear coda context: "asma" — a + h + m + a
        out = phonemize("asma")
        assert "h" in out
        assert "ʃ" not in out

    def test_intervocalic_s_stays_z(self):
        # intervocalic <s> is /z/ (casa, rosa) — not affected
        out = phonemize("casa")
        assert "z" in out

    def test_initial_s_stays_s(self):
        out = phonemize("saku")
        assert out[0] == "s"


# ---------------------------------------------------------------------------
# <x> — three-way convention rule
# (Convenção pp. 28, 31; Gramática pp. 18–19)
# ---------------------------------------------------------------------------

class TestXDisambiguation:
    def test_x_initial_is_sh(self):
        # xaili, xisto — word-initial <x> → [ʃ]
        out = phonemize("xisto")
        assert out[0] == "ʃ"

    def test_x_after_n_is_sh(self):
        # enxame: <n> before <x> → [ʃ] (Convenção p. 29 — <ns>/<nx> aspiration)
        # Previously crashed due to None-guard bug; fixed.
        out = phonemize("enxame")
        assert "ʃ" in out

    def test_x_before_xc_is_s(self):
        # exceção: x before c → [s], c elided
        out = phonemize("exceção")
        assert out[1] == "s"

    def test_x_after_double_vowel_ei_is_z(self):
        # peixe: e-i-x — in the new three-way rule, intervocalic x is [z]
        # unless the word is in the learned-[ks] set.
        # (Pt-PT "ameixa/peixe → [ʃ]" branch is removed; Barranquenho convention
        # does not enumerate this class separately.)
        out = phonemize("peixe")
        assert "z" in out

    def test_x_exame_vowel_x_vowel(self):
        # exame: intervocalic <x> → [z] (Gramática p. 19: "z escreve-se com z, -s, x")
        out = phonemize("exame")
        assert "z" in out

    def test_x_before_p_is_s(self):
        # exportar: x before p → [s] (consonant cluster onset)
        out = phonemize("exportar")
        assert "s" in out

    def test_x_before_t_is_s(self):
        # texto: x before t → [s]
        out = phonemize("texto")
        assert "s" in out

    def test_x_default_is_sh(self):
        # marx: r before x, no following vowel — default → [ʃ]
        out = phonemize("marx")
        assert out[-1] == "ʃ"

    def test_x_vowel_x_vowel_is_z(self):
        # luxo: vowel-x-vowel → [z]
        out = phonemize("luxo")
        assert "z" in out

    def test_x_auxiliar_intervocalic_z(self):
        # auxiliar: au-x — the old "aux-" → [s] pt-PT branch is removed;
        # this is now intervocalic → [z] per the convention three-way rule.
        out = phonemize("auxiliar")
        assert "z" in out

    def test_x_crucifixu_learned_ks(self):
        # crucifixu: enumerated learned-word set → [ks]
        # (Convenção p. 31; Gramática p. 20)
        out = phonemize("crucifixu")
        assert "ks" in out


# ---------------------------------------------------------------------------
# Stress-conditioned vowel quality
# ---------------------------------------------------------------------------

class TestStressVowelQuality:

    def test_stressed_a_is_open(self):
        out = phonemize("kata")
        assert out[1] == "a"
        assert out[-1] == "ɐ"

    def test_unstressed_a_reduces_to_schwa(self):
        out = phonemize("paraba")
        assert "a" in out
        assert "ɐ" in out

    def test_final_a_is_schwa(self):
        out = phonemize("mesa")
        assert out[-1] == "ɐ"

    def test_stressed_e_is_close_mid(self):
        out = phonemize("mesa")
        assert out[1] == "e"

    def test_final_e_is_schwa(self):
        out = phonemize("peixe")
        assert out[-1] == "ɨ"

    def test_unstressed_e_reduces(self):
        out = phonemize("café")
        assert out[1] == "ɐ"
        assert out[-1] == "ɛ"

    def test_stressed_o_is_close_mid(self):
        out = phonemize("bolo")
        assert out[1] == "o"
        assert out[-1] == "u"

    def test_unstressed_o_raises_to_u(self):
        out = phonemize("toco")
        assert out[-1] == "u"


# ---------------------------------------------------------------------------
# Accented vowels
# ---------------------------------------------------------------------------

class TestAccentedVowels:
    def test_acute_a(self):
        assert phonemize("má") == ["m", "a"]

    def test_acute_e(self):
        assert phonemize("pé") == ["p", "ɛ"]

    def test_circumflex_e(self):
        out2 = phonemize("vêde")
        assert "e" in out2

    def test_circumflex_a(self):
        out = phonemize("câmara")
        assert out[1] == "ɐ"

    def test_acute_o(self):
        assert phonemize("só") == ["s", "ɔ"]

    def test_acute_i(self):
        # <í> accented → /i/ vowel (Gramática p. 14; Convenção p. 20)
        out = phonemize("aquí")
        assert "i" in out

    def test_circumflex_o(self):
        out = phonemize("côto")
        assert "o" in out


# ---------------------------------------------------------------------------
# r and rr
# ---------------------------------------------------------------------------

class TestRhotics:
    def test_initial_r_is_trill(self):
        out = phonemize("rato")
        assert out[0] == "r"

    def test_medial_r_is_tap(self):
        out = phonemize("paraba")
        assert out[2] == "ɾ"

    def test_rr_collapses_to_trill(self):
        out = phonemize("carro")
        assert "r" in out
        assert out.count("r") == 1

    def test_initial_r_word_perro(self):
        out = phonemize("perro")
        assert "r" in out


# ---------------------------------------------------------------------------
# s and ss
# ---------------------------------------------------------------------------

class TestSibilants:
    def test_initial_s_voiceless(self):
        out = phonemize("saku")
        assert out[0] == "s"

    def test_medial_s_voiced(self):
        out = phonemize("mesa")
        assert "z" in out

    def test_ss_collapses_to_voiceless(self):
        out = phonemize("pássaru")
        assert "z" not in out
        assert "s" in out

    def test_medial_rosa(self):
        out = phonemize("rosa")
        assert "z" in out


# ---------------------------------------------------------------------------
# c and g before front vowels
# ---------------------------------------------------------------------------

class TestStops:
    def test_c_before_e_is_s(self):
        out = phonemize("celo")
        assert out[0] == "s"

    def test_c_before_i_is_s(self):
        out = phonemize("cipo")
        assert out[0] == "s"

    def test_c_elsewhere_is_k(self):
        out = phonemize("cato")
        assert out[0] == "k"

    def test_cedilla_is_s(self):
        out = phonemize("paço")
        assert "s" in out

    def test_g_before_e_is_zh(self):
        out = phonemize("gelo")
        assert out[0] == "ʒ"

    def test_g_before_i_is_zh(self):
        out = phonemize("gira")
        assert out[0] == "ʒ"

    def test_g_elsewhere_is_g(self):
        out = phonemize("gato")
        assert out[0] == "g"

    def test_v_is_b(self):
        # Betacism: <v> → /b/ (Gramática p. 17; Convenção p. 30)
        out = phonemize("vida")
        assert out[0] == "b"


# ---------------------------------------------------------------------------
# Convention-signature headwords from Dicionário 2025
# Diagnostic entries whose spelling directly demonstrates grapheme rules.
# ---------------------------------------------------------------------------

class TestDicionarioHeadwords:
    def test_mehmu(self):
        # mehmu (mesmo): coda-s already written as <h> (Convenção pp. 28–29)
        out = phonemize("mehmu")
        assert out == ["m", "e", "h", "m", "u"]

    def test_passaru(self):
        # pássaru (pássaro): proparoxytone, final <u> is /u/ atone
        out = phonemize("pássaru")
        assert out == ["p", "a", "s", "ɐ", "ɾ", "u"]

    def test_altu(self):
        # altu (alto): final <u> → /u/
        out = phonemize("altu")
        assert out[-1] == "u"

    def test_pequenu(self):
        # pequenu (pequeno): pretonic <e> kept; final <u> → /u/
        out = phonemize("pequenu")
        assert out[-1] == "u"

    def test_cantá(self):
        # cantá (cantar): tonic final <á>, -r deleted in spelling
        out = phonemize("cantá")
        assert out[-1] == "a"

    def test_bêju(self):
        # bêju (beijo): <ê> closed → [e]
        out = phonemize("bêju")
        assert "e" in out

    def test_nasal_diphthong_âu(self):
        # comunhâu (comunhão): tonic nasal diphthong [ɐ̃w]
        # (Convenção pp. 26–27; Gramática pp. 16–17)
        out = phonemize("comunhâu")
        joined = "".join(out)
        assert "ɐ̃w" in joined  # <âu> → [ɐ̃w] nasal diphthong


    def test_catchondeu_tch(self):
        # catchondeu: <tch> → /tʃ/ (Convenção p. 31; Gramática p. 20)
        out = phonemize("catchondeu")
        assert "tʃ" in out

    def test_libri_final_i(self):
        # libri (livre): final <i> is /i/ vowel (Gramática p. 14)
        out = phonemize("libri")
        assert out[-1] == "i"

    def test_piconeru_ê(self):
        # piconêru: <ê> → [e] closed tonic
        out = phonemize("piconêru")
        assert "e" in out
