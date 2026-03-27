from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


WORKFLOW_SECTIONS = ["BACKLOG", "SHAPING", "READY", "IN_PROGRESS", "DONE", "DEFER"]
SECTION_RE = re.compile(r"^## \[(?P<name>[A-Z_]+)\]$")
FEATURE_ENTRY_RE = re.compile(
    r"^###\s+`(?P<id>[^`]+)`(?:\s+\[(?P<tag>[^\]]+)\])?\s+\[(?P<title>[^\]]+)\]\((?P<link>[^)]+)\)$"
)
BACKLOG_ITEM_RE = re.compile(
    r"^###\s+`(?P<id>v\d+-b\d+)`(?:\s+\[(?P<tag>[^\]]+)\])?\s+(?P<title>.+?)\s*$"
)
TASK_HEADER_RE = re.compile(r"^### (?P<id>T\d+): (?P<title>.+)$")
TASK_STATUS_RE = re.compile(r"^- Status: `(?P<status>[^`]+)`$")
FIELD_HEADER_RE = re.compile(r"^- (?P<field>[^:]+):(?P<rest>.*)$")
TASK_REF_RE = re.compile(r"`([^`]+)`")
FEATURE_ID_RE = re.compile(r"^- Feature ID: `([^`]+)`$", re.MULTILINE)
OPEN_SPEC_CHANGE_RE = re.compile(r"^- OpenSpec Change: `([^`]+)`$", re.MULTILINE)
OPEN_SPEC_STATUS_RE = re.compile(r"^- OpenSpec Status: `([^`]+)`$", re.MULTILINE)
CURRENT_TASK_RE = re.compile(r"^- Current Task: `([^`]+)`$", re.MULTILINE)
TOP_LEVEL_TASK_ID_RE = re.compile(r"^\d+$")
OPEN_SPEC_TASK_RE = re.compile(r"^- \[(?P<done>[ xX])\]\s+(?P<id>\d+)\s+(?P<title>.+)$")
OPEN_SPEC_NESTED_TASK_RE = re.compile(
    r"^\s+- \[(?P<done>[ xX])\]\s+(?P<id>\d+\.\d+(?:\.\d+)*)\s+(?P<title>.+)$"
)
HEADING_RE = re.compile(r"^##(?:\s+\d+(?:\.\d+)*)?\.?\s+(?P<name>.+?)\s*$", re.MULTILINE)
LEGACY_INLINE_SECTION_NAMES = {
    "problem",
    "goal",
    "scope",
    "design spec",
    "implementation plan",
    "tasks",
}


class WorkflowStateError(RuntimeError):
    pass


@dataclass(frozen=True)
class TaskRecord:
    task_id: str
    task_title: str
    status: str
    depends_on: tuple[str, ...]
    status_line_index: int


@dataclass(frozen=True)
class RawOpenSpecTaskRecord:
    task_id: str
    task_title: str
    done: bool
    depends_on: tuple[str, ...]
    status_line_index: int


@dataclass(frozen=True)
class TaskReadinessDrift:
    promotable_task_ids: list[str]
    invalid_ready_task_ids: list[str]
    unknown_dependency_errors: list[str]

    def has_errors(self) -> bool:
        return bool(self.invalid_ready_task_ids or self.unknown_dependency_errors)

    def has_drift(self) -> bool:
        return bool(self.promotable_task_ids or self.invalid_ready_task_ids or self.unknown_dependency_errors)


@dataclass(frozen=True)
class CompletionHandoff:
    all_top_level_tasks_complete: bool
    decision: str
    next_ready_task_ids: list[str]
    remaining_open_task_ids: list[str]


@dataclass(frozen=True)
class DependencyResolution:
    status: str | None
    error: str | None = None


@dataclass(frozen=True)
class BacklogFeatureEntry:
    feature_id: str
    title: str
    link: str
    tag: str | None = None


@dataclass(frozen=True)
class BacklogItemEntry:
    backlog_id: str
    title: str
    backlog_index: int
    tag: str | None = None


@dataclass(frozen=True)
class ParsedBacklogDocument:
    feature_sections: dict[str, list[BacklogFeatureEntry]]
    backlog_items: list[BacklogItemEntry]
    malformed_entries: list[str]


