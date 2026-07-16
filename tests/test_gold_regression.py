"""Gold-set regression: score the engine against source-tied Barranquenho gold.

Two gold sets, both shipped by the ``orthography2ipa`` dependency:

- ``portuguese_tts/ext-PT-x-barrancos.tsv`` — 20 Barranquenho sentences whose
  IPA was blind-verified by two judges against Navas (2011) and arbitrated,
  aligned to the 2025 orthographic convention. This is the primary target.
- ``primary_sources/rows.jsonl`` — worked examples printed by Navas (2011),
  each pinned to a page. Narrow phonetic transcriptions (with sub-phonemic
  detail like [β ɣ ð] and idiolectal syncope the phonemic spec does not model),
  so a looser ceiling applies.

Phone Error Rate is a phone-level edit distance over the transcription. Ceilings
are set above the measured error with margin, so the test guards against
regression without pinning brittle exact strings.
"""
import csv
import json
import os
import unicodedata

import pytest

import orthography2ipa
from g2p_barranquenho import transcribe

_GOLD_DIR = os.path.join(os.path.dirname(orthography2ipa.__file__), "data", "gold")
_TTS = os.path.join(_GOLD_DIR, "portuguese_tts", "ext-PT-x-barrancos.tsv")
_PRIMARY = os.path.join(_GOLD_DIR, "primary_sources", "rows.jsonl")

_BINDING = "ːʲʷˠˤ͡"
_STRESS = set("ˈˌ")


def _phones(ipa, keep_stress):
    """Split an IPA string into comparable phones (diacritics bind left)."""
    ipa = unicodedata.normalize("NFC", ipa)
    out = []
    for ch in ipa:
        if ch == " ":
            continue
        if ch in _STRESS:
            if keep_stress:
                out.append(ch)
            continue
        if unicodedata.combining(ch) or ch in _BINDING:
            if out:
                out[-1] += ch
            else:
                out.append(ch)
        else:
            out.append(ch)
    return out


def _edit_distance(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def _corpus_per(rows, keep_stress):
    errors = ref = 0
    worst = []
    for text, gold in rows:
        g = _phones(gold, keep_stress)
        h = _phones(transcribe(text), keep_stress)
        e = _edit_distance(g, h)
        errors += e
        ref += len(g)
        worst.append((e, text, gold, transcribe(text)))
    worst.sort(reverse=True)
    return errors / ref, worst


def _load_tts():
    with open(_TTS, encoding="utf-8") as f:
        return [(r["sentence"], r["ipa"]) for r in csv.DictReader(f, delimiter="\t")]


def _load_primary():
    rows = []
    with open(_PRIMARY, encoding="utf-8") as f:
        for line in f:
            o = json.loads(line)
            if o.get("lang") == "ext-PT-x-barrancos":
                rows.append((o["orthography"], o["ipa"]))
    return rows


@pytest.mark.skipif(not os.path.exists(_TTS), reason="orthography2ipa gold data not packaged")
class TestConventionGold:
    """The 20-sentence convention-aligned TSV — the primary accuracy target."""

    def test_per_with_stress(self):
        per, worst = _corpus_per(_load_tts(), keep_stress=True)
        assert per <= 0.12, f"PER(with stress)={per:.3f}; worst: {worst[0]}"

    def test_per_segmental(self):
        per, _ = _corpus_per(_load_tts(), keep_stress=False)
        assert per <= 0.06, f"PER(segmental)={per:.3f}"


@pytest.mark.skipif(not os.path.exists(_PRIMARY), reason="orthography2ipa gold data not packaged")
class TestPrimarySourceGold:
    """Navas (2011) narrow transcriptions — diagnostic, looser ceiling."""

    def test_per_segmental(self):
        rows = _load_primary()
        assert rows, "no ext-PT-x-barrancos primary rows found"
        per, _ = _corpus_per(rows, keep_stress=False)
        assert per <= 0.40, f"PER(segmental)={per:.3f}"
