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

env_name="$(awk '
  BEGIN {
    found = 0
  }
  /^[[:space:]]*name:[[:space:]]*/ {
    sub(/^[[:space:]]*name:[[:space:]]*/, "")
    if (length($0) > 0) {
      print
      found = 1
      exit 0
    }
  }
  END {
    if (!found) {
      exit 1
    }
  }
' "${environment_file}")" || die "environment.yml must declare a top-level name:"

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
if [[ ! -e "${candidate}" ]]; then
  die "script entrypoint does not exist: ${entrypoint}"
fi

candidate_dir="${candidate%/*}"
if [[ "${candidate_dir}" == "${candidate}" ]]; then
  candidate_dir="."
fi
candidate_dir="$(CDPATH= cd -- "${candidate_dir}" && pwd -P)"
resolved_script="${candidate_dir}/${candidate##*/}"
case "${resolved_script}" in
  "${repo_root}"/*) ;;
  "${repo_root}") ;;
  *)
    die "script path must stay inside the repository"
    ;;
esac

cd "${repo_root}"
exec conda run -n "${env_name}" python "${entrypoint}" "$@"
