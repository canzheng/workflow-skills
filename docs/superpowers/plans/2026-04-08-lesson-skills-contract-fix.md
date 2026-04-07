# Lesson Skills Contract Fix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the lesson workflow fully actionable and internally consistent by adding standalone lesson bootstrap, aligning schema and skill contracts, and fixing lifecycle rules across capture, promote, retrieve, record, and refresh.

**Architecture:** Keep the lesson system split into three layers: bootstrap scripts under `bin/`, schema files under `docs/lessons/`, and behavior contracts under `skills/`. The bootstrap layer seeds both lesson files and is wired into the workflow initializer, while the skills layer stays responsible for runtime behavior only. The lesson workflow should remain usable on its own, but the existing workflow initializer should also delegate to it so repos adopting the broader workflow get lessons for free.

**Tech Stack:** Bash, Python, Markdown, `unittest`

---

## File Structure

- Create: `bin/init-lessons.sh`
  - Standalone lesson bootstrap entrypoint.
  - Accepts the repo root from the caller's current working directory.
  - Seeds `docs/lessons/lessons.md` and `docs/lessons/lesson-candidates.md`.
  - Supports `--tools codex` for now.
- Modify: `skills/initialize-workflow-artifacts/scripts/init_workflow_artifacts.py`
  - Delegates lesson bootstrap to `bin/init-lessons.sh`.
- Modify: `docs/lessons/lessons-schema.md`
  - Changes `applied_count` to a float accumulator and aligns usage-count rules.
- Modify: `docs/lessons/lesson-candidates-schema.md`
  - Adds archive support for processed candidate records.
- Modify: `skills/capture-lessons/SKILL.md`
  - Makes direct promotion follow the same promotion rules as `promote-lessons`.
  - Removes `AGENTS.md` handling from this path.
- Modify: `skills/promote-lessons/SKILL.md`
  - Archives processed candidate records and removes `AGENTS.md` handling.
- Modify: `skills/retrieve-lessons/SKILL.md`
  - Keeps retrieval a pure selection step and leaves handoff state out of scope.
- Modify: `skills/record-lesson-usage/SKILL.md`
  - Switches usage recording to `lesson_id + applied status/value` and float counters.
- Modify: `skills/refresh-lessons/SKILL.md`
  - Makes refresh the only `AGENTS.md` path and expands merge/archive behavior.
- Add: `tests/test_lesson_contract_docs.py`
  - Locks in the lesson contract rules and bootstrap behavior.
- Modify: `tests/test_initialize_workflow_artifacts.py`
  - Verifies the workflow initializer delegates to lesson bootstrap.
- Add or modify: any lesson-specific test helpers if needed, but keep the scope narrow.

### Task 1: Add Standalone Lesson Bootstrap

**Files:**
- Create: `bin/init-lessons.sh`
- Modify: `skills/initialize-workflow-artifacts/scripts/init_workflow_artifacts.py`
- Test: `tests/test_initialize_workflow_artifacts.py`

- [ ] **Step 1: Write failing bootstrap tests**

Add tests that assert:
- the lesson initializer can run from a repo root without extra context
- it creates `docs/lessons/lessons.md`
- it creates `docs/lessons/lesson-candidates.md`
- it accepts `--tools codex`
- the workflow initializer calls the lesson bootstrap path

- [ ] **Step 2: Run the focused test target and confirm it fails**

Run: `python3 -m unittest tests.test_initialize_workflow_artifacts -v`
Expected: FAIL because the lesson bootstrap script and delegation path do not exist yet.

- [ ] **Step 3: Implement the minimal lesson bootstrap script**

Implement `bin/init-lessons.sh` so it:
- treats the caller's current working directory as the repo root
- creates `docs/lessons/lessons.md` as an empty file if missing
- creates `docs/lessons/lesson-candidates.md` as an empty file if missing
- accepts `--tools codex`
- rejects unsupported tool values for now

- [ ] **Step 4: Wire the existing workflow initializer into lesson bootstrap**

Update `skills/initialize-workflow-artifacts/scripts/init_workflow_artifacts.py` so lesson bootstrap is invoked during workflow initialization instead of being duplicated inline.

- [ ] **Step 5: Re-run the initializer test target**

Run: `python3 -m unittest tests.test_initialize_workflow_artifacts -v`
Expected: PASS

- [ ] **Step 6: Commit the bootstrap task**

