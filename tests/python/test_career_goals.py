import unittest

from validation import validate_career_goals


class CareerGoalValidationTests(unittest.TestCase):
    def setUp(self):
        self.snapshot_date = "2026-09-30"

        self.workers = [
            {
                "WorkerId": 1,
                "RegisteredDate": "2024-01-01",
            }
        ]

        self.career_goals = [
            {
                "CareerGoalId": 1,
                "WorkerId": 1,
                "RecordedDate": "2024-01-01",
                "GoalFamily": "Software",
                "GoalDescription": "Pursue software development.",
            }
        ]

    def test_accepts_valid_date_boundaries(self):
        for recorded_date in ("2024-01-01", "2026-09-30"):
            with self.subTest(recorded_date=recorded_date):
                self.career_goals[0]["RecordedDate"] = recorded_date

                validate_career_goals(
                    self.workers,
                    self.career_goals,
                    self.snapshot_date,
                )

    def test_accepts_worker_without_recorded_goals(self):
        validate_career_goals(
            self.workers,
            [],
            self.snapshot_date,
        )

    def test_accepts_multiple_dated_goals_for_worker(self):
        later_goal = self.career_goals[0].copy()
        later_goal["CareerGoalId"] = 2
        later_goal["RecordedDate"] = "2025-01-01"
        later_goal["GoalFamily"] = "StableEmployment"
        self.career_goals.append(later_goal)

        validate_career_goals(
            self.workers,
            self.career_goals,
            self.snapshot_date,
        )

    def test_rejects_duplicate_goal_id(self):
        self.career_goals.append(self.career_goals[0].copy())

        with self.assertRaisesRegex(ValueError, "Duplicate career goal ID"):
            validate_career_goals(
                self.workers,
                self.career_goals,
                self.snapshot_date,
            )

    def test_rejects_nonexistent_worker(self):
        self.career_goals[0]["WorkerId"] = -999

        with self.assertRaisesRegex(ValueError, "references a nonexistent worker"):
            validate_career_goals(
                self.workers,
                self.career_goals,
                self.snapshot_date,
            )

    def test_rejects_invalid_goal_family(self):
        self.career_goals[0]["GoalFamily"] = "Unsupported"

        with self.assertRaisesRegex(ValueError, "invalid goal family"):
            validate_career_goals(
                self.workers,
                self.career_goals,
                self.snapshot_date,
            )

    def test_rejects_dates_outside_worker_timeline(self):
        for recorded_date in ("2023-12-31", "2026-10-01"):
            with self.subTest(recorded_date=recorded_date):
                self.career_goals[0]["RecordedDate"] = recorded_date

                with self.assertRaisesRegex(ValueError, "recorded date"):
                    validate_career_goals(
                        self.workers,
                        self.career_goals,
                        self.snapshot_date,
                    )


if __name__ == "__main__":
    unittest.main()