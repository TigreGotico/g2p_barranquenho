# Quickstart — Barranquenho in IPA

`g2p_barranquenho` is a rule-based grapheme-to-phoneme (G2P) converter for
[Barranquenho](https://en.wikipedia.org/wiki/Barranquenho), the Ibero-Romance
variety spoken in Barrancos, Portugal. You hand it a written word and it hands
back the IPA phonemes.

## 1. Install

```bash
pip install -e .
```

Pure Python, no runtime dependencies.

## 2. The one thing to understand

There is exactly one public function. It takes a single word and returns a flat
list of IPA phoneme strings:

```python
from g2p_barranquenho import phonemize

phonemize("boca")     # ['b', 'o', 'k', 'ɐ']
```

The conversion runs in two passes over the letters: first the digraphs
(`tch ch nh lh qu gu`), then the remaining individual graphemes — vowels with
their nasal, stressed and closed variants, then consonants. The output items are
plain strings, some of them multi-character (`tʃ`, `ɐ̃`, `ɐ̃w`).

## 3. First real call

```python
from g2p_barranquenho import phonemize

for word in ["paraba", "cahtelu", "manhán", "aquí"]:
    print(word, phonemize(word))

# paraba  ['p', 'ɐ', 'ɾ', 'a', 'b', 'ɐ']
# cahtelu ['k', 'ɐ', 'h', 't', 'e', 'l', 'u']
# manhán  ['m', 'ɐ', 'ɲ', 'ɐ̃']
# aquí    ['ɐ', 'k', 'j']
```

`phonemize` lower-cases internally, so case does not matter. It expects a single
word — split a sentence on whitespace and phonemize each token.

## 4. Whole-phrase transcription

A one-liner turns a phrase into a list of per-word phoneme lists:

```python
from g2p_barranquenho import phonemize

phrase = "boca cantá que"
transcription = [phonemize(w) for w in phrase.split()]
# [['b', 'o', 'k', 'ɐ'], ['k', 'ɐ̃', 't', 'a'], ['k', 'ɨ']]
```

Join the phonemes of a word into a single string when you want a compact form:

```python
"".join(phonemize("cantá"))   # 'kɐ̃ta'
```

## Where next

- [api.md](api.md) — the signature, the return contract and the rule passes
- [advanced.md](advanced.md) — the diacritics that drive the rules, gotchas, and batch recipes
