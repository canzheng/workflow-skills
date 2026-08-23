from __future__ import annotations

import re
import subprocess
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
# A field's continuation ends at the next BLOCK, not at the next field header. `Depends On` and
# `OpenSpec Specs` are written as a header plus indented bullets, so both collect backticked refs
# from the lines that follow. With no stop condition that collection ran until the next field
# header, which meant a nested checklist item's filenames and the following section heading's prose
# were both read as refs. Nothing errors: the result is a plausible list of dependencies nobody
# declared, and the referenced IDs are never checked to exist. Plain bullets must still continue a
# field -- that is the documented multi-line form -- so only headings, checklist items, and blank
# lines terminate.
FIELD_CONTINUATION_STOP_RE = re.compile(r"^(?:#{1,6}\s|-\s*\[[ xX]\]|$)")


def _terminates_field_continuation(stripped_line: str) -> bool:
    return bool(FIELD_CONTINUATION_STOP_RE.match(stripped_line))
FEATURE_ID_RE = re.compile(r"^- Feature ID: `([^`]+)`$", re.MULTILINE)
OPEN_SPEC_CHANGE_RE = re.compile(r"^- OpenSpec Change: `([^`]+)`$", re.MULTILINE)
OPEN_SPEC_STATUS_RE = re.compile(r"^- OpenSpec Status: `([^`]+)`$", re.MULTILINE)
CURRENT_TASK_RE = re.compile(r"^- Current Task: `([^`]+)`$", re.MULTILINE)
BRANCH_FEATURE_ID_RE = re.compile(r"^(v\d+-f\d+)(?:$|[-/])")
TOP_LEVEL_TASK_ID_RE = re.compile(r"^\d+$")
OPEN_SPEC_TASK_RE = re.compile(r"^- \[(?P<done>[ xX])\]\s+(?P<id>\d+)\s+(?P<title>.+)$")
# `\s+` REQUIRED indentation, so `- [ ] 1.3 x` at column 0 matched neither this nor
# OPEN_SPEC_TASK_RE (which needs a bare integer id) - the item vanished, and complete-task's
# open-nested-item gate was bypassed by deleting two spaces. Indentation is now optional; the dotted
# id is what makes an item nested.
OPEN_SPEC_NESTED_TASK_RE = re.compile(
    r"^\s*- \[(?P<done>[ xX])\]\s+(?P<id>\d+\.\d+(?:\.\d+)*)\s+(?P<title>.+)$"
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
REQUIREMENT_HEADER_RE = re.compile(r"^###\s+Requirement:\s+(?P<name>.+?)\s*$")
DELTA_OPERATION_RE = re.compile(r"^##\s+(?P<op>ADDED|MODIFIED|REMOVED|RENAMED)\s+Requirements\s*$")
RENAMED_TO_RE = re.compile(r"^-\s+TO:\s+`###\s+Requirement:\s+(?P<name>.+?)`\s*$")


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
    action: str
    target_feature_id: str | None
    target_task_id: str | None
    reason: str
    requires_human_decision: bool


@dataclass(frozen=True)
class ReviewVerdict:
    scope: str
    target: str
    verdict: str
    blocking_findings: tuple[str, ...]
    terminal: bool
    # The entry's own `- `YYYY-MM-DD`:` header. Present so "latest" can mean the newest DATE rather
    # than a position in the file: handoff ordering is not an invariant anywhere (v1-f005 is neither
    # newest- nor oldest-first), and `latest_review_verdict` used `reversed()`, which under the
    # newest-first convention actually returned the OLDEST matching verdict.
    entry_date: str | None = None


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


@dataclass(frozen=True)
class FeatureLocation:
    repo_root: Path
    feature_section: str


@dataclass(frozen=True)
class ImplementationPlanSummary:
    contract_surface_lines: tuple[str, ...]
    proof_obligation_lines: tuple[str, ...]
    required_validation_classes: tuple[str, ...]
    unit_only_justification: str | None


@dataclass(frozen=True)
class ClaimEvidenceIssue:
    relative_path: str
    line_number: int
    reason: str
    line: str


@dataclass(frozen=True)
class ValidationEvidenceSummary:
    task_id: str
    evidence_lines: tuple[str, ...]
    evidence_categories: tuple[str, ...]


RUNTIME_FACING_VALIDATION_CLASSES = {
    "integration",
    "runtime-path",
    "runtime_path",
    "manual-inspection",
    "manual inspection",
    "manual-artifact-inspection",
    "artifact-inspection",
}
RUNTIME_FACING_SURFACE_KEYWORDS = (
    "behavioral",
    "orchestration",
    "persistence",
    "repair",
    "prompt-interface",
    "prompt interface",
    "runtime",
    "artifact mutation",
)
FILE_LINE_CITATION_RE = re.compile(
    r"(?<![:/\w.-])(?:[A-Za-z0-9_.-]+/)*[A-Za-z0-9_.-]+\.[A-Za-z0-9]+:\d+(?:-\d+)?"
)
DECIMAL_OR_PERCENT_PIN_RE = re.compile(
    r"(?:[~<>]=?\s*)?\b\d+\.\d+\b|\b\d+(?:\.\d+)?\s?%|\b\d{1,3}(?:,\d{3})+(?:\.\d+)?\b"
)
STRUCTURE_COUNT_PIN_RE = re.compile(
    r"\b(?:single|one|two|three|four|five|six|seven|eight|nine|ten|\d+)"
    r"\s+(?:centralized\s+)?(?:tiers?|paths?|levers?|copies|implementations?|locations?)\b",
    re.IGNORECASE,
)
INLINE_CODE_SPAN_RE = re.compile(r"`[^`]*`")
ISO_DATE_RE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
# A dotted TASK REFERENCE is not a measurement, for the same reason an ISO date is not: nothing
# about the export, the population, or the run produced it. `DECIMAL_OR_PERCENT_PIN_RE` cannot tell
# `task 3.2` from a ratio of 3.2, so the reference is removed before the pin test runs -- exactly as
# ISO_DATE_RE already removes dates. Only the EXPLICIT form is stripped: a bare `3.2` in prose stays
# a pin, because at that point the tool would be guessing.
TASK_REFERENCE_RE = re.compile(
    r"\b(?:task|tasks|item|items|subitem|subitems|step|steps|subtask|subtasks)\s+\d+(?:\.\d+)+",
    re.IGNORECASE,
)
EVIDENCE_ADJACENCY_RE = re.compile(r"^\s*(?:evidence|grep|rg|read|output)\s*:?\s*$", re.IGNORECASE)
EVIDENCE_BLOCK_RE = re.compile(r"\b(evidence|grep|rg|read|output)\b", re.IGNORECASE)
EVIDENCE_COMMAND_RE = re.compile(
    r"^\s*(?:\$?\s*)?(?:rtk\s+)?(?:rg|grep|sed|nl|python|cat|read)\b",
    re.IGNORECASE,
)
VALIDATION_EVIDENCE_CATEGORY_ALIASES = {
    "schema": "schema",
    "schema proof": "schema",
    "runtime path": "runtime_path",
    "runtime-path": "runtime_path",
    "runtime_path": "runtime_path",
    "runtime path proof": "runtime_path",
    "artifact repair": "artifact_repair",
    "artifact-repair": "artifact_repair",
    "artifact_repair": "artifact_repair",
    "prompt contract": "prompt_contract",
    "prompt-contract": "prompt_contract",
    "prompt_contract": "prompt_contract",
    "orchestration": "orchestration",
    "composed runtime proof": "runtime_path",
    "composed-runtime-proof": "runtime_path",
    "negative path": "negative_case",
    "negative-path": "negative_case",
    "negative case": "negative_case",
    "negative_case": "negative_case",
    "manual inspection": "manual_inspection",
    "manual-inspection": "manual_inspection",
    "manual inspection proof": "manual_inspection",
    "manual-inspection-proof": "manual_inspection",
}


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


def list_git_worktrees(root: Path) -> tuple[list[Path], list[Path]]:
    """(branch-attached worktree roots, DETACHED worktree roots), the caller's own root first.

    Detached worktrees are separated because they are not workflow-managed checkouts. `start-task`
    creates a feature worktree with `-b <branch>`, so every feature checkout has a named branch. A
    detached one is a throwaway - a mutation-harness or fixture tree - and it can live anywhere on
    disk, including a /tmp scratchpad.

    Measured: three detached fixture worktrees under another session's scratchpad were walked as if
    they were feature checkouts, and their fixture planning state produced errors attributed BY NAME
    to a real feature file ("v1-f012-options-surface.md nested checklist item `1.1` is missing
    parent..."). The findings looked real and the paths were the only clue.

    They are RETURNED rather than dropped so the caller can disclose them. Anyone genuinely working
    in a detached worktree can audit from inside it, where it is the caller's own root and always
    included.
    """
    resolved = subprocess.run(
        ["git", "worktree", "list", "--porcelain"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    if resolved.returncode != 0:
        return [root.resolve()], []

    attached = [root.resolve()]
    detached: list[Path] = []
    current: Path | None = None
    is_detached = False

    def flush() -> None:
        nonlocal current, is_detached
        if current is not None:
            bucket = detached if is_detached else attached
            if current not in attached and current not in detached:
                bucket.append(current)
        current, is_detached = None, False

    for line in resolved.stdout.splitlines():
        if line.startswith("worktree "):
            flush()
            current = Path(line.removeprefix("worktree ")).resolve()
        elif line.strip() == "detached":
            is_detached = True
    flush()
    return attached, detached


def list_git_worktree_roots(root: Path) -> list[Path]:
    """Branch-attached worktree roots only. See `list_git_worktrees` for why detached ones are out."""
    return list_git_worktrees(root)[0]


def is_primary_checkout(root: Path) -> bool:
    git_dir_result = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    common_dir_result = subprocess.run(
        ["git", "rev-parse", "--git-common-dir"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    if git_dir_result.returncode != 0 or common_dir_result.returncode != 0:
        return False

    git_dir = (root / git_dir_result.stdout.strip()).resolve()
    common_dir = (root / common_dir_result.stdout.strip()).resolve()
    return git_dir == common_dir


def infer_selected_feature_id(root: Path) -> str | None:
    branch_result = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    if branch_result.returncode != 0:
        return None
    branch_name = branch_result.stdout.strip()
    if not branch_name:
        return None
    match = BRANCH_FEATURE_ID_RE.match(branch_name)
    if match:
        return match.group(1)
    return None


def ensure_clean_feature_worktree_for_handoff(root: Path, feature_id: str) -> None:
    status_result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    if status_result.returncode != 0:
        return
    if status_result.stdout.strip():
        raise WorkflowStateError(
            f"feature worktree has uncommitted handoff changes for {feature_id}; "
            "run/finish complete-task before starting the next task"
        )


def _locate_feature_in_repo(root: Path, feature_id: str) -> FeatureLocation | None:
    current_version = root / "docs" / "planning" / "current_version"
    if not current_version.exists() or not current_version.is_symlink():
        return None

    backlog_path = current_version.resolve() / "BACKLOG.md"
    if not backlog_path.exists():
        return None

    parsed_backlog = parse_backlog_document(read_text_or_error(backlog_path))
    for section_name in WORKFLOW_SECTIONS[1:]:
        for entry in parsed_backlog.feature_sections.get(section_name, []):
            if entry.feature_id == feature_id:
                return FeatureLocation(repo_root=root.resolve(), feature_section=section_name)
    return None


def resolve_feature_repo_root(root: Path, feature_id: str) -> Path:
    locations: list[FeatureLocation] = []
    for candidate_root in list_git_worktree_roots(root):
        location = _locate_feature_in_repo(candidate_root, feature_id)
        if location is not None:
            locations.append(location)

    feature_worktree_locations = [
        location
        for location in locations
        if location.feature_section == "IN_PROGRESS" and not is_primary_checkout(location.repo_root)
    ]
    if len(feature_worktree_locations) == 1:
        return feature_worktree_locations[0].repo_root
    if len(feature_worktree_locations) > 1:
        raise WorkflowStateError(
            f"multiple feature worktrees report {feature_id} in [IN_PROGRESS]; re-run from the intended checkout"
        )

    current_location = _locate_feature_in_repo(root.resolve(), feature_id)
    if current_location is not None:
        if current_location.feature_section == "IN_PROGRESS" and is_primary_checkout(current_location.repo_root):
            raise WorkflowStateError(
                f"no active feature worktree found for {feature_id} in [IN_PROGRESS]; "
                "create or re-enter the intended worktree"
            )
        return current_location.repo_root

    return root.resolve()


def find_backlog_section_order_errors(text: str) -> list[str]:
    found_sections = [
        match.group("name")
        for line in text.splitlines()
        for match in [SECTION_RE.match(line)]
        if match
    ]
    if found_sections != WORKFLOW_SECTIONS:
        return [f"has section order {found_sections}, expected {WORKFLOW_SECTIONS}"]
    return []


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
    parsed_backlog = parse_backlog_document(read_text_or_error(backlog_path))
    for section_name in WORKFLOW_SECTIONS[1:]:
        for entry in parsed_backlog.feature_sections.get(section_name, []):
            feature_path = (backlog_path.parent / entry.link).resolve()
            if not feature_path.exists():
                continue
            change_id = parse_feature_openspec_change(read_text_or_error(feature_path))
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


def parse_feature_openspec_specs(feature_text: str) -> list[str]:
    specs: list[str] = []
    current_field: str | None = None

    for line in feature_text.splitlines():
        field_match = FIELD_HEADER_RE.match(line)
        if field_match:
            current_field = field_match.group("field")
            if current_field == "OpenSpec Specs":
                specs.extend(TASK_REF_RE.findall(field_match.group("rest")))
            continue

        if line.startswith("## "):
            current_field = None
            continue

        if current_field == "OpenSpec Specs":
            if _terminates_field_continuation(line.strip()):
                current_field = None
                continue
            specs.extend(TASK_REF_RE.findall(line))

    return specs


def validate_promoted_feature_openspec_specs(feature_text: str, *, section_name: str) -> list[str]:
    if section_name == "DONE" and parse_feature_openspec_status(feature_text) == "legacy-exempt":
        return []
    if section_name in {"SHAPING", "READY", "IN_PROGRESS", "DONE"} and not parse_feature_openspec_specs(feature_text):
        return ["feature is missing OpenSpec Specs metadata"]
    return []


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


def current_task_reference_error(current_task: str | None, tasks: list[TaskRecord]) -> str | None:
    """Return an error message when `Current Task` is set but no active in-progress task backs it.

    `current_task` is the value already parsed by `parse_current_task` (`None` means
    no active task is declared). Returns `None` when the invariant holds. Shared by
    the audit gate and the autonomous-backlog-loop resolver so both refuse to advance
    task-close state that left `Current Task` pointing at a task that is not
    `in_progress`.
    """
    if current_task is None:
        return None
    referenced_task = next((task for task in tasks if task.task_id == current_task), None)
    if referenced_task is None:
        return f"Current Task `{current_task}` does not reference any top-level OpenSpec task"
    if referenced_task.status != "in_progress":
        return (
            f"Current Task `{current_task}` references a task with status "
            f"`{referenced_task.status}`, expected `in_progress`"
        )
    return None

# Features currently being parsed, so a cross-feature `Depends On` cycle raises a named error
# instead of RecursionError. `parse_tasks` allocates a FRESH dependency cache per call, so A -> B -> A
# never observed that it was re-entering A.
_PARSING_FEATURES: set[Path] = set()


def read_text_or_error(path: Path) -> str:
    """Read UTF-8 text, converting the three measured crash modes into `WorkflowStateError`.

    There are eleven `read_text` sites in this module. A non-UTF-8 feature file, a path that is a
    directory, or an unreadable file aborted the entire audit from whichever site reached it first -
    so one malformed file hid every other finding, and the traceback named a helper rather than the
    file at fault.
    """
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise WorkflowStateError(f"{path} is not valid UTF-8 ({exc.reason})") from None
    except IsADirectoryError:
        raise WorkflowStateError(f"{path} is a directory, not a file") from None
    except OSError as exc:
        raise WorkflowStateError(f"{path} could not be read: {exc.strerror}") from None



def parse_handoff_review_verdicts(feature_text: str) -> list[ReviewVerdict]:
    handoff_notes_header = "## 2. Handoff Notes\n"
    handoff_start = feature_text.find(handoff_notes_header)
    if handoff_start == -1:
        return []

    handoff_text = feature_text[handoff_start + len(handoff_notes_header):]
    verdicts: list[ReviewVerdict] = []
    current_scope: str | None = None
    current_target: str | None = None
    current_verdict: str | None = None
    current_blocking_findings: tuple[str, ...] = ()
    current_terminal: bool | None = None
    current_date: str | None = None

    def flush() -> None:
        nonlocal current_scope, current_target, current_verdict, current_blocking_findings, current_terminal
        # `Review Terminal` used to be REQUIRED here, so a newer `blocked` verdict missing only that
        # line was silently discarded and `latest_review_verdict` returned the older `approved`.
        # Absence of a terminal CLAIM is not a terminal claim, so it reads as False.
        if current_terminal is None and current_verdict is not None:
            current_terminal = False
        if (
            current_scope is None
            or current_target is None
            or current_verdict is None
        ):
            current_scope = None
            current_target = None
            current_verdict = None
            current_blocking_findings = ()
            current_terminal = None
            return
        verdicts.append(
            ReviewVerdict(
                scope=current_scope,
                target=current_target,
                verdict=current_verdict,
                blocking_findings=current_blocking_findings,
                terminal=current_terminal,
                entry_date=current_date,
            )
        )
        current_scope = None
        current_target = None
        current_verdict = None
        current_blocking_findings = ()
        current_terminal = None

    for raw_line in handoff_text.splitlines():
        line = raw_line.strip()
        if line.startswith("- `") and line.endswith("`:"):
            flush()
            current_date = line.removeprefix("- `").removesuffix("`:").strip()
            continue
        if line.startswith("- Review Scope: `") and line.endswith("`"):
            current_scope = line.removeprefix("- Review Scope: `").removesuffix("`")
            continue
        if line.startswith("- Review Target: `") and line.endswith("`"):
            current_target = line.removeprefix("- Review Target: `").removesuffix("`")
            continue
        if line.startswith("- Review Verdict: `") and line.endswith("`"):
            current_verdict = line.removeprefix("- Review Verdict: `").removesuffix("`")
            continue
        if line.startswith("- Blocking Findings: `") and line.endswith("`"):
            raw_findings = line.removeprefix("- Blocking Findings: `").removesuffix("`")
            if raw_findings == "none":
                current_blocking_findings = ()
            else:
                current_blocking_findings = tuple(
                    finding.strip() for finding in raw_findings.split(",") if finding.strip()
                )
            continue
        if line.startswith("- Review Terminal: `") and line.endswith("`"):
            raw_terminal = line.removeprefix("- Review Terminal: `").removesuffix("`").lower()
            current_terminal = raw_terminal == "true"

    flush()
    return verdicts


def latest_review_verdict(feature_text: str, *, scope: str, target: str | None = None) -> ReviewVerdict | None:
    """The newest matching verdict BY DATE, falling back to document order only for undated entries.

    This used `reversed()`, which assumes oldest-first. Handoff notes are newest-first by convention
    (and `v1-f005` is neither), so it returned the OLDEST matching verdict - and callers put that in
    the `ready_review_verdict` payload as the current one.
    """
    matches = [
        (index, verdict)
        for index, verdict in enumerate(parse_handoff_review_verdicts(feature_text))
        if verdict.scope == scope and (target is None or verdict.target == target)
    ]
    if not matches:
        return None
    # Newest date wins; among equal or absent dates the EARLIER document position wins, which is the
    # newest entry under the newest-first convention the real files follow.
    dated = [(i, v) for i, v in matches if v.entry_date]
    if dated:
        return max(dated, key=lambda pair: (pair[1].entry_date, -pair[0]))[1]
    return matches[0][1]


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
            if _terminates_field_continuation(line.strip()):
                current_field = None
                continue
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


def _collect_markdown_section(lines: list[str], *, title: str, level: int) -> list[str] | None:
    heading_re = re.compile(rf"^{'#' * level}(?:\s+\d+(?:\.\d+)*)?\.?\s+{re.escape(title)}\s*$")
    collected: list[str] = []
    collecting = False
    in_fence = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            if collecting:
                collected.append(line)
            continue

        if not collecting:
            if not in_fence and heading_re.match(stripped):
                collecting = True
            continue

        # A `#`-comment inside a fenced code block is content, not a heading, so it
        # must not terminate the section.
        if not in_fence and stripped.startswith("#"):
            marker = stripped.split(maxsplit=1)[0]
            if set(marker) == {"#"} and len(marker) <= level:
                break
        collected.append(line)

    return collected if collecting else None


def _meaningful_markdown_lines(lines: list[str] | None) -> list[str]:
    if lines is None:
        return []
    meaningful: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("<!--") and stripped.endswith("-->"):
            continue
        meaningful.append(stripped)
    return meaningful


def _parse_bullet_values(lines: list[str]) -> list[str]:
    values: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("- "):
            continue
        value = stripped[2:].strip()
        # Accept both bare-name bullets (`- `integration``) and named bullets that
        # carry a trailing description (`- `integration` — runs the resolver`) by
        # extracting the first backtick-quoted token as the value.
        if value.startswith("`"):
            closing = value.find("`", 1)
            if closing != -1:
                values.append(value[1:closing])
                continue
        values.append(value.rstrip("."))
    return values


def _requires_runtime_facing_validation(contract_surface_lines: list[str]) -> bool:
    joined = " ".join(contract_surface_lines).lower()
    return any(keyword in joined for keyword in RUNTIME_FACING_SURFACE_KEYWORDS)


def _collect_validation_log_task_block(feature_text: str, task_id: str) -> list[str]:
    validation_log = _collect_markdown_section(feature_text.splitlines(), title="Validation Log", level=2)
    if validation_log is None:
        return []

    task_block: list[str] = []
    collecting = False

    for line in validation_log:
        task_heading = re.match(r"^- `[^`]+` Task `(?P<task_id>\d+)`[^:]*:$", line.strip())
        if task_heading:
            if collecting and task_heading.group("task_id") != task_id:
                break
            collecting = task_heading.group("task_id") == task_id
            if collecting:
                task_block.append(line)
            continue

        if not collecting:
            continue

        if line.startswith("- ") and not line.startswith("  - "):
            break
        task_block.append(line)

    return task_block


def _normalize_validation_evidence_category(text: str) -> str | None:
    """Match a single evidence TOKEN exactly, never an alias found somewhere inside prose.

    This searched for any alias anywhere in the text and returned the first hit, so
    `no schema proof applicable` counted AS schema proof - a negation satisfying the claim it denies -
    and `manual inspection of the schema section` was read as schema because iteration order decided.
    The template's contract is "comma-separated validation categories", so the token is compared whole.
    """
    normalized = re.sub(r"[_\-]+", " ", text.lower()).strip().strip("`.,;")
    normalized = re.sub(r"\s+", " ", normalized)
    if not normalized:
        return None
    for alias, category in VALIDATION_EVIDENCE_CATEGORY_ALIASES.items():
        alias_normalized = re.sub(r"[_\-]+", " ", alias.lower()).strip()
        alias_normalized = re.sub(r"\s+", " ", alias_normalized)
        if alias_normalized and normalized == alias_normalized:
            return category
    return None


def _parse_validation_evidence_lines(task_block: list[str]) -> list[str]:
    evidence_lines: list[str] = []
    for line in task_block:
        stripped = line.strip()
        if "Evidence:" not in stripped:
            continue
        evidence_lines.append(stripped.split("Evidence:", 1)[1].strip())
    return evidence_lines


def _parse_validation_evidence_categories(evidence_lines: list[str]) -> tuple[str, ...]:
    categories: list[str] = []
    for evidence_line in evidence_lines:
        for segment in re.split(r",|;|/|\band\b", evidence_line, flags=re.IGNORECASE):
            segment = segment.strip(" `.-")
            if not segment:
                continue
            category = _normalize_validation_evidence_category(segment)
            if category is None or category in categories:
                continue
            categories.append(category)
    return tuple(categories)


def collect_task_validation_evidence(feature_text: str, task_id: str) -> ValidationEvidenceSummary:
    task_block = _collect_validation_log_task_block(feature_text, task_id)
    evidence_lines = _parse_validation_evidence_lines(task_block)
    evidence_categories = _parse_validation_evidence_categories(evidence_lines)
    return ValidationEvidenceSummary(
        task_id=task_id,
        evidence_lines=tuple(evidence_lines),
        evidence_categories=evidence_categories,
    )


def _iter_claim_lint_markdown_files(change_dir: Path) -> list[Path]:
    candidates: list[Path] = []
    for name in ("proposal.md", "design.md"):
        path = change_dir / name
        if path.is_file():
            candidates.append(path)

    implementation_plans = change_dir / "implementation-plans"
    if implementation_plans.is_dir():
        candidates.extend(sorted(implementation_plans.rglob("*.md")))

    seen: set[Path] = set()
    unique_candidates: list[Path] = []
    for path in candidates:
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        unique_candidates.append(path)
    return unique_candidates


def _collect_fenced_markdown_blocks(lines: list[str]) -> list[tuple[int, int, bool]]:
    blocks: list[tuple[int, int, bool]] = []
    fence_start: int | None = None
    fence_marker: str | None = None
    for index, line in enumerate(lines, start=1):
        stripped = line.lstrip()
        if fence_start is None:
            if stripped.startswith("```") or stripped.startswith("~~~"):
                fence_start = index
                fence_marker = stripped[:3]
            continue
        if fence_marker is not None and stripped.startswith(fence_marker):
            block_lines = lines[fence_start - 1 : index]
            context_before = lines[max(0, fence_start - 3) : fence_start - 1]
            evidence_text = "\n".join([*context_before, *block_lines])
            is_evidence = bool(
                EVIDENCE_BLOCK_RE.search(evidence_text)
                or any(EVIDENCE_COMMAND_RE.search(block_line) for block_line in block_lines)
                or any(FILE_LINE_CITATION_RE.search(block_line) for block_line in block_lines)
            )
            blocks.append((fence_start, index, is_evidence))
            fence_start = None
            fence_marker = None
    if fence_start is not None:
        blocks.append((fence_start, len(lines), False))
    return blocks


def _line_is_inside_block(line_number: int, blocks: list[tuple[int, int, bool]]) -> bool:
    return any(start <= line_number <= end for start, end, _is_evidence in blocks)


def _only_evidence_adjacency_lines(lines: list[str]) -> bool:
    meaningful = [line for line in lines if line.strip()]
    if len(meaningful) > 1:
        return False
    return not meaningful or all(EVIDENCE_ADJACENCY_RE.match(line) for line in meaningful)


def _has_adjacent_evidence_block(
    line_number: int,
    lines: list[str],
    blocks: list[tuple[int, int, bool]],
) -> bool:
    for start, end, is_evidence in blocks:
        if not is_evidence:
            continue
        if line_number < start and _only_evidence_adjacency_lines(lines[line_number : start - 1]):
            return True
        if line_number > end and _only_evidence_adjacency_lines(lines[end : line_number - 1]):
            return True
    return False


def _line_has_numeric_pin(line: str) -> bool:
    text = INLINE_CODE_SPAN_RE.sub("", line)
    text = ISO_DATE_RE.sub("", text)
    text = TASK_REFERENCE_RE.sub("", text)
    return bool(DECIMAL_OR_PERCENT_PIN_RE.search(text) or STRUCTURE_COUNT_PIN_RE.search(text))


def _claim_evidence_issues_for_file(path: Path, *, relative_path: str) -> list[ClaimEvidenceIssue]:
    lines = read_text_or_error(path).splitlines()
    blocks = _collect_fenced_markdown_blocks(lines)
    issues: list[ClaimEvidenceIssue] = []
    for index, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or _line_is_inside_block(index, blocks):
            continue

        has_evidence = _has_adjacent_evidence_block(index, lines, blocks)
        if FILE_LINE_CITATION_RE.search(line) and not has_evidence:
            issues.append(
                ClaimEvidenceIssue(
                    relative_path=relative_path,
                    line_number=index,
                    reason="file-line citation lacks adjacent grep/Read evidence block",
                    line=stripped,
                )
            )
        if _line_has_numeric_pin(line) and not has_evidence:
            issues.append(
                ClaimEvidenceIssue(
                    relative_path=relative_path,
                    line_number=index,
                    reason="numeric claim lacks adjacent grep/Read evidence block",
                    line=stripped,
                )
            )
    return issues


def lint_openspec_claim_evidence(change_dir: Path) -> list[ClaimEvidenceIssue]:
    issues: list[ClaimEvidenceIssue] = []
    for path in _iter_claim_lint_markdown_files(change_dir):
        relative_path = path.relative_to(change_dir).as_posix()
        issues.extend(_claim_evidence_issues_for_file(path, relative_path=relative_path))
    return issues


def required_validation_evidence_categories_for_plan(summary: ImplementationPlanSummary) -> tuple[str, ...]:
    contract_surface = " ".join((*summary.contract_surface_lines, *summary.proof_obligation_lines)).lower()
    required_categories: list[str] = []

    def add(category: str) -> None:
        if category not in required_categories:
            required_categories.append(category)

    if any(keyword in contract_surface for keyword in ("prompt", "prompt interface", "prompt-interface")):
        add("prompt_contract")
    if any(keyword in contract_surface for keyword in ("repair", "artifact mutation")):
        add("artifact_repair")
    if any(keyword in contract_surface for keyword in ("schema", "persistence")):
        add("schema")
    if any(keyword in contract_surface for keyword in ("documentation/process", "documentation", "process", "review", "guidance")):
        add("manual_inspection")
    if any(keyword in contract_surface for keyword in ("orchestration", "runtime", "behavioral", "completion", "resolver")):
        add("runtime_path")
    if any(keyword in contract_surface for keyword in ("negative", "reject", "drift", "narrow proof")):
        add("negative_case")

    if not required_categories:
        add("runtime_path")

    return tuple(required_categories)


def validate_implementation_plan_file(plan_path: Path) -> ImplementationPlanSummary:
    lines = read_text_or_error(plan_path).splitlines()
    plan_label = str(plan_path)

    contract_surface = _meaningful_markdown_lines(
        _collect_markdown_section(lines, title="Contract Surface", level=2)
    )
    if not contract_surface:
        raise ValueError(f"{plan_label} is missing required section `## Contract Surface`")

    proof_obligations = _meaningful_markdown_lines(
        _collect_markdown_section(lines, title="Proof Obligations", level=2)
    )
    if not proof_obligations:
        raise ValueError(f"{plan_label} is missing required section `## Proof Obligations`")

    validation_plan = _collect_markdown_section(lines, title="Validation Plan", level=2)
    if validation_plan is None:
        raise ValueError(f"{plan_label} is missing required section `## Validation Plan`")

    required_validation_lines = _meaningful_markdown_lines(
        _collect_markdown_section(validation_plan, title="Required Validation Classes", level=3)
    )
    required_validation_classes = tuple(
        value.lower()
        for value in _parse_bullet_values(required_validation_lines)
    )
    if not required_validation_classes:
        raise ValueError(
            f"{plan_label} is missing required validation classes under `### Required Validation Classes`"
        )

    justification_lines = _meaningful_markdown_lines(
        _collect_markdown_section(validation_plan, title="Unit-Only Justification", level=3)
    )
    unit_only_justification = " ".join(justification_lines).strip() or None

    if _requires_runtime_facing_validation(contract_surface):
        has_runtime_facing_class = any(
            validation_class in RUNTIME_FACING_VALIDATION_CLASSES
            for validation_class in required_validation_classes
        )
        has_unit_only_justification = bool(unit_only_justification) and unit_only_justification.lower() not in {
            "none",
            "none.",
        }
        if not has_runtime_facing_class and not has_unit_only_justification:
            raise ValueError(
                f"{plan_label} requires a runtime-facing validation class or an explicit unit-only justification"
            )

    return ImplementationPlanSummary(
        contract_surface_lines=tuple(contract_surface),
        proof_obligation_lines=tuple(proof_obligations),
        required_validation_classes=required_validation_classes,
        unit_only_justification=unit_only_justification,
    )


def _parse_main_spec_requirement_names(spec_path: Path) -> set[str]:
    if not spec_path.exists():
        return set()
    names: set[str] = set()
    for line in read_text_or_error(spec_path).splitlines():
        match = REQUIREMENT_HEADER_RE.match(line.strip())
        if match:
            names.add(match.group("name"))
    return names


def _parse_delta_spec_modified_and_renamed(spec_path: Path) -> tuple[list[str], set[str]]:
    modified_requirements: list[str] = []
    renamed_to_names: set[str] = set()
    current_operation: str | None = None
    for line in read_text_or_error(spec_path).splitlines():
        stripped = line.strip()
        operation_match = DELTA_OPERATION_RE.match(stripped)
        if operation_match:
            current_operation = operation_match.group("op")
            continue
        if current_operation == "MODIFIED":
            requirement_match = REQUIREMENT_HEADER_RE.match(stripped)
            if requirement_match:
                modified_requirements.append(requirement_match.group("name"))
        elif current_operation == "RENAMED":
            to_match = RENAMED_TO_RE.match(stripped)
            if to_match:
                renamed_to_names.add(to_match.group("name"))
    return modified_requirements, renamed_to_names


def openspec_archive_modified_without_rename_bridge(change_dir: Path, repo_root: Path) -> list[str]:
    """Return archive-readiness issues for delta `## MODIFIED` requirements that
    cannot be located in the main spec and lack a `## RENAMED` bridge.

    OpenSpec archive applies a "## MODIFIED" block by matching its
    "### Requirement: <name>" header against the same-named requirement in the main
    spec. When a change renames a requirement, the new header only resolves if a
    "## RENAMED Requirements" bridge with a matching "- TO:" line maps it from the
    old main-spec header. A MODIFIED header that is neither present in the main spec
    nor a RENAMED TO target would fail only at archive time, so this gate surfaces it
    during readiness instead.
    """
    issues: list[str] = []
    specs_root = change_dir / "specs"
    if not specs_root.is_dir():
        return issues
    main_specs_root = repo_root / "openspec" / "specs"
    for delta_spec_path in sorted(specs_root.glob("*/spec.md")):
        capability = delta_spec_path.parent.name
        modified_requirements, renamed_to_names = _parse_delta_spec_modified_and_renamed(delta_spec_path)
        if not modified_requirements:
            continue
        main_requirement_names = _parse_main_spec_requirement_names(main_specs_root / capability / "spec.md")
        for requirement_name in modified_requirements:
            if requirement_name in main_requirement_names or requirement_name in renamed_to_names:
                continue
            issues.append(
                f"openspec/changes/{change_dir.name}/specs/{capability}/spec.md "
                f"`## MODIFIED` requirement `{requirement_name}` header differs from the main spec "
                f"and has no `## RENAMED` bridge"
            )
    return issues


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
    spec_errors = validate_promoted_feature_openspec_specs(feature_text, section_name="READY")
    if spec_errors:
        raise WorkflowStateError(f"{feature_label} is missing OpenSpec Specs metadata")

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
            if _terminates_field_continuation(stripped):
                current_field = None
                continue
            current_depends_on.extend(TASK_REF_RE.findall(stripped))

    flush_task()
    return tasks


def parse_openspec_tasks_file(tasks_file: Path, *, current_task: str | None = None) -> list[TaskRecord]:
    raw_tasks = _parse_openspec_tasks_text(read_text_or_error(tasks_file))
    return _derive_openspec_task_statuses(raw_tasks, current_task=current_task)


def find_openspec_task_structure_errors(tasks_text: str) -> list[str]:
    top_level_task_ids = {
        task.task_id
        for task in _parse_openspec_tasks_text(tasks_text)
    }
    errors: list[str] = []
    nested_task_ids: list[str] = []

    for line in tasks_text.splitlines():
        nested_match = OPEN_SPEC_NESTED_TASK_RE.match(line)
        if not nested_match:
            continue

        nested_task_id = nested_match.group("id")
        nested_task_ids.append(nested_task_id)
        parent_task_id = nested_task_id.split(".", 1)[0]
        if parent_task_id in top_level_task_ids:
            continue

        errors.append(
            f"nested checklist item `{nested_task_id}` is missing parent top-level executable task `{parent_task_id}`"
        )

    if nested_task_ids and not top_level_task_ids:
        errors.insert(
            0,
            "tasks.md has nested checklist items but no top-level executable tasks; "
            "add parent tasks like `- [ ] 1 ...` before nested items such as `1.1`",
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
    # A cross-feature `Depends On` cycle used to blow the stack: the caches below are allocated per
    # call, so A -> B -> A re-entered A with no memory of being inside it.
    if feature_file is not None:
        key = feature_file.resolve()
        if key in _PARSING_FEATURES:
            raise WorkflowStateError(
                f"dependency cycle: {key.name} is reached again while its own tasks are being "
                f"resolved; a cross-feature `Depends On` chain loops back to it")
        _PARSING_FEATURES.add(key)
        try:
            return _parse_tasks_inner(feature_text, feature_file=feature_file, repo_root=repo_root)
        finally:
            _PARSING_FEATURES.discard(key)
    return _parse_tasks_inner(feature_text, feature_file=feature_file, repo_root=repo_root)


def _parse_tasks_inner(
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
        _parse_openspec_tasks_text(read_text_or_error(tasks_file)),
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
    nested_items_by_task = _parse_openspec_open_nested_items(read_text_or_error(tasks_file))
    return nested_items_by_task.get(task_id, [])


def parse_feature_id(feature_text: str, *, feature_file: Path | None = None) -> str | None:
    feature_id_match = FEATURE_ID_RE.search(feature_text)
    if feature_id_match:
        return feature_id_match.group(1)
    if feature_file is None:
        return None
    parts = feature_file.stem.split("-", 2)
    if len(parts) >= 2:
        return f"{parts[0]}-{parts[1]}"
    return feature_file.stem


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
            read_text_or_error(dependency_feature_file),
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
    done_task_ids = {task.task_id for task in tasks if task.status == "done"}
    done_task_ids.add(completed_task_id)
    feature_file_cache: dict[str, Path | None] = {}
    task_cache: dict[Path, dict[str, TaskRecord]] = {}

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

        if dependencies_satisfied:
            return CompletionHandoff(
                action="start_task",
                target_feature_id=local_feature_id,
                target_task_id=task.task_id,
                reason="next_ready_task",
                requires_human_decision=False,
            )

    if any(task.task_id not in done_task_ids for task in tasks):
        return CompletionHandoff(
            action="stop",
            target_feature_id=local_feature_id,
            target_task_id=None,
            reason="no_ready_task",
            requires_human_decision=True,
        )

    return CompletionHandoff(
        action="finish_feature",
        target_feature_id=local_feature_id,
        target_task_id=None,
        reason="all_tasks_complete",
        requires_human_decision=False,
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
