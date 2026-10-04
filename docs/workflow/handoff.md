# Continuation and evidence

A latest Issue/PR handoff contains repository, Issue/source ID, branch/full SHA,
dirty state, plan/spec/docs paths, completed scope, passed/failed/skipped/pending
checks, environment, prerequisites/blockers and exact next action. No second plan.
When remote writes fail, append evidence to the existing rewrite tasks checkpoint.
Use full revision and actual content; doctor reports revision/branch/dirty/content
SHA-256 digest for tracked/nonignored files without exposing file content or secrets.
For schema-2 consumers it also hashes materialized ignored dependency bytes and
reports dependency modification, so an ignored edit invalidates evidence even with
a clean Git status. Record both consumer SHA and pinned source SHA across environments.
Compare `--expect-branch`, `--expect-revision` and, for dirty tested content,
`--expect-content`. Missing or mismatched targets fail explicitly. Commit tested
content and rerun before declaring an exact commit verified. Material changes
invalidate affected checks; doc-only later commits may cite earlier unchanged-code
checks accurately, never pretend those were rerun at the new head.

```sh
python3 tools/workflow/workflow.py doctor --repo /exact/repository --expect-branch BRANCH --expect-revision FULL_SHA --json
```

A same-SHA Ubuntu handoff must run the documented setup/verify/spec commands on
Ubuntu and record OS/runtime/revision/exit result. This Debian checkout is not an
Ubuntu acceptance environment. Missing Ubuntu or fresh Cloud discovery remains
integration pending. Preserve summaries in PR/Issue records; raw logs may be CI
artifacts with declared retention (CI uses 14 days), not permanent proof by URL alone.

Read/auth/write/publication/admin are independent capabilities. Doctor's gh auth
probe suppresses raw credential output and reports other capabilities unprobed.
Use actual authorized reads/writes to establish them; never copy secrets into the
checkout. Native operation fault fixtures cover unknown creation, repeated source
IDs, permission loss and concurrent human edits. These are fixture proof, not live
remote success. An unknown write is reconciled by re-reading before retry.
