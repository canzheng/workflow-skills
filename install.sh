#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_SKILLS_DIR="${REPO_ROOT}/skills"
TARGET_SKILLS_DIR="${CODEX_HOME:-${HOME}/.codex}/skills"

SKILLS=(
  audit-workflow
  initialize-workflow-artifacts
  shape-backlog-item
  ready-feature
  start-task
  complete-task
  repair-drift
  defer-feature
  prioritize-backlog
  autonomous-backlog-loop
  _workflow
)

mkdir -p "${TARGET_SKILLS_DIR}"

for skill in "${SKILLS[@]}"; do
  source_dir="${SOURCE_SKILLS_DIR}/${skill}"
  target_dir="${TARGET_SKILLS_DIR}/${skill}"

  if [[ ! -d "${source_dir}" ]]; then
    printf 'Missing source skill directory: %s\n' "${source_dir}" >&2
    exit 1
  fi

  rsync_args=(
    -a
    --delete
    --exclude
    __pycache__
    --exclude
    '*.pyc'
  )

  if [[ "${skill}" == "_workflow" ]]; then
    rsync_args+=(--exclude tests)
  fi

  rsync "${rsync_args[@]}" "${source_dir}/" "${target_dir}/"
done

printf 'Installed %d workflow skill directories into %s\n' "${#SKILLS[@]}" "${TARGET_SKILLS_DIR}"
