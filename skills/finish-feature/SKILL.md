---
name: finish-feature
description: Use when a feature in `[IN_PROGRESS]` has satisfied its feature-level acceptance bar and branch finalization must be gated on linked OpenSpec validation and archive state
---

# Finish Feature

## Overview

This skill is the workflow-owned preflight for moving a feature from `[IN_PROGRESS]` to `[DONE]` and finalizing its development branch.

It enforces a mandatory feature-level code review, then the acceptance-plus-OpenSpec validate/archive gate for the linked change after task execution is complete, then hands off to the generic `finishing-a-development-branch` skill as the final branch/worktree step owned by `finish-feature`.

`finish-feature` is intentionally strict: completing the final task is not enough on its own. The expected handoff is that `complete-task` leaves the feature in `[IN_PROGRESS]`, and only a feature whose top-level OpenSpec tasks are all done and whose `Current Task` is `none` is startable here.

## Defaults

- If the user names a feature ID, use it.
- Otherwise select the only finishable feature in `[IN_PROGRESS]`.

## Workflow

1. Run `audit-workflow`.
2. Resolve the target feature in `[IN_PROGRESS]`.
   - require all top-level OpenSpec tasks to be done and `Current Task` to be `none`
3. Read the linked feature file and confirm it records exactly one OpenSpec change.
3.5. Run a mandatory feature-level code review before any OpenSpec verification or archive work.
   - invoke `/code-review` at `medium` effort over the feature branch's cumulative diff against its base branch (the full feature changes, which `complete-task` has already committed). Do not pass `--comment`; this is a local pre-finalization gate, not a PR comment.
   - this review is additive: it does not replace the task-level reviews recorded during `complete-task`, and it must run even when every task already passed its own review.
   - if the review returns blocking findings, stop: do not run `openspec-verify-change` or archive, and do not move the feature to `[DONE]`. Keep the feature `[IN_PROGRESS]` and run the REMEDIATION ROUND below. Do not re-invoke this gate until every step of it has completed.
   - increment `Gate Iteration` in the feature file on every invocation of this step, so the loop can see its own length.
