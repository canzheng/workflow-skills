from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LESSONS_SCHEMA = REPO_ROOT / "docs" / "lessons" / "lessons-schema.md"
CANDIDATE_SCHEMA = REPO_ROOT / "docs" / "lessons" / "lesson-candidates-schema.md"


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


if __name__ == "__main__":
    unittest.main()
