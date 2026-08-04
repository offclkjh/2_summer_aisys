"""Focused tests for curriculum metadata and context assembly."""

import unittest

from tools.curriculum_lib import ancestors, load_curriculum
from tools.session_context import build_context


class CurriculumToolTests(unittest.TestCase):
    def test_has_exactly_s01_through_s40(self) -> None:
        _, sessions, _ = load_curriculum()
        self.assertEqual(
            [session["id"] for session in sessions],
            [f"S{number:02d}" for number in range(1, 41)],
        )

    def test_s01_points_to_external_refresh_cards(self) -> None:
        context = build_context("s01")
        self.assertEqual(context["status"], "ready")
        self.assertEqual(context["depends_on"], [])
        self.assertTrue(
            all(item["refresh"] for item in context["required_concepts"])
        )

    def test_s38_can_reach_both_concept_sources(self) -> None:
        _, _, by_id = load_curriculum()
        self.assertTrue({"S12", "S37"}.issubset(ancestors("S38", by_id)))
        context = build_context("S38")
        self.assertTrue(
            all(
                item["available_through_dependency"]
                for item in context["required_concepts"]
            )
        )

    def test_every_session_context_includes_authoring_scope(self) -> None:
        for number in range(1, 41):
            context = build_context(f"S{number:02d}")
            self.assertTrue(context["authoring"]["question"])
            self.assertTrue(context["authoring"]["core_case"])
            self.assertTrue(context["authoring"]["exclude"])


if __name__ == "__main__":
    unittest.main()
