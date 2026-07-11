# Advanced — diacritics, the `x` rule, gotchas and recipes

`phonemize` is heuristic: the spelling carries most of the information the rules
need, so the more faithfully a word is written (diacritics included), the better
the transcription.

## Diacritics steer the vowels

The same base vowel maps to different IPA depending on its accent. Spell the
accents and the open/closed/nasal distinction comes through:

```python
from g2p_barranquenho import phonemize

phonemize("cantá")    # ['k', 'ɐ̃', 't', 'a']   — á is open stressed /a/
phonemize("ambu")     # ['ɐ̃', 'b', 'u']        — a before m nasalises
phonemize("manhán")   # ['m', 'ɐ', 'ɲ', 'ɐ̃']   — final án nasalises
```

A bare `a` is also raised after `c` and reduced word-finally:

```python
phonemize("boca")     # ['b', 'o', 'k', 'ɐ']   — final -a → ɐ
phonemize("paraba")   # ['p', 'ɐ', 'ɾ', 'a', 'b', 'ɐ']
```

## Word-final reduction

Final `-a`/`-e` (and `-as`/`-es`) reduce, mirroring European Portuguese:

```python
phonemize("que")      # ['k', 'ɨ']             — final e → ɨ
phonemize("boca")     # ['b', 'o', 'k', 'ɐ']   — final a → ɐ
```

## Position-sensitive consonants

`r` and `s` depend on where they sit; `ss`/`rr` collapse to a single phoneme:

```python
phonemize("rato")     # ['r', 'ɐ', 't', 'o']   — initial r → r
phonemize("paraba")   # ['p', 'ɐ', 'ɾ', 'a', 'b', 'ɐ']  — medial r → ɾ
phonemize("pássaru")  # ['p', 'a', 's', 'ɐ', 'ɾ', 'u']  — ss → single s
```

## The `x` disambiguation

Word-medial `x` has no single rule in Portuguese spelling, so `phonemize` walks a
ladder of pt-PT context heuristics to pick `ʃ`, `s` or `z`:

- after `n`/`m`: `ʃ` (enxofre, enxame)
- `x` + `c`: `s`, consuming the `c` (exceção)
- vowel-vowel before `x`: `ʃ`, except `au` → `s` (peixe vs auxiliar)
- vowel-`x`-vowel: `z`, except `ó/á` + `i` → `s` (exame vs máximo)
- `x` + `p`/`t`: `s` (explorar, texto)
- otherwise: `ʃ`

```python
phonemize("peixe")     # ['p', 'e', 'j', 'ʃ', 'ɨ']    — vowel-vowel-x → ʃ
phonemize("texto")     # ['t', 'e', 's', 't', 'o']    — x + t → s
phonemize("auxiliar")  # ['a', 'u', 's', 'j', 'l', 'j', 'a', 'ɾ']  — au-x → s
```

## Gotchas

- **One word per call.** `phonemize` does not tokenise. Pass `"boca cantá"` and
  the space is treated as part of one word; split first.
- **`v` and `k` are reshaped.** Barranquenho writes `b` for `v`, so `v → b`; `k`
  (only in loanwords) and `q` both yield `k`.
- **Output is flat.** No syllable boundaries and no stress marks — just the
  segment list. Build your own grouping if you need syllables.
- **Heuristic vowel quality.** Bare `e` and `o` default to `e`/`o`; bare `a`
  uses a stress heuristic. Hand-written accents override these defaults, so prefer
  fully-accented input.

## Recipes

### Batch a vocabulary into a transcription map

```python
from g2p_barranquenho import phonemize

vocab = ["boca", "cantá", "que", "manhán"]
table = {w: phonemize(w) for w in vocab}
```

### Compact string form

```python
from g2p_barranquenho import phonemize

"".join(phonemize("manhán"))   # 'mɐɲɐ̃'
```

### Transcribe a phrase, keeping word boundaries

```python
from g2p_barranquenho import phonemize

phrase = "boca cantá que"
[(w, phonemize(w)) for w in phrase.split()]
```

## Where next

- [quickstart.md](quickstart.md) — install and the first call
- [api.md](api.md) — the signature, return contract and rule passes
