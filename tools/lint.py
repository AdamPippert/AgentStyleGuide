#!/usr/bin/env python3
"""Mechanical checks for AgentStyleGuide STANDARD.md.

Enforces only what a script can judge. Rules in sections 7 and 10 need a
reader; see CHECKLIST.md.

Usage:  python3 tools/lint.py FILE [FILE...]
Exit:   0 clean, 1 findings, 2 usage error
"""
import re
import sys

# Rule 4.1 / 4.2
MAX_PROCEDURAL = 20
MAX_DESCRIPTIVE = 25
MAX_PARA_SENTENCES = 6  # Rule 5.1

# Appendix B, high-confidence subset only. Takes precedence over FILLER,
# because naming the replacement is more useful than naming the offense.
REPLACE = {
    "utilize": "use", "leverage": "use", "in order to": "to",
    "prior to": "before", "subsequent to": "after",
    "in the event that": "if", "is able to": "can",
    "has the ability to": "can", "approximately": "about",
    "additional": "more", "obtain": "get", "sufficient": "enough",
    "commence": "start", "initiate": "start",
}

# Rule 10.5. Phrases with no single-word replacement; delete and rewrite.
# Anything already in REPLACE is excluded, or every hit reports twice.
FILLER = [
    p for p in [
        "it is worth noting", "worth noting that", "generally speaking",
        "in many cases", "it should be noted", "essentially", "of course",
        "seamless", "robust", "click here",
    ] if p not in REPLACE
]

# Rule 4.7. A sentence split only to pass 4.1/4.2 leaves a fragment that cannot
# stand alone. The two reliable signatures are an opening coordinating
# conjunction and a bare demonstrative that leans on the sentence before it.
CONJUNCTION_OPEN = re.compile(
    r"^[*_]{0,2}(And|But|Or|Nor|Yet|So)\b", re.I
)
# "It" is excluded deliberately. Run against the repository it produced twelve
# hits, all of the form "X is a thing. It is also a thing", where number
# agreement makes the referent unambiguous. Flagging those would force rewrites
# of correct prose to satisfy the checker, which is the gaming 4.7 exists to
# stop. Rule 10.7 covers "it" under reviewer judgment, where it belongs.
BARE_DEMONSTRATIVE = re.compile(
    r"^[*_]{0,2}(This|That|These|Those)\s+"
    r"(is|are|was|were|means|makes|gives|does|do|can|could|will|would|should|"
    r"lets|leaves|causes|has|have|had)\b",
    re.I,
)

# Abbreviations whose trailing period does not end a sentence.
ABBREV = [
    "e.g.", "i.e.", "etc.", "vs.", "cf.", "approx.", "al.", "Inc.", "Ltd.",
    "Dr.", "Mr.", "Ms.", "St.", "No.", "Fig.", "Sec.", "Ch.", "Rev.", "Vol.",
]


def strip_exempt(text):
    """Blank content exempt under Rule 11.1, preserving line count.

    Deleting the lines instead would shift every line number after a table,
    so reported locations would not match the file.
    """
    text = re.sub(
        r"```.*?```", lambda m: re.sub(r"[^\n]", "", m.group(0)), text, flags=re.S
    )
    return "\n".join(
        "" if ln.strip().startswith("|") else ln for ln in text.split("\n")
    )


def mask_exempt(text):
    """Blank exempt regions but preserve offsets, so line numbers stay true.

    Masks fenced code, inline code spans, tables, and blockquotes. A document
    that names a banned word inside backticks is citing it, not using it.
    """
    def blank(m):
        return re.sub(r"[^\n]", " ", m.group(0))

    text = re.sub(r"```.*?```", blank, text, flags=re.S)
    text = re.sub(r"`[^`\n]*`", blank, text)
    text = re.sub(r"^[ \t]*[|>].*$", blank, text, flags=re.M)
    return text


def units(text):
    """Yield (kind, block, line). List items are separate units per Rule 5.1.1.

    kind is "para", "step" (a numbered list item), or "item" (a bullet).
    Rule 6.3 defines a procedure as numbered steps, so only "step" is held to
    the 20-word procedural limit. A bullet is descriptive prose and gets 25.
    """
    marker = re.compile(r"^\s*([-*]|\d+\.)\s")
    lines = strip_exempt(text).split("\n")

    block, start = [], 0
    for idx, line in enumerate(lines + [""]):
        if line.strip():
            if not block:
                start = idx
            block.append(line)
            continue
        if block:
            yield from _classify(block, start, marker)
            block = []


