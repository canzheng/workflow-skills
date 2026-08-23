from __future__ import annotations

import sys
from pathlib import Path


for _candidate in Path(__file__).resolve().parents:
    if (_candidate / "_workflow").is_dir():
        if str(_candidate) not in sys.path:
            sys.path.insert(0, str(_candidate))
        break


# `test_audit_checks.py` and `mutate_audit_checks.py` are self-running SCRIPTS, not pytest modules:
# their checks execute at import and `sys.exit(1)` on failure, which pytest would surface as a
# collection error rather than a test failure. Run them directly:
#   bin/run-python.sh skills/_workflow/tests/test_audit_checks.py
#   bin/run-python.sh skills/_workflow/tests/mutate_audit_checks.py
collect_ignore = ["test_audit_checks.py", "mutate_audit_checks.py"]
