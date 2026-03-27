## Context

The user direction narrows the installer behavior clearly:
- if target `AGENTS.md` is missing, installation should fail
- if `AGENTS.md` exists but lacks workflow markers, installation should append the managed section as initialization

The environment problem is separate but adjacent: the repo uses Python syntax that requires a newer interpreter, while `environment.yml` leaves Python and Conda channels unconstrained. That weakens reproducibility for both local development and the wrapper script.

## Goals / Non-Goals

**Goals:**
- Make installer initialization behavior explicit and tested.
- Preserve failure on missing target `AGENTS.md`.
- Make the managed Conda environment declare a compatible Python floor and explicit channels.
- Document the installer's `rsync` dependency where contributors will see it.

**Non-Goals:**
- Redesign the installer beyond marker initialization behavior.
- Replace Conda with a different environment manager.
- Turn the repo into a generic package installer.

## Decisions

### Decision: Distinguish missing-file failure from missing-marker initialization
Those are separate states and should not be handled the same way. Missing `AGENTS.md` is still a hard failure; missing markers inside an existing file is an initialization path.

### Decision: Keep the environment contract explicit in tracked metadata
The repo should state the Python floor and channels in `environment.yml` instead of depending on contributor-local Conda defaults.

### Decision: Treat installer dependency documentation as part of the capability
If `install.sh` requires `rsync`, that requirement belongs in the repo's documented tooling contract, not only in the script implementation.

## Risks / Trade-offs

- [Marker initialization could duplicate the managed block] -> Make the append path insert exactly one managed section and keep the existing replace-in-place path for files that already have markers.
- [Conda constraints can be slightly more prescriptive] -> Use a minimal explicit Python floor and the standard channel set needed for reproducibility.
- [Docs/tests can drift from installer behavior] -> Add focused coverage for both missing-file and missing-marker paths.

## Migration Plan

1. Update installer control flow for missing markers versus missing files.
2. Document the dependency and initialization behavior in repo docs.
3. Constrain the tracked Conda environment.
4. Add regression coverage.

## Open Questions

- None.
