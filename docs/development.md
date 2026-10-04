# Development

Runtime: Python >=3.10 and Git. Tested here: Python 3.12.14. No Conda,
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
During transition only tests/v2 is the v2 suite. The old root tests and
skills/_workflow/tests assert retired v1 lifecycle behavior and are not counted
as v2 passes; safety outcomes are ported before F13 removes these tests.

## Cloud preparation
Use the current host environment preparation UI to run the three commands above.
At task start verify branch/SHA, dependency definitions and installed versions;
published environments may retain prepared dependencies after repository changes.
This execution is a /workspace task checkout, not a proven fresh published Cloud
skill-discovery session. Current platform guide retrieval was attempted but the
network proxy returned HTTP 403; no legacy cache or secret lifetime is assumed.
Host GitHub tools and gh authentication are separate capabilities. An unavailable
write must not stop local work or be described as a successful publication.

Node/OpenSpec are optional until spec validation is selected at F07.
