#!/usr/bin/env bash
set -euo pipefail

die() {
  printf '%s\n' "$1" >&2
  exit 1
}

repo_root="$(pwd -P)"
tools="codex"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --tools)
      shift
      [[ $# -gt 0 ]] || die "missing value for --tools"
      tools="$1"
      shift
      ;;
    --tools=*)
      tools="${1#*=}"
      shift
      ;;
    *)
      die "unsupported argument: $1"
      ;;
  esac
done

if [[ "${tools}" != "codex" ]]; then
  die "unsupported tool: ${tools}"
fi

lessons_dir="${repo_root}/docs/lessons"
mkdir -p "${lessons_dir}"
touch "${lessons_dir}/lessons.md"
touch "${lessons_dir}/lesson-candidates.md"
