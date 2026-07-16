# Quickstart — Barranquenho in IPA

`g2p_barranquenho` is a grapheme-to-phoneme (G2P) converter for
[Barranquenho](https://en.wikipedia.org/wiki/Barranquenho), the Ibero-Romance
variety spoken in Barrancos, Portugal. You hand it written Barranquenho and it
hands back IPA.

## 1. Install

```bash
pip install -e .
```

It builds on [`orthography2ipa`](https://github.com/OpenVoiceOS/orthography2ipa),
which is pulled in automatically. The Barranquenho phonology comes from that
library's `ext-PT-x-barrancos` language spec.

## 2. Two functions

`phonemize` takes a single word and returns a flat list of IPA phones:

```python
from g2p_barranquenho import phonemize

phonemize("boca")     # ['ˈb', 'ɔ', 'k', 'ɐ']
```

`transcribe` takes a whole utterance and returns one IPA string, applying
cross-word sandhi:

```python
from g2p_barranquenho import transcribe

transcribe("boca cantá")   # 'ˈbɔkɐ kɐ̃ˈta'
```

Lexical stress is marked with `ˈ` before the stressed syllable; word boundaries
in `transcribe` output are spaces.

## 3. First real calls

```python
from g2p_barranquenho import phonemize

for word in ["paraba", "cahtelu", "manhán", "aqui"]:
    print(word, phonemize(word))

# paraba  ['p', 'ɐ', 'ˈɾ', 'a', 'b', 'ɐ']
# cahtelu ['k', 'ɐ', 'ˈh', 't', 'ɛ', 'l', 'u']
# manhán  ['m', 'ɐ', 'ˈɲ', 'ɐ̃']
# aqui    ['ˈɐ', 'k', 'i']
```

Input is case-insensitive (it is lower-cased internally). `phonemize` expects a
single word; for a phrase, use `transcribe`, which also resolves what happens
between words.

## 4. Whole-utterance transcription

```python
from g2p_barranquenho import transcribe

transcribe("O tempu não ehtá nada bom agora.")
# 'o ˈtẽpu ˈnɐ̃w̃ eˈhta ˈnadɐ ˈbõ ɐˈɡɔɾɐ'
```

Because the utterance is scored as a whole, boundary effects surface — for
example `que o` elides to `k o`, which phonemising each word alone cannot see.

## Where next

- [api.md](api.md) — the functions, their return contracts, and the plugin
- [advanced.md](advanced.md) — stress, sandhi, the diacritics that drive the spec, and recipes
