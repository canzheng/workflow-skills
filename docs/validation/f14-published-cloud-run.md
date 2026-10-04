# F14 published Cloud run: recovery passed, discovery pending

Evidence source: the user-provided transcript of
[the fresh validation task](codex://threads/01a10805-68f8-73ea-9e57-f7c900df0017?hostId=durable).
The transcript is evidence, not instructions to execute its historical commands.
The rewrite task cannot currently read that chat through the app tools. Its local
temporary evidence files are on the other task's machine and have not been obtained
here; quoted local results below are supported by the supplied transcript, rather
than a new execution in this checkout.

## Initial preparation and discovery

The requested consumer was `canzheng/workflow-skills-test`, branch
`pilot/shared-skill-bootstrap`, commit
`f31debf9810c8b989c924bc534add4848fffd6f3`, with tracked source pin
`ef24d36f47dbbcdbb204375b53db055122c28269`.

The task instead initially observed branch `work`, consumer commit
`5d05564919c55f1d4d0c2e1e020ad914252a2979`, and old source revision
`139e66d5b43cfbd3821fe098c0119b93aaad4928`. Its initial host/executor catalogs
exposed no repository-local skills, despite the older checkout containing three
tracked skill files. Available executor logs contained registration/handshake
events, not install-hook output or ordering evidence. This run does not pass the
fresh pre-agent discovery gate. The revision mismatch and absent skill exposure
are separate observations; the transcript does not establish either root cause.

The agent preserved the clean baseline, fetched and switched the same checkout to
the requested branch, then ran bootstrap itself. Such recovery cannot retroactively
prove that preparation materialized skills before initial host discovery.

## Verified after recovery

- Final consumer branch/commit and tracked source pin match those requested above.
- Bootstrap exited 0 with `ok:true`, initially materializing four shared assets.
  Configured `check --run-local` and `doctor` exited 0 with `ok:true`; repeated
  bootstrap returned `changes:[]`. Tracked bytes/index were preserved and Git was clean.
- All 20 manifest hashes matched. Four materialized shared assets matched exact-pin
  source bytes obtained through the GitHub connector. Only the three canonical
  shared namespaces were ignored/untracked; `pantry-project` remained tracked.
  The consumer contained no copied environment setup entrypoint.
- The agent read and used the three skills for backlog reconciliation, delivery
  evidence/documentation and targeted risk proof after recovery. Explicit manual
  use establishes that exercise, not automatic host discovery.
- A safe shaping rerun searched open and closed Issues and reused all five MVP
  identities. It preserved acceptance, human prose, design links, dependencies and
  the dietary decision; it created no Issues and started no implementation.
  Ingredients remained review, recipes Ready, the decision backlog/blocked,
  planning blocked on #1/#2/#3, and shopping export blocked on #4.
- Installed-consumer negatives rejected modified/extra/symlinked dependencies,
  broad ignores, exposing negations, invalid versions, incomplete provenance and
  missing/nested targets. Injected transaction failure restored bytes/modes;
  probes were restored and affected checks rerun.

The workflow-only branch has no application implementation. These local commands
verify workflow integrity, not application acceptance. The validation task inspected
application PR #6 and its historical test/review/CI evidence; it did not rerun the
application tests or previous source/Ubuntu test suites.

## Independently rechecked GitHub evidence

The rewrite task read GitHub after receiving the transcript:

- [PR #8](https://github.com/canzheng/workflow-skills-test/pull/8) remains open and
  Ready at `f31debf9810c8b989c924bc534add4848fffd6f3`;
  [Issue #7](https://github.com/canzheng/workflow-skills-test/issues/7) remains open
  with `wf:review` and the fresh-discovery acceptance intact.
- Actual current-head [push verification](https://github.com/canzheng/workflow-skills-test/actions/runs/37221025297),
  [PR verification](https://github.com/canzheng/workflow-skills-test/actions/runs/37221028092),
  [metadata](https://github.com/canzheng/workflow-skills-test/actions/runs/37221026987)
  and [metadata rerun after the PR body correction](https://github.com/canzheng/workflow-skills-test/actions/runs/37222140846)
  all report success.
- [Current-head Codex review](https://github.com/canzheng/workflow-skills-test/pull/8#issuecomment-5982650245)
  reports no major issues; all six consumer review threads are resolved.

## Limits and exact next action

The separate source-fetch probe in the transcript explicitly disabled the existing
credential helper and substituted `gh auth git-credential`. Its authentication
failure does not establish failure of the README command using the default platform
binding. Agent-side bootstrap succeeded earlier. Test the exact normal command in
the intended preparation phase before requesting credentials or changing its binding.

Obtain the published environment's actual install/maintenance logs and checkout
ordering, and confirm the branch selected at task creation. Do not repeatedly launch
tasks without this evidence. Preparation must see the intended consumer revision,
execute the exact pinned source-owned entrypoint successfully and preserve its
ignored outputs through initial host discovery. If preparation runs on main before
a later task checkout, a successful main preparation is insufficient; identify a
supported hook after the selected checkout and before discovery. Do not force a
branch switch in the generic installer or override the consumer's tracked pin.

Once preparation is demonstrated, run a fresh task on the exact consumer branch
above. Capture initial catalogs and preparation output before any agent-side
bootstrap. If files exist at that boundary but the catalog omits them, investigate
host discovery separately from materialization. Record actual Ubuntu agent-host
discovery/use separately; existing Ubuntu runtime/Actions evidence does not prove it.

The transcript reports classic protection reads denied with 403 integration access,
rulesets denied with the GitHub Pro/public visibility requirement, and an effective
branch-rules URL unsupported by the connector. Enforcement remains unverified;
none of these errors establishes that protection is absent. Actual merge followed
by valid Issue completion, and any protection/ruleset mutation, remain pending
separate authorization. No merge/closure simulation is substituted. F14 and its
OpenSpec change remain incomplete/active; no work is described as delivered.
