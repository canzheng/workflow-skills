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