3.5.1. REMEDIATION ROUND — a first-class gated unit, not free-form commits.
   - A remediation round is NOT task execution and does NOT reopen a task. `Current Task` stays `none`. This is stated because the previous wording ("resolve the findings through normal task execution") named a `done -> ready` transition the Task Status Model does not define, so in practice remediation ran as raw commits with no gate of any kind. On `v1-f010` roughly half of the blocking findings across nine gates were introduced by a previous gate's own remediation.
   - **(a0) THE REVIEW'S OUTPUT CONTRACT — set it when INVOKING the review, not after.** Every review
     feeding a remediation round MUST be told: report EVERY finding you verified, each tagged with a
     confidence and a severity; do NOT filter by confidence; and for each, name the defect SHAPE and
     every other site it occurs at. Triage is the round's decision, not the reviewer's.
     - **A PROMPT ALONE DOES NOT ACHIEVE THIS — the AGENT is what filters, so change the agent.** The
       filtering is not a tendency to be talked out of, it is a written instruction in the reviewer's
       own definition: `feature-dev:code-reviewer`'s system prompt says "**Only report issues with
       confidence >= 80**" and "Focus on issues that truly matter - quality over quantity". A
       task-level "report everything" argues with the agent's own charter and will not reliably win.
       Point `(d)` at the built-in `code-review` skill instead, with this contract in the invocation
       text. It is a different component and it does NOT filter (see the next bullet), and measured
       head-to-head it honoured the contract from prompt text alone — it returned the accounting line
       and a `Considered and not raised` list without any agent-definition change.
       - **A purpose-built `remediation-reviewer` agent was built for this and then RETIRED. Do not
         rebuild it without new evidence.** Measured against the skill on `bt:v1-f047` `main...HEAD`,
         it returned 15 findings to the skill's 9 with only 4 overlapping — but **zero unique BLOCKING
         findings**: both reached the round's one blocker independently, so it never changed a verdict.
         Its unique contribution was non-blocking accuracy defects, on the hypothesis that those become
         later rounds. That hypothesis was never confirmed, and the cost was a second ~31-minute review
         per gate plus an unreviewed agent file to maintain. The defect that motivated it — the >= 80
         filter — turned out to live in `feature-dev:code-reviewer` and in the PR plugin, NOT in the
         component we were already using. Fix the agent you point at; do not add a second reviewer.
     - **Do NOT replace the built-in `code-review` skill on this reasoning — MEASURE FIRST.** It is a
       different component from the agent and it did NOT filter. Measured on `bt:v1-f047` gate 18: one
       `code-review` invocation returned **15 findings**, ranging down to `confidence ~55` and including
       latent/LOW items the round explicitly deferred. Meanwhile every `(d)` review that round, run
       through `feature-dev:code-reviewer`, stated its own bar verbatim — "below the 80-confidence bar
       for a formal finding, INCLUDED PER THE TASK'S EXPLICIT PROMPTS" and "(~65) ... hence below the
       reporting bar". Same feature, same prompts, opposite behaviour: the agent suppressed and the
       skill did not.
       - The official code-review PLUGIN (`/code-review`, for GitHub PRs) is a third component and DOES
         filter — its command file says "Filter out any issues with a score less than 80". Do not
         generalise from the plugin to the built-in skill; they are not the same code path.
       - The built-in skill's definition is not on disk (it ships inside the CLI binary, ~342MB, and is
         not extractable), so it CANNOT be forked faithfully. That is a reason to leave it alone, not a
         reason to reimplement it from observed behaviour: replacing a component you cannot read means
         silently dropping whatever it does that you never observed.
     - **Why the default is wrong HERE specifically, not wrong in general.** The >= 80 bar is sensible
       when a reviewer's output is read once by a human with limited attention. In a gated remediation
       loop the economics invert: a withheld finding is re-found by the next review and costs a full
       cycle, while a false positive costs a paragraph. Note the rubric those tools use defines **75**
       as "Highly confident ... very likely a real issue that will be hit in practice ... very important
       and will directly impact the code's functionality" — so the default discards findings it has
       itself verified as real and important.
     - **A filtered review is indistinguishable from a clean one**, which is why this is invisible until
       you count rounds. Measured on `bt:v1-f047`: reviewers stated the bar in their own output —
       "Non-blocking observations (below the 80-confidence bar for a formal finding, INCLUDED PER THE
       TASK'S EXPLICIT PROMPTS)" and "(~65) ... hence below the reporting bar". Those items reached the
       round only because that gate's prompt happened to ask for them; by default they are dropped, and
       the next gate re-finds them as a fresh round.
     - Do not write prompts that invite brevity here ("most-severe-first", "say so plainly if nothing
       blocks") without pairing them with the completeness requirement. Ranking is fine; truncating is
       not.
   - **(a) Catalogue.** Write `openspec/changes/<change-id>/remediation/gate-<n>.md` enumerating EVERY finding from that gate, blocking and non-blocking, each with: the finding, its attribution (original work, or introduced by an earlier round's fix), the intended fix, the proof obligation, and the validation class. Findings the round will not fix are listed with a reason. This file is the round's committed audit trail — without it, no later reviewer can tell whether a prescribed fix was ever implemented, and on `v1-f010` a fixture prescribed at gate 1 went unwritten for eight gates because nothing tracked it.
     - **The findings go in ONE fenced `yaml` block, parsed by a real parser.** Prose elsewhere in the
       catalogue is free-form; the linted schema is not:
       ```yaml
       findings:
         - id: F1
           title: what is wrong, in a line
           attribution: original work | gate-N fix
           guard: true                       # does the fix add or amend a test/assertion?
           class_sweep:
             shape: the defect SHAPE, not this instance
             command: grep -rn "pattern" paths     # the search you RAN; it is RE-RUN at (e)
             sites: ["a.py:12", "b.py:77"]         # every site the command found
           mutants:                          # required when guard: true
             revert: undo the behaviour the guard targets
             substitute: the most plausible WRONG implementation of it
           reconciliation:                   # filled in after (b); gates (e)
             - {site: "a.py:12", disposition: fixed}
             - {site: "b.py:77", disposition: deferred, reason: needs v1-b046 first, filed as v1-b049}
       ```
       For a genuinely single-site defect, replace `shape:` with `single_site: <why the shape cannot
       recur>` — but STILL declare the one site. `sites` is always required, because reconciliation is
       per site and a finding with none would escape it. On `bt:v1-f047` gate 14 declared its
       index-space defect single-site ("it's the T9 driver") and gate 15 found the identical defect in
       `null_driver.py`.
     - **Why YAML and not a markdown convention.** The first two versions of this lint hand-rolled a
       markdown parser and each shipped false PASSes — the failure mode worse than no gate, because it
       reports success. v1: a fenced schema EXAMPLE parsed as a real finding, so a copy-pasted template
       satisfied the no-empty-catalogue check, and the evidence test matched the WORD "grep" anywhere in
       the block. v2 fixed those and grew four more of the same class: a fence INSIDE a finding supplied
       every key, an unclosed fence swallowed all later findings, the command check accepted prose that
       merely STARTED with a tool word, and `- **Finding:**` / `1. Finding:` were still ignored silently.
       Every one is a PARSING defect. Patching them is unbounded — markdown has endless ways to write the
       same thing and each patch moves the evasion one level in. One tagged block and `yaml.safe_load`
       removes the second way to write it, which is the same remedy this feature reached for its own code.
   - **(a2) LINT THE CATALOGUE — this GATES (b).** Run
     `python "${AGENTS_HOME:-$HOME/.agents}/skills/_workflow/scripts/lint_remediation_round.py" openspec/changes/<change-id>/remediation/gate-<n>.md`.
     It checks FORM, and only what is decidable from the text: valid YAML in exactly one tagged block,
     no aliases or merge keys or duplicate keys (each finding must carry its OWN sweep and mutants),
     every required field present and not a placeholder, `guard` a boolean, `sites` non-empty, and
     `mutants` carrying a `revert:` and a distinct `substitute:` when `guard: true`. Do not implement
     - **A line-based sweep cannot see a claim that WRAPS.** `grep`/`rg` match within one line, so a
       contradiction split across two lines of prose — or a predicate split across two lines of code —
       is invisible to the command you recorded, and the sweep reports a clean result. Measured in this
       skill's own edit history: a line sweep for residual contradictions found two and missed a third
       that only a whitespace-normalised scan caught. When the swept artifact is PROSE, normalise
       whitespace first (`python3 -c "import re,sys;print(re.sub(r'\\s+',' ',open(sys.argv[1]).read()))"`
       piped to the pattern) or sweep with `rg -U`. Recording a command whose blind spot covers the
       claim is the sweep equivalent of a guard that cannot fail.
     until it is clean.
     - **What it deliberately does NOT check, and where that is checked instead.** Whether the command
       really ran, and whether a field is an unfilled template slot, are not decidable from a string —
       three mechanisms were tried for the first and two for the second, and each was unsound in both
       directions. Both are decided at (e0) by RUNNING the command. Read a green lint as "the catalogue
       is well-formed and complete", never as "the sweep is real".
     - Point it at the `remediation/` directory to lint every gate (`--glob` defaults to `gate-*.md`).
       `--allow-empty` opts out of the no-findings error; the default is to fail, because a gate that
       passes an empty catalogue is not a gate.
     - The lint has a negative-control corpus at
       `skills/_workflow/tests/remediation_round/run.sh` in the workflow-skills development repo. It is
       NOT installed with the skills, because it is only ever run when the lint itself is edited, and
       that happens in that repo. Run it after any change to the lint. It asserts four things, and each exists because an earlier version
       of the corpus lacked it: every negative fixture fails AND for its EXPECTED reason; every negative
       fixture HAS an expected reason (a fixture without one used to be checked for non-zero exit
       alone); every positive passes; and each tagged check DISCRIMINATES — with that one check
       disabled, its fixture must flip to PASS.
     - **Do not read a green corpus as "the lint is sound."** Three versions of this lint were reviewed
       and each shipped false PASSes: v1 three, v2 four, v3 eleven. The corpus is a regression net for
       defects already found, not evidence about the ones that have not been. The assurance in this
       workflow comes from (a0)'s review, not from this gate.   - **(a3) Snapshot the background — BEFORE implementing, WHEN the deliverable extends past the test suite.**
     `python "${AGENTS_HOME:-$HOME/.agents}/skills/_workflow/scripts/snapshot_round_state.py" <cmds.json>
     --repo <root> --state <state.json> --baseline`, re-checked at (c). It is the only gate covering the
     third failure class: a correct fix silently invalidating something elsewhere. On `bt:v1-f047`,
     gate 20's edit made §8's `checks run: 124` false and surfaced as gate 21 — a whole round spent on a
     change the previous round made and never looked at.
     - **Polarity, and why it is not redundant with (b).** (b) requires ONE designated check to MOVE;
       this requires EVERYTHING ELSE to stay still. Two sets that must be disjoint and jointly
       exhaustive — an observable in neither is unwatched, and that gap is where the next round's
       finding lives. They meet at the acknowledgements: (b)'s new test appears here as a delta and is
       acknowledged as that finding's fix-proof, so every acknowledged delta should map to a finding.
       One that maps to none is work the round did without deciding to.
     - **SKIP IT when the test suite is the whole story.** Snapshotting the suite adds only a removed or
       renamed test, and composition change inside a pre-existing failure set at constant tally.
       Everything else it would say, a red suite already says. The value is in the NON-suite commands —
       a numbers verifier, a doc-consistency checker, an artifact inventory. A code repo with strong
       tests and no prose deliverable should not run this; it buys ceremony.
     - Choose commands by enumerating what (c) already runs plus the readers of whatever the round
       edits — do not invent them. The set's coverage is testable by perturbation (edit a changed file,
       see whether any command moves), run WITH THE SUITE EXCLUDED, since perturbing any source file
       moves the suite and makes every surface look covered.
   - **(b) Implement — TEST FIRST, PER FINDING.** For each finding in turn: write the test or check that
     binds the defect, RUN IT, and record that it FAILED — against the working tree as it stands, with
     the previous findings already fixed. Then fix, and record that it passes. Not "write the tests for
     the round, then implement the round": per finding, so the only delta between the failing run and
     the passing run is that one fix.
     - **This is the PREFERRED instrument for the `revert:` question, not a replacement for it.** Both
       answer "does this test bind to the behaviour at all?", and the failing-first run answers it with
       better evidence: a revert mutant is a RECONSTRUCTION of the pre-fix state — prose the author
       wrote, applied by hand, by the party who wants the check to pass — while the failing-first run is
       the code. Sequencing per finding supplies the isolation the revert had.
       - **But it only earns that when the before-run is CHEAP and ASSERTION-SHAPED.** When it is not —
         the proof needs an artifact regeneration or a re-fit, or the thing being fixed does not exist
         yet so any check fails trivially — fall back to the `revert:` mutant at (c-ii) and say that is
         what ran. Do not run an expensive before-run for form's sake, and do not record a degenerate
         one as if it were evidence.
       - A script-enforced version of this (`fixed_when` declared per finding, baselined and re-checked
         by a gate) was built and REMOVED. Reasons, so it is not rebuilt on the same reasoning: checked
         against the six self-inflicted defects on `bt:v1-f047` it caught ONE; it costs 2N command runs
         per round with N unbounded by anything cheap; it degenerates on exactly the findings that most
         need it; and it is environment-coupled — the gate could not find `pytest` because the repo's
         interpreter is a conda env, so every declared command would have to name it. Keep the
         DISCIPLINE, which is free; do not build the GATE, which is not.
     - **It does NOT replace the `substitute:` mutant.** A failing-first run shows the test fails when
       the fix is absent. It says nothing about whether a plausible WRONG fix would pass too. Measured
       on `bt:v1-f047`, the gate-16 guard would have passed a failing-first run honestly and was still
       hollow: it bound to "a restricted band was computed", not to "fold k's band scored fold k".
     - **Where there is no test** — a stale number, a prose claim, a regenerated artifact — the same
       obligation lands as `fixed_when`: a command whose result is FALSE before and TRUE after, both
       runs recorded. A `fixed_when` that already passes before the fix proves nothing and is worse than
       none, because it converts unverified into verified.
     - **The before-run must fail on an ASSERTION, not on an ERROR.** An `ImportError`, `AttributeError`,
       `NameError` or collection error is not evidence the test binds to the defect — it is evidence the
       symbol was absent, which was going to be true of any test at all. Record the failure MODE, not
       just the red. This is the vacuous-failing-first shape and it is the same trap as a guard that
       watches a value being produced: the output is identical to the real thing.
     - **State it plainly when the before-run is weak rather than letting it read as strong.** If the
       pre-fix state cannot be run (the thing being fixed does not exist yet), the failing-first
       evidence is trivially satisfied; say so. If observing the failure is expensive, build the
       scoped-down reproduction and say that is what ran.
     - **SCOPE — do not oversell this step.** Failing-first is a LOCAL check on ONE fix, and every
       self-inflicted defect measured on `bt:v1-f047` was NON-local. Checked against the record: the
       gate-15 second caller (No — the sibling test passes throughout), the gate-16 hollow guard (No —
       it fails-before honestly and is still hollow; §12.2's exposing mutation kept the computation and
       dropped the USE, which is a substitute), gate 21's stale `checks run` (No — local fix, non-local
       breakage), gate 17's wrong verdict count (Yes, but via `fixed_when`), the non-discriminating
       fixtures (Partial). One clear catch and one partial out of six. This step is BETTER EVIDENCE than
       the revert mutant where it is cheap, and it retires nothing; the class sweep, the substitute
       mutant and the intent diff are what address repeat rounds. Do not treat a clean failing-first run
       as a round-quality signal.
   - **(c) Verify deterministically** before any reviewer is invoked: (a3)'s snapshot re-checked with `--check` and every delta acknowledged with a reason; the test suite; the mutation obligation below; `yaml.safe_load` over every changed YAML artifact; `openspec validate --strict`; and a live run of each changed tool including one negative case.
     - **The mutation obligation is TWO different checks. Do not conflate them — they ask different questions and need different scopes.**
     - **(c-i) Mutation TABLE — only where the repo has one.** Run it UNFILTERED and AFTER the final commit. It asks "which mutants survive the whole suite?", a coverage-quality question, so `-k` genuinely hides survivors; and the harness builds a worktree at HEAD, so uncommitted work is invisible. SKIPPED is not a pass. If the repo has no such harness, say so explicitly and record the substitution — do not silently drop the obligation, and do not claim the named artifact ran.
     - **(c-ii) Per-guard mutation check — ALWAYS, harness or not.** For every guard, assertion, or regression test this round ADDED or AMENDED: mutate the behaviour it targets and re-run its OWNING TEST FILE **unfiltered**. It asks a narrower question — "does this test bind to this behaviour, and is it load-bearing rather than redundant with a sibling?" — and file scope answers it in seconds where a whole-suite run costs minutes. Record which scope was used.
       - **Which mutants: `substitute:` always; `revert:` unless (b) already answered it.** The two bullets below say which, and why. ALWAYS governs the CHECK, not one particular mutant — every added guard faces at least one executed mutant, and a guard that faced none has not been checked whatever else ran.
       - Run the file, NOT `-k <testname>`. A `-k` run shows only that YOUR test fails; the file run also shows whether a sibling already caught it, which is the difference between "this test is necessary" and "this test is decoration".
       - A test that still passes when its target behaviour is removed — by (b)'s pre-fix run or by a hand-applied revert — is not a weak test, it is not a test. Fix it in the same round; do not carry it to the gate.
       - **The `substitute:` mutant must be executed and must fail.** It asks "does this test bind to the
         RIGHT behaviour, or would a plausible wrong implementation pass too?" A guard that fails when
         the behaviour is absent and survives a plausible wrong implementation is the dominant
         hollow-guard shape and is not fixed.
       - **The `revert:` mutant is still required WHEN (b)'s failing-first run was not available or was
         degenerate** — an expensive before-run, or one that could only fail trivially because the code
         did not exist yet. Where (b) DID record a cheap assertion-shaped failing run for this guard,
         that answers the revert question with better evidence and the hand-applied revert is
         redundant; record which one ran. What is never acceptable is neither.
       - Measured on `bt:v1-f047`: SEVEN guards across the feature could not discriminate, every one
         because the FIXTURE made the compared quantities equal — and several were written inside the
         round documenting that exact failure, so awareness did not prevent it. The worst passed its
         revert mutant honestly: reverting the behaviour failed the test, while substituting a
         `den`-weighted mean for a plain mean passed, because the fixture's weights summed equal. Only
         a substitute mutant exposes that, and it exposes it by making the bad fixture impossible.
       - Measured on `bt:v1-f047`: three separate tests passed against the very defect they were written for — a tautology asserting only Python arithmetic, a guard test that raised on a SIBLING guard and never reached its own branch, and an assertion that actively blessed the hole it was meant to close. All three were green, specific, and plausible. The per-guard mutation is what caught each one; nothing else did.
     - **(c-iii) Re-run the repo's own record/consistency checkers — WHEN THE ROUND ADDED, RENAMED, OR DELETED A NAMED ARTIFACT.** A named artifact is anything another file refers to BY NAME: a test named in an acceptance manifest, a scenario closer, a fixture, a script a task cites. The suite cannot see these — deleting a test that something names leaves a green suite and a dangling reference.
       - The situational trigger is the rename/delete, not the round. A round that only changes the body of an existing function has nothing to re-check here and should skip it.
       - Prefer the repo's checker to your own reasoning about what still resolves. Measured on `technical-strategy:v1-f007` gate 1: a remediation round deleted a test that an acceptance manifest named as a scenario closer. The suite passed, the unfiltered mutation table passed, `openspec validate --strict` passed, and the generic record-consistency script reported OK — because it compared the manifest's ROW COUNT against the scenario count, and both stayed 14. Only the repo's own closure checker, which resolves each closer to a definition, saw the dangling name. A count is adjacent to resolution and is not it.
   - **(c2) Lightweight pre-check — CONDITIONAL.** A cheap, timeboxed reviewer over THIS round's diff, before the full review in (d). Tell it explicitly NOT to run the test suite or the mutation table: (c) has already run them and (d) will again, and a lightweight pass that spends its budget re-running them is just a slow (d).
     - **Run it when this feature has ALREADY shown remediation injecting defects** — i.e. any finding in any earlier `remediation/*.md` for this feature carries an attribution to an earlier round's fix. Step (a) records that attribution per finding, so this is a lookup in files that already exist, not a judgment call.
     - **Do not run it otherwise.** On a feature whose remediation has been clean it is a second reviewer over the same diff at the same cost, and it adds a round to the very loop this section exists to keep short. The trigger is the point; an unconditional pre-check is not this rule.
     - **Point it at the seams THIS round created** — the specific assertions, slices, and fixtures the fixes introduced — not at a general review of the diff. The defect to hunt is the recurring one: a fix that is itself hollow.
     - **Its FINDINGS are evidence; its `approved` is NOT.** This is a screen, not a gate. A cheap timeboxed pass has low sensitivity by construction — it was told to skip the suite and the mutation table — so a clean result means "this screen found nothing", never "the round is sound". Concretely: a clean (c2) MUST NOT shorten, narrow, or skip (d); it MUST NOT be recorded as a `Review Verdict` or under `Review Scope: remediation_code`, which belong to (d) alone; and it MUST NOT be cited to a later gate as a review the round passed. The only thing a clean (c2) buys is that (d) starts on a diff with fewer known defects in it.
     - The asymmetry is the same one this workflow applies to SKIPPED mutations and to passing tests: a cheap check's positives are informative and its negatives are not. Treating a screen's silence as assurance is how a gate gets quietly downgraded to the cheapest thing that ran.
     - Measured on `v1-f010` (`biotech-catalyst`): two consecutive rounds each introduced a new defect INSIDE the very test written to close the previous finding — first a fixture that could not produce the label it asserted, then a legend slice that swept in a table containing the labels it searched for. Both were caught only by a full gate costing 20–37 minutes and a whole reviewer context. Both were reachable in about two minutes by a reviewer told where to look.

   - **(d) Code review the remediation diff ALONE** — not the cumulative branch diff — WHEN THE ROUND TOUCHED CODE. Use the built-in `code-review` skill with the (a0) contract in the invocation text — NOT `feature-dev:code-reviewer`; see (a0) for why the choice of agent, not the choice of prompt, is what determines whether findings are withheld. Record the verdict with canonical `Review Scope: remediation_code`, `Review Target: <feature-id>/gate-<n>` lines.
     - **SKIP (d) for a prose-only round.** Still record the entry with `Review Scope: remediation_code`, `Review Target: <feature-id>/gate-<n>`, `Blocking Findings: none`, and a Notes line naming the files changed and stating the round was prose-only — but OMIT the `Review Verdict` line entirely, because no review happened and there is no verdict to record.
     - Do NOT invent a verdict value for this. `Review Verdict` is enforced against `CANONICAL_REVIEW_VERDICTS` (`approved`, `changes_requested`, `blocked`) by `audit-workflow`'s `_unknown_review_verdicts`, so a value like `skipped_prose_only` fails the audit; and writing `approved` would claim a review that did not occur. Omitting the line satisfies both checks — verified against the real audit: the `Review Scope: remediation_code` line alone is what `_remediation_gaps` requires between two `feature_finish` gates, and it does not read that entry's verdict.
     - "Prose-only" means the diff changes no executable behaviour: `.md` files, comments, and docstrings. A changed test, script, or source statement is code, and (d) runs. Determine it by inspecting the diff, not by assuming.
     - Rationale, measured on `v1-f003` over 8 gates: 15 of 36 findings were introduced by a previous round's own fix, and the 7 remediation-diff reviews caught 1 of those 15. The other 14 were approved here and found by the NEXT feature gate. The step's recall against injected defects is low because the dominant injected defect in a mature feature is a CLAIM the fix invalidated — a comment, spec sentence, or task now contradicting the code — and a diff-scoped review sees the lines that changed, not the lines that should have. Spending a review pass on a diff with no code in it buys nothing.
     - What DOES catch injected defects, and stays mandatory: the unfiltered mutation sweep in (c). It caught two tests that could not fail, both introduced by the immediately preceding round.
   - **(e0) RECONCILE EVERY SWEPT SITE — this GATES the next round.** Run
     `python "${AGENTS_HOME:-$HOME/.agents}/skills/_workflow/scripts/reconcile_remediation_sites.py" openspec/changes/<change-id>/remediation/gate-<n>.md --repo . --since <the round's base commit>`.
     Every site the sweep declared must be `fixed`, `deferred` or `rejected`. `fixed` is checked against
     the round's diff; `deferred` and `rejected` need a reason, so dropping a site is a decision on the
     record rather than an omission. The command is also RE-RUN, and a sweep that finds files the
     catalogue never declared fails the gate.
     - **This is the check that actually stops round-multiplication.** The lint at (a2) makes the author
       WRITE the sweep; it cannot make the fix GO there. An unreconciled site is precisely what a
       catalogue looks like when someone fixes the reported instance and moves on — gates 10/11, 14/15
       and 19/20 on `bt:v1-f047` are each a pair this would have collapsed into one round.
     - **Why the command is executed rather than inspected.** Three attempts to decide "is this string a
       command?" from the string failed in both directions; the last rejected `rg -n "is None" src/`
       because `is` and `None` are English function words, in a tool that gates sweeps OF SOURCE CODE.
       An author's rational response to that is to edit the command until the linter accepts it — at
       which point the recorded command is no longer the command that ran, destroying the only property
       the field exists to preserve. Running it is decidable: prose does not execute, an unfilled
       `<pattern>` slot finds nothing, and an under-reported sweep is caught BEFORE the fix.
     - Execution is bounded: read-only search tools only, no shell, a timeout, cwd = repo root.
       `--no-run` skips execution and is a deliberate weakening — say so in the round's entry.
   - **(e) Report the loop's health, THEN re-invoke step 3.5.** Run
     `python "${AGENTS_HOME:-$HOME/.agents}/skills/_workflow/scripts/report_remediation_health.py" openspec/changes/<change-id>/remediation/`
     and put its summary line in the round's feature-file entry. It reads the `attribution` and
     `class_sweep` fields the catalogue already carries, so it costs nothing.
     - **The number to watch is SELF-INFLICTED RATE** — findings caused by an earlier round's fix. Above
       50% the loop is not converging, and the remedy is NOT a better review: it is slowing down on (b).
       Measured on `bt:v1-f047`, hand-counted after the fact: at least 14 of 23 rounds named a previous
       round's fix as their subject, ~6 defect classes spread over 23 rounds. That diagnosis was only
       available in hindsight; this makes it available during the loop.
     - **The leading indicator is SWEEPS FINDING MORE THAN ONE SITE.** Every extra site is a round that
       did not happen. On `v1-f047` it was structurally zero — no sweep existed — and gates 10/11, 14/15
       and 19/20 are each a pair a sweep would have collapsed into one round.
     - A high SINGLE-SITE rate is a smell, not a pass: it is the sweep's escape hatch, and gate 14 took
       it ("it's the T9 driver") one round before gate 15 found the same defect in a second caller.
   - if the remediation code review returns blocking findings, fix them and re-run (d). Do not carry them into the next feature gate.
   - record the feature-level review verdict in the feature file handoff notes using canonical `Review Scope`, `Review Target`, `Review Verdict`, `Blocking Findings`, and `Review Terminal` lines, with `Review Scope: feature_finish` and `Review Target` set to the feature ID, so downstream workflow can consume it without prose inference.
