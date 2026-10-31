import random
from datetime import date, timedelta

def generate_workers(count, seed, coverage_start, snapshot_date):
    if count < 1:
        raise ValueError("Worker count must be at least one.")

    start_date = date.fromisoformat(coverage_start)
    end_date = date.fromisoformat(snapshot_date)

    if end_date < start_date:
        raise ValueError("Snapshot date cannot precede coverage start.")

    random_generator = random.Random(seed)

    regions = [
        "San Francisco",
        "San Jose",
        "Santa Clara",
        "Palo Alto",
        "Oakland",
        "Alameda",
        "Fremont",
    ]

    prior_work_categories = [
        "Gig",
        "Operations",
        "Technical",
        "Other",
    ]

    available_days = (end_date - start_date).days
    workers = []

    for worker_id in range(1, count + 1):
        registration_offset = random_generator.randint(0, available_days)
        registered_date = start_date + timedelta(days=registration_offset)

        worker = {
            "WorkerId": worker_id,
            "WorkerCode": f"WRK-{worker_id:06d}",
            "DisplayName": f"InnoStaff Demo Worker {worker_id:06d}",
            "HomeRegion": random_generator.choice(regions),
            "PriorWorkCategory": random_generator.choice(prior_work_categories),
            "RegisteredDate": registered_date.isoformat(),
        }

        workers.append(worker)

    return workers