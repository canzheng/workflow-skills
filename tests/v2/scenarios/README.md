# Workflow scenario corpus

These fixtures exercise outcomes, not universal model reliability. Run
`python3 tools/workflow/verify.py`; `npm ci --ignore-scripts` enables actual
OpenSpec fixture validation/archive. `test_scenarios.py` installs the real pinned
production bundle and executes its checker/consumer paths. Source bundle inputs
must be committed before that test; uncommitted bundle bytes correctly conflict.

| Input / cases | Expected outcome | Prohibited outcome | Procedure / evidence |
| --- | --- | --- | --- |
| shaping/design.md (S08/S09) | Bounded subtotal/receipt candidates; retention decision isolated | Execute unapproved candidates or include excluded sync/dashboard | Read shaping skill; inspect candidate artifacts in skill-evaluations |
| initial-backlog/design.md (S33) | One MVP outcome batch, one approval, two independent Ready catalogs; unknown/dependent backlog/blocked; stable reruns | Per-Issue invocation, engineering-task explosion, later-scope execution, duplicate IDs or implementation dispatch | test_initial_backlog + primary-author output.json; real consumer/Cloud pilot separate |
| delivery/prompts.md + before/after/repaired (S10/S11/S12/S14) | 697 bug restoration; 747 shipping; accurate defaults/errors; justified no-impact for repair | Per-task ledger/plan/reviewer requirement; stale shipping guidance accepted | Read deliver skill, implement artifacts, run test_delivery/test_scenarios |
| delivery/contradiction.md (S13) | Report exact default contradiction and correct docs | Count a Markdown edit as semantic completion | Compare code default 0 with stated 50; record primary-author finding |
| risk/protocol.py (S19/S20/S21/S30) | Detect wrong formula, ignored currency, weakened subtotal | Parser-only or weakened assertion declared proof | Read risk skill, run test_risk; inspect intended negative reasons |
| Git/setup/check snapshots (S01–S07/S16/S18/S22/S23/S26–S28/S31) | Explicit targets, rollback, preserved edits, safe metadata, pending gates | Cwd fallback, fabricated write/enforcement, metadata execution | Run public CLIs via test_setup/test_checks/test_handoff/test_records |
| OpenSpec receipt fixture (S15/S24) | Partial work active; final actual archive and validated current spec | Early archive or duplicate plan | test_openspec with pinned CLI |
| v1 inventories (S04/S25/S32) | Done retained as history; active dispositions and findings | Recreate Done Issues or guess missing records | test_migration added with F12 |
| fresh Cloud / Ubuntu (S02/S17/S29/S31) | Actual discovery, same-SHA portability and observed settings | Count local directory/fixtures as environment acceptance | F14 procedure; record pending until actually run |
| pinned dependency clones (S34) | Shared namespaces ignored/untracked; exact-pin bootstrap preserves project files/index, then no-op | Fetch latest, hide pin in environment, ignore project skills, overwrite local dependency edits | test_dependency_bootstrap; real CI/Cloud/Ubuntu proof recorded separately |

Host/manual evaluation procedure: start a fresh authorized session, provide fixture
prompt and skill path, inspect actual outputs against expected and prohibited results,
run code proof and record environment/model, revision/content, commands/results,
authorship, doc impact, blockers and next action. Do not store live backlog status
in this corpus. Proposed evaluations and actual in-turn runs are distinguished in
docs/validation/skill-evaluations.md; Cloud/Ubuntu gaps stay in v2-acceptance.md.
