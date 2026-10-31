import random
from datetime import date, timedelta


def generate_hiring_cohorts(job_orders, config, seed):
    minimum_count = config["minimum_cohorts_per_order"]
    maximum_count = config["maximum_cohorts_per_order"]

    if minimum_count < 1 or maximum_count < minimum_count:
        raise ValueError("Cohort counts must be positive and ordered.")

    snapshot_date = date.fromisoformat(config["snapshot_date"])
    random_generator = random.Random(seed)

    hiring_cohorts = []
    hiring_cohort_id = 1

    for job_order in job_orders:
        open_date = date.fromisoformat(job_order["OpenDate"])
        latest_start_date = snapshot_date

        if job_order["CloseDate"] is not None:
            close_date = date.fromisoformat(job_order["CloseDate"])
            latest_start_date = min(
                snapshot_date,
                close_date - timedelta(days=1),
            )

        available_days = (latest_start_date - open_date).days + 1

        if available_days < minimum_count:
            raise ValueError(
                f"Job order {job_order['JobOrderId']} has too few "
                "available dates for the minimum cohort count."
            )

        allowed_maximum = min(maximum_count, available_days)

        cohort_count = random_generator.randint(
            minimum_count,
            allowed_maximum,
        )

        selected_offsets = sorted(
            random_generator.sample(range(available_days), k=cohort_count)
        )

        for offset in selected_offsets:
            cohort_start_date = open_date + timedelta(days=offset)

            hiring_cohort = {
                "HiringCohortId": hiring_cohort_id,
                "JobOrderId": job_order["JobOrderId"],
                "CohortCode": f"COH-{hiring_cohort_id:05d}",
                "CohortStartDate": cohort_start_date.isoformat(),
            }

            hiring_cohorts.append(hiring_cohort)
            hiring_cohort_id += 1

    return hiring_cohorts