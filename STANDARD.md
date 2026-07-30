# The Standard

A controlled language for specifications and development documentation, written
for human authors and agent authors alike.

**Version 2.1.** Cite rules by number, for example `STANDARD 7.4`.
Sources and licenses: [`PROVENANCE.md`](./PROVENANCE.md).

---

## 0. About

### 0.1 Who this binds

Sections 1 to 9 and 11 bind **every author, human or agent**. Section 10 binds
**agent authors only**, because it addresses failure modes humans do not have.

Humans should still read section 10. It tells you what to check in an agent's
output.

### 0.2 What it governs

In scope: specifications, design docs, RFCs, ADRs, READMEs, runbooks, operator
guides, API documentation, release notes, migration guides, and long-form
comments that explain a design.

Out of scope: code and its identifiers, commit messages, PR descriptions, review
comments, and conversational replies.

### 0.3 Lineage

Derived from ASD-STE100 Simplified Technical English, extended with procedure
rules from DOE-STD-1029-92, and extended again for agent authors. This standard
is not ASD-STE100, is not compliant with it, and is not endorsed by ASD.
See `PROVENANCE.md` §3.

---

## 1. Words

**1.1** Use one term for one concept, for the life of the document. Do not vary
wording for style.

**1.2** Do not use a word Appendix B lists as replaceable. Appendix B is the
observable form of this rule; "prefer the shortest word" is not checkable and
is not the standard.

**1.3** Two open vocabularies extend ordinary English:
- **Technical nouns** — things in the domain: `pod`, `mutex`, `webhook`, `WAL`.
- **Technical verbs** — operations in the domain. See Appendix A.

**1.4** A word may be approved in one sense and barred in another. `verify` is a
technical verb for cryptographic and test checks. It is not a substitute for
`make sure` in an instruction.

**1.5** Define an abbreviation on first use, then use it without variation. Do
not define an abbreviation you use once.

**1.6** No slang, no undefined jargon, no humor, no idiom. Idiom does not
survive translation or a non-native reader.

**1.7** Established software phrasal verbs are permitted and are technical
verbs: `roll back`, `fall back`, `back up`, `spin up`, `tear down`, `fail over`,
`opt in`, `time out`, `log in`, `shut down`, `set up`, `scale out`. Do not coin
new ones. Appendix C gives the spellings.

---

## 2. Nouns and noun phrases

**2.1** Use no more than three words in a noun cluster **that you construct**.
Break longer ones apart with prepositions and articles.

**2.2** An established proper name counts as one unit and is exempt from 2.1:
`Kubernetes horizontal pod autoscaler`, `OAuth 2.0 device authorization grant`.
Do not rewrite a product, protocol, or API name to shorten it.

**2.3** Keep the articles. Write `the request fails`, not `request fails`.

**2.4** Do not nominalize a working verb. Write `the service starts`, not
`startup of the service occurs`.

---

## 3. Verbs

**3.1** Use the active voice. Name the actor.

**3.2** Passive voice is permitted only when the actor is genuinely unknown,
genuinely irrelevant, or is an attacker. If you cannot name the actor, see 10.3.

**3.3** Permitted forms: infinitive, imperative, simple present, simple past,
simple future, past participle as an adjective.

**3.4** No past perfect. No continuous form as the main verb.

**3.5** Present perfect only where present relevance carries meaning the simple
past loses, typically a state check. `If the migration has already run, the
command exits.`

**3.6** The `-ing` form is permitted inside a technical noun (`rate limiting`,
`logging`) and as a noun subject (`Retrying costs one round trip.`). Never as
the main verb.

**3.7** Do not stack auxiliaries. Write `the job fails`, not `the job would end
up failing`.

---

## 4. Sentences

**4.1** Procedural sentence: **20 words maximum**.

**4.2** Descriptive sentence: **25 words maximum**.

**4.3** An identifier, path, flag, URL, or code span counts as **one word**.

**4.4** One instruction per sentence. Two actions means two sentences.

**4.5** Do not omit the subject, the verb, or the articles. Never write
telegraphically.