```bash
git add bin/init-lessons.sh skills/initialize-workflow-artifacts/scripts/init_workflow_artifacts.py tests/test_initialize_workflow_artifacts.py
git commit -m "feat: add lesson bootstrap script"
```

### Task 2: Align Lesson Schemas With The New Lifecycle

**Files:**
- Modify: `docs/lessons/lessons-schema.md`
- Modify: `docs/lessons/lesson-candidates-schema.md`
- Add or modify: tests in `tests/test_lesson_contract_docs.py`

- [ ] **Step 1: Write schema contract tests first**

Add assertions that:
- `applied_count` is documented as a float accumulator
- `partially_applied` contributes a model-selected value from `0.1` to `0.9`
- `lessons.md` can be seeded as an empty file
- candidate records can be archived after processing

- [ ] **Step 2: Run the new contract test target and verify it fails**

Run: `python3 -m unittest tests.test_lesson_contract_docs -v`
Expected: FAIL because the schema text has not been updated yet.

- [ ] **Step 3: Update the promoted lesson schema**

Change `docs/lessons/lessons-schema.md` so:
- `applied_count` is a float, not an integer
- counting rules explicitly allow `applied = 1.0`, `not_applied = 0.0`, and `partially_applied = 0.1-0.9`
- any other counter semantics remain unchanged

- [ ] **Step 4: Update the candidate schema**

Change `docs/lessons/lesson-candidates-schema.md` so:
- candidate records support an archived lifecycle state
- the archive state is explicit in the schema, not implied

- [ ] **Step 5: Re-run the contract tests**

Run: `python3 -m unittest tests.test_lesson_contract_docs -v`
Expected: PASS for the schema-specific assertions

- [ ] **Step 6: Commit the schema task**

```bash
git add docs/lessons/lessons-schema.md docs/lessons/lesson-candidates-schema.md tests/test_lesson_contract_docs.py
git commit -m "docs: align lesson schemas"
```

### Task 3: Make Capture And Promote Share One Promotion Policy

**Files:**
- Modify: `skills/capture-lessons/SKILL.md`
- Modify: `skills/promote-lessons/SKILL.md`
- Modify: `tests/test_lesson_contract_docs.py`

- [ ] **Step 1: Write contract tests for promotion behavior**

Add assertions that:
- direct promotion in `capture-lessons` follows the same rules as `promote-lessons`
- neither skill writes to `AGENTS.md`
- promoted lessons still use the promoted lesson schema exactly
- processed candidate records are archived after promotion

- [ ] **Step 2: Run the contract tests and verify they fail**

Run: `python3 -m unittest tests.test_lesson_contract_docs -v`
Expected: FAIL because the skill docs still describe the old behavior.

- [ ] **Step 3: Update `capture-lessons`**

Make the direct-promotion path:
- use the same promotion rules as `promote-lessons`
- validate duplicates and overlaps before writing
- initialize promoted entries using the promoted schema defaults
- stop describing any `AGENTS.md` write path

- [ ] **Step 4: Update `promote-lessons`**

Make `promote-lessons`:
- archive the source candidate record after it is processed
- keep `AGENTS.md` out of the promotion path
- keep the existing promotion threshold and merge behavior unless the candidate lifecycle rule requires a wording update

- [ ] **Step 5: Re-run the contract tests**

Run: `python3 -m unittest tests.test_lesson_contract_docs -v`
Expected: PASS for the promotion-policy assertions

- [ ] **Step 6: Commit the promotion-policy task**

```bash
git add skills/capture-lessons/SKILL.md skills/promote-lessons/SKILL.md tests/test_lesson_contract_docs.py
git commit -m "docs: unify lesson promotion policy"
```

### Task 4: Make Retrieval And Usage Recording Self-Contained

**Files:**
- Modify: `skills/retrieve-lessons/SKILL.md`
- Modify: `skills/record-lesson-usage/SKILL.md`
- Modify: `tests/test_lesson_contract_docs.py`

- [ ] **Step 1: Write contract tests for retrieval and usage**

Add assertions that:
- `retrieve-lessons` remains a pure selection step
- `record-lesson-usage` consumes `lesson_id` plus applied status/value
- `record-lesson-usage` updates `applied_count` as a float
- `last_applied_at` changes only for `applied` and `partially_applied`

- [ ] **Step 2: Run the contract tests and verify they fail**

