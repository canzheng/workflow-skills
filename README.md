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

## Cloud and local environment setup

The environment entrypoint lives in this repository, not in the consumer. Fetch an
explicit full workflow-skills commit, then run its source-owned
[environment-setup.sh](tools/workflow/environment-setup.sh) with the consumer Git root
and GitHub identity. Python >=3.10, Bash, Git and HTTPS read access are required.
The target must already be a Git checkout; it may have no tools or first commit.

For Codex Cloud, paste the following into the environment **install script** field
(and maintenance hook when available). Set the exact source SHA, checkout path and
owner/name for your project. For local/Ubuntu setup, run the same command in Bash
with your local absolute checkout path. No global installation is involved.

```sh
set -eu
WF2_SOURCE_SHA=608b4e6ee16017bca3e63e98b2e1e91235b1a004
WF2_CONSUMER_ROOT=/workspace/workflow-skills-test
WF2_CONSUMER_REPOSITORY=canzheng/workflow-skills-test
WF2_SOURCE_DIR=$(mktemp -d)
trap 'rm -rf -- "$WF2_SOURCE_DIR"' EXIT
git -C "$WF2_SOURCE_DIR" init --quiet
git -C "$WF2_SOURCE_DIR" fetch --no-tags --depth=1 https://github.com/canzheng/workflow-skills.git "$WF2_SOURCE_SHA"
git -C "$WF2_SOURCE_DIR" checkout --detach --quiet "$WF2_SOURCE_SHA"
bash "$WF2_SOURCE_DIR/tools/workflow/environment-setup.sh" "$WF2_CONSUMER_ROOT" "$WF2_CONSUMER_REPOSITORY"
```

Use a tested full SHA from the [current pilot handoff](docs/validation/cloud-bootstrap-handoff.md);
never substitute main/latest. Initial adoption previews and applies bounded project
policy/configuration, utilities, CI/templates, docs, dependency pin and three scoped
ignore entries, then bootstraps and verifies. Review and commit those project-owned
files. The setup script is not copied into the target; project skills remain trackable.

On an adopted repository, the **tracked dependency pin wins** over the fetched
entrypoint revision. Repeated setup only bootstraps that exact pin and runs
check/doctor, without rewriting project-owned files or changing the Git index.
Matching skills need no bootstrap fetch. The outer command fetches its pinned
entrypoint each time; denied source reads fail clearly rather than choosing latest.
An old tracked-skill adoption needs the explicit reviewed [migration](docs/operations.md).
Modified files conflict; unrelated instructions remain. Setup never commits, pushes,
merges or configures protections. Require successful exits and `ok: true` diagnostics.

Publish/apply Cloud configuration and select the intended consumer branch. The host
must check out the repo before the install hook and discover skills afterward;
maintenance may be needed after branch/pin changes. A successful shell run does not
prove host discovery or setup persistence: verify both in a fresh Cloud task.
See [operations](docs/operations.md) for offline preview/update/uninstall and
[migration/rollback](docs/migration-v1-v2.md). Source authoring uses .workflow/bundle.json;
consumer provenance contains the durable dependency pin, not task state.

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