**4.6** Use a vertical list, not a sentence, for three or more items.

**4.7** The limits in 4.1 and 4.2 are diagnostics, not targets. A sentence you
split only to pass a limit must still stand alone. Do not open a new sentence
with a coordinating conjunction. Do not open one with a bare `This`, `That`,
`These`, or `Those`. For `it`, see 10.7.

---

## 5. Documents and structure

**5.1** Six sentences maximum per **prose paragraph**. One topic per paragraph.
Put the topic in the first sentence.

**5.1.1** The limit in 5.1 does not apply to a list. Count each list item
separately against 4.1 and 4.2.

**5.2** Use a table when the content has two or more dimensions. Do not narrate
a table in prose.

**5.3** Front-load. State the conclusion, requirement, or result first.

**5.4** Use the same section order for every document of the same kind. Appendix
E defines the kinds.

**5.5** Every heading is a noun phrase or an imperative. Not a question.

**5.6** Link text describes the destination. Never `click here`, never `this
link`, never a bare URL in prose.

---

## 6. Procedures and action steps

**6.1** Write each step as an imperative in the second person. `Set the flag to
true.`

**6.2** One step does one thing.

**6.3** Number steps when order matters. Use bullets when it does not.

**6.4** State the precondition before step 1 and the end state after the last
step.

**6.5** Begin each step with a verb from Appendix A. The verb is the contract.

**6.6** A vague verb is a defect unless followed by specifying information.
`Increase the timeout` is meaningless. `Increase the timeout to 30s` is not.

**6.7** Give the **acceptance criterion** for any step whose success is not
self-evident. State what the reader observes, not what they should feel.

> 3. Restart the controller.
>    **Verify:** `kubectl get pods -n argocd` reports `Running` within 60s.

**6.8** A cross-reference names the target and the return path. `Go to step 7`
is acceptable inside one procedure. `See the backup runbook` is not — name the
file and the section, and say whether the reader returns here.

---

## 7. Conditional logic

Adapted from DOE-STD-1029-92 §4. Ambiguous conditions cause more incidents than
any other documentation defect.

**7.1** State the condition first, the action second. Never invert.

**7.2** Write `IF`, `WHEN`, `THEN`, `AND`, `OR` in **uppercase**, each starting
a new line. Reserve that emphasis for logic keywords only.

> **IF** the token expired,
> **THEN** request a new token.

**7.3** Use `WHEN` for a condition that will occur, `IF` for one that may.

**7.4** **Never combine `AND` and `OR` in one conditional.** The precedence is
ambiguous to a reader. Split the statement or use a table.

> Do not write: **IF** A **OR** B **AND** C, **THEN** stop.

**7.5** At three or more conditions, use a decision table, not prose.

| Auth header | Token valid | Result |
| --- | --- | --- |
| absent | — | `401` |
| present | no | `403` |
| present | yes | request proceeds |

**7.6** Reserve uppercase `AND` and `OR` for joining **full clauses**. For a
compound subject or predicate, use lowercase. `IF the CPU and memory limits are
unset, THEN the pod uses the namespace default.`

**7.7** State the negative branch. If nothing happens when the condition is
false, say so.

---

## 8. Descriptive and reference text

**8.1** Describe what the system does, not what it was intended to do.

**8.2** Give the unit for every number: bytes, milliseconds, requests per
second. A bare number is a defect.

**8.3** Give the default for every configurable value, and say whether it can
change at runtime.

**8.4** State the failure behavior of anything you document: timeout, malformed
input, permission error.

---

## 9. Precautions, limitations, and warnings

DOE-STD-1029-92 separates these three. Conflating them is why warnings get
skipped.

**9.1** A **precaution** names a hazard and its consequence. It does not contain
an action.

**9.2** A **limitation** names a boundary that must not be crossed. `Do not run
this against a cluster with more than 500 nodes.`

**9.3** Precautions and limitations that apply to a whole document go at the
top. **Never put a user action there.** If the reader must act, write a
conditional step at the point of use (section 7).

