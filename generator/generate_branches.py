
def generate_branches():
    branch_definitions = [
        {
            "BranchName": "InnoStaff San Francisco Branch",
            "Region": "San Francisco",
        },
        {
            "BranchName": "InnoStaff Peninsula Branch",
            "Region": "Palo Alto",
        },
        {
            "BranchName": "InnoStaff South Bay Branch",
            "Region": "San Jose",
        },
        {
            "BranchName": "InnoStaff East Bay Branch",
            "Region": "Oakland",
        },
    ]

    branches = []

    for branch_id, definition in enumerate(branch_definitions, start=1):
        branch = {
            "BranchId":branch_id,
            "BranchCode": f"BR-{branch_id:04d}",
            "BranchName": definition["BranchName"],
            "Region": definition["Region"],
        }

        branches.append(branch)

    return branches