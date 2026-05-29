# Roadmap — g2p_barranquenho

A rule-based grapheme-to-phoneme converter for Barranquenho, an Ibero-Romance
variety spoken in Barrancos, returning IPA phoneme lists. Rules derive from the
official Barranquenho Orthographic Convention.

## Phase 0 — Hardening

Bring the repo to org standard before extending the linguistics.

- Adopt `pyproject.toml` packaging; retire `setup.py` and the duplicate
  `extended_langcodes/version.py`, keeping a single `g2p_barranquenho/version.py`.
- Wire the `OpenVoiceOS/gh-automations@dev` reusable workflows (build-tests,
  coverage, license_check, release_workflow, publish_stable, conventional-label).
- Add `LICENSE`, fill `description`, add a `.gitignore`, and remove the committed
  `g2p_barranquenho.egg-info/`.
- Stand up a `tests/` suite seeded from the README examples and the Orthographic
  Convention worked forms.

## Phase 1 — Correctness & coverage

Close the open linguistic gaps, gated by the new test suite.

- Resolve the three vowel-quality disambiguations (bare `a`, `e`, `o`) using the
  stress/position context the Convention specifies, rather than fixed defaults.
- Verify nasalisation (`ɐ͂`, `ẽj`) and digraph handling (`tch`, `ch`, `nh`, `lh`,
  `qu`, `gu`) against the dictionary entries.
- Decide on a stress/syllable-annotated output mode (flat IPA list stays the
  default) and reuse `silabificador` for boundaries where possible.

## Phase 2 — Integration

Make the converter composable inside the org phonetics stack.

- Expose it as a `phoonnx` phonemizer backend: add a Barranquenho module under
  `phoonnx/phonemizers/` subclassing `BasePhonemizer`, emitting `Alphabet.IPA`,
  registered via a `PhonemeType` value (alongside the existing `tugaphone` / `mwl`
  entries).
- Align the IPA inventory and tokenisation with `orthography2ipa`: contribute a
  Barranquenho `LanguageSpec` (grapheme→IPA + allophone maps, ancestry linking it
  to pt/es Extremaduran-Andalusian neighbours) so it validates against
  `orthography2ipa`'s tokenizer and distance metrics.

## Phase 3 — Datasets & publishing

- Publish a small gold word→IPA evaluation set derived from the dictionary so the
  rule changes can be scored (phoneme error rate), mirroring the corpus approach
  used by the other Lusophone phonemizers.
- Release to PyPI through the standard publish workflow once Phase 0 lands.
