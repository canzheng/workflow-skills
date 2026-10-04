# S33 one-shot initial MVP backlog

Fresh repository input: design.md plus installed repository workflow/config; no
application implementation or specs. Initial request: "Create the MVP backlog from
this design." Second interaction approves the entire candidate batch once and says
"Do not implement it." This is one shaping run and its approval continuation, not
one invocation per Issue. Expected output artifacts: output.json is an immutable
primary-author candidate artifact with logical IDs, not a live backlog/database.
GitHub snapshot numbers in tests are explicitly simulated, never remote claims.

Expected: five bounded outcome/decision Issues; preserve explicit catalog acceptance;
link relevant design sections; represent direct dependencies; two independent catalog
outcomes become Ready after approval, while unresolved dietary input and dependent
planning/export remain backlog/blocked. No later-scope/coding-task Issues, no duplicated
intermediate capability document, no application code, execution claim or new branch/PR.
Before approval all published candidates are backlog. No remote creation is authorized
by this fixture exercise; actual consumer publication is a separately authorized pilot.

Evolved-design rerun: rename a section/title while retaining logical identity, expand
only genuinely new approved outcome scope, preserve a human acceptance amendment,
reuse closed matches without reopening them and surface contradictory human/design
acceptance or duplicates. Reconcile timeout/partial success before retry.

Run test_initial_backlog via verify.py for actual pinned setup and native snapshot
helper proof. Semantic batch shaping is a primary-author evaluation unless a fresh
host/model actually runs this prompt. For a host pilot, publish using native GitHub
operations, resolve candidate dependency IDs to confirmed Issue URLs and record
actual repository/Issue identities, phases, one approval and zero execution. Test a
rerun preserving a real human edit when authorized; do not introduce a sync engine.
Capture actual skill discovery/read calls and outputs. Do not substitute these
fixtures for live GitHub, a separate fresh Cloud task or Ubuntu agent-host discovery.