@dataclass(frozen=True)
class OpenSpecChangeLinkage:
    active_change_ids: list[str]
    linked_promoted_change_ids: list[str]
    orphan_active_change_ids: list[str]


def parse_backlog_document(text: str) -> ParsedBacklogDocument:
    feature_sections: dict[str, list[BacklogFeatureEntry]] = {name: [] for name in WORKFLOW_SECTIONS}
    backlog_items: list[BacklogItemEntry] = []
    malformed_entries: list[str] = []
    current_section: str | None = None

    for line_number, line in enumerate(text.splitlines(), start=1):
        header = SECTION_RE.match(line)
        if header:
            current_section = header.group("name")
            continue

        if current_section not in feature_sections or not line.startswith("###"):
            continue

        if current_section == "BACKLOG":
            backlog_match = BACKLOG_ITEM_RE.match(line)
            if backlog_match:
                backlog_items.append(
                    BacklogItemEntry(
                        backlog_id=backlog_match.group("id"),
                        title=backlog_match.group("title"),
                        backlog_index=len(backlog_items) + 1,
                        tag=backlog_match.group("tag"),
                    )
                )
                continue

            malformed_entries.append(
                f"line {line_number} in section [BACKLOG] has malformed backlog entry: {line}"
            )
            continue

        feature_match = FEATURE_ENTRY_RE.match(line)
        if feature_match:
            feature_sections[current_section].append(
                BacklogFeatureEntry(
                    feature_id=feature_match.group("id"),
                    title=feature_match.group("title"),
                    link=feature_match.group("link"),
                    tag=feature_match.group("tag"),
                )
            )
            continue

        malformed_entries.append(
            f"line {line_number} in section [{current_section}] has malformed feature entry: {line}"
        )

    return ParsedBacklogDocument(
        feature_sections=feature_sections,
        backlog_items=backlog_items,
        malformed_entries=malformed_entries,
    )


def collect_openspec_change_linkage(repo_root: Path) -> OpenSpecChangeLinkage:
    current_version = repo_root / "docs" / "planning" / "current_version"
    if not current_version.exists():
        raise WorkflowStateError("docs/planning/current_version is missing")
    if not current_version.is_symlink():
        raise WorkflowStateError("docs/planning/current_version is not a symlink")

    version_root = current_version.resolve()
    backlog_path = version_root / "BACKLOG.md"
    if not backlog_path.exists():
        raise WorkflowStateError(f"{backlog_path.relative_to(repo_root)} is missing")

    linked_change_ids: set[str] = set()
    parsed_backlog = parse_backlog_document(backlog_path.read_text(encoding="utf-8"))
    for section_name in WORKFLOW_SECTIONS[1:]:
        for entry in parsed_backlog.feature_sections.get(section_name, []):
            feature_path = (backlog_path.parent / entry.link).resolve()
            if not feature_path.exists():
                continue
            change_id = parse_feature_openspec_change(feature_path.read_text(encoding="utf-8"))
            if change_id is not None:
                linked_change_ids.add(change_id)

    changes_root = repo_root / "openspec" / "changes"
    active_change_ids = sorted(
        path.name
        for path in changes_root.iterdir()
        if path.is_dir() and path.name != "archive"
    ) if changes_root.exists() else []
    linked_promoted_change_ids = sorted(linked_change_ids)
    orphan_active_change_ids = sorted(set(active_change_ids) - linked_change_ids)

    return OpenSpecChangeLinkage(
        active_change_ids=active_change_ids,
        linked_promoted_change_ids=linked_promoted_change_ids,
        orphan_active_change_ids=orphan_active_change_ids,
    )


def parse_feature_openspec_change(feature_text: str) -> str | None:
    match = OPEN_SPEC_CHANGE_RE.search(feature_text)
    if match:
        return match.group(1)
    return None


def parse_feature_openspec_status(feature_text: str) -> str | None:
    match = OPEN_SPEC_STATUS_RE.search(feature_text)
    if match:
        return match.group(1)
    return None


def parse_current_task(feature_text: str) -> str | None:
    match = CURRENT_TASK_RE.search(feature_text)
    if not match:
        return None
    current_task = match.group(1)
    if current_task == "none":
        return None
    if not TOP_LEVEL_TASK_ID_RE.fullmatch(current_task):
        raise ValueError(
            f"Current Task must be `none` or a top-level OpenSpec task ID, got `{current_task}`"
        )
    return current_task


