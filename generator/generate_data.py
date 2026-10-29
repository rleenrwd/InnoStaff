import json
import random
import csv
from pathlib import Path


def generate_clients(count, seed):
    random_generator = random.Random(seed)

    industry_segments = [
        "Robotics",
        "Autonomous Vehicles",
        "Software",
        "Cloud Services",
    ]

    clients = []

    for client_id in range(1, count + 1):
        client = {
            "ClientId": client_id,
            "ClientCode": f"CLI-{client_id:04d}",
            "ClientName": f"InnoStaff Demo Client {client_id:04d}",
            "IndustrySegment": random_generator.choice(industry_segments),
        }

        clients.append(client)

    return clients

def generate_client_sites(clients, seed):
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

    client_sites = []

    for site_id, client in enumerate(clients, start=1):
        region = random_generator.choice(regions)

        site = {
            "ClientSiteId": site_id,
            "ClientId": client["ClientId"],
            "SiteCode": f"SITE-{site_id:04d}",
            "SiteName": f"{region} Site {site_id:04d}",
            "Region": region,
        }

        client_sites.append(site)

    return client_sites



def validate_client_sites(clients, client_sites):
    client_ids = {client["ClientId"] for client in clients}

    for site in client_sites:
        if site["ClientId"] not in client_ids:
            raise ValueError(
                f"Site {site['ClientSiteId']} references "
                f"nonexistent client {site['ClientId']}."
            )



def write_csv(records, output_path):
    if not records:
        raise ValueError("Cannot export an empty list of records.")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(records[0].keys()))
        writer.writeheader()
        writer.writerows(records)



if __name__ == "__main__":
    clients = generate_clients(count=10, seed=41027)
    client_sites = generate_client_sites(clients, seed=41028)

    validate_client_sites(clients, client_sites)

    generated_data = {
        "Clients": clients,
        "ClientSites": client_sites,
    }

    print(json.dumps(generated_data, indent=4))
    print("PASS: Every client site references an existing client.")

    output_directory = Path(__file__).resolve().parent / "output"

    write_csv(clients, output_directory / "Clients.csv")
    write_csv(client_sites, output_directory / "ClientSites.csv")

    print(f"CSV files exported to: {output_directory}")