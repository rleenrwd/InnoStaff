import unittest

from generate_clients import generate_clients, generate_client_sites
from generate_branches import generate_branches
from generate_recruiters import generate_recruiters
from validation import validate_client_sites, validate_recruiters



class ClientSiteValidationTests(unittest.TestCase):
    def test_rejects_site_with_nonexistent_client(self):
        clients = generate_clients(count=10, seed=41027)
        client_sites = generate_client_sites(clients, seed=41028)

        client_sites[0]["ClientId"] = -999

        with self.assertRaisesRegex(ValueError, "references nonexistent client"):
            validate_client_sites(clients, client_sites)


class RecruiterValidationTests(unittest.TestCase):
    def test_rejects_recruiter_with_nonexistent_branch(self):
        branches = generate_branches()
        recruiters = generate_recruiters(branches, recruiters_per_branch=2)

        recruiters[0]["BranchId"] = -999

        with self.assertRaisesRegex(ValueError, "references nonexistent branch"):
            validate_recruiters(branches, recruiters)

if __name__ == "__main__":
    unittest.main()