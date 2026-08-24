## Gate N

```yaml
findings:
  - {id: F1, title: "guard asserts a < b and c > d", attribution: original, guard: false,
     class_sweep: {shape: "returns Optional<str> not str", command: "rg -n \"is None\" src/",
                   sites: ["parser.py:12 (in <listcomp>)"]}}
```
