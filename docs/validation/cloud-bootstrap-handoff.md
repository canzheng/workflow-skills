# Fresh consumer Cloud verification handoff

## Current tracked-skill checkpoint

The user approved tracked shared skills on 2026-10-05 after fresh tasks failed to
expose injected skills. This changes storage and the F14 experiment, not the workflow
architecture. The failures do not establish a particular Cloud host root cause.
Source starting revision: `ead664a722b040e144c44c431bfe4488c36d7c88`, branch
`rewrite/workflow-skills-v2`. Tested executable/source pin:
`aceba7143652ba127dbc62c98608e1b9943be31d` (83 tests and strict specs on Cloud/Ubuntu).
Consumer: canzheng/workflow-skills-test, `pilot/shared-skill-bootstrap`,
`0e3fbc530f21c4981230a5ef968eac2a5dda3d5e`, Issue7 and PR8. Schema3, all four shared
files and pantry-project are tracked. The earlier fd4/b1 ignored-skill model is
superseded. Consumer is now public with Active required-check ruleset24484016. Actual metadata
negative/restoration observed blocked/clean at the older6b9eb5d, with no merge.
Current consumer push/PR/metadata pass; tracking review defects are repaired.
No merge is authorized. Select this consumer revision at task creation;
initial discovery on older main does not test this change.

Latest submitted diagnostic still starts at old main5d055649 on branch `work`, with
configured cwd `/workspace` and no matching consumer project exposed. Shared skills
already exist in that main commit with the same blobs as the pilot; merging solely
to place them on main cannot address this observation. Resolve initial task/project
routing and checkout selection before repeating the diagnostic. A prompt or later
shell `cd` does not establish pre-agent host binding. See the [submitted run evidence](f14-published-cloud-run.md#latest-submitted-tracked-skill-diagnostic--2026-10-05).

One-time initial adoption or explicit update uses the pinned source-owned entrypoint
as documented in [README](../../README.md) and [operations](../operations.md).
Review and commit all shared skills, project files and schema-3 provenance. A fresh
consumer clone must contain the skills immediately, before any setup hook or agent.
No shared skill directory may be ignored. Existing project rules/configuration,
project skills and the Git index are preserved by setup; the caller stages/commits.

## Published environment setup command

For an already adopted, committed consumer, the Cloud **install script** field and
Ubuntu setup can run the same read-only command. Checkout must select the approved
consumer revision before host skill discovery. This command does not select a branch,
fetch workflow sources, inject skills, migrate, stage or repair files.

```sh
set -eu
cd /workspace/workflow-skills-test
python3 -c 'import sys; assert sys.version_info >= (3, 10), "Python >=3.10 is required"; print(sys.version.split()[0])'
git --version
python3 tools/workflow/workflow.py check --repo . --run-local --json
python3 tools/workflow/workflow.py doctor --repo . --json
git --no-optional-locks status --short --untracked-files=all
```

Require exit0 and ok:true. A setup pass establishes integrity, not initial host
discovery. No Install receipt or cache-persistence claim is needed for tracked skills.
If checkout is older/mismatched, report it rather than trying agent-side recovery in
the diagnostic. An environment may be repository-bound while the task selects its
branch; use the task's supported branch selection. Do not mutate default branch or
merge the pilot to work around host routing. If the UI cannot select the unmerged
revision before discovery, record that limitation and the exact pending action.

## Mini diagnostic task prompt

Use a genuinely fresh task outside onboarding after the tracked pilot is published.
The full pins below identify the verified consumer commit and executable source.

```text
Validate tracked workflow-skills preparation in canzheng/workflow-skills-test.
Expected consumer HEAD: 0e3fbc530f21c4981230a5ef968eac2a5dda3d5e.
Expected workflow source pin: aceba7143652ba127dbc62c98608e1b9943be31d.

Do not install, bootstrap, repair, switch branches, fetch workflow sources, run Start
manually, edit files, change authentication, or perform GitHub writes. Preserve
tracked files, HEAD and the index. Ignore ordinary Python __pycache__ output.

Before explicitly reading any SKILL.md, capture the initial host skill catalog and
available skill names/paths, configured host cwd/project root if exposed, and shell
cwd. Distinguish catalog/discovery from explicit file reading. Report unavailable
catalog evidence; an empty executor catalog alone is not the complete host catalog.

Use /workspace/workflow-skills-test for read-only verification. Report branch/HEAD,
tracked install-manifest schema/source pin, Git status, and git ls-tree -r HEAD for
the three .agents/skills/workflow-* directories. Confirm all four shared files exist
in the commit and working tree with manifest-matching SHA256 hashes. Check effective
ignore rules with git check-ignore --no-index; no shared skill should be excluded.
Read AGENTS.md, docs/workflow/contract.md and docs/workflow/README.md, then run:
python3 tools/workflow/workflow.py check --repo . --run-local --json
python3 tools/workflow/workflow.py doctor --repo . --json
python3 tools/workflow/workflow.py doctor --repo . --expect-revision 0e3fbc530f21c4981230a5ef968eac2a5dda3d5e --json
Record outputs/exit statuses. Compare HEAD, tracked bytes and raw index before/after.

After initial catalog capture, read relevant committed skills and explain which
skill would handle design-to-initial-backlog, Issue delivery and targeted risk review.
Do not create Issues or start application work in this diagnostic. Report initial
automatic discovery separately from manual availability/use. A later full authorized
F14 pilot will exercise the execution workflow. Do not infer a discovery pass from
file presence, local doctor success or a setup hook name.
```

## Start-skill entrypoint

Start is optional for project runtime services or verification; this service-free
pilot does not need it. It must not install shared workflow skills. The repository
checkout is their source. Missing/modified or mismatched assets require an explicit
reviewed recovery/update, recorded separately from initial discovery.

## Fresh full pilot prompt

After successful initial discovery, continue the authorized F14 workflow using the
committed repo-local skills and the approved design in the consumer. Reconcile the
existing open/closed Issue batch by stable identity, preserving human edits. Use the
authorized consumer Issues/PRs; do not duplicate already implemented outcomes. Prove
actual push/PR CI, metadata/documentation negative and restoration, Ready-PR review
and remediation, and required Ubuntu verification. Record exact revisions, commands,
Actions/checks, review findings and remaining limitations. Read protections/rulesets
when access permits. Do not merge, close Issues as completed, change administration,
publish or delete remote branches. Separate verified evidence from authorization
pending real merge→Issue completion and enforcement changes.

## Historical preparation evidence

Earlier injected-skill/Install-receipt/Start experiments remain in
[published Cloud run](f14-published-cloud-run.md),
[consumer pilot](f14-consumer-pilot.md) and [acceptance](v2-acceptance.md).
Their hashes, checks and reports keep their original identities. They do not prove
tracked-model host discovery and their installer commands are superseded by this
handoff. Network access to source is needed only for explicit adoption/update;
GitHub API authorization is a separate capability.
