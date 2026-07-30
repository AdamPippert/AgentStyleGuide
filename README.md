# AgentStyleGuide

Writing standards for specifications and development documentation, for human
authors and agent authors.

## Files

| File | Purpose |
| --- | --- |
| [`STANDARD.md`](./STANDARD.md) | The normative rules. Start here. |
| [`PROVENANCE.md`](./PROVENANCE.md) | Every source, its license, and what we took from it. |
| [`CHECKLIST.md`](./CHECKLIST.md) | Pre-commit checklist. |
| [`tools/lint.py`](./tools/lint.py) | Mechanical checks for the rules a script can enforce. |
| [`sources/`](./sources/) | Pinned public-domain sources, with checksums. |

## Quick start

Read `STANDARD.md` §0 to see whether your document is in scope. If it is:

```sh
python3 tools/lint.py path/to/your.md
```

The linter catches sentence length, paragraph length, banned filler, and mixed
`AND`/`OR` conditionals. It cannot catch the rules that matter most — sections 7
and 10 need judgment. Use `CHECKLIST.md` for those.

## Scope

**Governed:** specifications, design docs, RFCs, ADRs, READMEs, runbooks,
operator guides, API documentation, release notes, migration guides.

**Not governed:** code, commit messages, PR descriptions, review comments,
conversational replies.

## For agents

Section 10 of `STANDARD.md` binds you specifically. The two that matter most:

- **10.1** — never state a version, flag, path, or signature from memory.
  Verify it, or mark it unknown.
- **10.3** — if you cannot name the actor, write `Unknown:` and leave the gap
  visible. Do not invent a plausible subject.

## Changing the standard

Every rule needs a provenance entry. See `PROVENANCE.md` §5 for the process.
A rule with no entry is a defect.

## Sources

These tables give every source, its license, and what it contributed.
`PROVENANCE.md` records the derivation rule by rule.

### The parent, which we cannot redistribute

ASD-STE100 is the conceptual parent of this standard. It is free on request but
not redistributable, so no copy of it and no text from it appears here. Request
your own copy from ASD.

| Source | License | What it contributed |
| --- | --- | --- |
| [ASD-STE100 Simplified Technical English](https://www.asd-ste100.org/), Issue 9 (2025) | Copyright and trademark of ASD, Brussels | The controlled-language model: 53 rules in 9 sections, and a dictionary of 875 approved and about 1400 unapproved words |
| [Zambrini & Chiarello, *From Specification to Standard*](https://ceur-ws.org/Vol-3990/short24.pdf), MDTT 2025 | CC BY 4.0 | Our factual basis for Issue 9, written by two STEMG participants, including the rename of *technical name* to *technical noun* |

### Public domain, vendored in `sources/`

These two are committed to this repository because link rot is real.

| Source | License | What it contributed |
| --- | --- | --- |
| [DOE-STD-1029-92, *Writer's Guide for Technical Procedures*](https://www.osti.gov/biblio/308015), US Department of Energy | Public domain | The largest influence after ASD-STE100: conditional logic in section 7, action steps in section 6, and the precaution and limitation split in section 9 |
| [NASA SP-7084, *Grammar, Punctuation, and Capitalization*](https://ntrs.nasa.gov/citations/19900017394), NASA 1990 | Public domain | The tie-breaker for grammar questions this standard does not answer |

Verify them:

```sh
cd sources && shasum -a 256 -c SHA256SUMS
```

### Free to read, linked not vendored

| Source | License | What it contributed |
| --- | --- | --- |
| [Federal Plain Language Guidelines](https://www.plainlanguage.gov/guidelines/) | Public domain | Front-loading, and the word-choice discipline behind Appendix B |
| [Google developer documentation style guide](https://developers.google.com/style) | CC BY 4.0 | Code-sample handling, link text, second person for instructions. A [Vale implementation](https://github.com/vale-cli/Google) exists |
| [Diátaxis](https://diataxis.fr/) | CC BY-SA 4.0 | The four document kinds in Appendix E |
| [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) and [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174) | IETF, free | Requirement keywords, and the rule that only uppercase carries normative weight |
| [RFC 7322](https://www.rfc-editor.org/rfc/rfc7322.txt) | IETF, free | Section ordering for specifications |
| [Red Hat supplementary style guide](https://redhat-documentation.github.io/supplementary-style-guide/) | CC BY-SA 4.0 | Consulted for alignment with Ansible and OpenShift documentation |

## Licensing

This repository is dual-licensed, because documentation and code want different
instruments.

| What | Licence |
| --- | --- |
| Documentation: `STANDARD.md`, `PROVENANCE.md`, `CHECKLIST.md`, `README.md`, `dist/` | [CC BY 4.0](./LICENSE-docs) |
| Code: `tools/`, `.github/` | [Apache-2.0](./LICENSE) |
| `sources/*.pdf` | US Government public domain, covered by neither |

Diátaxis and the Red Hat supplementary style guide are both CC BY-SA 4.0.
Neither contributed protected expression to this repository, so ShareAlike does
not reach it. `PROVENANCE.md` §4a records that analysis.

This repository is original work. It derives concepts from ASD-STE100
Simplified Technical English but copies no text from it and is not endorsed by
ASD. Public-domain and CC BY sources are listed in `PROVENANCE.md` with
attribution. Read `PROVENANCE.md` §3 before quoting any external standard here.

Portions informed by the Google developer documentation style guide, used under
CC BY 4.0.