def find_legacy_inline_planning_sections(feature_text: str) -> list[str]:
    found: list[str] = []
    seen: set[str] = set()
    for match in HEADING_RE.finditer(feature_text):
        normalized = match.group("name").strip().lower()
        if normalized in LEGACY_INLINE_SECTION_NAMES and normalized not in seen:
            seen.add(normalized)
            found.append(match.group("name").strip())
    return found


def _parse_feature_file_tasks(feature_text: str) -> list[TaskRecord]:
    lines = feature_text.splitlines()
    tasks: list[TaskRecord] = []

    current_id: str | None = None
    current_title: str | None = None
    current_status = ""
    current_status_line_index = -1
    current_depends_on: list[str] = []
    current_field: str | None = None

    def flush_task() -> None:
        nonlocal current_id, current_title, current_status, current_status_line_index, current_depends_on, current_field
        if current_id is None or current_title is None:
            return
        tasks.append(
            TaskRecord(
                task_id=current_id,
                task_title=current_title,
                status=current_status,
                depends_on=tuple(current_depends_on),
                status_line_index=current_status_line_index,
            )
        )
        current_id = None
        current_title = None
        current_status = ""
        current_status_line_index = -1
        current_depends_on = []
        current_field = None

    for line_index, line in enumerate(lines):
        task_header = TASK_HEADER_RE.match(line)
        if task_header:
            flush_task()
            current_id = task_header.group("id")
            current_title = task_header.group("title")
            continue

        if current_id is None:
            continue

        status_match = TASK_STATUS_RE.match(line)
        if status_match:
            current_status = status_match.group("status")
            current_status_line_index = line_index
            current_field = "Status"
            continue

        field_match = FIELD_HEADER_RE.match(line)
        if field_match:
            current_field = field_match.group("field")
            if current_field == "Depends On":
                current_depends_on.extend(TASK_REF_RE.findall(field_match.group("rest")))
            continue

        if current_field == "Depends On":
            current_depends_on.extend(TASK_REF_RE.findall(line))

    flush_task()
    return tasks


def _resolve_repo_root_from_feature_file(feature_file: Path | None, repo_root: Path | None) -> Path | None:
    if repo_root is not None:
        return repo_root
    if feature_file is None:
        return None
    for parent in [feature_file.parent, *feature_file.parents]:
        if (parent / ".git").exists():
            return parent
    return None


def _linked_openspec_tasks_file(
    feature_text: str,
    *,
    feature_file: Path | None = None,
    repo_root: Path | None = None,
) -> Path | None:
    change_dir = linked_openspec_change_dir(feature_text, feature_file=feature_file, repo_root=repo_root)
    if change_dir is None:
        return None
    tasks_file = change_dir / "tasks.md"
    if not tasks_file.exists():
        return None
    return tasks_file


def _find_openspec_change_dir(repo_root: Path, change_id: str) -> Path | None:
    active_change_dir = repo_root / "openspec" / "changes" / change_id
    if active_change_dir.exists():
        return active_change_dir

    archive_root = repo_root / "openspec" / "changes" / "archive"
    if not archive_root.exists():
        return None

    archived_matches = sorted(archive_root.glob(f"*-{change_id}"))
    if len(archived_matches) != 1:
        return None
    return archived_matches[0]


def linked_openspec_implementation_plan_path(
    feature_text: str,
    task_id: str,
    *,
    feature_file: Path | None = None,
    repo_root: Path | None = None,
) -> Path | None:
    change_dir = linked_openspec_change_dir(feature_text, feature_file=feature_file, repo_root=repo_root)
    if change_dir is None:
        return None
    return change_dir / "implementation-plans" / f"{task_id}.md"


def linked_openspec_change_dir(
    feature_text: str,
    *,
    feature_file: Path | None = None,
    repo_root: Path | None = None,
) -> Path | None:
    change_id = parse_feature_openspec_change(feature_text)
    if change_id is None:
        return None
    resolved_repo_root = _resolve_repo_root_from_feature_file(feature_file, repo_root)
    if resolved_repo_root is None:
        return None
    return _find_openspec_change_dir(resolved_repo_root, change_id)


