## Context

The human-facing docs consistently say `Current Task` must be a raw top-level ID such as `1`, but the parser currently just returns whatever string is present unless it is `none`. That means malformed metadata is not stopped early even though downstream task parsing only understands top-level OpenSpec task IDs.

## Goals / Non-Goals

**Goals:**
- Enforce the documented `Current Task` contract mechanically.
- Surface invalid subtask-style values as workflow errors.
- Keep valid top-level IDs and `none` behavior unchanged.

**Non-Goals:**
- Change the OpenSpec task format itself.
- Introduce richer feature-file task metadata.

## Decisions

### Decision: Validate `Current Task` at the workflow helper layer
The shared parser is the narrowest and most reusable place to enforce the rule.

### Decision: Treat subtask IDs as invalid workflow metadata
Values like `1.1` should fail workflow checks instead of being silently tolerated.

## Risks / Trade-offs

- [Existing malformed fixtures may start failing] -> Update tests to make the documented constraint explicit.
- [Helpers need a slightly richer parse result] -> Keep validation narrow and focused on the accepted ID shape.

## Migration Plan

1. Add shared validation for `Current Task`.
2. Surface the validation through audit and diagnosis.
3. Add coverage for valid and invalid values.

## Open Questions

- None.
