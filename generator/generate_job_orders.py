import random
from datetime import date, timedelta
from decimal import Decimal


def generate_job_orders(client_sites, job_roles, recruiters, config, seed):
    if not client_sites or not job_roles or not recruiters:
        raise ValueError("Job orders require sites, roles, and recruiters.")

    count = config["job_order_count"]

    if count < len(job_roles):
        raise ValueError("Job order count must cover every role.")

    start_date = date.fromisoformat(config["coverage_start"])
    snapshot_date = date.fromisoformat(config["snapshot_date"])

    if snapshot_date < start_date:
        raise ValueError("Snapshot date cannot precede coverage start.")

    random_generator = random.Random(seed)

    shifts = ["Day", "Swing", "Overnight", "Rotating"]
    weekly_hours_options = ["20.00", "24.00", "30.00", "32.00", "40.00"]
    weekly_hours_weights = [1, 1, 1, 3, 6]

    available_days = (snapshot_date - start_date).days
    job_orders = []

    for job_order_id in range(1, count + 1):
        role_index = (job_order_id - 1) % len(job_roles)
        role = job_roles[role_index]

        site = random_generator.choice(client_sites)
        recruiter = random_generator.choice(recruiters)

        wage_band = config["hourly_wage_bands"][role["ExperienceLevel"]]
        minimum_cents = int(Decimal(str(wage_band["minimum"])) * 100)
        maximum_cents = int(Decimal(str(wage_band["maximum"])) * 100)

        if minimum_cents <= 0 or maximum_cents < minimum_cents:
            raise ValueError("Hourly wage bands must be positive and ordered.")

        wage_cents = random_generator.randint(minimum_cents, maximum_cents)
        hourly_wage = Decimal(wage_cents) / Decimal("100")

        open_offset = random_generator.randint(0, available_days)
        open_date = start_date + timedelta(days=open_offset)

        weekly_hours = random_generator.choices(
            weekly_hours_options,
            weights=weekly_hours_weights,
            k=1,
        )[0]

        job_order = {
            "JobOrderId": job_order_id,
            "JobOrderCode": f"ORD-{job_order_id:05d}",
            "ClientSiteId": site["ClientSiteId"],
            "JobRoleId": role["JobRoleId"],
            "RecruiterId": recruiter["RecruiterId"],
            "OpenDate": open_date.isoformat(),
            "CloseDate": None,
            "AdvertisedHourlyWage": format(hourly_wage, ".2f"),
            "AdvertisedWeeklyHours": weekly_hours,
            "AdvertisedShift": random_generator.choice(shifts),
            "AdvertisedWeekendRequired": random_generator.choice([0, 1]),
            "AdvertisedHolidayRequired": random_generator.choice([0, 1]),
            "AdvertisedDuties": (
                f"Perform assigned {role['RoleName']} duties, "
                "follow documented procedures, and report work outcomes."
            ),
            "TransferAvailable": random_generator.choice([0, 1]),
        }

        job_orders.append(job_order)

    return job_orders