def _classify(lines, start, marker):
    """Split one block into a lead paragraph and its list items.

    Markdown allows a list to follow its introducing sentence with no blank
    line. Treating that as one unit merges the intro with the first bullet and
    reports a sentence that does not exist.
    """
    head = lines[0].lstrip()
    if head.startswith("#") or head.startswith(">"):
        return

    first = next((i for i, l in enumerate(lines) if marker.match(l)), None)

    if first is None:
        yield "para", "\n".join(lines), start + 1
        return
    if first > 0:
        yield "para", "\n".join(lines[:first]), start + 1

    item, item_line = [], first
    for i in range(first, len(lines)):
        if marker.match(lines[i]) and item:
            yield _kind(item), "\n".join(item), start + item_line + 1
            item, item_line = [], i
        item.append(lines[i])
    if item:
        yield _kind(item), "\n".join(item), start + item_line + 1


def _kind(item_lines):
    """Rule 6.3: a procedure is numbered steps. A bullet is descriptive."""
    return "step" if re.match(r"^\s*\d+\.\s", item_lines[0]) else "item"


def normalize(s):
    """Collapse to prose. Rule 4.3: a code span counts as one word."""
    s = re.sub(r"^\s*(\*\*[\d.]+\*\*|[-*]|\d+\.|\[[ x]\])\s*", "", s)
    s = s.replace("\n", " ")
    s = re.sub(r"`[^`]*`", "X", s)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"https?://\S+", "X", s)
    return s.strip()


def sentences(s):
    """Split on sentence boundaries.

    A period ends a sentence only when the next token starts like one. This
    keeps "e.g. the staging cluster" and "Fig. 2" as single sentences, which
    otherwise inflate the 5.1 count and deflate the 4.1/4.2 measurement.
    """
    guard = s
    for i, abbr in enumerate(ABBREV):
        guard = guard.replace(abbr, f"\x00{i}\x00")
    # Emphasis markers are common at sentence start: "**Never** do X."
    parts = re.split(r"(?<=[.!?])\s+(?=[*_]{0,2}[A-Z(\[`\"'])", guard)
    out = []
    for p in parts:
        for i, abbr in enumerate(ABBREV):
            p = p.replace(f"\x00{i}\x00", abbr)
        if p.strip():
            out.append(p)
    return out


def check(path):
    try:
        with open(path, encoding="utf-8") as fh:
            raw = fh.read()
    except OSError as exc:
        return [f"{path}: cannot read: {exc}"]

    out = []

    for kind, block, line in units(raw):
        body = normalize(block)
        sents = sentences(body)

        if kind == "para" and len(sents) > MAX_PARA_SENTENCES:
            out.append(
                f"{path}:{line}: [5.1] paragraph has {len(sents)} sentences "
                f"(max {MAX_PARA_SENTENCES}): {body[:60]}..."
            )

        limit = MAX_PROCEDURAL if kind == "step" else MAX_DESCRIPTIVE
        rule = "4.1" if kind == "step" else "4.2"
        for sent in sents:
            n = len(sent.split())
            if n > limit:
                out.append(
                    f"{path}:{line}: [{rule}] sentence is {n} words "
                    f"(max {limit}): {sent[:70]}..."
                )

        # Only sentences after the first: 4.7 is about what a split leaves
        # behind, so an opening sentence has nothing to lean on.
        for sent in sents[1:]:
            s = sent.strip()
            if CONJUNCTION_OPEN.match(s):
                out.append(
                    f"{path}:{line}: [4.7] sentence opens with a coordinating "
                    f"conjunction; join it or rewrite: {s[:60]}..."
                )
            elif BARE_DEMONSTRATIVE.match(s):
                out.append(
                    f"{path}:{line}: [4.7] sentence opens with a bare "
                    f"demonstrative; name the referent: {s[:60]}..."
                )

    masked = mask_exempt(raw)
    low = masked.lower()
    for phrase in FILLER:
        for m in re.finditer(re.escape(phrase), low):
            line = raw.count("\n", 0, m.start()) + 1
            out.append(f"{path}:{line}: [10.5] filler: {phrase!r}")

    for bad, good in REPLACE.items():
        for m in re.finditer(r"\b" + re.escape(bad) + r"\b", low):
            line = raw.count("\n", 0, m.start()) + 1
            out.append(f"{path}:{line}: [B] {bad!r} -> {good!r}")

    # Rule 7.4: never combine AND and OR in one conditional
    for m in re.finditer(r"\bIF\b.{0,200}?\bTHEN\b", masked, re.S):
        seg = m.group(0)
        if re.search(r"\bAND\b", seg) and re.search(r"\bOR\b", seg):
            line = raw.count("\n", 0, m.start()) + 1
            out.append(
                f"{path}:{line}: [7.4] conditional mixes AND with OR; "
                "split it or use a decision table"
            )

    return out


def main(argv):
    if len(argv) < 2:
        print(__doc__.strip())
        return 2
    findings = []
    for path in argv[1:]:
        findings += check(path)
    for f in findings:
        print(f)
    if findings:
        print(f"\n{len(findings)} finding(s)")
        return 1
    print(f"clean: {len(argv) - 1} file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
