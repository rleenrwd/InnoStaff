import unittest

from validation import validate_hiring_cohorts


class HiringCohortValidationTests(unittest.TestCase):
    def setUp(self):
        self.snapshot_date = "2026-09-30"

        self.job_orders = [
            {
                "JobOrderId": 1,
                "OpenDate": "2024-01-01",
                "CloseDate": None,
            }
        ]

        self.hiring_cohorts = [
            {
                "HiringCohortId": 1,
                "JobOrderId": 1,
                "CohortCode": "COH-00001",
                "CohortStartDate": "2024-02-01",
            }
        ]

    def validate(self):
        validate_hiring_cohorts(
            self.job_orders,
            self.hiring_cohorts,
            self.snapshot_date,
        )

    def test_accepts_opening_and_snapshot_boundaries(self):
        for start_date in ("2024-01-01", "2026-09-30"):
            with self.subTest(start_date=start_date):
                self.hiring_cohorts[0]["CohortStartDate"] = start_date
                self.validate()

    def test_rejects_duplicate_identifiers(self):
        for field, message in (
            ("HiringCohortId", "Duplicate hiring cohort ID"),
            ("CohortCode", "Duplicate hiring cohort code"),
        ):
            with self.subTest(field=field):
                duplicate = self.hiring_cohorts[0].copy()
                duplicate["HiringCohortId"] = 2
                duplicate["CohortCode"] = "COH-00002"
                duplicate["CohortStartDate"] = "2024-03-01"
                duplicate[field] = self.hiring_cohorts[0][field]
                self.hiring_cohorts.append(duplicate)

                with self.assertRaisesRegex(ValueError, message):
                    self.validate()

                self.hiring_cohorts.pop()

    def test_rejects_nonexistent_order(self):
        self.hiring_cohorts[0]["JobOrderId"] = -999

        with self.assertRaisesRegex(ValueError, "nonexistent job order"):
            self.validate()

    def test_rejects_dates_outside_opening_and_snapshot(self):
        for start_date in ("2023-12-31", "2026-10-01"):
            with self.subTest(start_date=start_date):
                self.hiring_cohorts[0]["CohortStartDate"] = start_date

                with self.assertRaisesRegex(
                    ValueError,
                    "before order opening or after the snapshot",
                ):
                    self.validate()

    def test_accepts_day_before_closing(self):
        self.job_orders[0]["CloseDate"] = "2024-02-02"
        self.validate()

    def test_rejects_start_on_or_after_closing(self):
        self.job_orders[0]["CloseDate"] = "2024-02-01"

        for start_date in ("2024-02-01", "2024-02-02"):
            with self.subTest(start_date=start_date):
                self.hiring_cohorts[0]["CohortStartDate"] = start_date

                with self.assertRaisesRegex(ValueError, "on or after order closing"):
                    self.validate()

    def test_rejects_repeated_order_start_date(self):
        duplicate = self.hiring_cohorts[0].copy()
        duplicate["HiringCohortId"] = 2
        duplicate["CohortCode"] = "COH-00002"
        self.hiring_cohorts.append(duplicate)

        with self.assertRaisesRegex(ValueError, "order/start-date pair"):
            self.validate()

    def test_accepts_same_date_for_different_orders(self):
        second_order = self.job_orders[0].copy()
        second_order["JobOrderId"] = 2
        self.job_orders.append(second_order)

        second_cohort = self.hiring_cohorts[0].copy()
        second_cohort["HiringCohortId"] = 2
        second_cohort["CohortCode"] = "COH-00002"
        second_cohort["JobOrderId"] = 2
        self.hiring_cohorts.append(second_cohort)

        self.validate()


if __name__ == "__main__":
    unittest.main()