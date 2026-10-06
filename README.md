# Workflow Skills v2

Three shared skills for bounded GitHub Issue delivery with Codex: design-to-backlog,
deliver-issue and targeted risk-review. GitHub owns delivery records; Git owns project
intent/specs/docs. No Conda, Superpowers, feature ledger or mandatory task wrappers.
Read [the document index](docs/README.md), [contract](docs/workflow/contract.md),
[approved scope](docs/v2/v2-feature-list.md) and [Issue links](docs/v2/issue-links.md).
Ubuntu workstation use is the required first-release path; Cloud discovery is deferred.

## Development

Runtime: Python >=3.10 and Git. Installation mutations require Linux renameat2
exchange/no-replace and inotify directory creation observation from libc/kernel
and the target filesystem; unsupported
operations fail without an overwrite fallback. Source verification:
python3 tools/workflow/verify.py.
Optional pinned OpenSpec 1.14.0: npm ci --ignore-scripts, then
python3 tools/workflow/workflow.py check --repo . --specs --json.
[Development](docs/development.md) covers full history and supported versions.

## Pinned consumer adoption

Canonical shared skills are authored and tracked in this source repository. Consumers track their
AGENTS/config, CI/templates, docs/specs, project skills and exact source pin;
the three shared skill directories/references and Python runtime in
`.agents/tools/workflow/` are materialized repo-locally and ignored together.
Setup adds only those four anchored ignore rules, never all of .agents. It is idempotent,
previews before apply, preserves unrelated files/index and never stages/commits.

The source owns the installer; a fresh target needs no existing workflow tools.
Set the full tested source SHA from the [Ubuntu handoff](docs/validation/ubuntu-workstation-handoff.md)
and actual consumer root/owner/name, then fetch/run in Bash:

```sh
set +e
(
set -eu
: "${WF2_SOURCE_SHA:?Set the exact tested 40-character source commit from the handoff}"
: "${WF2_CONSUMER_ROOT:?Set the absolute consumer Git root}"
: "${WF2_CONSUMER_REPOSITORY:?Set owner/repository}"
WF2_SOURCE_DIR=$(mktemp -d)
trap 'python3 -c "import shutil, sys; shutil.rmtree(sys.argv[1])" "$WF2_SOURCE_DIR"' EXIT
git -C "$WF2_SOURCE_DIR" init --quiet
git -C "$WF2_SOURCE_DIR" fetch --no-tags --depth=1 https://github.com/canzheng/workflow-skills.git "$WF2_SOURCE_SHA"
git -C "$WF2_SOURCE_DIR" checkout --detach --quiet "$WF2_SOURCE_SHA"
bash "$WF2_SOURCE_DIR/tools/workflow/environment-setup.sh" "$WF2_CONSUMER_ROOT" "$WF2_CONSUMER_REPOSITORY"
)
printf 'Installation exit status: %s\n' "$?"
```

Review/commit project adoption and schema-5 provenance before acceptance. Existing
tracked consumers need an explicit reviewed source setup/update and caller-owned
untracking of only the dependency namespaces; startup never changes storage/index.
See [operations](docs/operations.md) for preview/apply, migration and recovery.

The Python entry point in consumers is `.agents/tools/workflow/workflow.py`.
A fresh clone has no shared Python files yet: fetch the exact source pin and run
this source-owned entrypoint first. It bootstraps the pin before running consumer
checks. Matching reruns are offline/idempotent once the pinned source checkout is
available. CI similarly fetches its tracked pin; PR metadata uses the base checkout's
pin and never executes PR head code. `--dependency-storage tracked` explicitly
tracks both runtime and skills for compatibility. Source authoring retains the
canonical runtime in `tools/workflow/`.

### Repository workflow routing

Adoption creates `AGENTS.md` if absent or appends an owned section between
`<!-- workflow-v2:start -->` and `<!-- workflow-v2:end -->`. It instructs agents
to use repo-local workflow-skills v2 in `.agents/skills/`, read the installed
contract/document index, and avoid obsolete workflow wrappers. Existing project
instructions remain intact; repeating setup does not duplicate the section.

Globally discoverable v1 skills such as `start-task`, `complete-task` and
`audit-workflow` do not select this repository's workflow. Do not invoke them for
v2 delivery or delete global files during adoption. Higher-level host policies
still apply; report an actual conflict rather than claiming this section overrides
them. Active repository-local v1 routing requires the documented bounded migration
before setup; the installer refuses to silently append conflicting instructions.
Commit the generated `AGENTS.md` with the other project-owned adoption files.

## Repeatable Ubuntu bootstrap

Before starting Codex, from the selected consumer root:

```sh
python3 .agents/tools/workflow/workflow.py bootstrap --repo . --apply --json
python3 .agents/tools/workflow/workflow.py check --repo . --run-local --json
python3 .agents/tools/workflow/workflow.py doctor --repo . --json
git --no-optional-locks status --short --untracked-files=all
codex
```

For a fresh clone, first fetch the tracked pin and run the source-owned setup
entrypoint above; the installed CLI is initially absent. Bootstrap installs only
missing ignored skills and runtime files from the manifest's full commit;
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

F01–F14 premerge acceptance is verified and the rewrite change is archived on this
delivering branch. Required Ubuntu native skill discovery/use, runtime verification,
GitHub checks, semantic review and consumer enforcement are recorded; the separately
authorized merge/deployed-base checks remain. [Evidence](docs/validation/v2-acceptance.md) distinguishes
runtime, native discovery, semantic use/review, actual CI/enforcement and merge.
Cloud is deferred/unverified, not passed. Merge/release/admin/global writes require
explicit authorization; no local pass or PR alone means delivered. The v1 tree is
retired, with provenance at the [recorded baseline](docs/migration-v1-v2.md).
