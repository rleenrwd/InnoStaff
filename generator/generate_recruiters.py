def generate_recruiters(branches, recruiters_per_branch):
    if recruiters_per_branch < 1:
        raise ValueError("Recruiters per branch must be at least one.")

    recruiters = []
    recruiter_id = 1

    for branch in branches:
        for _ in range(recruiters_per_branch):
            recruiter = {
                "RecruiterId": recruiter_id,
                "BranchId": branch["BranchId"],
                "RecruiterCode": f"REC-{recruiter_id:04d}",
                "DisplayName": f"InnoStaff Demo Recruiter {recruiter_id:04d}",
            }

            recruiters.append(recruiter)
            recruiter_id += 1

    return recruiters