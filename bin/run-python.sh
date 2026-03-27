#!/usr/bin/env bash
set -euo pipefail

die() {
  printf '%s\n' "$1" >&2
  exit 1
}

wrapper_source="${BASH_SOURCE[0]}"
wrapper_dir="${wrapper_source%/*}"
if [[ "${wrapper_dir}" == "${wrapper_source}" ]]; then
  wrapper_dir="."
fi
wrapper_dir="$(CDPATH= cd -- "${wrapper_dir}" && pwd -P)"
repo_root="$(CDPATH= cd -- "${wrapper_dir}/.." && pwd -P)"
environment_file="${repo_root}/environment.yml"

if [[ ! -f "${environment_file}" ]]; then
  die "environment.yml is missing"
fi

if ! command -v conda >/dev/null 2>&1; then
  die "conda is required but was not found on PATH"
fi

extract_env_name() {
  local line remainder env_value

  while IFS= read -r line || [[ -n "${line}" ]]; do
    case "${line}" in
      name:*)
        remainder="${line#name:}"
        remainder="${remainder#${remainder%%[![:space:]]*}}"
        case "${remainder}" in
          \"*)
            remainder="${remainder#\"}"
            env_value="${remainder%%\"*}"
            ;;
          \'*)
            remainder="${remainder#\'}"
            env_value="${remainder%%\'*}"
            ;;
          *)
            env_value="${remainder%%\#*}"
            env_value="${env_value%${env_value##*[![:space:]]}}"
            ;;
        esac
        env_value="${env_value%${env_value##*[![:space:]]}}"
        if [[ -n "${env_value}" ]]; then
          printf '%s\n' "${env_value}"
          return 0
        fi
        return 1
        ;;
    esac
  done < "${environment_file}"

  return 1
}

env_name="$(extract_env_name)" || die "environment.yml must declare a top-level name:"

if ! conda env list | awk -v env="${env_name}" '
  $1 == env {
    found = 1
  }
  END {
    exit found ? 0 : 1
  }
' >/dev/null; then
  die "conda environment '${env_name}' is not installed"
fi

if [[ $# -eq 0 ]]; then
  die "missing entrypoint"
fi

if [[ "${1}" == "-m" ]]; then
  shift
  if [[ $# -eq 0 ]]; then
    die "missing python module name"
  fi
  cd "${repo_root}"
  exec conda run -n "${env_name}" python -m "$@"
fi

entrypoint="${1}"
shift

if [[ "${entrypoint}" == /* ]]; then
  die "absolute script paths are not allowed"
fi

if [[ "${entrypoint}" != *.py ]]; then
  die "script entrypoints must end with .py"
fi

candidate="${repo_root}/${entrypoint}"
if [[ ! -f "${candidate}" ]]; then
  die "script entrypoint does not exist: ${entrypoint}"
fi

resolved_script="$(python3 - "$candidate" <<'PY'
from pathlib import Path
import sys

print(Path(sys.argv[1]).resolve())
PY
)"
case "${resolved_script}" in
  "${repo_root}"/*) ;;
  "${repo_root}") ;;
  *)
    die "script path must stay inside the repository"
    ;;
esac

cd "${repo_root}"
exec conda run -n "${env_name}" python "${entrypoint}" "$@"
