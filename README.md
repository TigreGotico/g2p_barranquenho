## `g2p_barranquenho` - Barranquenho Phonemizer

This repository provides a simple, rule-based Grapheme-to-Phoneme (G2P) converter for the **Barranquenho** language.

[Barranquenho](https://en.wikipedia.org/wiki/Barranquenho) is an Ibero-Romance language (often classified as a dialect) spoken in the municipality of Barrancos, Portugal, which shares many features with the nearby Spanish dialects of Extremadura and Andalusia.

The rules implemented in the `phonemize` function are primarily based on the official Barranquenho Orthographic Convention

### 🚀 Usage

The core functionality is provided by the `phonemize` function, which takes a word (string) and returns a list of International Phonetic Alphabet (IPA) phonemes.

```python
from g2p_barranquenho import phonemize

for word in [...]:
    phonemes = phonemize(word)
    print(word, phonemes)
    
# paraba ['p', 'ɐ', 'ɾ', 'a', 'b', 'ɐ']
# pássaru ['p', 'a', 's', 'ɐ', 'ɾ', 'u']
# biba ['b', 'j', 'b', 'ɐ']
# cahtelu ['k', 'ɐ', 'h', 't', 'e', 'l', 'u']
# boca ['b', 'o', 'k', 'ɐ']
# ambu ['ɐ͂', 'b', 'u']
# cantá ['k', 'ɐ͂', 't', 'a']
# manhán ['m', 'ɐ', 'ɲ', 'ɐ͂']
# que ['k', 'ɨ']
# aquí ['ɐ', 'k', 'j']
```
