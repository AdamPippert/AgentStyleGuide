#!/usr/bin/env python3
"""Build the single-file deliverable from the repository sources.

The repository is canonical. Machines receive only dist/WRITING-STANDARD.md,
which sits beside CLAUDE.md and AGENTS.md in ~/Development.

Usage:  python3 tools/build-deliverable.py
Output: dist/WRITING-STANDARD.md
"""
import hashlib
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO_URL = "https://github.com/AdamPippert/AgentStyleGuide"

# Files the deliverable is built from. The stamp and the dirty check consider
# only these. Stamping HEAD instead would lag by one commit forever, because
# committing the built artifact changes HEAD.
INPUTS = [
    "STANDARD.md",
    "CHECKLIST.md",
    "tools/pointer-template.md",
    "tools/build-deliverable.py",
]

# The three files that ship to ~/Development on each machine. All three are
# generated. Hand-maintaining the pointer files meant a REPO_URL change reached
# only the standard, leaving the internal URL in the other two.
POINTERS = ["CLAUDE.md", "AGENTS.md"]


class BuildError(Exception):
    """The build cannot produce a trustworthy artifact."""


def git(*args, tolerate_failure=False):
    """Run git. Raise rather than degrade: an unstamped deliverable is worse
    than no deliverable, because it still looks distributable.

    tolerate_failure covers the one legitimate failure, a branch with no
    commits yet. A fresh orphan branch is exactly that, and the release
    pipeline builds on one before its first commit exists.
    """
    try:
        return subprocess.run(
            ["git", *args], cwd=ROOT, capture_output=True, text=True, check=True
        ).stdout.strip()
    except FileNotFoundError:
        raise BuildError("git is not on PATH; cannot stamp the deliverable")
    except subprocess.CalledProcessError as exc:
        if tolerate_failure:
            return ""
        raise BuildError(f"git {' '.join(args)} failed: {exc.stderr.strip()}")


def source_digest():
    """Content hash of the build inputs.

    Deliberately not a commit hash. On a squashed history the inputs and the
    built artifact share one commit, so stamping the commit can never settle:
    amending changes the hash the artifact is supposed to carry. A content
    digest is stable across squash, rebase, and re-homing, and a reader can
    recompute it from the files themselves.
    """
    h = hashlib.sha256()
    for name in INPUTS:
        path = ROOT / name
        if not path.exists():
            raise BuildError(f"build input missing: {name}")
        h.update(path.read_bytes())
    return h.hexdigest()[:12]


def source_date():
    """Author date of the last commit touching an input.

    Author date, not committer date: it survives --amend, so rebuilding after
    an amend produces identical bytes. Not today's date, which would make
    every rebuild dirty.
    """
    out = git("log", "-1", "--format=%as", "--", *INPUTS, tolerate_failure=True)
    return out or "uncommitted"


def inputs_dirty():
    """Uncommitted changes to build inputs only. dist/ churn is not a defect."""
    return git("status", "--porcelain", "--", *INPUTS, tolerate_failure=True)


def rewrite_links(text):
    """Point repo-relative links at the hosted repository."""
    text = re.sub(
        r"\[`(PROVENANCE|CHECKLIST|README|STANDARD)\.md`\]\(\./\1\.md\)",
        rf"[`\1.md`]({REPO_URL}/src/branch/main/\1.md)",
        text,
    )
    text = re.sub(
        r"\[`tools/lint\.py`\]\(\./tools/lint\.py\)",
        f"[`tools/lint.py`]({REPO_URL}/src/branch/main/tools/lint.py)",
        text,
    )
    return text


def strip_heading(text):
    """Drop the source file's H1 and its lead block; the deliverable adds its own."""
    parts = text.split("\n---\n", 1)
    return parts[1].lstrip("\n") if len(parts) == 2 else text


def checklist_body():
    raw = (ROOT / "CHECKLIST.md").read_text(encoding="utf-8")
    body = strip_heading(raw) if "\n---\n" in raw else raw
    body = re.sub(r"^# .*\n", "", body)
    # The linter does not ship with the deliverable.
    body = body.replace(
        "```sh\npython3 tools/lint.py path/to/doc.md\n```",
        f"The linter lives in the repository, not on this machine:\n"
        f"`{REPO_URL}` → `tools/lint.py`",
    )
    return rewrite_links(body).strip()


