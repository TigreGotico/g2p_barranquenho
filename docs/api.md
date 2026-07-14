# API reference

The package exposes a single public symbol.

## `phonemize(word)`

```python
from g2p_barranquenho import phonemize

phonemize(word: str) -> list[str]
```

Convert one written Barranquenho word to a list of IPA phoneme strings.

**Parameters**

- `word` (`str`) — a single word. It is lower-cased internally, so case is
  irrelevant. Pass one token at a time; for phrases, split on whitespace first.

**Returns**

- `list[str]` — the phonemes in reading order. Each item is one IPA segment.
  Items may be multi-character: nasal vowels carry a combining tilde (`ɐ̃`, `ɐ̃w`),
  and the `tch` digraph yields the affricate `tʃ`. Letters consumed by a digraph
  or by a doubled consonant produce a single entry, so the list is generally
  shorter than the input string.

```python
phonemize("ambu")     # ['ɐ̃', 'b', 'u']
phonemize("biba")     # ['b', 'j', 'b', 'ɐ']
phonemize("pássaru")  # ['p', 'a', 's', 'ɐ', 'ɾ', 'u']
```

### How the rules apply

`phonemize` walks the word twice.

**Pass 1 — digraphs.** Multi-letter spellings are resolved before anything else,
so their component letters are not re-read in pass 2:

| spelling | phoneme | example |
| --- | --- | --- |
| `nh` | `ɲ` | `manhán` |
| `ch` | `ʃ` | — |
| `lh` | `ʎ` | — |
| `tch` | `tʃ` | — |
| `qu` (before `e é i í`) | `k` | `que`, `aquí` |
| `gu` (before `e é i í`) | `g` | — |

**Pass 2 — single graphemes.** Vowels are resolved by their diacritic and
position:

- Nasal context — a vowel directly before `m`/`n` nasalises and swallows that
  consonant: `a→ɐ̃`, `e→ẽ`, `i→ĩ`, `o→õ`, `u→ũ` (`ambu → ['ɐ̃', 'b', 'u']`).
- Tilde vowels (`ã õ`) are nasal on their own; acute/grave (`á à`, `ó ò`, …) mark
  open stressed quality (`á→a`, `ó→ɔ`); circumflex (`â ê ô`) marks closed quality.
- Word-final `-a` / `-e` reduce (`a→ɐ`, `e→ɨ`), as do `-as` / `-es`.
- `i`/`í` between consonants surfaces as the glide `j` (`biba → ['b', 'j', 'b', 'ɐ']`).

Consonants are mostly one-to-one, with a few context rules:

- `c` → `s` before `e i`, else `k`; `ç` → `s`.
- `g` → `ʒ` before `e i í`, else `g`.
- `r` → `r` word-initial or doubled, `ɾ` elsewhere.
- `s` → `s` word-initial or doubled, `z` elsewhere.
- `v` → `b` and `k`/`q` → `k` (Barranquenho writes `b` for `v`; `k` only in loanwords).
- `x` is disambiguated by pt-PT context (`ʃ` / `s` / `z`) — see
  [advanced.md](advanced.md).

### Run the bundled demo

The module is runnable and prints a fixed sample list:

```bash
python -m g2p_barranquenho
```

## Where next

- [quickstart.md](quickstart.md) — install and first calls
- [advanced.md](advanced.md) — diacritics in depth, the `x` rule, gotchas, recipes