**9.4** A **warning** attaches to one step and goes **immediately before** it.
Never after.

**9.5** Start a warning with the consequence or the condition. Not with
pleasantries.

**9.6** Warn on: data loss, irreversible migration, secret exposure, production
writes, bulk delete, and anything needing a restore to undo.

**9.7** Give the reversal for every destructive step, or state plainly that
there is none.

---

## 10. Rules for agent authors

Original to this standard. Sections 1 to 9 assume an author who knows what they
do not know. That assumption does not hold for a language model.

**10.1 Verify, do not recall.** Never state a version, flag, config key, path,
API signature, schema field, or default from memory. Read the source, run
`--help`, or query the data. **An unverified specific is a defect even when it
is right.**

**10.2 Mark epistemic status.** Separate what you observed from what you infer.
`Observed:` versus `Expected:`. Never present inference in the grammar of
observation.

**10.3 No confabulated actors.** If you cannot name the component that performs
an action, write `Unknown: which component performs X` and leave it visible. Do
not guess a plausible subject. Do not hide the gap in a passive.

**10.4 Every claim carries re-runnable evidence.** Give the check itself, as a
command a reader can run or a path they can open. Naming a check you did not
run looks exactly like running one. The artifact is what counts, never the
assertion.

> Not: benchmarked at 4ms.
> Yes: 4ms median, `hyperfine './x --bench'`, 2026-07-29.

**10.4.1** When the evidence and the claim disagree, state both. Give what you
observed and what you expected, separately. Never reconcile them silently.

**10.5 No hedging filler.** Delete: `it is worth noting`, `generally speaking`,
`in many cases`, `essentially`, `simply`, `just`, `of course`, `robust`,
`seamless`, `powerful`, `leverage`.

**10.6 No restatement.** Do not summarize a section at its end. Do not announce
a section at its start.

**10.7 Resolve every pronoun.** `This`, `it`, and `that` must have exactly one
possible antecedent in the previous sentence. Otherwise repeat the noun.

**10.8 No authoring narration.** A document describes the system, never the act
of writing it. Delete `I have updated`, `we will now add`, `as requested`.

**10.9 Scope discipline.** Document what exists. Mark planned work `Planned:` or
move it elsewhere.

**10.10 Stable ordering.** Keep existing section and list order when you edit.
Gratuitous reordering destroys the diff.

**10.11 Edit narrowly.** Apply this standard to text you write or change. Do not
rewrite untouched sections unless asked.


---

## 11. Exemptions and conflicts

### 11.1 Exempt from every rule above

Reproduce verbatim. Never restyle to fit:

- code blocks, inline code, identifiers
- command lines, flags, environment variable names
- file paths, URLs, log output, stack traces, error strings
- API field names, schema keys, JSON and YAML samples
- direct quotations from external specifications

### 11.2 Requirement keywords

Uppercase `MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT`, `MAY` are a closed set
with defined normative weight (RFC 2119, RFC 8174). They override 1.2 and
Appendix B.

- **Specifications, RFCs, ADRs:** keep them. Cite RFC 2119 near the top.
- **Guides, runbooks, READMEs:** do not use them. Use `must` and `can` in the
  imperative.

Never mix conventions in one document. Never use lowercase `may` or `should` in
a document that uses the uppercase keywords.

### 11.3 Conflict order

1. Correctness. A rule never justifies a false statement.
2. This standard.
3. `PROVENANCE.md` sources, for questions this standard does not answer.
4. NASA SP-7084 for grammar and punctuation edge cases.

### 11.4 When to deviate

Deviate when a rule would make the document **wrong** rather than merely longer:
a legal, cryptographic, or protocol term with no equivalent; an exact quotation.
Deviate deliberately. Never to save effort.

---

## Appendix A — Action verbs

Begin every action step with one of these. Each has **one meaning**. Where two
verbs look similar, the distinction is the point.

Extend this list for your project. Define every addition here before use.

### Checking

