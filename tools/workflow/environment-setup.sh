#!/usr/bin/env bash
# Source-owned Ubuntu/local entrypoint; Cloud use is optional. Intentionally excluded from the consumer bundle.
set -eu
if [ "$#" -ne 2 ]; then
    echo 'Usage: bash environment-setup.sh /absolute/consumer/git/root owner/repository' >&2
    exit 2
fi
WF2_SOURCE_ROOT=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd -P)
WF2_CONSUMER_ROOT=$1
WF2_CONSUMER_REPOSITORY=$2
python3 -c 'import sys; assert sys.version_info >= (3, 10), "Python >=3.10 is required"; print(sys.version.split()[0])'
git --version
python3 - "$WF2_SOURCE_ROOT" "$WF2_CONSUMER_ROOT" "$WF2_CONSUMER_REPOSITORY" <<'PY'
import pathlib, re, sys
sys.dont_write_bytecode = True
sys.path.insert(0, str(pathlib.Path(sys.argv[1]) / 'tools/workflow'))
from core import Invalid, config, repository, safe
if not pathlib.Path(sys.argv[2]).is_absolute():
    sys.exit('Target must be an explicit absolute Git root')
if not re.fullmatch(r'[\w.-]+/[\w.-]+', sys.argv[3]):
    sys.exit('Repository identity must be owner/repository')
try:
    root = repository(sys.argv[2])
    if safe(root, '.workflow/install-manifest.json').exists() or safe(root, '.workflow/config.json').exists():
        if config(root)['repository'] != sys.argv[3]:
            sys.exit('Repository identity mismatch; refusing setup/bootstrap for a different project')
except Invalid as exc:
    sys.exit(str(exc))
PY
cd -- "$WF2_CONSUMER_ROOT"
if [ ! -f .workflow/install-manifest.json ]; then
    WF2_SOURCE_SHA=$(git -C "$WF2_SOURCE_ROOT" rev-parse --verify 'HEAD^{commit}')
    python3 "$WF2_SOURCE_ROOT/tools/workflow/workflow.py" setup --source "$WF2_SOURCE_ROOT" --revision "$WF2_SOURCE_SHA" --target "$PWD" --repository "$WF2_CONSUMER_REPOSITORY" --json
    python3 "$WF2_SOURCE_ROOT/tools/workflow/workflow.py" setup --source "$WF2_SOURCE_ROOT" --revision "$WF2_SOURCE_SHA" --target "$PWD" --repository "$WF2_CONSUMER_REPOSITORY" --apply --json
fi
python3 -c 'import json, pathlib, sys; m=json.loads(pathlib.Path(".workflow/install-manifest.json").read_text(encoding="utf-8")); sys.exit(0 if m.get("schema_version") in (3, 4, 5) else "Existing adoption needs reviewed setup/update; do not migrate during environment startup")'
python3 "$WF2_SOURCE_ROOT/tools/workflow/workflow.py" bootstrap --repo . --apply --json
WF2_CONSUMER_CLI=$(python3 -c 'import json; m=json.load(open(".workflow/install-manifest.json")); print(".agents/tools/workflow/workflow.py" if ".agents/tools/workflow/workflow.py" in m["files"] else "tools/workflow/workflow.py")')
python3 "$WF2_CONSUMER_CLI" check --repo . --run-local --json
python3 "$WF2_CONSUMER_CLI" doctor --repo . --json
git --no-optional-locks status --short --untracked-files=all