def validate_active_feature_execution(
    feature_text: str,
    *,
    feature_file: Path,
    repo_root: Path,
) -> tuple[str, Path]:
    feature_label = str(feature_file.relative_to(repo_root))
    change_id = parse_feature_openspec_change(feature_text)
    if change_id is None:
        raise WorkflowStateError(f"{feature_label} is missing OpenSpec Change metadata")

    active_change_dir = repo_root / "openspec" / "changes" / change_id
    if not active_change_dir.exists():
        raise WorkflowStateError(
            f"{feature_label} links missing active OpenSpec change directory "
            f"{active_change_dir.relative_to(repo_root)}"
        )

    readiness_drift = compute_task_readiness_drift(
        feature_text,
        feature_file=feature_file,
        repo_root=repo_root,
    )
    if readiness_drift.has_drift():
        drift_messages = "; ".join(
            format_task_readiness_drift_messages(
                readiness_drift,
                feature_label=feature_label,
            )
        )
        raise WorkflowStateError(f"workflow-derived task readiness drift detected: {drift_messages}")

    return change_id, active_change_dir


def list_openspec_change_context_files(
    feature_text: str,
    *,
    task_id: str | None = None,
    feature_file: Path | None = None,
    repo_root: Path | None = None,
) -> list[Path]:
    change_dir = linked_openspec_change_dir(feature_text, feature_file=feature_file, repo_root=repo_root)
    if change_dir is None:
        return []

    primary_files = [change_dir / name for name in ("proposal.md", "design.md", "tasks.md")]
    primary_existing = [path for path in primary_files if path.exists()]
    primary_set = {path.resolve() for path in primary_existing}
    implementation_plans_dir = change_dir / "implementation-plans"

    extra_markdown = sorted(
        path
        for path in change_dir.rglob("*.md")
        if path.resolve() not in primary_set and implementation_plans_dir not in path.parents
    )
    context_files = [*primary_existing, *extra_markdown]
    if task_id is not None:
        task_plan = linked_openspec_implementation_plan_path(
            feature_text,
            task_id,
            feature_file=feature_file,
            repo_root=repo_root,
        )
        if task_plan is not None and task_plan.exists():
            context_files.append(task_plan)
    return context_files


def _parse_openspec_tasks_text(tasks_text: str) -> list[RawOpenSpecTaskRecord]:
    lines = tasks_text.splitlines()
    tasks: list[RawOpenSpecTaskRecord] = []

    current_id: str | None = None
    current_title: str | None = None
    current_done = False
    current_status_line_index = -1
    current_depends_on: list[str] = []
    current_field: str | None = None

    def flush_task() -> None:
        nonlocal current_id, current_title, current_done, current_status_line_index, current_depends_on, current_field
        if current_id is None or current_title is None:
            return
        tasks.append(
            RawOpenSpecTaskRecord(
                task_id=current_id,
                task_title=current_title,
                done=current_done,
                depends_on=tuple(current_depends_on),
                status_line_index=current_status_line_index,
            )
        )
        current_id = None
        current_title = None
        current_done = False
        current_status_line_index = -1
        current_depends_on = []
        current_field = None

    for line_index, line in enumerate(lines):
        task_match = OPEN_SPEC_TASK_RE.match(line)
        if task_match:
            flush_task()
            current_id = task_match.group("id")
            current_title = task_match.group("title")
            current_done = task_match.group("done").lower() == "x"
            current_status_line_index = line_index
            continue

        if current_id is None:
            continue

        stripped = line.strip()
        field_match = FIELD_HEADER_RE.match(stripped)
        if field_match:
            current_field = field_match.group("field")
            if current_field == "Depends On":
                current_depends_on.extend(TASK_REF_RE.findall(field_match.group("rest")))
            continue

        if current_field == "Depends On":
            current_depends_on.extend(TASK_REF_RE.findall(stripped))

    flush_task()
    return tasks


def parse_openspec_tasks_file(tasks_file: Path, *, current_task: str | None = None) -> list[TaskRecord]:
    raw_tasks = _parse_openspec_tasks_text(tasks_file.read_text(encoding="utf-8"))
    return _derive_openspec_task_statuses(raw_tasks, current_task=current_task)


