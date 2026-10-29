import unittest

from generate_data import generate_clients, generate_client_sites, validate_client_sites


class ClientSiteValidationTests(unittest.TestCase):
    def test_rejects_site_with_nonexistent_client(self):
        clients = generate_clients(count=10, seed=41027)
        client_sites = generate_client_sites(clients, seed=41028)

        client_sites[0]["ClientId"] = -999

        with self.assertRaisesRegex(ValueError, "references nonexistent client"):
            validate_client_sites(clients, client_sites)


if __name__ == "__main__":
    unittest.main()