# TODO — g2p_barranquenho

## Hardening (CI / packaging / hygiene)

- [x] Wire up the standard `OpenVoiceOS/gh-automations@dev` reusable workflows: `build-tests`, `coverage`, `license_check`, `release_workflow`, `publish_stable`, `conventional-label` (plus `lint`, `pip_audit`, `release-preview`, `repo-health`).
- [x] Migrate packaging to `pyproject.toml` (drop `setup.py`); the version block in `version.py` stays untouched, resolved dynamically via `g2p_barranquenho.version.VERSION_STR`.
- [x] Resolve the dual version-file hazard: packaging now reads only `g2p_barranquenho/version.py`; the `extended_langcodes/version.py` path the old `setup.py` pointed at is no longer referenced.
- [x] Fill in package metadata: `license` (Apache-2.0) and `description` set, and a `LICENSE` file added.
- [x] Build artifacts and `__pycache__` covered by `.gitignore` (egg-info, build/dist, etc.).
- [x] Add a real test suite under `test/`, seeded with the worked examples in the README plus per-rule coverage.
- [ ] Clarify or remove `extended_langcodes/`: it holds only a stray `version.py`, is not a declared package, and ships no code. (No longer referenced by packaging; left for follow-up.)
- [ ] The large source PDFs at the repo root (Orthographic Convention, dictionary, basic grammar) inflate the clone. Keep them as references but consider extracting the derived rule tables into data.

## Correctness gaps

- [x] Vowel-quality disambiguation for bare `a` (`a` stressed / `ɐ` unstressed), bare `e` (`e` stressed / `ɨ` unstressed), and bare `o` (`o` stressed / `u` unstressed), driven by a stress-position helper.
- [ ] Output is a flat list of IPA strings (some multi-character, e.g. `tʃ`, `ɐ͂`, `ẽj`) with no syllable or stress annotation. Decide whether to add stress/syllable structure (reusing `silabificador`).

## Code TODOs

- [x] `g2p_barranquenho/__init__.py` — disambiguate bare `a` (`a` / `ɐ`).
- [x] `g2p_barranquenho/__init__.py` — disambiguate bare `e` (`e` / `ɨ`).
- [x] `g2p_barranquenho/__init__.py` — disambiguate bare `o` (`o` / `u`).
