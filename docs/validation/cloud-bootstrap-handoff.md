# Fresh consumer Cloud verification handoff

## Current tracked-skill checkpoint

The user approved tracked shared skills on 2026-10-05 after fresh tasks failed to
expose injected skills. This changes storage and the F14 experiment, not the workflow
architecture. The failures do not establish a particular Cloud host root cause.
Source tracked-storage starting revision: `ead664a722b040e144c44c431bfe4488c36d7c88`,
branch `rewrite/workflow-skills-v2`; original rewrite baseline remains in Git.
Tested executable/source pin: `a4eb9f1303d80cc18f83b5bbd734063cac03b9c3`
(87 tests and strict specs on Cloud/Ubuntu at that code commit).
Consumer: canzheng/workflow-skills-test, `pilot/shared-skill-bootstrap`,
`f6394326cd410b82567b8fea76bfd5c44fa9261a`, Issue7/ReadyPR8. Schema3, all4 shared
files and pantry-project tracked; all20 hashes match before hooks. Explicit update
preserved config/AGENTS/ignores/project skill/raw index before caller commit.
Current actual push37272954548/PR37272958814/metadata37272957270 pass. Fresh actual
runtime/Ubuntu clones repeat check/doctor/read-only bootstrap without writes and
reject missing/untracked/corrupt-staged files or partial provenance staging without
repair. Source review repair now validates the independent staged commit candidate;
consumer finding4181129303 was reproduced with old installed CLI before acceptance.
Two additional regression cases cover partial provenance staging and intent-to-add.
At source test/evidence head `b0323c903901bc33fb16a144aec413f3b31ff087`, all89/no skips
and strict specs pass on managed runtime/Ubuntu; executable bundle remains a4eb9f1.
Source push37273309768 passes; PR37273314869 was still running when recorded.
Current-head semantic review is pending: the previous source request returned an
unknown-error response, which is not a review pass.

Consumer is public with Active required-check ruleset24484016. Historical actual
metadata negative/restoration at6b9eb5d demonstrated blocked/clean with no merge.
No merge is authorized. Exact schema-3 acceptance needs the intended consumer
revision before discovery; initial discovery on older main does not test the update.
User's completed fresh-environment diagnostic preserved old main5d055649/source139e66d5,
again exposing no workflow entries despite intact tracked skills. Recreating the
environment did not resolve this. Current consumer/source pins are no longer frozen
at0e3fbc53/aceba714; this update followed completion of that diagnostic, not during it.

The user reports that current environment creation offers repository selection only.
The [current Cloud documentation](https://learn.chatgpt.com/docs/environments/cloud-environments)
documents repository selection and starting tasks from a published environment,
but does not document a branch selector for that flow. Do not direct users to an
assumed control. If their launcher cannot select this unmerged revision, report
that constraint. A fresh task on main can still probe discovery of the identical
shared skill blobs; it cannot certify the current schema-3 installation/runtime pin.

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

The user has now recreated the environment and reproduced the same catalog absence
with intact tracked skills on old main. Do not ask for further environment recreation
or installer changes without new host evidence. See the [recreated-environment comparison](f14-published-cloud-run.md#recreated-environment-reproduced-catalog-absence--2026-10-05).
The next host action is a support/debugging handoff about initial repository/project
binding, discovery catalogs and checkout ordering. Manual repo-file reading/use is
available but cannot satisfy automatic discovery acceptance.

Native Codex CLI0.159.0-alpha.3 catalog now recognizes all3 workflow skills at the
consumer Git root on managed runtime and Ubuntu, while a parent-root query returns
none. A real old-main clone also has all3 recognized at its repo root. See the
[controlled catalog comparison](f14-published-cloud-run.md#native-codex-catalog-root-comparison--2026-10-05).
This validates package discoverability and strengthens the root-binding lead;
it does not establish the published Cloud scanner/root or initial agent catalog.

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
the diagnostic. Use branch selection only if the actual task launcher supports it;
the current published-environment flow has no documented branch selector. Do not mutate default branch or
merge the pilot to work around host routing. If the UI cannot select the unmerged
revision before discovery, record that limitation and the exact pending action.

## Mini diagnostic task prompt

Use a genuinely fresh task outside onboarding after the tracked pilot is published.
The full pins below identify the verified consumer commit and executable source.
If the UI offers only environment/repository selection, a run from main is a discovery
baseline with an expected current-pilot mismatch. Record that result; do not repeat
environment creation merely to seek an undocumented branch selector.

```text
Validate tracked workflow-skills preparation in canzheng/workflow-skills-test.
Expected consumer HEAD: f6394326cd410b82567b8fea76bfd5c44fa9261a.
Expected workflow source pin: a4eb9f1303d80cc18f83b5bbd734063cac03b9c3.

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
python3 tools/workflow/workflow.py doctor --repo . --expect-revision f6394326cd410b82567b8fea76bfd5c44fa9261a --json
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
