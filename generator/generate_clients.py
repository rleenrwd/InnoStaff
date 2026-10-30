import random

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

    if len(clients) < len(regions):
        raise ValueError(
            "Regional coverage requires at least seven clients "
            "when generating one site per client."
        )

    client_sites = []

    for site_id, client in enumerate(clients, start=1):
        if site_id <= len(regions):
            region = regions[site_id - 1]
        else:
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


