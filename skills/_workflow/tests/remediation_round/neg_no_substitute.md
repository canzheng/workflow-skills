## Gate N

```yaml
findings:
  - {id: F1, title: t, attribution: original, guard: true,
     class_sweep: {shape: s, sites: ["a.py:1"], command: "rg -n x src/"},
     mutants: {revert: delete the assertion}}
```
