# Provenance

Every rule in `STANDARD.md` traces to a source in this file, or is marked
**original**. This file records what each source is, what license governs it,
what we took, and what we deliberately rejected.

Read this before you change `STANDARD.md`. A rule with no provenance entry is a
defect.

---

## 1. Source register

| # | Source | Publisher | Date | License | Obtained | Local copy |
| --- | --- | --- | --- | --- | --- | --- |
| S1 | ASD-STE100 Simplified Technical English, Issue 9 | ASD, Brussels | 2025-01-15 | **Copyright, all rights reserved** | Not obtained — see §3 | None. Cannot redistribute |
| S2 | DOE-STD-1029-92 CN1, *Writer's Guide for Technical Procedures* | US Dept. of Energy | 1992-12, CN1 1998-12 | **US Gov public domain**, "Distribution Statement A — approved for public release; distribution is unlimited" | [OSTI 308015](https://www.osti.gov/biblio/308015) | `sources/DOE-STD-1029-92.pdf` |
| S3 | NASA SP-7084, *Grammar, Punctuation, and Capitalization* | NASA (McCaskill) | 1990 | **US Gov public domain** | [NTRS 19900017394](https://ntrs.nasa.gov/citations/19900017394) | `sources/NASA-SP-7084.pdf` |
| S4 | Federal Plain Language Guidelines | US Plain Language Action and Information Network | rev. 2011 | **US Gov public domain** | <https://www.plainlanguage.gov/guidelines/> | Link only |
| S5 | Google developer documentation style guide | Google | current | **CC BY 4.0** (code: Apache 2.0) | <https://developers.google.com/style> | Link only |
| S6 | Diátaxis documentation framework | Daniele Procida | current | **CC BY-SA 4.0** | <https://diataxis.fr/> | Link only |
| S7 | RFC 2119 / RFC 8174 — requirement keywords | IETF | 1997 / 2017 | IETF Trust, free | <https://www.rfc-editor.org/rfc/rfc2119> | Link only |
| S8 | RFC 7322 — RFC Style Guide | IETF | 2014 | IETF Trust, free | <https://www.rfc-editor.org/rfc/rfc7322.txt> | Link only |
| S9 | Zambrini & Chiarello, *From Specification to Standard: A Meta-Terminological Evolution in ASD-STE100 Issue 9*, MDTT 2025 | CEUR-WS Vol-3990 | 2025 | **CC BY 4.0** | <https://ceur-ws.org/Vol-3990/short24.pdf> | Link only |
| S10 | Red Hat supplementary style guide | Red Hat | current | **CC BY-SA 4.0** | <https://redhat-documentation.github.io/supplementary-style-guide/> | Link only |

Verify the local copies:

```sh
cd sources && shasum -a 256 -c SHA256SUMS
```

Re-fetch them with `sources/fetch-sources.sh`.

---

## 2. What we took, per source

### S2 — DOE-STD-1029-92 (public domain)

The heaviest single influence after S1. It is a procedure-writing standard from
a domain where an ambiguous instruction injures somebody.

| Taken | Where it lands |
| --- | --- |
| `IF` / `THEN` / `WHEN` as emphasized keywords on their own lines | 7.1, 7.2 |
| Condition stated before action | 7.1 |
| Never mix `AND` and `OR` in one conditional — precedence is ambiguous | 7.4 |
| Use a decision table at three or more conditions | 7.5 |
| Reserve emphasized `AND`/`OR` for full clauses; use plain conjunctions for compound subjects | 7.6 |
| Action verb list, each verb defined *as used in an action step* | Appendix A |
| A vague verb is a defect unless followed by specifying information | 6.6 |
| Precautions (hazards) separated from limitations (boundaries) | 9.1, 9.2 |
| No user actions inside a precautions section | 9.3 |
| Acceptance criteria on action steps | 6.7 |
| Branching and referencing rules | 6.8 |
| Site-specific verb lists are expected and encouraged | Appendix A preamble |

Rejected: placekeeping and sign-off columns (§4.13). They assume a paper
procedure executed under supervision. Our equivalent is a checklist in the PR.

Verb definitions in Appendix A are **adapted, not copied**. The DOE list is
public domain, so verbatim reuse would be lawful; we rewrote for software
because the DOE senses are mechanical (`Bleed`, `Bolt`, `Barricade`).

### S3 — NASA SP-7084 (public domain)

Held as the tie-breaker reference for grammar, punctuation, and capitalization
questions the standard does not answer. No rule is derived from it yet.

### S4 — Federal Plain Language Guidelines (public domain)

| Taken | Where |
| --- | --- |
| Front-load the conclusion | 5.3 |
| Write for the reader who is in a hurry and under stress | Rationale for §4, §5 |
| Plain-word substitution discipline | Appendix B |

### S5 — Google developer documentation style guide (CC BY 4.0)

| Taken | Where |
| --- | --- |
| Code samples and identifiers are reproduced verbatim, never restyled | 11.1 |
| Second person and imperative for instructions | 6.1 |
| Descriptive link text; never "click here" | 5.6 |

Attribution: portions informed by the Google developer documentation style
guide, used under CC BY 4.0. No text is copied verbatim.

Not adopted: its house conventions on capitalization and product naming, which
conflict with S3 and with our own identifiers.

### S6 — Diátaxis (CC BY-SA 4.0)

| Taken | Where |
| --- | --- |
| The four-part taxonomy, and the names of the four kinds | Appendix E |
| The proposition that a document mixing kinds serves none of them | Appendix E |

Appendix E supplies the document kinds that rule 5.4 depends on.

**No expression was taken.** Diátaxis is licensed CC BY-SA 4.0, so this
distinction decides whether ShareAlike reaches this repository. Appendix E uses
a taxonomy and a proposition. US copyright law places both outside protection,
as a system and as an idea (17 U.S.C. §102(b)). No sentence, phrase, or
definition is copied. The table's columns, criteria, and wording are original.

ShareAlike attaches to Adapted Material, which CC BY-SA 4.0 §1(a) defines as
material modified in a manner requiring permission under copyright. Using an
unprotectable taxonomy requires no permission. This repository is therefore
not Adapted Material, and is not obliged to adopt CC BY-SA.

Attribution is given because credit is owed, not because a licence compels it.
**Paste Diátaxis wording into Appendix E and this analysis stops holding.** The
whole guide would then have to become CC BY-SA 4.0. Do not do it.

### S7 — RFC 2119 / RFC 8174

Requirement keywords and their normative weight. Lands in 11.3. RFC 8174 adds
that only uppercase keywords carry the defined meaning — that is why 11.3 bars
lowercase `may` in a document using the keywords.

### S8 — RFC 7322

Section-ordering conventions for specifications. Informs 5.4.

### S9 — Zambrini & Chiarello (CC BY 4.0)

Our factual basis for what ASD-STE100 Issue 9 actually contains, written by two
STEMG participants. It is the source for:

- 53 rules in 9 sections
- 875 approved and about 1400 unapproved dictionary entries
- the Issue 9 rename of *technical name* to *technical noun*
- rule anchors 1.5, 1.10, 1.12, and 9.3
- the phrasal-verb prohibition we reverse in Appendix D #2

### S10 — Red Hat supplementary style guide (CC BY-SA 4.0)

Consulted for alignment with Ansible and OpenShift documentation conventions.
**Nothing is derived from it.** No rule, no wording, and no example in this
repository comes from it.

It is also CC BY-SA 4.0, so the same test applies as for S6. Reading a work
creates no licence obligation; only using its protected expression does. This
entry records that it was read. Should a rule ever derive from it, record what
was taken here and re-run the licence analysis in §6 before publishing.

---

## 3. ASD-STE100 and what we may not do

ASD-STE100 is a copyright and trademark of **ASD (AeroSpace, Security and
Defence Industries Association of Europe), Brussels**. It is the conceptual
parent of this standard.

**We do not hold a copy.** Issue 9 is distributed free of charge on request from
<https://www.asd-ste100.org/>, under terms that do not permit redistribution.
The only public copy of Issue 7 we located is an AES-encrypted PDF; we did not
circumvent it.

Therefore:

- **Never** copy rule text, explanatory text, or examples from ASD-STE100 into
  this repository.
- **Never** reproduce any part of the controlled dictionary. It is the
  commercial core of the standard.
- **Never** describe this standard as STE-compliant, STE-certified, or endorsed
  by ASD or STEMG. It is none of those.
- Restating a widely documented *principle* in original words is fine. Copying
  the sentence that states it is not.

Everything this repository says about ASD-STE100 derives from S9 and from public
secondary descriptions, not from the standard itself. Appendix D of
`STANDARD.md` lists every point where we deliberately depart from it.

If you get an official copy, check Appendix D against it and correct this
repository where it is wrong.

---

## 4. Original material

These carry no external provenance. They exist because the sources above assume
a human author who knows the limits of their own knowledge.

| Rule | Subject |
| --- | --- |
| 10.1 | Verify, do not recall |
| 10.2 | Mark epistemic status |
| 10.3 | No confabulated actors |
| 10.4 | Every claim carries its check |
| 10.5–10.12 | Filler, restatement, anaphora, narration, scope, ordering, edit width, length |
| 2.2 | Proper-name exemption from noun-cluster limits |
| 4.3 | Identifiers count as one word |
| 11.1 | The verbatim-content exemption list |

Rules 10.1, 10.2, and 10.4 restate working principles from the operator's global
agent instructions. They are original to this project, not to any standard.

---

## 4a. Licensing

This repository is dual-licensed, because documentation and code want different
instruments.

| What | Licence | File |
| --- | --- | --- |
| Documentation: `STANDARD.md`, `PROVENANCE.md`, `CHECKLIST.md`, `README.md`, `dist/` | **CC BY 4.0** | `LICENSE-docs` |
| Code: `tools/*.py`, `tools/*.sh`, `.github/` | **Apache-2.0** | `LICENSE` |
| `sources/*.pdf` | **US Government public domain**, covered by neither | `sources/README.md` |

Creative Commons advises against applying its licences to software, and
Apache-2.0 carries a patent grant that CC does not. Google splits its own style
guide the same way.

**Why not CC BY-SA.** Two sources are CC BY-SA 4.0: Diátaxis (S6) and the Red
Hat supplementary style guide (S10). Neither contributed protected expression,
so neither triggers ShareAlike. §2 records the analysis for each. Both remain
attributed.

**Obligations we do carry.** Google's style guide (S5) and the Zambrini &
Chiarello paper (S9) are CC BY 4.0, which requires attribution. Both are
credited in §2, in `README.md`, and in Appendix G of the deliverable. Keep them
there.

---

## 5. Changing the standard

1. Find or add the source. An original rule is allowed; say so explicitly.
2. Add the row to §2 or §4 of this file **in the same commit** as the rule.
3. If the rule departs from ASD-STE100, add a row to Appendix D with the reason.
4. Re-run the checker in `CHECKLIST.md` against the standard itself.