4. Run `openspec-verify-change` with the name of the openspec change to verify the change against the specs
5. Run the finish-feature resolver script to inspect active-vs-archived state for that change.
6. If the linked change is still active:
   - run `openspec-archive-change` for that exact change. This updates the main specs from the delta specs itself (`openspec archive`: "Archive a completed change and update main specs"), so there is no separate sync step to run first.
   - rerun the resolver script and confirm the active change directory is gone and exactly one archive directory now exists
   - move the feature from `[IN_PROGRESS]` to `[DONE]` only after acceptance plus archive succeed
7. If the linked change is already archived:
   - confirm no active change directory still exists
   - confirm exactly one matching archive directory exists
   - move the feature from `[IN_PROGRESS]` to `[DONE]` only after acceptance is confirmed
8. Record the archive result and feature-completion evidence in the feature file when that evidence is not already present. Archive paths are written in evidence and notes sections only. Do not modify the `OpenSpec Change` metadata field — it stays as the bare change id throughout the feature's lifecycle, including the `[DONE]` transition.
9. Re-run `audit-workflow` if the feature file changed.
10. Move the feature from `[IN_PROGRESS]` to `[DONE]` only after the linked change is validated and archived and feature-level acceptance is confirmed.
11. Only after the feature has been moved to `[DONE]`, invoke `finishing-a-development-branch`.

