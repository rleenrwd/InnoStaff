import unittest

from validation import validate_job_orders


class JobOrderValidationTests(unittest.TestCase):
    def setUp(self):
        self.client_sites = [{"ClientSiteId": 1}]
        self.job_roles = [{"JobRoleId": 1, "ExperienceLevel": "Entry"}]
        self.recruiters = [{"RecruiterId": 1}]

        self.config = {
            "coverage_start": "2023-10-01",
            "snapshot_date": "2026-09-30",
            "hourly_wage_bands": {
                "Entry": {
                    "minimum": 23,
                    "maximum": 38,
                }
            },
        }

        self.job_orders = [
            {
                "JobOrderId": 1,
                "JobOrderCode": "ORD-00001",
                "ClientSiteId": 1,
                "JobRoleId": 1,
                "RecruiterId": 1,
                "OpenDate": "2024-01-01",
                "CloseDate": None,
                "AdvertisedHourlyWage": "30.00",
                "AdvertisedWeeklyHours": "40.00",
                "AdvertisedShift": "Day",
                "AdvertisedWeekendRequired": 0,
                "AdvertisedHolidayRequired": 0,
                "AdvertisedDuties": "Perform scripted vehicle tests.",
                "TransferAvailable": 1,
            }
        ]

    def validate(self):
        validate_job_orders(
            self.client_sites,
            self.job_roles,
            self.recruiters,
            self.job_orders,
            self.config,
        )

    def test_accepts_valid_order(self):
        self.validate()

    def test_rejects_duplicate_identifiers(self):
        for field, message in (
            ("JobOrderId", "Duplicate job order ID"),
            ("JobOrderCode", "Duplicate job order code"),
        ):
            with self.subTest(field=field):
                duplicate = self.job_orders[0].copy()
                duplicate["JobOrderId"] = 2
                duplicate["JobOrderCode"] = "ORD-00002"
                duplicate[field] = self.job_orders[0][field]
                self.job_orders.append(duplicate)

                with self.assertRaisesRegex(ValueError, message):
                    self.validate()

                self.job_orders.pop()

    def test_rejects_missing_references(self):
        for field, message in (
            ("ClientSiteId", "nonexistent site"),
            ("JobRoleId", "nonexistent role"),
            ("RecruiterId", "nonexistent recruiter"),
        ):
            with self.subTest(field=field):
                self.job_orders[0][field] = -999

                with self.assertRaisesRegex(ValueError, message):
                    self.validate()

                self.job_orders[0][field] = 1

    def test_accepts_wage_band_boundaries(self):
        for wage in ("23.00", "38.00"):
            with self.subTest(wage=wage):
                self.job_orders[0]["AdvertisedHourlyWage"] = wage
                self.validate()

    def test_rejects_invalid_wages(self):
        for wage in ("0.00", "-1.00", "22.99", "38.01", "NaN", "Infinity"):
            with self.subTest(wage=wage):
                self.job_orders[0]["AdvertisedHourlyWage"] = wage

                with self.assertRaisesRegex(ValueError, "wage"):
                    self.validate()

    def test_rejects_invalid_weekly_hours(self):
        for hours in ("0.00", "-1.00", "84.01", "NaN", "Infinity"):
            with self.subTest(hours=hours):
                self.job_orders[0]["AdvertisedWeeklyHours"] = hours

                with self.assertRaisesRegex(ValueError, "weekly hours"):
                    self.validate()

    def test_rejects_invalid_shift(self):
        self.job_orders[0]["AdvertisedShift"] = "Unsupported"

        with self.assertRaisesRegex(ValueError, "advertised shift"):
            self.validate()

    def test_rejects_invalid_flags(self):
        for field in (
            "AdvertisedWeekendRequired",
            "AdvertisedHolidayRequired",
            "TransferAvailable",
        ):
            with self.subTest(field=field):
                original_value = self.job_orders[0][field]
                self.job_orders[0][field] = 2

                with self.assertRaisesRegex(ValueError, "flag"):
                    self.validate()

                self.job_orders[0][field] = original_value

    def test_rejects_opening_outside_coverage(self):
        for open_date in ("2023-09-30", "2026-10-01"):
            with self.subTest(open_date=open_date):
                self.job_orders[0]["OpenDate"] = open_date

                with self.assertRaisesRegex(ValueError, "outside dataset coverage"):
                    self.validate()

    def test_rejects_invalid_closing_dates(self):
        for close_date in ("2023-12-31", "2024-01-01", "2026-10-01"):
            with self.subTest(close_date=close_date):
                self.job_orders[0]["CloseDate"] = close_date

                with self.assertRaisesRegex(ValueError, "closing date"):
                    self.validate()

    def test_accepts_closing_on_snapshot(self):
        self.job_orders[0]["CloseDate"] = self.config["snapshot_date"]
        self.validate()


if __name__ == "__main__":
    unittest.main()