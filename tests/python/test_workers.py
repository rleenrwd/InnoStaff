import unittest

from generate_workers import generate_workers
from validation import validate_workers


class WorkerValidationTests(unittest.TestCase):
    def setUp(self):
        self.coverage_start = "2023-10-01"
        self.snapshot_date = "2026-09-30"

        self.workers = generate_workers(
            count=3,
            seed=41029,
            coverage_start=self.coverage_start,
            snapshot_date=self.snapshot_date,
        )

    def test_accepts_valid_workers(self):
        validate_workers(
            self.workers,
            self.coverage_start,
            self.snapshot_date,
        )

    def test_rejects_duplicate_worker_id(self):
        self.workers[1]["WorkerId"] = self.workers[0]["WorkerId"]

        with self.assertRaisesRegex(ValueError, "Duplicate worker ID"):
            validate_workers(
                self.workers,
                self.coverage_start,
                self.snapshot_date,
            )

    def test_rejects_duplicate_worker_code(self):
        self.workers[1]["WorkerCode"] = self.workers[0]["WorkerCode"]

        with self.assertRaisesRegex(ValueError, "Duplicate worker code"):
            validate_workers(
                self.workers,
                self.coverage_start,
                self.snapshot_date,
            )

    def test_rejects_invalid_prior_work_category(self):
        self.workers[0]["PriorWorkCategory"] = "Unsupported"

        with self.assertRaisesRegex(ValueError, "invalid prior-work category"):
            validate_workers(
                self.workers,
                self.coverage_start,
                self.snapshot_date,
            )

    def test_rejects_registration_outside_coverage(self):
        for registered_date in ("2023-09-30", "2026-10-01"):
            with self.subTest(registered_date=registered_date):
                self.workers[0]["RegisteredDate"] = registered_date

                with self.assertRaisesRegex(ValueError, "outside dataset coverage"):
                    validate_workers(
                        self.workers,
                        self.coverage_start,
                        self.snapshot_date,
                    )


if __name__ == "__main__":
    unittest.main()