def provenance_summary():
    return f"""\
This standard derives from published sources. The full source register, with
licenses and a per-source account of what was taken, is in `PROVENANCE.md` in
the repository.

| Source | License | Contribution |
| --- | --- | --- |
| ASD-STE100 Simplified Technical English, Issue 9 | **Copyright ASD, Brussels** | Conceptual parent. No text reproduced. |
| DOE-STD-1029-92, *Writer's Guide for Technical Procedures* | US Gov **public domain** | Sections 6, 7, 9; Appendix A method |
| NASA SP-7084, *Grammar, Punctuation, and Capitalization* | US Gov **public domain** | Grammar tie-breaker (11.3) |
| Federal Plain Language Guidelines | US Gov **public domain** | 5.3, Appendix B |
| Google developer documentation style guide | **CC BY 4.0** | 5.6, 6.1, 11.1 |
| Diátaxis | attribution required | Appendix E |
| RFC 2119 / RFC 8174 / RFC 7322 | IETF, free | 11.2, 5.4 |
| Zambrini & Chiarello, MDTT 2025 | **CC BY 4.0** | Factual basis for Appendix D |

Portions informed by the Google developer documentation style guide, used under
CC BY 4.0. No text is copied verbatim.

**ASD-STE100 boundary.** ASD-STE100 is a copyright and trademark of ASD
(AeroSpace, Security and Defence Industries Association of Europe), Brussels.
This standard is not ASD-STE100, is not compliant with it, and is not endorsed
by ASD or STEMG. Never copy ASD-STE100 rule text or dictionary content into any
document governed by this standard. The official standard is free on request
from <https://www.asd-ste100.org/>."""


def main():
    standard = (ROOT / "STANDARD.md").read_text(encoding="utf-8")
    digest = source_digest()
    build_date = source_date()
    dirty = inputs_dirty()

    m = re.search(r"\*\*Version ([\d.]+)\.\*\*", standard)
    if not m:
        raise BuildError("no '**Version X.Y.**' found in STANDARD.md")
    version = m.group(1)

    header = f"""\
# Writing Standard

A controlled language for specifications and development documentation, for
human authors and agent authors. Applies to every project under `~/Development`.

> **Generated file — do not edit on this machine.**
> Version {version} · source digest `{digest}` · {build_date}{' · UNCOMMITTED' if dirty else ''}
> Source of truth: <{REPO_URL}>
> To change a rule: edit `STANDARD.md` in the repository, add its
> `PROVENANCE.md` entry in the same commit, rebuild, redistribute.

---

"""

    out = (
        header
        + rewrite_links(strip_heading(standard))
        + "\n\n---\n\n## Appendix F — Pre-commit checklist\n\n"
        + checklist_body()
        + "\n\n---\n\n## Appendix G — Provenance and licensing\n\n"
        + provenance_summary()
        + "\n"
    )

    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    target = dist / "WRITING-STANDARD.md"
    target.write_text(out, encoding="utf-8")

    template = (ROOT / "tools" / "pointer-template.md").read_text(encoding="utf-8")
    if "{{REPO_URL}}" not in template or "{{NAME}}" not in template:
        raise BuildError("pointer-template.md is missing a placeholder")
    for name in POINTERS:
        body = template.replace("{{NAME}}", name).replace("{{REPO_URL}}", REPO_URL)
        (dist / name).write_text(body, encoding="utf-8")

    print(f"built {target.relative_to(ROOT)} and {', '.join(POINTERS)}")
    print(f"  version {version}, digest {digest} ({build_date})"
          f"{' DIRTY' if dirty else ''}")
    print(f"  {len(out.splitlines())} lines, {len(out)} bytes")

    # The artifact is what ships, so the artifact is what gets checked.
    # Assembly can introduce defects the inputs never had.
    findings = lint_module().check(str(target))
    if findings:
        print(f"  FAIL: the assembled deliverable breaks its own standard "
              f"({len(findings)} finding(s)):")
        for f in findings[:10]:
            print(f"    {f}")
        return 1
    print("  self-check: deliverable conforms to its own standard")

    if dirty:
        print("  WARNING: build inputs have uncommitted changes.")
        print("  Commit them, rebuild, then distribute.")
        return 1
    return 0


def lint_module():
    """Import the sibling linter without requiring a package install."""
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "asg_lint", ROOT / "tools" / "lint.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BuildError as exc:
        print(f"build failed: {exc}", file=sys.stderr)
        sys.exit(2)
