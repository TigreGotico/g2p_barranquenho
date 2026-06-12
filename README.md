## `g2p_barranquenho` - Barranquenho Phonemizer

This repository provides a simple, rule-based Grapheme-to-Phoneme (G2P) converter for the **Barranquenho** language.

[Barranquenho](https://en.wikipedia.org/wiki/Barranquenho) is an Ibero-Romance language (often classified as a dialect) spoken in the municipality of Barrancos, Portugal, which shares many features with the nearby Spanish dialects of Extremadura and Andalusia.

The rules implemented in the `phonemize` function are based on the three official 2025 normative sources listed in the **Sources** section below.

### 🚀 Usage

The core functionality is provided by the `phonemize` function, which takes a word (string) and returns a list of International Phonetic Alphabet (IPA) phonemes.

```python
from g2p_barranquenho import phonemize

for word in [...]:
    phonemes = phonemize(word)
    print(word, phonemes)
    
# paraba ['p', 'ɐ', 'ɾ', 'a', 'b', 'ɐ']
# pássaru ['p', 'a', 's', 'ɐ', 'ɾ', 'u']
# biba ['b', 'i', 'b', 'ɐ']
# cahtelu ['k', 'ɐ', 'h', 't', 'e', 'l', 'u']
# boca ['b', 'o', 'k', 'ɐ']
# ambu ['ɐ͂', 'b', 'u']
# cantá ['k', 'ɐ͂', 't', 'a']
# manhán ['m', 'ɐ', 'ɲ', 'ɐ͂']
# que ['k', 'ɨ']
# aquí ['ɐ', 'k', 'i']
```

### Sources

The phoneme rules are derived from the coordinated normative suite produced under the *Programa de Preservação e Valorização da Língua e Cultura Barranquenhas*:

- **Convenção Ortográfica do Barranquenho** (June 2025). Câmara Municipal de Barrancos / II Congresso Barranquenho working group. Available at: https://cm-barrancos.pt/upload_files/1/3/Noticias/2025/II%20Congresso%20Barranquenho/Conven%C3%A7%C3%A3o%20Ortogr%C3%A1fica%20do%20Barranquenho%20junho%202025%20final.pdf
- **Gramática Básica de Barranquenho** (July 2025). Maria Filomena Gonçalves (Universidade de Évora / CIDEHUS-UÉ / FCT / Cátedra UNESCO em Património Imaterial e Saber-Fazer Tradicional), María Victoria Navas (Universidad Complutense de Madrid / CLUL), Victor M. Diogo Correia (Universidade de Évora / CIDEHUS-UÉ / FCT). Universidade de Évora, 1ª edição. ISBN 978-972-778-464-6.
- **Dicionário de Barranquenho** (2025). Maria Filomena Gonçalves (Universidade de Évora / CIDEHUS-UÉ / FCT / Cátedra UNESCO), María Victoria Navas (Universidad Complutense de Madrid / CLUL), Vera Ferreira (CIDLeS — Centro de Documentação Linguística e Social). Universidade de Évora, 1ª edição. ISBN 978-972-778-460-8.
