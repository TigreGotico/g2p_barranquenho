# Advanced — stress, sandhi, diacritics, and recipes

The transcription is driven entirely by the `ext-PT-x-barrancos` language spec in
[`orthography2ipa`](https://github.com/OpenVoiceOS/orthography2ipa). The spelling
carries most of the information the spec needs, so the more faithfully a word is
written — diacritics included — the better the transcription.

## Stress

Output carries lexical stress, marked with `ˈ` before the stressed syllable. In a
phone list the mark leads the phone that opens the stressed syllable:

```python
from g2p_barranquenho import phonemize

phonemize("bonita")   # ['b', 'u', 'ˈn', 'i', 't', 'ɐ']  — paroxytone
phonemize("cantá")    # ['k', 'ɐ̃', 'ˈt', 'a']            — accent fixes stress
```

An explicit accent fixes the stressed syllable; otherwise the spec's default
placement applies. To match on a bare segment, strip the mark first:
`p.lstrip("ˈˌ")`.

## Cross-word sandhi

`transcribe` scores a whole utterance, so effects that only exist between words
surface. `phonemize`, working one word at a time, cannot see them.

```python
from g2p_barranquenho import transcribe

transcribe("que o")   # 'k o'   — the vowel of que elides before a vowel
```

Coda-`/s/` aspiration and deletion, and the destressing of articles and the
conjunction `e`, are part of the same spec and show up in transcription:

```python
transcribe("O tempu não ehtá nada bom agora.")
# 'o ˈtẽpu ˈnɐ̃w̃ eˈhta ˈnadɐ ˈbõ ɐˈɡɔɾɐ'   — coda s of ehtá aspirated to [h]

transcribe("os meus currais")
# 'o ˈmew ˈkuraj'   — final /s/ dropped throughout
```

## Diacritics steer the vowels

The same base vowel maps to different IPA depending on its accent and position.
Spell the accents and the open/closed/nasal distinctions come through:

```python
phonemize("cantá")    # ['k', 'ɐ̃', 'ˈt', 'a']   — á is open stressed /a/
phonemize("ambu")     # ['ˈɐ̃', 'b', 'u']        — a before coda m nasalises
phonemize("manhán")   # ['m', 'ɐ', 'ˈɲ', 'ɐ̃']   — final -án nasalises
phonemize("boca")     # ['ˈb', 'ɔ', 'k', 'ɐ']   — final -a reduces to ɐ
```

A vowel directly before a syllable-final `m`/`n` nasalises and swallows that
consonant, so a nasal vowel is one list item, not a vowel plus a separate tilde.

## Position-sensitive consonants

`r` and `s` depend on where they sit, and `ss`/`rr` collapse to a single
phoneme:

```python
phonemize("rato")     # ['ˈr', 'a', 't', 'u']            — initial r → trill r
phonemize("paraba")   # ['p', 'ɐ', 'ˈɾ', 'a', 'b', 'ɐ']  — medial r → tap ɾ
phonemize("carro")    # ['ˈk', 'a', 'r', 'u']            — rr → single trill r
```

Barranquenho writes `b` for `v` (betacism), so `vinho` → `ˈbiɲu`; `g` before a
front vowel is `[ʒ]` (`gelo` → `ˈʒɛlu`).

## The digraphs

`tch ch nh lh` and the front-vowel `qu`/`gu` are resolved as units:

```python
phonemize("chave")    # 'ʃ' onset   -> 'ˈʃabɨ'
phonemize("lhano")    # 'ʎ' onset   -> 'ˈʎanu'
phonemize("nhada")    # 'ɲ' onset   -> 'ˈɲadɐ'
phonemize("tchapa")   # 'tʃ' onset  -> 'ˈtʃapɐ'
```

Because the transcription is a flat string, the affricate `tʃ` appears as two
adjacent characters; match it as a substring of the joined output rather than as
a single list item.

## The `x` letter

Word-medial `x` has no single rule in Portuguese-based spelling; the spec picks
`ʃ`, `s` or `z` from context:

```python
phonemize("peixe")    # -> 'ˈpejzɨ'
phonemize("texto")    # -> 'ˈtɛʃtu'
```

## Gotchas

- **`phonemize` is one word; `transcribe` is an utterance.** Only `transcribe`
  applies boundary effects. Passing a phrase to `phonemize` treats the whole
  string as one token.
- **Output carries stress marks.** Strip `ˈ`/`ˌ` if you need bare segments.
- **`v` becomes `b`.** Barranquenho betacism; `k`/`q` both yield `[k]`.
- **Prefer fully-accented input.** Missing diacritics leave the spec less to work
  from and lower the accuracy.

## Recipes

### Batch a vocabulary into a transcription map

```python
from g2p_barranquenho import phonemize

vocab = ["boca", "cantá", "que", "manhán"]
table = {w: "".join(phonemize(w)) for w in vocab}
```

### Transcribe a phrase with boundary effects

```python
from g2p_barranquenho import transcribe

transcribe("Comprámos pão e vinho na feira de Barrancos.")
# 'kõˈpɾamu ˈpɐ̃w̃ i ˈbiɲu nɐ ˈfejɾɐ dɨ bɐˈrɐ̃ku'
```

## Where next

- [quickstart.md](quickstart.md) — install and the first call
- [api.md](api.md) — the functions, their return contracts, and the plugin
