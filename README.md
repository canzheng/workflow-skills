# Workflow Skills v2

Three shared skills for bounded GitHub Issue delivery with Codex: design-to-backlog,
deliver-issue and targeted risk-review. GitHub owns delivery records; Git owns project
intent/specs/docs. No Conda, Superpowers, feature ledger or mandatory task wrappers.
Read [the document index](docs/README.md), [contract](docs/workflow/contract.md),
[approved scope](docs/v2/v2-feature-list.md) and [Issue links](docs/v2/issue-links.md).
Ubuntu workstation use is the required first-release path; Cloud discovery is deferred.

## Development

Runtime: Python >=3.10 and Git. Source verification: python3 tools/workflow/verify.py.
Optional pinned OpenSpec 1.14.0: npm ci --ignore-scripts, then
python3 tools/workflow/workflow.py check --repo . --specs --json.
[Development](docs/development.md) covers full history and supported versions.

## Pinned consumer adoption

Shared skills are tracked only in this source repository. Consumers track their
AGENTS/config, helpers, CI/templates, docs/specs, project skills and exact source pin;
the three shared directories/references are materialized repo-locally and ignored.
Setup adds only their anchored ignore rules, never all of .agents. It is idempotent,
previews before apply, preserves unrelated files/index and never stages/commits.

The source owns the installer; a fresh target needs no existing workflow tools.
Set the full tested source SHA from the [Ubuntu handoff](docs/validation/ubuntu-workstation-handoff.md)
and actual consumer root/owner/name, then fetch/run in Bash:

```sh
set -eu
: "${WF2_SOURCE_SHA:?Set the exact tested 40-character source commit from the handoff}"
: "${WF2_CONSUMER_ROOT:?Set the absolute consumer Git root}"
: "${WF2_CONSUMER_REPOSITORY:?Set owner/repository}"
WF2_SOURCE_DIR=$(mktemp -d)
trap 'rm -rf -- "$WF2_SOURCE_DIR"' EXIT
git -C "$WF2_SOURCE_DIR" init --quiet
git -C "$WF2_SOURCE_DIR" fetch --no-tags --depth=1 https://github.com/canzheng/workflow-skills.git "$WF2_SOURCE_SHA"
git -C "$WF2_SOURCE_DIR" checkout --detach --quiet "$WF2_SOURCE_SHA"
bash "$WF2_SOURCE_DIR/tools/workflow/environment-setup.sh" "$WF2_CONSUMER_ROOT" "$WF2_CONSUMER_REPOSITORY"
```

Review/commit project adoption and schema-4 provenance before acceptance. Existing
tracked consumers need an explicit reviewed source setup/update and caller-owned
untracking of only the three directories; startup never changes storage/index.
See [operations](docs/operations.md) for preview/apply, migration and recovery.

## Repeatable Ubuntu bootstrap

Before starting Codex, from the selected consumer root:

```sh
python3 tools/workflow/workflow.py bootstrap --repo . --apply --json
python3 tools/workflow/workflow.py check --repo . --run-local --json
python3 tools/workflow/workflow.py doctor --repo . --json
git --no-optional-locks status --short --untracked-files=all
codex
```

Bootstrap installs only missing ignored skills from the manifest's full commit;
complete matching reruns are offline/no-op. Project files/pin/index remain unchanged;
modified/extra/symlinked dependencies fail without overwrite. Consumer CI runs the
same bootstrap before declared verification. Never implicitly fetch main/latest.
Launch a fresh agent from the repository root, capture its initial catalog before
explicit skill-file reads, then record actual skill use. Presence/catalog alone is
not use evidence. Cloud environments may run the same script, but are not F14 gates.

## Optional global shared skills

Use the same exact checked-out source. Preview, then add --apply only when intended:

```sh
python3 /pinned/source/tools/workflow/workflow.py install-skills --source /pinned/source --revision FULL_40_CHAR_SHA --json
```

Default target is ~/.agents/skills; --target chooses an absolute alternate skills
root. Only the three skills/references and their provenance are installed, with
bounded update/uninstall and preservation of user modifications. Project/global
AGENTS, project helpers/config, authentication and other skills are untouched.
Repository adoption never installs globally. Choose one active location per name;
duplicates are conflicts. Global installation alone does not adopt project policy
or satisfy repo-local dependency checks. Global skills resolve project documents
from the selected repository, not the global install directory.

## Acceptance boundary

F01–F13 are implemented/locally verified; F14 retains required fresh Ubuntu agent
use/review/integration gates. [Evidence](docs/validation/v2-acceptance.md) distinguishes
runtime, native discovery, semantic use/review, actual CI/enforcement and merge.
Cloud is deferred/unverified, not passed. Merge/release/admin/global writes require
explicit authorization; no local pass or PR alone means delivered. The v1 tree is
retired, with provenance at the [recorded baseline](docs/migration-v1-v2.md).
