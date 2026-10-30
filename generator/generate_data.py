import json
from pathlib import Path

from generate_clients import generate_clients, generate_client_sites
from validation import validate_client_sites
from export import write_csv
from generate_job_roles import generate_job_roles


if __name__ == "__main__":
    clients = generate_clients(count=10, seed=41027)
    client_sites = generate_client_sites(clients, seed=41028)
    job_roles = generate_job_roles()

    validate_client_sites(clients, client_sites)

    generated_data = {
        "Clients": clients,
        "ClientSites": client_sites,
        "JobRoles":job_roles
    }

    print(json.dumps(generated_data, indent=4))
    print("PASS: Every client site references an existing client.")

    output_directory = Path(__file__).resolve().parent / "output"

    write_csv(clients, output_directory / "Clients.csv")
    write_csv(client_sites, output_directory / "ClientSites.csv")
    write_csv(job_roles, output_directory / "JobRoles.csv")

    print(f"CSV files exported to: {output_directory}")