## Rules

- Do not call `finishing-a-development-branch` before the linked OpenSpec change is archived.
- A mandatory feature-level `/code-review` runs before OpenSpec verification and archive. Do not run OpenSpec verification or archive, and do not move the feature to `[DONE]`, while that review has unresolved blocking findings.
- A remediation round is itself gated: its catalogue, its deterministic verification, and — when the round touched code — a code review of its own diff all complete before the feature gate is re-invoked. Skipping the catalogue or the mutation sweep is a workflow violation, not a shortcut.
- A PROSE-ONLY remediation round skips the diff review and records a `remediation_code` entry with NO `Review Verdict` line. This is not a weakened gate: the round still catalogues, still runs the full suite and the unfiltered mutation sweep, and still faces the next feature gate over the cumulative diff. See step 3.5.1(d) for the measurement behind it.
- `finish-feature` owns the terminal feature transition and the handoff into generic branch finalization.
- This skill must run `openspec-archive-change` when the linked change is still active.
- Archive proof is filesystem state, not memory:
  - `openspec/changes/<change-id>/` must not exist
  - exactly one `openspec/changes/archive/*-<change-id>/` directory must exist
- The `OpenSpec Change` metadata field is the bare change id (for example `v1-f062-cli-typer-split-and-security-id-rename`). Never rewrite it to include an `archive/...` prefix, a date, or any other archive-derived path when moving the feature to `[DONE]`. The audit and resolver scripts treat that field as the lookup key and derive archive state from filesystem globs; rewriting it produces self-contradictory audit errors.
- If the feature is not in `[IN_PROGRESS]`, stop instead of trying to finish the branch early.
- A feature is not startable here unless all top-level OpenSpec tasks are done and `Current Task` is `none`.
- OpenSpec archive is additive. It does not replace task-level verification or feature-level acceptance.
- The feature-level code review is additive to the task-level reviews from `complete-task` and does not replace them.
- Keep the generic branch-finishing workflow generic; this skill owns the OpenSpec-specific gate.

## Stop Conditions

- Zero or multiple candidate finishable `[IN_PROGRESS]` features exist and no feature was named
- The target feature is not in `[IN_PROGRESS]`
- The feature file is missing `OpenSpec Change` metadata
- Top-level OpenSpec tasks are not all done
- `Current Task` is not `none`
- The mandatory feature-level code review reports unresolved blocking findings
- OpenSpec validation fails
- The archive result is ambiguous or missing
- `audit-workflow` reports an invalid workflow state
