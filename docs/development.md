# Development

Runtime: Python >=3.10 and Git. Tested: Python 3.12.14 on Debian 13 and Python 3.12.3 on Ubuntu 24.04. No Conda,
Node, global AGENTS/skills or GitHub token is needed for offline verification.
The required runner uses Python's standard library. The optional pytest runner
and its dependencies are pinned in requirements.txt; never substitute an
unrelated interpreter if the selected environment is missing.

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

## Cloud preparation
Use the current host environment preparation UI to run the three commands above.
At task start verify branch/SHA, dependency definitions and installed versions;
published environments may retain prepared dependencies after repository changes.
This execution is a /workspace task checkout, not a proven fresh published Cloud
skill-discovery session. Current platform guide retrieval was attempted but the
network proxy returned HTTP 403; no legacy cache or secret lifetime is assumed.
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

This source repository authors and tracks the shared skills. Consumers track project
policy/config/utilities/CI/docs and a dependency pin, and materialize only three ignored
shared-skill namespaces. Their repeatable environment command is:

```sh
python3 tools/workflow/workflow.py bootstrap --repo . --apply --json
```

Run it after checkout and before agent discovery in the actual host preparation hook,
then the consumer's declared check/doctor commands. Repeat for branch/pin changes;
the source-owned setup entrypoint may have its own pinned fetch revision, but it
must never override an adopted consumer dependency pin. See the README for the
complete Cloud install-script/local fetch-and-run command. See [operations](operations.md)
for initial adoption, explicit untracking of old shared skills and conflict recovery.
Source contributors do not run consumer bootstrap here: there is no consumer pin.
