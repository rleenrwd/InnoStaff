import json
from pathlib import Path

from generate_clients import generate_clients, generate_client_sites
from validation import validate_client_sites, validate_recruiters, validate_workers, validate_career_goals, validate_job_orders, validate_hiring_cohorts
from export import write_csv
from generate_job_roles import generate_job_roles
from generate_branches import generate_branches
from generate_recruiters import generate_recruiters
from generate_workers import generate_workers
from generate_career_goals import generate_career_goals
from generate_job_orders import generate_job_orders
from generate_hiring_cohorts import generate_hiring_cohorts


if __name__ == "__main__":

    config_path = Path(__file__).resolve().parent / "config" / "small.json"

    with config_path.open("r", encoding="utf-8") as config_file:
        config = json.load(config_file)

    clients = generate_clients(count=config["client_count"], seed=config["seed"])
    client_sites = generate_client_sites(clients, seed=41028)
    job_roles = generate_job_roles()
    branches = generate_branches()
    recruiters = generate_recruiters(branches, recruiters_per_branch=config["recruiters_per_branch"])
    workers = generate_workers(count=config["worker_count"], seed=config["seed"] + 2, coverage_start=config["coverage_start"], snapshot_date=config["snapshot_date"] )
    career_goals = generate_career_goals(workers, seed=config["seed"] + 3, initial_goal_probability=config["initial_goal_probability"])
    job_orders = generate_job_orders(client_sites, job_roles, recruiters, config, seed=config["seed"] + 4)
    hiring_cohorts = generate_hiring_cohorts(job_orders, config, seed=config["seed"] + 5)
    validate_hiring_cohorts(job_orders, hiring_cohorts, snapshot_date=config["snapshot_date"]),


    validate_client_sites(clients, client_sites)
    validate_recruiters(branches, recruiters)
    validate_workers(workers, coverage_start=config["coverage_start"], snapshot_date=config["snapshot_date"])
    validate_career_goals(workers, career_goals, snapshot_date=config["snapshot_date"])
    validate_job_orders(client_sites, job_roles, recruiters, job_orders, config)

    generated_data = {
        "Clients": clients,
        "ClientSites": client_sites,
        "JobRoles": job_roles,
        "Branches": branches,
        "Recruiters": recruiters,
        "Workers": workers,
        "CareerGoals": career_goals,
        "JobOrders": job_orders,
        "HiringCohorts": hiring_cohorts,
    }

    print(json.dumps(generated_data, indent=4))
    print("PASS: Every client site references an existing client.")
    print("PASS: Every recruiter references an existing branch.")
    print("PASS: Worker IDs, codes, categories, and registration dates are valid.")
    print("PASS: Career goal IDs, worker references, families, and dates are valid.")
    print("PASS: Job order references, wages, hours, shifts, flags, and dates are valid.")
    print("PASS: Hiring cohort IDs, codes, order references, and dates are valid.")

    output_directory = Path(__file__).resolve().parent / "output"

    write_csv(clients, output_directory / "Clients.csv")
    write_csv(client_sites, output_directory / "ClientSites.csv")
    write_csv(job_roles, output_directory / "JobRoles.csv")
    write_csv(branches, output_directory / "Branches.csv")
    write_csv(recruiters, output_directory / "Recruiters.csv")
    write_csv(workers, output_directory / "Workers.csv")
    write_csv(career_goals, output_directory / "CareerGoals.csv")
    write_csv(job_orders, output_directory / "JobOrders.csv")
    write_csv(hiring_cohorts, output_directory / "HiringCohorts.csv")

    print(f"CSV files exported to: {output_directory}")