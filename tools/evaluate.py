#!/usr/bin/env python3
"""Readability benchmark for the standard, scored for both audiences.

The linter answers "does this break a rule". This answers "is this getting
harder to read". They fail for different reasons and both are needed: a
document can pass every rule and still drift toward being unreadable.

Metrics are grouped by who they serve:

  HUMAN   reading ease, grade level, sentence length, passive voice
  AGENT   cross-reference integrity, addressability, anaphora, term drift
  SHARED  structural completeness

Thresholds are floors, not targets. A metric that regresses past its floor
fails the build. Run with --baseline to record current values after an
intentional change.

Usage:
  tools/evaluate.py                 score and gate against thresholds
  tools/evaluate.py --json          machine-readable scorecard
  tools/evaluate.py --baseline      rewrite evals/baseline.json
Exit: 0 pass, 1 a metric is below its floor
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASELINE = ROOT / "evals" / "baseline.json"
TARGET = ROOT / "STANDARD.md"

# GATING metrics only. Each is a single, independently observable fact that a
# reader can confirm by hand, and none can be improved without improving the
# document. A cross-reference either resolves or it does not.
#
# Everything else this file computes is ADVISORY and never fails the build.
# Flesch scores, grade level, sentence length, and passive ratio are proxies,
# and every one of them is trivially gamed: chop sentences to raise reading
# ease, add "**N.N**" markers to raise addressability. Gating on a number an
# author can move without helping a reader rewards the gaming, not the writing.
# They are reported so a trend is visible, and that is all.
THRESHOLDS = {
    "xref_integrity_pct":     {"floor": 100.0, "higher_is_better": True},
    "structure_complete_pct": {"floor": 100.0, "higher_is_better": True},
    "term_drift_count":       {"floor": 0.0, "higher_is_better": False},
}

ADVISORY = [
    "flesch_reading_ease", "flesch_kincaid_grade", "mean_sentence_words",
    "passive_voice_pct", "addressable_rules_pct", "unresolved_anaphora_per_kw",
]

# Rule 1.1: one term per concept. Each group must not mix within the document
# body. These are the pairs that actually drift in software prose.
TERM_GROUPS = [
    ("make sure", "ensure"),
    ("lets you", "allows you to"),
    ("delete", "remove permanently"),
]

VOWELS = "aeiouy"


def prose(text):
    """Strip everything Rule 11.1 exempts, plus tables and headings."""
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`]*`", " X ", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"https?://\S+", " X ", text)
    kept = []
    for ln in text.split("\n"):
        s = ln.strip()
        if not s or s.startswith("#") or s.startswith("|") or s.startswith(">"):
            continue
        s = re.sub(r"^\s*(\*\*[\d.]+\*\*|[-*]|\d+\.|\[[ x]\])\s*", "", s)
        kept.append(s)
    return " ".join(kept)


def syllables(word):
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    count, prev_vowel = 0, False
    for ch in w:
        v = ch in VOWELS
        if v and not prev_vowel:
            count += 1
        prev_vowel = v
    if w.endswith("e") and count > 1 and not w.endswith(("le", "ee")):
        count -= 1
    return max(1, count)


def split_sentences(text):
    return [s for s in re.split(r"(?<=[.!?])\s+(?=[*_]{0,2}[A-Z(\[\"'])", text) if s.strip()]


def readability(text):
    sents = split_sentences(text)
    words = re.findall(r"\b[\w'-]+\b", text)
    if not sents or not words:
        return {}
    syl = sum(syllables(w) for w in words)
    wps = len(words) / len(sents)
    spw = syl / len(words)
    return {
        "flesch_reading_ease": round(206.835 - 1.015 * wps - 84.6 * spw, 1),
        "flesch_kincaid_grade": round(0.39 * wps + 11.8 * spw - 15.59, 1),
        "mean_sentence_words": round(wps, 1),
        "_words": len(words),
        "_sentences": len(sents),
    }


def passive_pct(text):
    sents = split_sentences(text)
    if not sents:
        return 0.0
    be = r"\b(is|are|was|were|be|been|being)\b"
    part = r"\b\w+(?:ed|en|own|ung|ade)\b"
    hits = sum(1 for s in sents if re.search(be + r"\s+(?:\w+ly\s+)?" + part, s))
    return round(100.0 * hits / len(sents), 1)


def defined_ids(raw):
    # Three formats are in use: "**1.1** text", "**10.3 Title.**", and
    # "### 11.2 Title". Matching only the first silently reports live rules
    # as broken references.
    rules = set(re.findall(r"^\*\*(\d+\.\d+(?:\.\d+)?)[ *]", raw, re.M))
    rules |= set(re.findall(r"^#{2,4} (\d+\.\d+(?:\.\d+)?)\s", raw, re.M))
    sections = set(re.findall(r"^## (\d+)\.", raw, re.M))
    appendices = set(re.findall(r"^## Appendix ([A-Z])", raw, re.M))
    return rules, sections, appendices


def xref_integrity(raw):
    rules, sections, appendices = defined_ids(raw)
    refs, bad = 0, []

    for m in re.finditer(r"\b(?:[Rr]ule|STANDARD|see)\s+(\d+\.\d+(?:\.\d+)?)\b", raw):
        refs += 1
        if m.group(1) not in rules:
            bad.append(f"rule {m.group(1)}")
    for m in re.finditer(r"\((\d+\.\d+(?:\.\d+)?)\)", raw):
        refs += 1
        if m.group(1) not in rules:
            bad.append(f"({m.group(1)})")
    for m in re.finditer(r"\b[Ss]ection (\d+)\b", raw):
        refs += 1
        if m.group(1) not in sections:
            bad.append(f"section {m.group(1)}")
    for m in re.finditer(r"\bAppendix ([A-Z])\b", raw):
        refs += 1
        if m.group(1) not in appendices:
            bad.append(f"Appendix {m.group(1)}")

    pct = 100.0 if not refs else round(100.0 * (refs - len(bad)) / refs, 1)
    return pct, refs, sorted(set(bad))


def addressable_pct(raw):
    """A normative statement an agent cannot cite is one it cannot be held to."""
    body = raw.split("## Appendix A")[0]
    normative, addressed = 0, 0
    for block in body.split("\n\n"):
        b = block.strip()
        if not b or b.startswith(("#", ">", "|", "```")):
            continue
        if re.match(r"^\*\*\d+\.\d+", b):
            normative += 1
            addressed += 1
        elif re.match(r"^(Use|Do not|Never|Always|Write|Keep|Put|State|Give|Prefer)\b", b):
            normative += 1
    return (100.0 if not normative else round(100.0 * addressed / normative, 1)), normative


def anaphora_per_kw(text):
    """Rule 10.7. Counts sentence-initial bare demonstratives, the form most
    likely to have an ambiguous antecedent."""
    sents = split_sentences(text)
    words = len(re.findall(r"\b[\w'-]+\b", text)) or 1
    hits = sum(
        1 for s in sents
        if re.match(r"^\s*(This|That|It|These|Those)\s+(is|are|was|were|means|makes|gives)\b", s)
    )
    return round(1000.0 * hits / words, 2), hits


def term_drift(raw):
    body = prose(raw.split("## Appendix B")[0])
    low = body.lower()
    drift = []
    for preferred, banned in TERM_GROUPS:
        if banned in low and preferred in low:
            drift.append(f"{banned!r} used alongside {preferred!r}")
        elif banned in low:
            drift.append(f"{banned!r} used instead of {preferred!r}")
    return len(drift), drift


def structure_pct(raw):
    _, sections, appendices = defined_ids(raw)
    want_s = {str(i) for i in range(0, 12)}
    want_a = set("ABCDEFG") - {"F", "G"}   # F and G exist only in the deliverable
    missing = sorted((want_s - sections) | {f"Appendix {a}" for a in (want_a - appendices)})
    total = len(want_s) + len(want_a)
    have = total - len(missing)
    return round(100.0 * have / total, 1), missing


def evaluate():
    raw = TARGET.read_text(encoding="utf-8")
    text = prose(raw)

    m = readability(text)
    xref, xref_n, xref_bad = xref_integrity(raw)
    addr, addr_n = addressable_pct(raw)
    ana, ana_n = anaphora_per_kw(text)
    drift_n, drift = term_drift(raw)
    struct, struct_missing = structure_pct(raw)

    return {
        "flesch_reading_ease": m["flesch_reading_ease"],
        "flesch_kincaid_grade": m["flesch_kincaid_grade"],
        "mean_sentence_words": m["mean_sentence_words"],
        "passive_voice_pct": passive_pct(text),
        "xref_integrity_pct": xref,
        "addressable_rules_pct": addr,
        "unresolved_anaphora_per_kw": ana,
        "term_drift_count": float(drift_n),
        "structure_complete_pct": struct,
        "_detail": {
            "words": m["_words"],
            "sentences": m["_sentences"],
            "xrefs_checked": xref_n,
            "broken_xrefs": xref_bad,
            "normative_statements": addr_n,
            "anaphora_hits": ana_n,
            "term_drift": drift,
            "structure_missing": struct_missing,
        },
    }


GROUP = {
    "flesch_reading_ease": "HUMAN", "flesch_kincaid_grade": "HUMAN",
    "mean_sentence_words": "HUMAN", "passive_voice_pct": "HUMAN",
    "xref_integrity_pct": "AGENT", "addressable_rules_pct": "AGENT",
    "unresolved_anaphora_per_kw": "AGENT", "term_drift_count": "AGENT",
    "structure_complete_pct": "SHARED",
}


def main(argv):
    scores = evaluate()
    detail = scores.pop("_detail")

    if "--json" in argv:
        print(json.dumps({**scores, "_detail": detail}, indent=2))
        return 0

    if "--baseline" in argv:
        BASELINE.parent.mkdir(exist_ok=True)
        BASELINE.write_text(json.dumps(scores, indent=2) + "\n", encoding="utf-8")
        print(f"baseline written to {BASELINE.relative_to(ROOT)}")
        for k, v in scores.items():
            print(f"  {GROUP[k]:<7} {k:<28} {v}")
        return 0

    prev = json.loads(BASELINE.read_text()) if BASELINE.exists() else {}
    print(f"STANDARD.md — {detail['words']} words, {detail['sentences']} sentences\n")
    print(f"  {'':<7} {'metric':<28} {'value':>8} {'floor':>8} {'prev':>8}")

    failed = []
    for key, val in scores.items():
        was = prev.get(key)
        shown_prev = "" if was is None else was
        if key in THRESHOLDS:
            spec = THRESHOLDS[key]
            floor, higher = spec["floor"], spec["higher_is_better"]
            bad = val < floor if higher else val > floor
            mark = "FAIL" if bad else "ok"
            if bad:
                failed.append(key)
            print(f"  {GROUP[key]:<7} {key:<28} {val:>8} {floor:>8} "
                  f"{shown_prev:>8}  {mark}")
        else:
            print(f"  {GROUP[key]:<7} {key:<28} {val:>8} {'—':>8} "
                  f"{shown_prev:>8}  advisory")

    if detail["broken_xrefs"]:
        print(f"\n  broken cross-references: {', '.join(detail['broken_xrefs'])}")
    if detail["term_drift"]:
        print(f"\n  terminology drift: {'; '.join(detail['term_drift'])}")
    if detail["structure_missing"]:
        print(f"\n  missing structure: {', '.join(detail['structure_missing'])}")

    print()
    if failed:
        print(f"FAILED: {len(failed)} metric(s) below floor: {', '.join(failed)}")
        print("Fix the document, or run --baseline if the change is intentional.")
        return 1
    print("All metrics within thresholds.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
