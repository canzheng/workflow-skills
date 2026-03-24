# Feature: <title>

Create this file only when a backlog item moves from `[BACKLOG]` to `[SHAPING]`.

## 0. Meta
- Feature ID: `v1-f001`
- Version: `v1`
- Backlog Reference: `<link or anchor>`
- OpenSpec Change: `<change-id>`
- OpenSpec Specs:
  - `openspec/specs/<capability>/spec.md`
- Current Task: `none`
  - Use `none` when no task is actively executing, including handoff gaps inside an `[IN_PROGRESS]` feature.
- Created: `YYYY-MM-DD`
- Last Updated: `YYYY-MM-DD`

## 1. Execution Scope
- Objective:
  - <execution target linked to the OpenSpec change>
- In Scope Files:
  - `<path/to/file>`
- Out of Scope:
  - <out-of-scope item>
- Constraints:
  - <constraint>
- Shaping Source:
  - `openspec/changes/<change-id>/proposal.md`
  - `openspec/changes/<change-id>/design.md`
  - `openspec/changes/<change-id>/tasks.md`

## 2. Tasks

Task status lives here. OpenSpec owns shaping artifacts; this file owns execution status, readiness, and evidence.

### T01: <title>
- Status: `todo`
- OpenSpec Task Reference:
  - `openspec/changes/<change-id>/tasks.md#task-group`
- Objective:
  - <what this task changes>
- Depends On:
  - none
- Scope:
  - `<path/to/file>`
- Constraints:
  - <constraint>
- Acceptance Criteria:
  - [ ] <observable outcome>
- Validation:
  - Run: `<command or inspection step>`
  - Expect: `<expected result>`
- Evidence:
  - Not run yet

---

### T02: <title>
- Status: `todo`
- OpenSpec Task Reference:
  - `openspec/changes/<change-id>/tasks.md#task-group`
- Objective:
  - <what this task changes>
- Depends On:
  - `T01`
- Scope:
  - `<path/to/file>`
- Constraints:
  - <constraint>
- Acceptance Criteria:
  - [ ] <observable outcome>
- Validation:
  - Run: `<command or inspection step>`
  - Expect: `<expected result>`
- Evidence:
  - Not run yet

## 3. Validation Log
- `<YYYY-MM-DD>` Task `<task-id>`:
  - Run: `<command or inspection step>`
  - Result: `<pass/fail and notable details>`

## 4. Change Log
- `<YYYY-MM-DD>`:
  - <summary of workflow state, task sync, or evidence update>
