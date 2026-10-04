# Workflow development

Python >=3.10 and Git run the installed utilities without Conda or global skills.
Run `python3 tools/workflow/workflow.py check --repo .` for bundle/config/link
checks, and the application verification commands declared in .workflow/config.json.
The generated default checks only the workflow bundle; add real application test
commands before accepting application delivery. Arguments are arrays, never shell
strings. Node/OpenSpec are optional until a relevant spec check is required.