Run: `python3 -m unittest tests.test_lesson_contract_docs -v`
Expected: FAIL because the skill docs still describe the old integer-count contract.

- [ ] **Step 3: Update `retrieve-lessons`**

Keep it as the retrieval step only:
- select up to 3 active lessons
- return the chosen lessons
- update retrieval metadata only for those lessons
- do not introduce a separate handoff artifact

- [ ] **Step 4: Update `record-lesson-usage`**

Make it:
- consume `lesson_id` plus applied status/value at task end
- increment `applied_count` with float semantics
- treat `partially_applied` as a model-provided value from `0.1` to `0.9`
- update `last_applied_at` only when the value is non-zero

- [ ] **Step 5: Re-run the contract tests**

Run: `python3 -m unittest tests.test_lesson_contract_docs -v`
Expected: PASS for the retrieval/usage assertions

- [ ] **Step 6: Commit the retrieval/usage task**

```bash
git add skills/retrieve-lessons/SKILL.md skills/record-lesson-usage/SKILL.md tests/test_lesson_contract_docs.py
git commit -m "docs: simplify lesson retrieval usage flow"
```

### Task 5: Make Refresh Own AGENTS.md, Merge, And Stale-Archive Behavior

**Files:**
- Modify: `skills/refresh-lessons/SKILL.md`
- Modify: `tests/test_lesson_contract_docs.py`

- [ ] **Step 1: Write contract tests for refresh behavior**

Add assertions that:
- only `refresh-lessons` owns the `AGENTS.md` path
- stale means not applied for 30 days
- refresh can merge similar lessons
- refresh can archive stale lessons
- merged lessons combine counters and timestamps as specified

- [ ] **Step 2: Run the contract tests and verify they fail**

Run: `python3 -m unittest tests.test_lesson_contract_docs -v`
Expected: FAIL because the refresh rules are still narrower than the desired contract.

- [ ] **Step 3: Update `refresh-lessons`**

Make refresh:
- the only skill that can update `AGENTS.md`
- able to merge similar lessons
- able to archive lessons stale for 30 days
- limited to merge/archive/AGENTS handling otherwise, with no unrelated field churn

- [ ] **Step 4: Define merge semantics precisely**

When merging lessons, the surviving lesson should absorb:
- `lesson`
- `applies_when`
- `confidence`
- `source_evidence`
- `applied_count`
- `retrieved_count`
- `last_retrieved_at`
- `last_applied_at` using the later timestamp
- `updated_at`

The merged-into lesson should be archived.

- [ ] **Step 5: Re-run the contract tests**

Run: `python3 -m unittest tests.test_lesson_contract_docs -v`
Expected: PASS for the refresh assertions

- [ ] **Step 6: Commit the refresh task**

```bash
git add skills/refresh-lessons/SKILL.md tests/test_lesson_contract_docs.py
git commit -m "docs: expand lesson refresh lifecycle"
```

### Task 6: Verify The Full Lesson Contract And Repo Hygiene

**Files:**
- Test: `tests/test_lesson_contract_docs.py`
- Test: `tests/test_initialize_workflow_artifacts.py`
- Test: `tests/test_workflow_contract_docs.py` if it needs a small lesson-related addition

- [ ] **Step 1: Run the narrow lesson contract test suite**

Run: `python3 -m unittest tests.test_lesson_contract_docs tests.test_initialize_workflow_artifacts -v`
Expected: PASS

- [ ] **Step 2: Run patch hygiene checks**

Run: `git diff --check`
Expected: PASS

- [ ] **Step 3: Check for accidental local-path leakage**

Run: `git status --short`
Expected: only the intended lesson bootstrap, schema, skill, and test files are changed

- [ ] **Step 4: Commit the final verification pass**

```bash
git add docs/lessons bin skills tests
git commit -m "test: lock in lesson skill contract"
```

## Notes

- Keep the lesson bootstrap separate from the broader workflow bootstrap, but let the workflow initializer call it so repos adopting the workflow get lessons seeded automatically.
- Treat `docs/lessons/lessons.md` as the promoted-lesson store and `docs/lessons/lesson-candidates.md` as the candidate queue, with archive support in the candidate schema rather than a separate archive file.
- Avoid reintroducing `AGENTS.md` writes in `capture-lessons` or `promote-lessons`; `refresh-lessons` owns that policy.
- Keep the plan scoped to the lesson system contract. Do not expand into unrelated workflow or feature-management changes while implementing this fix.
