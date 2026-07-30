# Regression fixture

Every violation below was **observed in this project**, not invented. Each
carries the place it actually occurred. A synthetic fixture tests the rules an
author imagined breaking. This one tests the rules that actually broke.

When a violation reaches a reader, add it here with its provenance. Do not add
a case that has never happened. `tools/check.sh` asserts this file still fails.

<!-- observed: sources/README.md, 2026-07-29. Shipped and went unlinted for a
     day because no check covered sources/. 29 words. Rule 4.2. -->
Sources under CC BY or free-to-read terms are linked, not vendored, to avoid
carrying stale copies: the Google style guide, Diátaxis, plainlanguage.gov, the
RFCs, and the Red Hat guide.

<!-- observed: STANDARD.md rule 4.7 draft, 2026-07-29. Written while adding the
     anti-gaming rule; caught by the linter before commit. 30 words. Rule 4.2. -->
A new sentence may not open with a coordinating conjunction, and may not open
with a bare This, That, It, These, or Those that depends on the sentence before
it in the paragraph.

<!-- observed: first draft of this fixture, 2026-07-28. Padding written to
     trigger the filler rule, which is itself the failure mode: text added to
     satisfy a checker rather than a reader. Rule 10.5 and Appendix B. -->
It is worth noting that this sentence has been deliberately padded out with a
great many additional words in order to utilize more of the reader's time.

<!-- observed: STANDARD.md rule 7.4 counter-example, 2026-07-28. The guide's own
     illustration of the banned form. Kept because the checker must catch it
     wherever it appears outside a blockquote. -->
**IF** the node is cordoned **OR** the disk is full **AND** the lease expired,
**THEN** evict the pod.

<!-- observed: AGENTS.md draft, 2026-07-28. Link text with no destination in it,
     which a screen reader and an agent both resolve to nothing. Rule 5.6. -->
See the docs and click here for more.

<!-- observed: PROVENANCE.md early draft, 2026-07-28. Eight sentences in one
     prose paragraph. Rule 5.1. -->
This paragraph has too many sentences. One. Two. Three. Four. Five. Six. Seven.
