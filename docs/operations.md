# Operations

## Repository setup
From a source checkout at a full pinned commit, preview the bounded bundle:

```sh
python3 tools/workflow/workflow.py setup --source /path/to/workflow-skills --revision FULL_40_CHAR_SHA --target /path/to/consumer --repository owner/name
```

Use an explicit Git root; paths with spaces need normal shell quoting. Inspect
`changes`, then repeat with `--apply` within the user's adoption authorization.
Missing skill assets fail; the assembled real bundle is exercised by the
production consumer test. Update uses the same command with a new
checked-out revision. Bundle bytes must match that revision; uncommitted source
bytes cannot be certified as HEAD. No global files are written.

All preflight checks precede staging. Multi-file installation is not inherently
atomic: bytes/backups are staged, per-file replacements applied, and original
content/modes restored on failure. A failed restoration reports a recovery path
and exact residuals. Resolve those before retrying. Local concurrent edits and
owned-file hash changes are conflicts; user configuration is validated but not
overwritten. Source authoring has a bundle definition, not an install manifest.

```sh
python3 tools/workflow/workflow.py doctor --repo /path/to/consumer --json
python3 tools/workflow/workflow.py setup --target /path/to/consumer --uninstall --apply
```

Uninstall removes unmodified owned files and the unmodified AGENTS block;
modified assets/configuration and unrelated documents remain. Residuals produce
exit 1 and retained provenance. Empty directories may remain. Inspect legacy
and duplicate skills manually; doctor never removes global installations and
cannot prove inaccessible host discovery. Add `--skill-root /explicit/skills`
to inspect another known location. CLI auth is tested without exposing tokens;
Issue reads, writes, publication and administration are independent, unprobed
capabilities until actually exercised. Return codes: 0 success, 1 check/conflict,
2 invalid invocation/configuration. JSON findings include code/severity/path,
message and remediation. `check` validates mechanical obligations; `migrate inspect` inventories known v1
records without mutation. See workflow/checks.md and migration-v1-v2.md.

A rollback residual's recovery directory includes recovery-index.json mapping each
original path to backup bytes and original mode; a null backup identifies a newly
created path. Use that index to restore originals deliberately before rerunning.
Preflight rejects file-valued parents and staging collisions before destination writes.
Conflicting known legacy instruction blocks require bounded migration cutover first.

`check --run-local` executes the configured local argv arrays with shell disabled;
`--run-integration` executes declared integration arrays only when this is the intended
environment. Plain check is mechanical and does not run application tests. Output
reports each exit without dumping potentially sensitive command output; rerun the
specific declared command to investigate. Missing runtime never falls back. Empty
integration arrays are not an environmental pass. Metadata-only forbids these flags.

## Consumer CI adoption
Setup includes owned workflow-v2-verify.yml and workflow-v2-pr-metadata.yml. The first
runs mechanical checks and declared local verification; the second uses trusted
base code for PR contract data. It does not copy source-only Python/Node/OpenSpec
tests, install application dependencies implicitly, execute integration commands in
the wrong environment, or configure repository settings. See installed development
instructions and [enforcement runbook](workflow/checks.md). Configure actual application
commands/prerequisites and observe Actions after authorized publication/base adoption.
Existing/modified workflow files obey the same collision/update/uninstall policy.

## Pinned shared-skill bootstrap

One-time adoption writes project-owned config, utilities, CI/templates, the managed
AGENTS block and a tracked schema-2 `.workflow/install-manifest.json`. That manifest
is the dependency pin: full source SHA, credential-free HTTPS GitHub source URL and
asset hashes. Shared skills remain tracked in the workflow-skills source repository;
consumers materialize them locally and ignore exactly these directories:

```gitignore
/.agents/skills/workflow-design-to-backlog/
/.agents/skills/workflow-deliver-issue/
/.agents/skills/workflow-risk-review/
```

Project-specific skills stay trackable. Setup adds/owns this delimited ignore block,
preserving other rules, and materializes the dependency initially. Repeating setup
with the same inputs returns no changes. It does not silently configure GitHub
administration or edit the Git index. Fork adoption may explicitly supply
`--source-url https://github.com/OWNER/REPO.git`; the default source is
`https://github.com/canzheng/workflow-skills.git`.

For an existing adoption with tracked shared skills, review their managed hashes and
any human changes first, then explicitly untrack only these paths, preserving bytes:

```sh
git rm --cached -r -- .agents/skills/workflow-design-to-backlog .agents/skills/workflow-deliver-issue .agents/skills/workflow-risk-review
```

Run the new pinned setup dry-run/apply and commit the reviewed migration. An ignore
rule alone cannot untrack files. Setup refuses tracked shared skills, unmanaged
collisions and modified managed bytes rather than silently discarding them.

Repeatable Cloud/Ubuntu environment preparation, from the consumer root:

```sh
python3 tools/workflow/workflow.py bootstrap --repo . --apply --json
python3 tools/workflow/workflow.py check --repo . --run-local --json
python3 tools/workflow/workflow.py doctor --repo . --json
```

Bootstrap reads the tracked dependency pin. A source-owned environment entrypoint
may itself be fetched at an explicit full SHA; that seed never overrides an existing
consumer pin. See the workflow-skills README for the Cloud install-script/local
fetch-and-run command; no setup script needs to be tracked in the target repository.
If files already match it, rerunning needs no network and returns `changes: []`.
Otherwise Python >=3.10, Git and Git HTTPS read access to the pinned source are
required. It fetches the full commit into a temporary checkout, verifies source and
skill hashes, then materializes only those ignored namespaces. `--source /exact/pinned/checkout`
provides an explicit offline source; omitting `--apply` previews missing assets.
It never changes config, docs, policy, pin or index. Modified/extra/symlinked shared
assets, missing ignore policy, source/hash mismatch and denied fetch fail safely;
resolve the reported conflict deliberately before retrying. Downloaded source code
is not executed. Only explicit setup/update changes the pin; bootstrap never upgrades.

Configure the host's preparation/maintenance hook to run these commands after the
consumer checkout and before agent skill discovery. Publishing a setup script or
running it from an already-started agent does not prove fresh host discovery. Recheck
after branch/pin changes and record consumer/source SHAs and the actual tested host
profile. Uninstall removes the owned ignore block only when unchanged and no modified
shared asset remains; retained modifications remain ignored and reported as residuals.

Effective Git ignore policy is checked before adoption/update writes and during
bootstrap/check/doctor, including nested/global/info excludes. A broad rule hiding
project skills or a negation exposing a shared dependency is a conflict even when
the managed block hash matches. Review and narrow the offending rule explicitly;
setup never silently rewrites unrelated ignore policy.

The pinned bundle must include every installed CLI runtime module, not just skill
entrypoints and CI files. Missing runtime assets fail adoption preflight. Unmanaged
files inside ignored shared namespaces are dependency modifications: diagnostics
report dirty dependency content even when Git status is clean.

Installed verification/diagnostics and dependency bootstrap also require the complete
runtime/CI/skill destination set in provenance. Deleting a file and its manifest entry
cannot turn an incomplete adoption into a pass. Partial uninstall residual provenance
remains available for recovery; it does not certify a complete usable installation.

Completeness includes required docs, Issue/PR templates and risk references as well
as runtime/CI/skill entrypoints. A new Git repository may bootstrap before its first
commit; doctor then reports revision:null and dirty:true, not a fabricated SHA. Commit
reviewed adoption files before claiming exact-commit/environment delivery evidence.

Environment setup validates the explicit owner/repository against any existing
project config before adoption or bootstrap, rejecting mismatches without writes.
