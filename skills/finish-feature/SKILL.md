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
   - **(a) Catalogue.** Write `openspec/changes/<change-id>/remediation/gate-<n>.md` enumerating EVERY finding from that gate, blocking and non-blocking, each with: the finding, its attribution (original work, or introduced by an earlier round's fix), the intended fix, the proof obligation, and the validation class. Findings the round will not fix are listed with a reason. This file is the round's committed audit trail — without it, no later reviewer can tell whether a prescribed fix was ever implemented, and on `v1-f010` a fixture prescribed at gate 1 went unwritten for eight gates because nothing tracked it.
   - **(b) Implement.**
   - **(c) Verify deterministically** before any reviewer is invoked: the test suite; the mutation table run UNFILTERED and AFTER the final commit (`-k` cannot show a survivor outside its filter, and the harness builds a worktree at HEAD so uncommitted work is invisible — SKIPPED is not a pass); `yaml.safe_load` over every changed YAML artifact; `openspec validate --strict`; and a live run of each changed tool including one negative case.
   - **(d) Code review the remediation diff ALONE** — not the cumulative branch diff — WHEN THE ROUND TOUCHED CODE. Record the verdict with canonical `Review Scope: remediation_code`, `Review Target: <feature-id>/gate-<n>` lines.
     - **SKIP (d) for a prose-only round.** Still record the entry with `Review Scope: remediation_code`, `Review Target: <feature-id>/gate-<n>`, `Blocking Findings: none`, and a Notes line naming the files changed and stating the round was prose-only — but OMIT the `Review Verdict` line entirely, because no review happened and there is no verdict to record.
     - Do NOT invent a verdict value for this. `Review Verdict` is enforced against `CANONICAL_REVIEW_VERDICTS` (`approved`, `changes_requested`, `blocked`) by `audit-workflow`'s `_unknown_review_verdicts`, so a value like `skipped_prose_only` fails the audit; and writing `approved` would claim a review that did not occur. Omitting the line satisfies both checks — verified against the real audit: the `Review Scope: remediation_code` line alone is what `_remediation_gaps` requires between two `feature_finish` gates, and it does not read that entry's verdict.
     - "Prose-only" means the diff changes no executable behaviour: `.md` files, comments, and docstrings. A changed test, script, or source statement is code, and (d) runs. Determine it by inspecting the diff, not by assuming.
     - Rationale, measured on `v1-f003` over 8 gates: 15 of 36 findings were introduced by a previous round's own fix, and the 7 remediation-diff reviews caught 1 of those 15. The other 14 were approved here and found by the NEXT feature gate. The step's recall against injected defects is low because the dominant injected defect in a mature feature is a CLAIM the fix invalidated — a comment, spec sentence, or task now contradicting the code — and a diff-scoped review sees the lines that changed, not the lines that should have. Spending a review pass on a diff with no code in it buys nothing.
     - What DOES catch injected defects, and stays mandatory: the unfiltered mutation sweep in (c). It caught two tests that could not fail, both introduced by the immediately preceding round.
   - **(e) Only then re-invoke step 3.5.**
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