| Verb | Meaning in an action step |
| --- | --- |
| `check` | Compare against a stated requirement. Observation only; changes nothing. |
| `verify` | Confirm cryptographically or by executing a test. Produces a pass or fail. |
| `validate` | Confirm conformance to a schema or contract. |
| `make sure` | Bring about a state, by any means, and confirm it. Use in instructions to a human. |
| `inspect` | Read a resource's current state without asserting a requirement. |

### Lifecycle

| Verb | Meaning in an action step |
| --- | --- |
| `create` | Bring a resource into existence. |
| `provision` | Create and configure a resource so it is ready to serve. |
| `instantiate` | Create an in-memory instance from a definition. |
| `allocate` | Reserve a finite resource: memory, disk, an address. |
| `delete` | Remove permanently. Not recoverable without a restore. |
| `remove` | Detach from a set or collection. The object may still exist. |
| `evict` | Remove from a cache or scheduler under pressure. Expected, not exceptional. |
| `purge` | Delete in bulk, including metadata and history. |
| `prune` | Delete only what is unreferenced or expired. |

### Running and stopping

| Verb | Meaning in an action step |
| --- | --- |
| `start` | Begin execution of a process that was not running. |
| `stop` | End execution gracefully, allowing cleanup. |
| `cancel` | End a pending or in-flight operation before it completes. |
| `drain` | Stop accepting new work; let in-flight work finish. |
| `kill` | End execution immediately, without cleanup. State may be inconsistent. |
| `restart` | Stop, then start the same process. Loses in-memory state. |
| `reload` | Re-read configuration without ending the process. |
| `refresh` | Re-fetch data into an existing structure. |

### Change and release

| Verb | Meaning in an action step |
| --- | --- |
| `set` | Assign a specific value to a named field or flag. |
| `configure` | Set one or more values so a component behaves a stated way. |
| `update` | Change existing data in place. |
| `patch` | Apply a partial change to an existing object. |
| `upgrade` | Move to a later version. |
| `migrate` | Move data or schema between two defined states. |
| `deploy` | Place a build into a target environment. |
| `release` | Make a version available to its consumers. |
| `roll out` | Deploy progressively across instances. |
| `roll back` | Return to the previously known-good state. |
| `publish` | Make an artifact or event available to subscribers. |

### Data and transport

| Verb | Meaning in an action step |
| --- | --- |
| `read` | Retrieve from local or attached storage. |
| `fetch` | Retrieve from a remote source over a network. |
| `query` | Retrieve a filtered subset by an expression. |
| `write` | Persist to storage. |
| `serialize` | Convert an in-memory structure to a transmissible form. |
| `deserialize` | Reconstruct an in-memory structure from that form. |
| `encode` / `decode` | Change representation. No secrecy implied. |
| `encrypt` / `decrypt` | Change representation for secrecy, using a key. |
| `hash` | Produce a fixed-length digest. Not reversible. |
| `sign` | Produce a verifiable authenticity proof. |
| `sanitize` | Remove or neutralize dangerous input. |
| `escape` | Encode so a parser treats the value as data, not syntax. |
| `redact` | Remove sensitive values from output intended for others. |

### Access

| Verb | Meaning in an action step |
| --- | --- |
| `authenticate` | Establish who the caller is. |
| `authorize` | Establish what the caller may do. |
| `grant` / `revoke` | Add or withdraw a permission. |
| `rotate` | Replace a credential and retire the old one. |

### Failure handling

| Verb | Meaning in an action step |
| --- | --- |
| `retry` | Attempt the identical operation again. |
| `fall back` | Switch to a lesser alternative after a failure. |
| `fail over` | Switch to a standby instance. |
| `throttle` | Reduce rate deliberately. |
| `back off` | Increase the delay between retries. |
| `escalate` | Hand to a human or a higher tier. Name who. |

These are also permitted where unambiguous, without individual definition:

`build`, `compile`, `install`, `mount`, `unmount`, `parse`, `format`, `render`,
`route`, `schedule`, `subscribe`, `sync`, `trace`, `log`, `emit`, `merge`,
`sort`, `filter`, `index`, `lock`, `unlock`, `wait`, `watch`.

