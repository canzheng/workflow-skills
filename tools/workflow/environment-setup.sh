#!/usr/bin/env bash
# Source-owned Cloud/local entrypoint. Intentionally excluded from the consumer bundle.
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
python3 - "$WF2_CONSUMER_ROOT" <<'PY'
import pathlib, subprocess, sys
p = pathlib.Path(sys.argv[1])
if not p.is_absolute() or not p.is_dir() or p.is_symlink():
    sys.exit('Target must be an explicit existing absolute Git root, not a symlink')
r = subprocess.run(['git', '-C', str(p), 'rev-parse', '--show-toplevel'], capture_output=True, text=True)
if r.returncode or pathlib.Path(r.stdout.strip()).resolve() != p.resolve():
    sys.exit('Target must be the Git root; refusing missing or nested checkout')
PY
cd -- "$WF2_CONSUMER_ROOT"
if [ ! -f .workflow/install-manifest.json ]; then
    WF2_SOURCE_SHA=$(git -C "$WF2_SOURCE_ROOT" rev-parse --verify 'HEAD^{commit}')
    python3 "$WF2_SOURCE_ROOT/tools/workflow/workflow.py" setup --source "$WF2_SOURCE_ROOT" --revision "$WF2_SOURCE_SHA" --target "$PWD" --repository "$WF2_CONSUMER_REPOSITORY" --json
    python3 "$WF2_SOURCE_ROOT/tools/workflow/workflow.py" setup --source "$WF2_SOURCE_ROOT" --revision "$WF2_SOURCE_SHA" --target "$PWD" --repository "$WF2_CONSUMER_REPOSITORY" --apply --json
fi
python3 -c 'import json, pathlib, sys; m=json.loads(pathlib.Path(".workflow/install-manifest.json").read_text(encoding="utf-8")); sys.exit(0 if m.get("schema_version")==2 else "Existing adoption needs reviewed dependency migration; do not overwrite it during environment setup")'
python3 tools/workflow/workflow.py bootstrap --repo . --apply --json
python3 tools/workflow/workflow.py check --repo . --run-local --json
python3 tools/workflow/workflow.py doctor --repo . --json
git status --short --untracked-files=all
