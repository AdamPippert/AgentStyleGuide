# Checklist

Run before you commit a governed document. Rule numbers refer to
[`STANDARD.md`](./STANDARD.md).

## Mechanical — run the linter

```sh
python3 tools/lint.py path/to/doc.md
```

Covers 4.1, 4.2, 5.1, 7.4, 10.5, and part of Appendix B. A clean run means only
that the countable rules pass.

## Judgment — no script can do these

### Accuracy

- [ ] **10.1** Every version, flag, path, config key, and signature was read
      from the source, not recalled.
- [ ] **10.2** Observation and inference are marked apart.
- [ ] **10.3** No invented actors. Gaps are visible as `Unknown:`.
- [ ] **10.4** Every performance, behavior, and compatibility claim carries its
      check.
- [ ] **8.2** Every number has a unit.
- [ ] **8.3** Every setting has a default, and its runtime mutability is stated.
- [ ] **8.4** Failure behavior is documented.

### Structure

- [ ] **5.4 / Appendix E** The document is one kind, not a blend.
- [ ] **5.3** The conclusion is first.
- [ ] **11.2** One requirement-keyword convention, stated near the top.

### Procedures

- [ ] **6.5** Every step begins with an Appendix A verb.
- [ ] **6.6** No vague verb without specifying information.
- [ ] **6.7** Steps carry acceptance criteria where success is not obvious.
- [ ] **6.8** Cross-references name the target and the return path.

### Conditionals

- [ ] **7.1** Condition precedes action.
- [ ] **7.2** Logic keywords are uppercase, each on its own line.
- [ ] **7.5** Three or more conditions use a decision table.
- [ ] **7.7** The negative branch is stated.

### Safety

- [ ] **9.1 / 9.2** Precautions and limitations are not conflated.
- [ ] **9.3** No user actions in the precautions section.
- [ ] **9.4** Warnings precede their step.
- [ ] **9.7** Every destructive step states its reversal, or states there is
      none.

### Language

- [ ] **1.1** One term per concept throughout.
- [ ] **3.1** Active voice; the actor is named.
- [ ] **10.7** No `this`, `it`, or `that` with an ambiguous antecedent.
- [ ] **10.6 / 10.8** No restatement, no authoring narration.
- [ ] **11.1** Code, paths, and output are verbatim.

### Diff hygiene

- [ ] **10.10** Existing section order preserved.
- [ ] **10.11** Only the intended sections changed.

## If you changed the standard

- [ ] `PROVENANCE.md` updated in the same commit (§5).
- [ ] Appendix D updated if the change departs from ASD-STE100.
- [ ] `python3 tools/lint.py STANDARD.md PROVENANCE.md README.md` is clean.
- [ ] `python3 tools/lint.py tools/testdata/bad.md` still reports findings.
