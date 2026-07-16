## `g2p_barranquenho` - Barranquenho Phonemizer

This repository provides a grapheme-to-phoneme (G2P) converter for the **Barranquenho** language: hand it written Barranquenho, get back IPA.

[Barranquenho](https://en.wikipedia.org/wiki/Barranquenho) is an Ibero-Romance variety spoken in the municipality of Barrancos, Portugal, sharing many features with the neighbouring Extremaduran and Andalusian varieties of Spanish — coda-`/s/` aspiration, betacism (`v` → `[b]`), the alveolar trill, and southern vowel reduction.

### Architecture

The phonology lives in the shared [`orthography2ipa`](https://github.com/OpenVoiceOS/orthography2ipa) language spec `ext-PT-x-barrancos`. That spec — its grapheme table, allophone rules, stress model and cross-word sandhi — is the single source of truth for how Barranquenho is realised. This package is a thin wrapper around `orthography2ipa.G2P` driven by that spec:

- **`transcribe(text)`** phonemises a whole utterance, so the spec's cross-word sandhi applies (coda-`/s/` aspiration and deletion, article and conjunction destressing, vowel elision at word boundaries).
- **`phonemize(word)`** phonemises one word and returns its phones as a list.
- The package owns only caller-side text handling (case/Unicode normalisation) and this stable surface. The linguistic rules belong to the spec, so improving a rule is an upstream edit that every consumer shares.

Lexical stress is marked with `ˈ` before the stressed syllable. Nasal vowels carry the combining tilde `U+0303` (`ɐ̃`), and a coda `m`/`n` is absorbed into the preceding nasal vowel rather than surfacing as its own segment.

### 🚀 Usage

`phonemize` takes one word and returns a list of IPA phones; join the list for a compact string:

```python
from g2p_barranquenho import phonemize

phonemize("boca")      # ['ˈb', 'ɔ', 'k', 'ɐ']
phonemize("manhán")    # ['m', 'ɐ', 'ˈɲ', 'ɐ̃']
phonemize("ambu")      # ['ˈɐ̃', 'b', 'u']

"".join(phonemize("cahtelu"))   # 'kɐˈhtɛlu'
```

`transcribe` takes a whole utterance and applies cross-word sandhi:

```python
from g2p_barranquenho import transcribe

transcribe("O tempu não ehtá nada bom agora.")
# 'o ˈtẽpu ˈnɐ̃w̃ eˈhta ˈnadɐ ˈbõ ɐˈɡɔɾɐ'

transcribe("Comprámos pão e vinho na feira de Barrancos.")
# 'kõˈpɾamu ˈpɐ̃w̃ i ˈbiɲu nɐ ˈfejɾɐ dɨ bɐˈrɐ̃ku'
```

The `BarranquenhoG2PPlugin` class in `g2p_barranquenho.plugin` exposes the same engine behind the string-returning `transcribe` / `transcribe_word` methods other components in the toolchain expect.

### Numbers

Digits carry no orthography the lattice can read, so numeric tokens are spelled
out into Barranquenho words *before* transcription — the normalizer stage. It is
on by default in `transcribe`; pass `expand_numbers=False` to leave digits as-is.

```python
from g2p_barranquenho import transcribe
from g2p_barranquenho.number_utils import normalize_numbers, BarranquenhoNumberParser

transcribe("tenho 3 gatu")                       # 3 -> 'treh', then transcribed
transcribe("tenho 3 gatu", expand_numbers=False)  # digit left to the spec

# spell numbers to text without phonemising
normalize_numbers("tenho 20 anu")                # 'tenho binti anu'
normalize_numbers("la casa 1ª")                  # 'la casa primeira' (º masc / ª fem)

# the verbaliser directly
p = BarranquenhoNumberParser()
p.cardinal(256)              # 'duzentuh e cinquenta e seih'
p.cardinal(2, "feminine")    # 'duah'
p.ordinal(1, "feminine")     # 'primeira'
p.pronounce_token("3,5")     # 'treh birgula cincu'
```

Numeral groups join with the copulative **e** ("and"). Navas Sánchez-Élez (2011)
documents no numeral paradigm, so most forms are reconstructed by the Convenção
Ortográfica do Barranquenho (2025) spelling rules — final `-o→-u` / `-e→-i`, coda
`-s` written `-h`, `v→b`. The lexemes Navas does attest (2 *douh*, 3 *treh*,
6 *seih*, 7 *seti*, 10 *deh*, 14 *catorzi*, 20 *binti*, 100 *cien*, 1000 *mil*,
1st *primeiru*) are in `number_utils.ATTESTED`; everything else is in
`number_utils.DERIVED`, so a reader can tell citation from reconstruction.

### Documentation

- [docs/quickstart.md](docs/quickstart.md) — install and the first call
- [docs/api.md](docs/api.md) — the functions, their contracts, and the plugin
- [docs/advanced.md](docs/advanced.md) — stress, sandhi, diacritics, and recipes
- [examples/](examples/) — runnable scripts

### Sources

The `ext-PT-x-barrancos` spec derives from the coordinated normative suite produced under the *Programa de Preservação e Valorização da Língua e Cultura Barranquenhas*, plus the phonetic descriptions of Navas Sánchez-Élez:

- **Convenção Ortográfica do Barranquenho** (June 2025). Câmara Municipal de Barrancos / II Congresso Barranquenho working group.
- **Gramática Básica de Barranquenho** (July 2025). Maria Filomena Gonçalves, María Victoria Navas, Victor M. Diogo Correia. Universidade de Évora, 1ª edição. ISBN 978-972-778-464-6.
- **Dicionário de Barranquenho** (2025). Maria Filomena Gonçalves, María Victoria Navas, Vera Ferreira. Universidade de Évora, 1ª edição. ISBN 978-972-778-460-8.
- **Navas Sánchez-Élez, M. V.** (2011). *El barranqueño: un modelo de lenguas en contacto*. Madrid: Editorial Complutense.