def find_openspec_task_structure_errors(tasks_text: str) -> list[str]:
    top_level_task_ids = {
        task.task_id
        for task in _parse_openspec_tasks_text(tasks_text)
    }
    errors: list[str] = []

    for line in tasks_text.splitlines():
        nested_match = OPEN_SPEC_NESTED_TASK_RE.match(line)
        if not nested_match:
            continue

        nested_task_id = nested_match.group("id")
        parent_task_id = nested_task_id.split(".", 1)[0]
        if parent_task_id in top_level_task_ids:
            continue

        errors.append(
            f"nested checklist item `{nested_task_id}` is missing parent top-level executable task `{parent_task_id}`"
        )

    return errors


def _parse_openspec_open_nested_items(tasks_text: str) -> dict[str, list[str]]:
    open_nested_items: dict[str, list[str]] = {}
    current_top_level_task_id: str | None = None

    for line in tasks_text.splitlines():
        task_match = OPEN_SPEC_TASK_RE.match(line)
        if task_match:
            current_top_level_task_id = task_match.group("id")
            open_nested_items.setdefault(current_top_level_task_id, [])
            continue

        if current_top_level_task_id is None:
            continue

        nested_match = OPEN_SPEC_NESTED_TASK_RE.match(line)
        if not nested_match:
            continue
        if nested_match.group("done").lower() == "x":
            continue
        nested_task_id = nested_match.group("id")
        if nested_task_id.startswith(f"{current_top_level_task_id}."):
            open_nested_items.setdefault(current_top_level_task_id, []).append(nested_task_id)

    return open_nested_items


def _derive_openspec_task_statuses(
    raw_tasks: list[RawOpenSpecTaskRecord],
    *,
    current_task: str | None,
    local_feature_id: str | None = None,
    repo_root: Path | None = None,
) -> list[TaskRecord]:
    local_tasks_by_id = {
        task.task_id: TaskRecord(
            task_id=task.task_id,
            task_title=task.task_title,
            status="done" if task.done else ("in_progress" if current_task == task.task_id else "todo"),
            depends_on=task.depends_on,
            status_line_index=task.status_line_index,
        )
        for task in raw_tasks
    }
    feature_file_cache: dict[str, Path | None] = {}
    task_cache: dict[Path, dict[str, TaskRecord]] = {}
    tasks: list[TaskRecord] = []

    for task in raw_tasks:
        status = local_tasks_by_id[task.task_id].status
        if status == "todo":
            dependencies_satisfied = True
            for dependency in task.depends_on:
                resolved = _resolve_dependency(
                    dependency,
                    local_feature_id=local_feature_id,
                    local_tasks_by_id=local_tasks_by_id,
                    repo_root=repo_root,
                    feature_file_cache=feature_file_cache,
                    task_cache=task_cache,
                )
                if resolved.status != "done":
                    dependencies_satisfied = False
                    break
            if dependencies_satisfied:
                status = "ready"

        tasks.append(
            TaskRecord(
                task_id=task.task_id,
                task_title=task.task_title,
                status=status,
                depends_on=task.depends_on,
                status_line_index=task.status_line_index,
            )
        )
    return tasks


def parse_tasks(
    feature_text: str,
    *,
    feature_file: Path | None = None,
    repo_root: Path | None = None,
) -> list[TaskRecord]:
    feature_tasks = _parse_feature_file_tasks(feature_text)
    if feature_tasks:
        return feature_tasks

    resolved_repo_root = _resolve_repo_root_from_feature_file(feature_file, repo_root)
    tasks_file = _linked_openspec_tasks_file(feature_text, feature_file=feature_file, repo_root=resolved_repo_root)
    if tasks_file is None:
        return []

    current_task = parse_current_task(feature_text)
    return _derive_openspec_task_statuses(
        _parse_openspec_tasks_text(tasks_file.read_text(encoding="utf-8")),
        current_task=current_task,
        local_feature_id=parse_feature_id(feature_text, feature_file=feature_file),
        repo_root=resolved_repo_root,
    )