## Appendix B — Replacements

| Do not write | Write |
| --- | --- |
| verify / check / confirm / ensure *(ordinary sense)* | make sure |
| utilize / leverage | use |
| in order to | to |
| prior to | before |
| subsequent to / following | after |
| in the event that | if |
| is able to / has the ability to | can |
| perform an update of | update |
| terminate / abort *(ordinary sense)* | stop |
| initiate / commence | start |
| attempt to | try to |
| additional | more |
| approximately | about |
| assist | help |
| obtain / acquire | get |
| require | need |
| sufficient | enough |
| a number of / several | some, or the exact count |
| it is recommended that you | use the imperative |
| there is / there are | name the subject |
| allows you to | lets you |
| in terms of | *(delete and rewrite)* |
| functionality | *(name the function)* |
| robust / seamless / powerful | *(delete)* |

## Appendix C — Noun and verb spellings

The noun is closed, the verb is open. This distinction is load-bearing.

| Noun | Verb |
| --- | --- |
| a backup | to back up |
| a rollback | to roll back |
| a fallback | to fall back |
| a login | to log in |
| a logout | to log out |
| a setup | to set up |
| a timeout | to time out |
| a failover | to fail over |
| a shutdown | to shut down |
| a teardown | to tear down |
| a checkout | to check out |
| a lookup | to look up |
| a handoff | to hand off |

## Appendix D — Deviations from ASD-STE100

Why this is not STE. See `PROVENANCE.md` §3 for what we may not copy.

| # | ASD-STE100 | Here | Why |
| --- | --- | --- | --- |
| 1 | 875-word controlled dictionary | No closed dictionary; defined verbs in Appendix A | The aerospace dictionary lacks `deploy` and `serialize`. It also cannot be redistributed. |
| 2 | Phrasal verbs barred (Rule 9.3) | Established software phrasal verbs approved (1.7) | `roll back` and `fail over` **are** the terms. `revert` is less precise, not more. |
| 3 | Present perfect barred | Permitted for state relevance (3.5) | `has already run` states a precondition the simple past cannot. |
| 4 | `-ing` barred outside technical nouns | Permitted as gerund and noun subject (3.6) | `rate limiting` and `caching` are the domain's nouns. |
| 5 | Noun clusters ≤ 3 words | Constructed clusters only; proper names exempt (2.2) | `OAuth 2.0 device authorization grant` is a name. Shortening it makes it wrong. |
| 6 | `CAN` preferred over `MAY` | RFC 2119 overrides in specs (11.2) | `MAY` carries defined normative weight. |
| 7 | `make sure` replaces `verify` | Split by sense (1.4, Appendix A) | `verify a signature` is a cryptographic operation. |
| 8 | Word limits count every word | Identifiers count as one (4.3) | Otherwise one long path exhausts a 20-word budget. |
| 9 | Warnings framed for physical harm | Reframed for data and security loss (9.6) | Our irreversible operations are deletes, migrations, and secret exposure. |
| 10 | No epistemic or sourcing rules | Section 10 | ASD-STE100 assumes an author who knows what they do not know. |

## Appendix E — Document kinds

The four kinds follow the taxonomy Diátaxis identifies. The wording, the
columns, and the criteria below are original to this standard. A document that
mixes kinds serves none of them well.

| Kind | Serves | Voice | Never contains |
| --- | --- | --- | --- |
| **Tutorial** | A newcomer learning by doing | Imperative, second person | Options, alternatives, edge cases |
| **How-to / runbook** | A competent reader with a goal | Imperative, second person | Teaching, background theory |
| **Reference** | A reader looking something up | Declarative, third person | Instructions, opinions |
| **Explanation** | A reader seeking understanding | Declarative, discursive | Step-by-step instructions |

Specifications, RFCs, and ADRs are **reference** with an explanation section.
Keep the normative and rationale parts visibly separate.

Rule 5.4 means: every runbook shares one section order, every ADR shares
another.
