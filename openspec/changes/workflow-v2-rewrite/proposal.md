# Workflow Skills v2 rewrite

Acceptance refinement approved by the user on 2026-10-05: Ubuntu workstation
discovery/use and portability replace mandatory Cloud acceptance. Cloud is deferred;
no merge, release, administration or global-change authority is added.

## Why
Replace local v1 lifecycle machinery with repository-scoped skills and GitHub delivery.

## What Changes
Implement the approved [design](../../../docs/v2/v2-design.md),
[capabilities](../../../docs/v2/v2-capability-map.md) and
[WF2-F01–F14 acceptance](../../../docs/v2/v2-feature-list.md).
This change owns the whole bounded rewrite; WF2-F14 is its closing owner.
No intermediate feature archives it. Required environment acceptance is pending.

## Impact
Repository routing, portable utilities, three skills, GitHub templates/checks,
current docs/specs, migration and retirement. No merge/release/admin/global changes.
