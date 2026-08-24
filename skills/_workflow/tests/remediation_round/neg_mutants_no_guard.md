## Gate N

```yaml
findings:
  - id: F1
    title: a prose-only finding that carries mutants it does not need
    attribution: original work
    guard: false
    class_sweep:
      single_site: the value appears exactly once in tracked prose
      command: grep -rn "0.5839" docs/
      sites: ["docs/findings/v1-f047.md:386"]
    mutants:
      revert: drop the apply_warmup_trim call in oos_tune
      substitute: trim with hold instead of hold minus one
```
