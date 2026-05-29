# TODO — g2p_barranquenho

## Hardening (CI / packaging / hygiene)

- [ ] Wire up the standard `OpenVoiceOS/gh-automations@dev` reusable workflows: `build-tests`, `coverage`, `license_check`, `release_workflow`, `publish_stable`, `conventional-label`. The repo currently has no `.github/workflows/`.
- [ ] Migrate packaging to `pyproject.toml` (drop `setup.py`); keep the version block in `version.py` untouched by humans.
- [ ] Resolve the dual version-file hazard: `setup.py` reads the package version from `extended_langcodes/version.py`, but the shipped package is `g2p_barranquenho`, which has its own `version.py`. The two can drift. Standardise on `g2p_barranquenho/version.py`.
- [ ] Clarify or remove `extended_langcodes/`: it holds only a stray `version.py`, is not a declared package, and ships no code.
- [ ] Fill in package metadata: `license` and `description` are empty. Add a `LICENSE` file.
- [ ] Remove the committed build artifact `g2p_barranquenho.egg-info/` and add a `.gitignore` (egg-info, `__pycache__`, build/dist).
- [ ] Add a real test suite under `tests/`. The only check today is the `__main__` demo (`python -m g2p_barranquenho`). Seed it with the worked examples in the README and from the Orthographic Convention.
- [ ] The large source PDFs at the repo root (Orthographic Convention, dictionary, basic grammar) inflate the clone. Keep them as references but consider extracting the derived rule tables into data.

## Correctness gaps

- [ ] Vowel-quality disambiguation is unresolved for bare `a` (`ɐ` vs `a`), bare `e` (`ɛ` / `e` / `j`), and bare `o` (`ɔ` vs `o`). Defaults are heuristic and the candidate forms are not consistently applied.
- [ ] Output is a flat list of IPA strings (some multi-character, e.g. `tʃ`, `ɐ͂`, `ẽj`) with no syllable or stress annotation. Decide whether to add stress/syllable structure (reusing `silabificador`).

## Code TODOs

- [ ] `g2p_barranquenho/__init__.py:75` — disambiguate bare `a` (`ɐ` vs `a`).
- [ ] `g2p_barranquenho/__init__.py:99` — disambiguate bare `e` (`ɛ` / `e` / `j`).
- [ ] `g2p_barranquenho/__init__.py:119` — disambiguate bare `o` (`ɔ` vs `o`).
