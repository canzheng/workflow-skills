# Development

Runtime: Python >=3.10 and Git. Installation mutations require Linux libc/kernel
and filesystem support for renameat2 exchange/no-replace, accessed through the
standard-library ctypes module; unsupported operations fail without an unsafe
overwrite fallback. No additional Python package is required. Private capture storage must share the
target filesystem (repository Git directory, or same-filesystem TMPDIR for explicit
shared-only installs). Captured files and empty private directories are retained; see operations for
recovery and manual-cleanup guidance.
 Tested: Python 3.12.14 on Debian 13 and Python 3.12.3 on Ubuntu 24.04. No Conda,
Node, global AGENTS/skills or GitHub token is needed for offline verification.
The required runner uses Python's standard library. The optional pytest runner
and its dependencies are pinned in requirements.txt; never substitute an
unrelated interpreter if the selected environment is missing.

Source development verification requires the full Git history, including recorded
baseline `d2aaf1904b2ccbe7fbab9733627e9c82fcf12f53`. Migration/retirement tests inspect
that tree and clone the source history; a shallow checkout can otherwise fail two
required tests. Before running the suite, fetch history when the source is shallow:

```sh
if [ "$(git rev-parse --is-shallow-repository)" = true ]; then
    git fetch --unshallow origin
fi
git cat-file -e 'd2aaf1904b2ccbe7fbab9733627e9c82fcf12f53^{commit}'
```

History preparation needs remote read access. Once present, the standard-library
suite runs offline. Consumer adoption/update uses an exact pinned source
fetch; repeat verification needs no fetch or source retirement suite. Source CI checks out full history.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python tools/workflow/verify.py
```

Offline equivalent: `python3 tools/workflow/verify.py`. Rerun installation after
requirements changes, then capture `python3 --version` and installed versions.
The entrypoint rejects an empty suite and propagates required failures.
tests/v2 is the required suite. Old root tests and skills/_workflow/tests are
retired, with disposition and ported safety outcomes documented in the migration
report. They are preserved in Git, not silently counted as v2 passes.

The user's Ubuntu26.04/Python3.13.13/codex-cli0.160.0 workstation separately passed
consumer bootstrap/checks, native discovery and actual skill use. Its source-suite
run reported an intermittent invalid-JSON helper error and two absent-pinned-tool
OpenSpec skips; it is not a full source-suite pass on Ubuntu26.04. The prepared
Ubuntu24.04.5 runtime-layout/index repair at9f3f1bd61ab017c570df3bc48a7e84a6947a9a7f passes146/no skips. See [session evidence](validation/ubuntu-workstation-session.md).

## Optional Cloud preparation
Use the current host environment preparation UI to run the three commands above.
At task start verify branch/SHA, dependency definitions and installed versions;
published environments may retain prepared dependencies after repository changes.
This execution is a /workspace task checkout, not a proven fresh published Cloud
skill-discovery session. Current platform guide retrieval was attempted but the
network proxy returned HTTP 403; no legacy cache or secret lifetime is assumed.
Cloud discovery is deferred for this first release. Use the [Ubuntu workstation
procedure](validation/ubuntu-workstation-handoff.md) for required F14 acceptance.
Host GitHub tools and gh authentication are separate capabilities. An unavailable
write must not stop local work or be described as a successful publication.

Node/OpenSpec are optional for offline runtime checks; the full rewrite acceptance
also requires the pinned specification checks below.

## Optional OpenSpec verification
Install pinned local tooling with `npm ci --ignore-scripts` (Node >=20.19.0).
Tested Node 24.19.0, npm 11.9.0, OpenSpec 1.14.0. See
[specification procedure](workflow/openspec.md). Disable telemetry only for commands:
`OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 node_modules/.bin/openspec validate workflow-v2-rewrite --strict --no-interactive`.
No global OpenSpec configuration is changed. Actual environment results and versions
are in [acceptance evidence](validation/v2-acceptance.md).

## Consumer preparation versus source authoring

Source canonical skills remain tracked. Consumers track project policy/config,
CI/docs/project skills and schema-5 provenance; shared skills and
.agents/tools/workflow runtime are ignored dependencies. Fetch the tracked pin and
run the source-owned entrypoint before using a fresh consumer clone.
Run installed exact-pin bootstrap before launching Ubuntu Codex at the consumer root:

```sh
python3 .agents/tools/workflow/workflow.py bootstrap --repo . --apply --json
python3 .agents/tools/workflow/workflow.py check --repo . --run-local --json
python3 .agents/tools/workflow/workflow.py doctor --repo . --json
```

Fresh clones fetch only the recorded source commit if dependency files are missing;
complete matching reruns are offline/no-op. Optional --source allows offline source
materialization. Project files/index/pin remain unchanged; dependency edits conflict.
[Operations](operations.md) covers explicit tracked-to-ignored migration and optional
global shared-only installation. Required Ubuntu discovery/use is a fresh-session
gate independent of hashes and CI. Cloud is deferred. Source authoring uses bundle.json.

Source bundle verification uses the same layout-aware required inventory as setup.
Complete legacy tracked compatibility bundles remain verifiable; missing runtime
modules and mixed legacy/new inventories are rejected. This does not permit legacy
runtime layouts for ignored schema-5 installations.
