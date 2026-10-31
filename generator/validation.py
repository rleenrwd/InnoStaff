from datetime import date
from decimal import Decimal

def validate_client_sites(clients, client_sites):
    client_ids = {client["ClientId"] for client in clients}

    for site in client_sites:
        if site["ClientId"] not in client_ids:
            raise ValueError(
                f"Site {site['ClientSiteId']} references "
                f"nonexistent client {site['ClientId']}."
            )

def validate_recruiters(branches, recruiters):
    branch_ids = {branch["BranchId"] for branch in branches}

    for recruiter in recruiters:
        if recruiter["BranchId"] not in branch_ids:
            raise ValueError(
                f"Recruiter {recruiter['RecruiterId']} references "
                f"nonexistent branch {recruiter['BranchId']}."
            )

def validate_workers(workers, coverage_start, snapshot_date):
    start_date = date.fromisoformat(coverage_start)
    end_date = date.fromisoformat(snapshot_date)

    if end_date < start_date:
        raise ValueError("Snapshot date cannot precede coverage start.")

    allowed_categories = {"Gig", "Operations", "Technical", "Other"}
    worker_ids = set()
    worker_codes = set()

    for worker in workers:
        worker_id = worker["WorkerId"]
        worker_code = worker["WorkerCode"]

        if worker_id in worker_ids:
            raise ValueError(f"Duplicate worker ID: {worker_id}.")

        if worker_code in worker_codes:
            raise ValueError(f"Duplicate worker code: {worker_code}.")

        worker_ids.add(worker_id)
        worker_codes.add(worker_code)

        if worker["PriorWorkCategory"] not in allowed_categories:
            raise ValueError(f"Worker {worker_id} has an invalid prior-work category.")

        registered_date = date.fromisoformat(worker["RegisteredDate"])

        if not start_date <= registered_date <= end_date:
            raise ValueError(f"Worker {worker_id} has a registration date outside dataset coverage.")


def validate_career_goals(workers, career_goals, snapshot_date):
    workers_by_id = {worker["WorkerId"]: worker for worker in workers}

    allowed_families = {
        "Operations",
        "Software",
        "Network", 
        "Systems",
        "IT",
        "Security",
        "StableEmployment",
        "Other",
    }

    end_date = date.fromisoformat(snapshot_date)
    career_goal_ids = set()

    for career_goal in career_goals:
        career_goal_id = career_goal["CareerGoalId"]
        worker_id = career_goal["WorkerId"]


        if career_goal_id in career_goal_ids:
            raise ValueError(f"Duplicate career goal ID: {career_goal_id}.")

        career_goal_ids.add(career_goal_id)

        if worker_id not in workers_by_id:
            raise ValueError(f"Career goal {career_goal_id} references a nonexistent worker {worker_id}.")

        if career_goal["GoalFamily"] not in allowed_families:
            raise ValueError(f"Career goal {career_goal_id} has an invalid goal family.")

        worker = workers_by_id[worker_id]
        registered_date = date.fromisoformat(worker["RegisteredDate"])
        recorded_date = date.fromisoformat(career_goal["RecordedDate"])

        if not registered_date <= recorded_date <= end_date:
            raise ValueError(f"Career goal {career_goal_id} has a recorded date before worker registration or after the snapshot.")


def validate_job_orders(client_sites, job_roles, recruiters, job_orders, config):
    site_ids = {site["ClientSiteId"] for site in client_sites}
    roles_by_id = {role["JobRoleId"]: role for role in job_roles}
    recruiter_ids = {recruiter["RecruiterId"] for recruiter in recruiters}

    coverage_start = date.fromisoformat(config["coverage_start"])
    snapshot_date = date.fromisoformat(config["snapshot_date"])

    allowed_shifts = {"Day", "Swing", "Overnight", "Rotating"}
    job_order_ids = set()
    job_order_codes = set()

    for job_order in job_orders:
        job_order_id = job_order["JobOrderId"]
        job_order_code = job_order["JobOrderCode"]

        if job_order_id in job_order_ids:
            raise ValueError(f"Duplicate job order ID: {job_order_id}.")

        if job_order_code in job_order_codes:
            raise ValueError(f"Duplicate job order code: {job_order_code}.")

        job_order_ids.add(job_order_id)
        job_order_codes.add(job_order_code)

        if job_order["ClientSiteId"] not in site_ids:
            raise ValueError(
                f"Job order {job_order_id} references a nonexistent site."
            )

        if job_order["JobRoleId"] not in roles_by_id:
            raise ValueError(
                f"Job order {job_order_id} references a nonexistent role."
            )

        if job_order["RecruiterId"] not in recruiter_ids:
            raise ValueError(
                f"Job order {job_order_id} references a nonexistent recruiter."
            )

        hourly_wage = Decimal(str(job_order["AdvertisedHourlyWage"]))
        weekly_hours = Decimal(str(job_order["AdvertisedWeeklyHours"]))

        role = roles_by_id[job_order["JobRoleId"]]
        wage_band = config["hourly_wage_bands"][role["ExperienceLevel"]]
        minimum_wage = Decimal(str(wage_band["minimum"]))
        maximum_wage = Decimal(str(wage_band["maximum"]))

        if not hourly_wage.is_finite() or hourly_wage <= 0:
            raise ValueError(
                f"Job order {job_order_id} has an invalid hourly wage."
            )

        if not minimum_wage <= hourly_wage <= maximum_wage:
            raise ValueError(
                f"Job order {job_order_id} has a wage outside its configured band."
            )

        if not weekly_hours.is_finite() or not 0 < weekly_hours <= 84:
            raise ValueError(
                f"Job order {job_order_id} has invalid weekly hours."
            )

        if job_order["AdvertisedShift"] not in allowed_shifts:
            raise ValueError(
                f"Job order {job_order_id} has an invalid advertised shift."
            )

        for field in (
            "AdvertisedWeekendRequired",
            "AdvertisedHolidayRequired",
            "TransferAvailable",
        ):
            if job_order[field] not in (0, 1):
                raise ValueError(
                    f"Job order {job_order_id} has an invalid {field} flag."
                )

        open_date = date.fromisoformat(job_order["OpenDate"])

        if not coverage_start <= open_date <= snapshot_date:
            raise ValueError(
                f"Job order {job_order_id} opens outside dataset coverage."
            )

        if job_order["CloseDate"] is not None:
            close_date = date.fromisoformat(job_order["CloseDate"])

            if not open_date < close_date <= snapshot_date:
                raise ValueError(
                    f"Job order {job_order_id} has an invalid closing date."
                )