from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LESSONS_SCHEMA = REPO_ROOT / "docs" / "lessons" / "lessons-schema.md"
CANDIDATE_SCHEMA = REPO_ROOT / "docs" / "lessons" / "lesson-candidates-schema.md"
RETRIEVE_SKILL = REPO_ROOT / "skills" / "retrieve-lessons" / "SKILL.md"
USAGE_SKILL = REPO_ROOT / "skills" / "record-lesson-usage" / "SKILL.md"
REFRESH_SKILL = REPO_ROOT / "skills" / "refresh-lessons" / "SKILL.md"


class LessonContractDocTests(unittest.TestCase):
    def test_promoted_schema_documents_float_applied_count(self) -> None:
        schema = LESSONS_SCHEMA.read_text(encoding="utf-8")

        self.assertIn("applied_count: float >= 0, required", schema)

    def test_promoted_schema_documents_partial_application_range(self) -> None:
        schema = LESSONS_SCHEMA.read_text(encoding="utf-8")

        self.assertIn("applied should add 1.0 to applied_count.", schema)
        self.assertIn("partially_applied should add the model-provided applied level between 0.1 and 0.9 to applied_count.", schema)
        self.assertIn("not_applied should add 0.0 to applied_count.", schema)

    def test_candidate_schema_supports_archived_records(self) -> None:
        schema = CANDIDATE_SCHEMA.read_text(encoding="utf-8")

        self.assertIn("status: candidate|archived, required", schema)
        self.assertIn("archived", schema)

    def test_retrieve_lessons_stays_a_pure_selection_step(self) -> None:
        skill = RETRIEVE_SKILL.read_text(encoding="utf-8")

        self.assertIn("It only selects and returns relevant lessons; end-of-task usage is recorded separately.", skill)
        self.assertIn("Return only `id`, `domain`, `lesson`, `applies_when`, and `rationale` for the final set.", skill)
        self.assertNotIn("handoff artifact", skill)

    def test_record_usage_uses_lesson_id_and_float_counts(self) -> None:
        skill = USAGE_SKILL.read_text(encoding="utf-8")

        self.assertIn("For each lesson_id you need to record at the end of the task", skill)
        self.assertIn("Record the matching `lesson_id` together with the chosen status.", skill)
        self.assertIn("recorded `applied_level`", skill)
        self.assertIn("add `1.0` to `applied_count`", skill)
        self.assertIn("add `0.0` to `applied_count` and leave `last_applied_at` unchanged.", skill)

    def test_refresh_lessons_owns_agents_and_merge_semantics(self) -> None:
        skill = REFRESH_SKILL.read_text(encoding="utf-8")

        self.assertIn("Only `refresh-lessons` may copy a lesson into `AGENTS.md`.", skill)
        self.assertIn("Treat a lesson as stale when it has not been applied for 30 days.", skill)
        self.assertIn(
            "For merges, update `lesson`, `applies_when`, `confidence`, `source_evidence`, `applied_count`, `retrieved_count`, `last_retrieved_at`, `last_applied_at`, and `updated_at`.",
            skill,
        )
        self.assertIn("When merging, set `last_applied_at` to the later timestamp among the merged lessons.", skill)
        self.assertIn("Set `status: archived` when archiving.", skill)


if __name__ == "__main__":
    unittest.main()
