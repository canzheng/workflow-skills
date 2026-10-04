# Proportional specifications

Pin @fission-ai/openspec 1.14.0 in package.json/package-lock.json. Registry metadata
requires Node >=20.19.0; tested here with Node 24.19.0 and OpenSpec 1.14.0.
Node is unnecessary for offline utility tests; optional spec tests explicitly report
skipped when the pinned local CLI is absent. Required spec acceptance stays pending.

```sh
npm ci --ignore-scripts
node_modules/.bin/openspec validate workflow-v2-rewrite --strict --no-interactive
node_modules/.bin/openspec validate --specs --strict --no-interactive
```

A small repair to an existing clear contract needs no new change, but inaccurate
current specs still need edits. Substantial contracts, cross-module protocols,
migration/security or expensive ambiguity need one change-owned proposal/design/
tasks/deltas. A multi-PR change names its closing Issue; partial PRs use Refs and
cannot archive incomplete scope. Do not duplicate its plan under docs/plans or
per-task folders. A non-OpenSpec long-running effort may have one optional plan.

After the closing owner confirms full required acceptance, sync current contracts
and run `node_modules/.bin/openspec archive CHANGE_ID --yes` in the delivering
branch, then rerun spec/docs checks on the archive diff. The CLI validates structure;
it cannot establish product completion or independent review. The skill/contract
prevents premature archive; do not claim that CLI flags enforce environmental gates.
Archive is not merge. Pending environment acceptance keeps the rewrite active.
The disposable receipt fixture executes actual validation/archive without changing
this repository's active rewrite. OpenSpec apply is allowed within authorized scope.
