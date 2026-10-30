def validate_client_sites(clients, client_sites):
    client_ids = {client["ClientId"] for client in clients}

    for site in client_sites:
        if site["ClientId"] not in client_ids:
            raise ValueError(
                f"Site {site['ClientSiteId']} references "
                f"nonexistent client {site['ClientId']}."
            )