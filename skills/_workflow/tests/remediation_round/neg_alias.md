## Gate N

```yaml
base: &b {shape: s, command: "rg -n x src/", sites: ["a.py:1"]}
findings:
  - {id: F1, title: t, attribution: original, guard: false, class_sweep: *b}
  - {id: F2, title: u, attribution: original, guard: false, class_sweep: *b}
```
