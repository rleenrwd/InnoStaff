from datetime import date

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