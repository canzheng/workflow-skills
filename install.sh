#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_SKILLS_DIR="${REPO_ROOT}/skills"
TARGET_SKILLS_DIR="${CODEX_HOME:-${HOME}/.codex}/skills"
TARGET_AGENTS_FILE="${CODEX_HOME:-${HOME}/.codex}/AGENTS.md"
MANAGED_WORKFLOW_FILE="${REPO_ROOT}/AGENTS-global-workflow.md"
SOURCE_FEATURE_TEMPLATE_FILE="${REPO_ROOT}/docs/planning/template/feature-template.md"
WORKFLOW_START_MARKER='<!-- Beginning of Workflow Section -->'
WORKFLOW_END_MARKER='<!-- End of Workflow Section -->'

SKILLS=(
  audit-workflow
  diagnose-workflow
  initialize-workflow-artifacts
  fastlane
  shape-backlog-item
  ready-feature
  start-task
  complete-task
  finish-feature
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
    rm -rf "${target_dir}/tests"
    rsync_args+=(--exclude tests)
  fi

  rsync "${rsync_args[@]}" "${source_dir}/" "${target_dir}/"
done

if [[ ! -f "${SOURCE_FEATURE_TEMPLATE_FILE}" ]]; then
  printf 'Missing tracked feature template source: %s\n' "${SOURCE_FEATURE_TEMPLATE_FILE}" >&2
  exit 1
fi

mkdir -p "${TARGET_SKILLS_DIR}/_workflow/templates"
cp "${SOURCE_FEATURE_TEMPLATE_FILE}" "${TARGET_SKILLS_DIR}/_workflow/templates/feature-template.md"

if [[ ! -f "${MANAGED_WORKFLOW_FILE}" ]]; then
  printf 'Missing managed workflow source file: %s\n' "${MANAGED_WORKFLOW_FILE}" >&2
  exit 1
fi

if [[ ! -f "${TARGET_AGENTS_FILE}" ]]; then
  printf 'Missing target AGENTS.md: %s\n' "${TARGET_AGENTS_FILE}" >&2
  exit 1
fi

if [[ "$(grep -Fc "${WORKFLOW_START_MARKER}" "${MANAGED_WORKFLOW_FILE}")" -ne 1 ]] || [[ "$(grep -Fc "${WORKFLOW_END_MARKER}" "${MANAGED_WORKFLOW_FILE}")" -ne 1 ]]; then
  printf 'Managed workflow source must contain exactly one start marker and one end marker: %s\n' "${MANAGED_WORKFLOW_FILE}" >&2
  exit 1
fi

target_start_marker_count="$(grep -Fc "${WORKFLOW_START_MARKER}" "${TARGET_AGENTS_FILE}" || true)"
target_end_marker_count="$(grep -Fc "${WORKFLOW_END_MARKER}" "${TARGET_AGENTS_FILE}" || true)"

if [[ "${target_start_marker_count}" -eq 1 ]] && [[ "${target_end_marker_count}" -eq 1 ]]; then
  tmp_agents_file="$(mktemp)"

  awk \
    -v start_marker="${WORKFLOW_START_MARKER}" \
    -v end_marker="${WORKFLOW_END_MARKER}" \
    -v replacement_file="${MANAGED_WORKFLOW_FILE}" \
    '
    BEGIN {
      while ((getline line < replacement_file) > 0) {
        replacement[++replacement_count] = line
      }
      close(replacement_file)
    }
    $0 == start_marker {
      for (i = 1; i <= replacement_count; i++) {
        print replacement[i]
      }
      in_managed_block = 1
      next
    }
    $0 == end_marker {
      in_managed_block = 0
      next
    }
    !in_managed_block {
      print
    }
    ' \
    "${TARGET_AGENTS_FILE}" > "${tmp_agents_file}"

  mv "${tmp_agents_file}" "${TARGET_AGENTS_FILE}"
elif [[ "${target_start_marker_count}" -eq 0 ]] && [[ "${target_end_marker_count}" -eq 0 ]]; then
  tmp_agents_file="$(mktemp)"
  cat "${TARGET_AGENTS_FILE}" > "${tmp_agents_file}"
  printf '\n' >> "${tmp_agents_file}"
  cat "${MANAGED_WORKFLOW_FILE}" >> "${tmp_agents_file}"
  mv "${tmp_agents_file}" "${TARGET_AGENTS_FILE}"
else
  printf 'Workflow section markers missing or duplicated in target AGENTS.md: %s\n' "${TARGET_AGENTS_FILE}" >&2
  exit 1
fi

printf 'Installed %d workflow skill directories into %s\n' "${#SKILLS[@]}" "${TARGET_SKILLS_DIR}"
