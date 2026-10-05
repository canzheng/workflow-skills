# Workflow Skills v2

Repository-scoped skills for bounded GitHub Issue delivery with Codex. The three
skills shape approved design, implement/verify/document an Issue, and select risk
proof. GitHub owns delivery records; Git owns design, current specs and documentation.
No global installation, Conda, Superpowers, feature ledger or per-task wrapper is required.

Read [the document index](docs/README.md) and [delivery contract](docs/workflow/contract.md).
The [approved v2 design and acceptance](docs/v2/v2-feature-list.md) remain the rewrite
baseline; [Issue links](docs/v2/issue-links.md) carry identity without local status mirrors.

## Development

```sh
python3 tools/workflow/verify.py
```

Runtime/offline verification: Python >=3.10 and Git. Optional development dependencies
are pinned in requirements.txt. `npm ci --ignore-scripts` installs pinned OpenSpec
1.14.0 when relevant; `python3 tools/workflow/workflow.py check --repo . --specs`
runs actual strict validation. See [development](docs/development.md).

## One-time adoption and explicit updates

Shared workflow skills are installed repo-locally **and committed in the consumer**.
Track all three `.agents/skills/` directories, risk references, project policy/config,
helpers, CI/templates, docs and schema-3 source provenance. Project skills stay tracked.
Fresh Cloud/Ubuntu tasks get the reviewed skills from Git, not environment injection.

The adoption entrypoint lives in workflow-skills, not the consumer. Fetch an explicit
full source commit and run [environment-setup.sh](tools/workflow/environment-setup.sh)
with the exact consumer Git root and owner/name. Python >=3.10, Bash and Git are
required; first fetch needs Git HTTPS access. A new target needs no existing tools
or first commit. Set WF2_SOURCE_SHA to the tested full source SHA in the
[current handoff](docs/validation/cloud-bootstrap-handoff.md), then run in Bash:

```sh
set -eu
: "${WF2_SOURCE_SHA:?Set the tested full source commit from the handoff}"
WF2_CONSUMER_ROOT=/workspace/workflow-skills-test
WF2_CONSUMER_REPOSITORY=canzheng/workflow-skills-test
WF2_SOURCE_DIR=$(mktemp -d)
trap 'rm -rf -- "$WF2_SOURCE_DIR"' EXIT
git -C "$WF2_SOURCE_DIR" init --quiet
git -C "$WF2_SOURCE_DIR" fetch --no-tags --depth=1 https://github.com/canzheng/workflow-skills.git "$WF2_SOURCE_SHA"
git -C "$WF2_SOURCE_DIR" checkout --detach --quiet "$WF2_SOURCE_SHA"
bash "$WF2_SOURCE_DIR/tools/workflow/environment-setup.sh" "$WF2_CONSUMER_ROOT" "$WF2_CONSUMER_REPOSITORY"
```

Review and commit generated files before publishing an agent environment. Setup
never stages, commits, pushes, merges or changes protection/global configuration.
For existing schema-1/2 adoption, use the new source's explicit setup preview/apply
[procedure](docs/operations.md); repeat startup does not silently migrate it.
Schema-2 migration removes only the verified owned shared-skill ignore block.
Modified files or other conflicting ignore rules are preserved and reported.

## Cloud install field and local repeat verification

For an adopted repo, the environment Install field needs only the following,
with the actual consumer path. Run the same commands locally/on Ubuntu:

```sh
set -eu
cd /workspace/workflow-skills-test
python3 tools/workflow/workflow.py check --repo . --run-local --json
python3 tools/workflow/workflow.py doctor --repo . --json
git --no-optional-locks status --short --untracked-files=all
```

No workflow repository fetch, global skills, ignored-file cache or Start skill is
needed for this CLI-only pilot. Repeating the source-owned entrypoint also preserves
project files/index/pin and only verifies an adopted schema-3 repository. Existing
`bootstrap --apply` callers perform read-only verification; they never fetch/repair
missing skills. Restore the reviewed Git checkout or perform an explicit update.
The installed pin wins over a newer source entrypoint; updates are separate changes.

Publish/apply the environment and launch a fresh task on the reviewed consumer
revision. Record the initial host skill catalog before explicit skill reads; verify
all shared files are committed, hashes/pin match and Git remains clean. Capture host
cwd/project-root routing separately from shell cwd. Presence and manual use alone
are not discovery proof. The [F14 handoff](docs/validation/cloud-bootstrap-handoff.md)
contains the current revisions, diagnostic and remaining boundaries. Earlier
ignored-file/receipt experiments are historical evidence, not the acceptance path.

## Acceptance boundary

Code/local checks and primary-author skill exercises do not establish fresh Cloud
skill discovery, Ubuntu portability, live Actions or merge protection. The rewrite
change stays active until required acceptance completes. PR/Issue evidence reports
implemented, locally verified, integration pending, ready for review, merged and
delivered distinctly. Merge/release/admin/global changes require separate authorization.
V1-only planning, lesson and archive trees are absent from the source head.
Original runtime/tests/specs and evidence remain reachable at the
[recorded baseline](docs/migration-v1-v2.md); they are retired from current distribution.

Environment setup validates the explicit owner/repository against any existing
project config before adoption or bootstrap, rejecting mismatches without writes.

An adopted repository missing its project configuration fails before dependency writes.
Source and installed provenance share the same v2 bundle-version validation.
