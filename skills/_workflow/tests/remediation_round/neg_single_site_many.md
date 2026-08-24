## Gate N

```yaml
findings:
  - {id: F1, title: t, attribution: original, guard: false,
     class_sweep: {single_site: it is the only place this can occur, command: "rg -n x src/",
                   sites: ["a.py:1", "b.py:2"]}}
```
