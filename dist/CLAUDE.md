# CLAUDE.md — Development root

Applies to every project under this directory. A project's own `CLAUDE.md`
overrides this file.

## Documentation standard

Write specifications and development documentation to the standard in
[`WRITING-STANDARD.md`](./WRITING-STANDARD.md), beside this file.

**Read it before you write or revise a governed document.** Cite rules by
number, for example `STANDARD 7.4`.

`WRITING-STANDARD.md` is a generated file. Do not edit it here. It is built
from the AgentStyleGuide repository, which holds the source, the provenance
register, the pinned sources, and the linter:

<https://github.com/AdamPippert/AgentStyleGuide>

### In scope

Specifications, design docs, RFCs, ADRs, READMEs, runbooks, operator guides, API
documentation, release notes, migration guides, and long-form comments that
explain a design.

### Out of scope

Code and its identifiers, commit messages, PR descriptions, review comments, and
conversational replies. Code, paths, log output, and quoted third-party text
inside a governed document are reproduced verbatim.

### The core rules

- Procedural sentence: 20 words maximum. Descriptive: 25. An identifier counts
  as one word.
- Prose paragraph: 6 sentences maximum, one topic. Lists are exempt.
- Active voice. Name the actor.
- No past perfect, no continuous main verbs. Present perfect only for state
  relevance.
- Constructed noun clusters: 3 words maximum. Proper names are exempt.
- One instruction per sentence. Every step starts with an Appendix A verb.
- Conditionals: `IF` / `WHEN` / `THEN` uppercase, each on a new line, condition
  first. **Never mix `AND` and `OR` in one conditional.** Use a decision table
  at three or more conditions.
- Warnings precede their step. State the reversal, or state there is none.
- One term per concept. Keep the articles.

Prefer the plain word: `use` not `utilize`, `make sure` not `verify`, `to` not
`in order to`, `before` not `prior to`, `can` not `is able to`.

### Section 10 binds you specifically

- **10.1** Never state a version, flag, path, key, or signature from memory.
  Verify it, or mark it unknown. An unverified specific is a defect even when
  it is right.
- **10.2** Mark what you observed apart from what you infer.
- **10.3** Never invent an actor. Write `Unknown:` and leave the gap visible.
- **10.4** Every claim carries the check that would falsify it.
- **10.5–10.8** No filler, no restatement, no unresolvable pronouns, no
  narration of your own editing.
- **10.11** Apply the standard to text you change. Do not rewrite untouched
  sections.

Appendix F is the pre-commit checklist. Work through it before you finish.

### Requirement keywords

Keep RFC 2119 keywords (`MUST`, `SHOULD`, `MAY`) in specifications and RFCs.
Drop them in guides and runbooks; use `must` and `can` in the imperative. State
the convention near the top. Never mix both in one document.

### Changing the standard

Do not edit `WRITING-STANDARD.md` on this machine. Changes are made in the
repository: edit `STANDARD.md`, add the `PROVENANCE.md` entry in the same
commit, rebuild with `tools/build-deliverable.py`, then redistribute.

Never commit ASD-STE100 rule text or dictionary content anywhere. See Appendix G
for the boundary.
