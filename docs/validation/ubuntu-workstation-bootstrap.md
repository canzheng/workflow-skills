# User workstation bootstrap evidence — 2026-10-05

This records terminal output supplied by the user, not commands run on their
workstation by the rewrite agent. The Bash validation block used `set -euo
pipefail` inside a subshell; its final reported exit status was 0. No fresh Codex
agent session was included in this report.

## Tested consumer and environment

- Checkout: `/home/canzheng/workflow-skills-test-ubuntu-pilot`.
- Repository: canzheng/workflow-skills-test, `pilot/shared-skill-bootstrap`.
- Expected-HEAD assertion and doctor passed at
  `9bd23d72dc24a741d669c1ea92532f8bf337aa42`.
- That committed schema-4 manifest pins workflow-skills source
  `a75c3f20e5f4032568b1d1a5cb17d001fc781918`; this output did not separately print
  the manifest or individual asset hashes.
- Reported OS: Ubuntu 26.04 LTS (Resolute Raccoon).
- Python 3.13.13; Git 2.53.0; codex-cli 0.160.0.
- Doctor additionally reported gh 2.96.0, Node v24.1.0 and OpenSpec 1.4.1.

## Actual reported command results

| Command | Evidence |
| --- | --- |
| Fresh `git clone --branch pilot/shared-skill-bootstrap` | Clone completed; exact expected-HEAD assertion passed. |
| `bootstrap --repo . --apply --json` | `ok: true`, `applied: true`, four shared files materialized. |
| `check --repo . --run-local --json` | `ok: true`; declared local command 1 exited 0. This is workflow integrity, not application acceptance. |
| `doctor --repo . --expect-revision 9bd23d72dc24a741d669c1ea92532f8bf337aa42 --json` | `ok: true`, revision matched, installed-consumer mode, dirty/dependency_modified both false. |
| Repeated `bootstrap --repo . --apply --json` | `ok: true`, `applied: true`, `changes: []`. |
| `git ls-files` for the three shared directories | No output: shared dependency files are not indexed. |
| Final `git status --short` | No output: clean working tree. |
| Enclosing validation | `Validation exit status: 0`. With the block's errexit, the preceding verification commands succeeded. |

The first materialization listed exactly:

```text
.agents/skills/workflow-deliver-issue/SKILL.md
.agents/skills/workflow-design-to-backlog/SKILL.md
.agents/skills/workflow-risk-review/SKILL.md
.agents/skills/workflow-risk-review/references/methods.md
```

Doctor reported content digest
`c6c9e6f199ecb33b3f49130c6968d3872e8e06c5db0bf91f79de0f2def1abef5`.
The installed checker validates the manifest's managed hashes and effective
dependency ignore/index policy. The supplied transcript contains no separate
`git check-ignore` output or before/after raw-index/tracked-file hash comparison.
Clean Git status and repeat changes:[] do not independently prove identical index
bytes. Earlier owned-clone index-preservation evidence retains its own revisions.

## Warnings and limits

Doctor returned three `discovery.legacy` warnings for existing global
`audit-workflow`, `start-task` and `complete-task` skills under
`/home/canzheng/.agents/skills/`. These are different names from v2, not evidence
of duplicate v2 installations. No global skills or host configuration were changed.
The pilot must follow the consumer's v2 contract, preserve higher-level host
instructions and report a real routing conflict instead of invoking obsolete
wrappers or deleting global skills.

`gh_authentication` was authenticated. GitHub read/write, branch publication,
Actions administration, merge enforcement, GitHub CI execution and host skill
discovery remained `unprobed` in this doctor invocation. The source fetch required
by successful materialization is narrower evidence than those GitHub capabilities.
Previously recorded actual consumer CI/enforcement evidence remains separate.

This verifies workstation bootstrap, repeatability and installed workflow checks
on the reported Ubuntu/Python versions. It does not report the source's 107-test
suite as run on this workstation, automatic discovery, actual agent skill use,
independent semantic review, merge, completed Issue closure or release.

## Exact next action

Launch a fresh `codex` session from the consumer checkout and use the
[fresh Ubuntu task prompt](ubuntu-workstation-handoff.md#fresh-ubuntu-task-prompt).
Capture the initial available catalog before explicit SKILL.md reads, then actual
delivery/backlog/risk-review artifacts and no-chat continuation evidence for the
existing Issue7/Ready PR8. Do not reinstall or modify global configuration.
F14 remains partial until the required session and review evidence exists; the
rewrite change remains active. Cloud is deferred. Merge/completed closure,
administration and release retain their separate authorization boundaries.
