## Gate N

```yaml
findings:
  - {id: F1, title: a real finding, attribution: original work, guard: false,
     class_sweep: {shape: s, sites: ["a.py:1"], command: "rg -n x src/"}}
```

And a second block where something could hide:

```yaml
findings:
  - {id: F2, title: hidden, attribution: TBD, guard: true}
```
