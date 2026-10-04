# Operations

## Repository setup
From a source checkout at a full pinned commit, preview the bounded bundle:

```sh
python3 tools/workflow/workflow.py setup --source /path/to/workflow-skills --revision FULL_40_CHAR_SHA --target /path/to/consumer --repository owner/name
```

Use an explicit Git root; paths with spaces need normal shell quoting. Inspect
`changes`, then repeat with `--apply` within the user's adoption authorization.
Missing skill assets fail; until F05/F06/F08 assemble the production bundle,
only the fixture bundle is installable. Update uses the same command with a new
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
message and remediation. During F03, `check`/`migrate` are reserved entrypoints
implemented at F10/F12; they are not usable verification claims yet.