def list_open_openspec_nested_items(
    feature_text: str,
    task_id: str,
    *,
    feature_file: Path | None = None,
    repo_root: Path | None = None,
) -> list[str]:
    tasks_file = _linked_openspec_tasks_file(feature_text, feature_file=feature_file, repo_root=repo_root)
    if tasks_file is None:
        return []
    nested_items_by_task = _parse_openspec_open_nested_items(tasks_file.read_text(encoding="utf-8"))
    return nested_items_by_task.get(task_id, [])


def parse_feature_id(feature_text: str, *, feature_file: Path | None = None) -> str | None:
    feature_id_match = FEATURE_ID_RE.search(feature_text)
    if feature_id_match:
        return feature_id_match.group(1)
    if feature_file is None:
        return None
    stem = feature_file.stem
    if "-" not in stem:
        return stem
    return stem.split("-", 2)[0] + "-" + stem.split("-", 2)[1] if stem.count("-") >= 1 else stem


def _feature_tasks_by_id(
    feature_text: str,
    *,
    feature_file: Path | None = None,
    repo_root: Path | None = None,
) -> dict[str, TaskRecord]:
    return {
        task.task_id: task
        for task in parse_tasks(feature_text, feature_file=feature_file, repo_root=repo_root)
    }


def _active_features_dir(repo_root: Path) -> Path:
    current_version = repo_root / "docs" / "planning" / "current_version"
    if not current_version.exists():
        raise WorkflowStateError("docs/planning/current_version is missing")
    return current_version.resolve() / "features"


def _find_feature_file_for_id(
    repo_root: Path,
    dependency_feature_id: str,
    feature_file_cache: dict[str, Path | None],
) -> Path | None:
    if dependency_feature_id in feature_file_cache:
        return feature_file_cache[dependency_feature_id]

    features_dir = _active_features_dir(repo_root)
    matches = sorted(features_dir.glob(f"{dependency_feature_id}-*.md"))
    if len(matches) == 1:
        feature_file_cache[dependency_feature_id] = matches[0]
    else:
        feature_file_cache[dependency_feature_id] = None
    return feature_file_cache[dependency_feature_id]


def _resolve_dependency(
    dependency: str,
    *,
    local_feature_id: str | None,
    local_tasks_by_id: dict[str, TaskRecord],
    repo_root: Path | None,
    feature_file_cache: dict[str, Path | None],
    task_cache: dict[Path, dict[str, TaskRecord]],
) -> DependencyResolution:
    if "/" not in dependency:
        task = local_tasks_by_id.get(dependency)
        if task is None:
            return DependencyResolution(status=None, error=f"references unknown dependency ids: {dependency}")
        return DependencyResolution(status=task.status)

    dependency_feature_id, dependency_task_id = dependency.split("/", 1)
    if local_feature_id is not None and dependency_feature_id == local_feature_id:
        task = local_tasks_by_id.get(dependency_task_id)
        if task is None:
            return DependencyResolution(status=None, error=f"references unknown dependency ids: {dependency}")
        return DependencyResolution(status=task.status)

    if repo_root is None:
        return DependencyResolution(status=None, error=f"references unknown dependency ids: {dependency}")

    dependency_feature_file = _find_feature_file_for_id(repo_root, dependency_feature_id, feature_file_cache)
    if dependency_feature_file is None:
        return DependencyResolution(status=None, error=f"references unknown dependency ids: {dependency}")

    dependency_tasks_by_id = task_cache.get(dependency_feature_file)
    if dependency_tasks_by_id is None:
        dependency_tasks_by_id = _feature_tasks_by_id(
            dependency_feature_file.read_text(encoding="utf-8"),
            feature_file=dependency_feature_file,
            repo_root=repo_root,
        )
        task_cache[dependency_feature_file] = dependency_tasks_by_id

    task = dependency_tasks_by_id.get(dependency_task_id)
    if task is None:
        return DependencyResolution(status=None, error=f"references unknown dependency ids: {dependency}")
    return DependencyResolution(status=task.status)


