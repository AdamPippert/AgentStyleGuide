# Pinned sources

Local copies of the sources this standard derives from, where the license
permits redistribution. See [`../PROVENANCE.md`](../PROVENANCE.md) for what was
taken from each.

## What is here

| File | Source | License |
| --- | --- | --- |
| `DOE-STD-1029-92.pdf` | US Dept. of Energy, *Writer's Guide for Technical Procedures*, 1992 (CN1 1998) | **Public domain.** "Distribution Statement A — approved for public release; distribution is unlimited." |
| `NASA-SP-7084.pdf` | NASA, *Grammar, Punctuation, and Capitalization*, 1990 | **Public domain.** US Government work. |

Both are US Government works in the public domain. They are committed here
because link rot is real: the 18F Content Guide went offline when 18F was shut
down, taking a source with it.

## What is not here, and why

**ASD-STE100** is copyright ASD, Brussels, and must never be committed to this
repository in any form. Read `PROVENANCE.md` §3 before adding anything.

These are linked, not vendored, so we do not carry stale copies:

- the Google developer documentation style guide
- Diátaxis
- plainlanguage.gov
- the RFCs
- the Red Hat supplementary style guide

## Verify

```sh
shasum -a 256 -c SHA256SUMS
```

## Re-fetch

```sh
./fetch-sources.sh
```

The script downloads to a temporary directory and compares checksums against
`SHA256SUMS`. It never overwrites a pinned file. If a checksum differs, the
upstream document changed — read the new version, update `PROVENANCE.md`, then
repin deliberately.
