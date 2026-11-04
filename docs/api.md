# API reference

The package exposes two functions and a plugin class.

## `phonemize(word)`

```python
from g2p_barranquenho import phonemize

phonemize(word: str) -> list[str]
```

Convert one written Barranquenho word to a list of IPA phones.

**Parameters**

- `word` (`str`) - a single word. It is normalised (NFC, lower-cased)
  internally, so case does not matter. Pass one token at a time. For a phrase, use
  [`transcribe`](#transcribetext), which also resolves boundary effects.

**Returns**

- `list[str]` - the phones in reading order, one IPA segment per item.
  `"".join(phonemize(word))` gives the word's IPA string. Items may be
  multi-character: nasal vowels carry a combining tilde (`ɐ̃`), and a stress mark
  leads the phone that carries it (`ˈɲ`). Letters consumed by a digraph or a
  doubled consonant produce a single entry.

```python
phonemize("ambu")      # ['ˈɐ̃', 'b', 'u']
phonemize("bonita")    # ['b', 'u', 'ˈn', 'i', 't', 'ɐ']
phonemize("pássaru")   # ['ˈp', 'a', 's̺', 'ɐ', 'ɾ', 'u']
```

## `transcribe(text)`

```python
from g2p_barranquenho import transcribe

transcribe(text: str, *, normalizer=normalize) -> str
```

Transcribe a whole utterance to a single IPA string. The utterance is scored as
a whole, so the spec's cross-word sandhi applies: coda-`/s/` aspiration and
deletion, article and conjunction destressing, and vowel elision at word
boundaries. Word boundaries surface as spaces.

```python
transcribe("boca cantá")                       # 'ˈbɔkɐ kɐ̃ˈta'
transcribe("O tempu não ehtá nada bom agora.") # 'o ˈtẽpu ˈnɐ̃w̃ eˈhta ˈnadɐ ˈbõ ɐˈɡɔɾɐ'
transcribe("que o")                            # 'k o'  (boundary elision)
```

- `normalizer` - the caller-side text folding applied before phonemisation.
  Defaults to [`normalize`](#normalizetext). Pass `normalizer=None` to feed the
  text to the spec unchanged.

## `normalize(text)`

```python
from g2p_barranquenho import normalize

normalize(text: str) -> str
```

Caller-side text normalisation (NFC, lower case). It does no phonological work.
That belongs to the spec. `phonemize` and `transcribe` apply it automatically.

```python
normalize("BÔA")   # 'bôa'
```

## `LANG`

The spec code this package drives: `"ext-PT-x-barrancos"`.

## `BarranquenhoG2PPlugin`

```python
from g2p_barranquenho.plugin import BarranquenhoG2PPlugin

plugin = BarranquenhoG2PPlugin()
plugin.language_codes                    # ['ext-PT-x-barrancos']
plugin.transcribe("boca cantá")          # 'ˈbɔkɐ kɐ̃ˈta'
plugin.transcribe_word("bonita")         # 'buˈnitɐ'
```

This is the string-returning adapter other components in the `orthography2ipa`
toolchain expect. `transcribe` phonemises the whole utterance, with sandhi.
`transcribe_word` phonemises a single word, with no cross-word effects, and
accepts an optional `context` argument.

## Where next

- [quickstart.md](quickstart.md) - install and first calls
- [advanced.md](advanced.md) - stress, sandhi, diacritics, gotchas, and recipes

---
[← Quickstart](quickstart.md) · [Home](../README.md) · [Advanced →](advanced.md)