def compute_task_readiness_drift(
    feature_text: str,
    *,
    feature_file: Path | None = None,
    repo_root: Path | None = None,
) -> TaskReadinessDrift:
    tasks = parse_tasks(feature_text, feature_file=feature_file, repo_root=repo_root)
    local_tasks_by_id = {task.task_id: task for task in tasks}
    local_feature_id = parse_feature_id(feature_text, feature_file=feature_file)
    feature_file_cache: dict[str, Path | None] = {}
    task_cache: dict[Path, dict[str, TaskRecord]] = {}

    unknown_dependency_errors: list[str] = []
    promotable_task_ids: list[str] = []
    invalid_ready_task_ids: list[str] = []

    for task in tasks:
        dependency_statuses: list[str] = []
        missing_dependency_errors: list[str] = []
        for dependency in task.depends_on:
            resolved = _resolve_dependency(
                dependency,
                local_feature_id=local_feature_id,
                local_tasks_by_id=local_tasks_by_id,
                repo_root=repo_root,
                feature_file_cache=feature_file_cache,
                task_cache=task_cache,
            )
            if resolved.error is not None:
                missing_dependency_errors.append(resolved.error)
                continue
            if resolved.status is not None:
                dependency_statuses.append(resolved.status)

        if missing_dependency_errors:
            unknown_dependency_errors.append(f"{task.task_id} {'; '.join(missing_dependency_errors)}")
            continue

        dependencies_satisfied = all(status == "done" for status in dependency_statuses)
        if task.status == "todo" and dependencies_satisfied:
            promotable_task_ids.append(task.task_id)
        if task.status == "ready" and not dependencies_satisfied:
            invalid_ready_task_ids.append(task.task_id)

    return TaskReadinessDrift(
        promotable_task_ids=promotable_task_ids,
        invalid_ready_task_ids=invalid_ready_task_ids,
        unknown_dependency_errors=unknown_dependency_errors,
    )


def compute_completion_handoff(
    feature_text: str,
    completed_task_id: str,
    *,
    feature_file: Path | None = None,
    repo_root: Path | None = None,
) -> CompletionHandoff:
    tasks = parse_tasks(feature_text, feature_file=feature_file, repo_root=repo_root)
    local_tasks_by_id = {task.task_id: task for task in tasks}
    local_feature_id = parse_feature_id(feature_text, feature_file=feature_file)
    feature_file_cache: dict[str, Path | None] = {}
    task_cache: dict[Path, dict[str, TaskRecord]] = {}
    done_task_ids = {task.task_id for task in tasks if task.status == "done"}
    done_task_ids.add(completed_task_id)

    next_ready_task_ids: list[str] = []
    remaining_open_task_ids: list[str] = []

    for task in tasks:
        if task.task_id in done_task_ids:
            continue

        dependencies_satisfied = True
        for dependency in task.depends_on:
            if "/" not in dependency:
                if dependency not in done_task_ids:
                    dependencies_satisfied = False
                    break
                continue

            dependency_feature_id, dependency_task_id = dependency.split("/", 1)
            if local_feature_id is not None and dependency_feature_id == local_feature_id:
                if dependency_task_id not in done_task_ids:
                    dependencies_satisfied = False
                    break
                continue

            resolved = _resolve_dependency(
                dependency,
                local_feature_id=local_feature_id,
                local_tasks_by_id=local_tasks_by_id,
                repo_root=repo_root,
                feature_file_cache=feature_file_cache,
                task_cache=task_cache,
            )
            if resolved.status != "done":
                dependencies_satisfied = False
                break

        remaining_open_task_ids.append(task.task_id)
        if dependencies_satisfied:
            next_ready_task_ids.append(task.task_id)

    all_top_level_tasks_complete = not remaining_open_task_ids
    decision = "confirm_feature_acceptance" if all_top_level_tasks_complete else "stay_in_progress"
    return CompletionHandoff(
        all_top_level_tasks_complete=all_top_level_tasks_complete,
        decision=decision,
        next_ready_task_ids=next_ready_task_ids,
        remaining_open_task_ids=remaining_open_task_ids,
    )


def format_task_readiness_drift_messages(
    drift: TaskReadinessDrift,
    *,
    feature_label: str | None = None,
) -> list[str]:
    prefix = f"{feature_label} " if feature_label else ""
    messages: list[str] = []
    for task_id in drift.promotable_task_ids:
        messages.append(f"{prefix}{task_id} could be `ready` but is still `todo`")
    for task_id in drift.invalid_ready_task_ids:
        messages.append(f"{prefix}{task_id} is `ready` but its dependencies are not all `done`")
    for error in drift.unknown_dependency_errors:
        messages.append(f"{prefix}{error}")
    return messages
