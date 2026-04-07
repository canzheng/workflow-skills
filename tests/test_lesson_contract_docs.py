from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LESSONS_SCHEMA = REPO_ROOT / "docs" / "lessons" / "lessons-schema.md"
CANDIDATE_SCHEMA = REPO_ROOT / "docs" / "lessons" / "lesson-candidates-schema.md"
CAPTURE_SKILL = REPO_ROOT / "skills" / "capture-lessons" / "SKILL.md"
PROMOTE_SKILL = REPO_ROOT / "skills" / "promote-lessons" / "SKILL.md"


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

    def test_capture_lessons_uses_promotion_policy_without_agents_md(self) -> None:
        skill = CAPTURE_SKILL.read_text(encoding="utf-8")

        self.assertIn("promote the lesson using the same rules as `promote-lessons`", skill)
        self.assertIn("archive the source candidate record after processing", skill)
        self.assertNotIn("AGENTS.md", skill)

    def test_promote_lessons_archives_processed_candidates_without_agents_md(self) -> None:
        skill = PROMOTE_SKILL.read_text(encoding="utf-8")

        self.assertIn("matching candidate records with `status: candidate`", skill)
        self.assertIn("Archive the source candidate record after it is processed.", skill)
        self.assertNotIn("Copy a lesson into `AGENTS.md`", skill)
        self.assertNotIn("write promoted lessons to `AGENTS.md`", skill)


if __name__ == "__main__":
    unittest.main()
