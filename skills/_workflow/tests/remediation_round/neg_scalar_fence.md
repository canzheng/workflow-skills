## Gate N

```yaml
findings:
  - id: F1
    title: t
    attribution: original
    guard: false
    class_sweep:
      shape: s
      command: rg -n x src/
      sites: ["a.py:1"]
    notes: |
      repro:
      ```
  - id: F2
    title: hidden by a naive scanner
    attribution: TBD
    guard: true
```
