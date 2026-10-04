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

## Adopt in a consumer repository

Preview from a source checkout at a full pinned commit:

```sh
python3 tools/workflow/workflow.py setup --source /path/to/workflow-skills --revision FULL_40_CHAR_SHA --target /path/to/consumer --repository owner/name
```

Add `--apply` after reviewing the bounded changes. Unrelated instructions remain;
modified owned files conflict. Consumer config stays user-owned. Doctor and migration
inventory are read-only; see [operations](docs/operations.md) and
[migration/rollback](docs/migration-v1-v2.md). Source authoring uses .workflow/bundle.json;
consumers get generated install provenance. Skills have one canonical authored home:
.agents/skills/. Utility tests exercise real installed consumer paths.

## Acceptance boundary

Code/local checks and primary-author skill exercises do not establish fresh Cloud
skill discovery, Ubuntu portability, live Actions or merge protection. The rewrite
change stays active until required acceptance completes. PR/Issue evidence reports
implemented, locally verified, integration pending, ready for review, merged and
delivered distinctly. Merge/release/admin/global changes require separate authorization.
Historical v1 records under docs/planning, docs/lessons and docs/history are read-only
and cannot select execution. Original runtime/tests/specs are reachable at the
[recorded baseline](docs/migration-v1-v2.md); they are retired from current distribution.
