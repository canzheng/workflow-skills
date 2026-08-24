## Gate N

A prose schema example that must be inert:

```
findings:
  - id: EXAMPLE
```

```yaml
findings:
  - id: F1
    title: null_driver re-derives a view oos_tune already returned
    attribution: gate-14 fix (incomplete)
    guard: true
    class_sweep:
      shape: a caller re-deriving a view the producer already returned
      command: grep -rn "common_calendar(" .local/research/ backtest/
      sites: ["fair_tuning.py:229", "t9_screen.py:39", "null_driver.py:77"]
    mutants:
      revert: drop the apply_warmup_trim call in oos_tune
      substitute: trim with hold instead of hold minus one
  - id: F2
    title: a stale premium quoted from a pre-gate-13 log
    attribution: original work
    guard: false
    class_sweep:
      single_site: the value appears exactly once in tracked prose
      command: grep -rn "0.5839" docs/
      sites: ["docs/findings/v1-f047.md:386"]
```
