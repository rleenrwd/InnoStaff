def generate_job_roles():
    role_definitions = [
        {
            "RoleName": "Autonomous Vehicle Operator",
            "RoleFamily": "Operations",
            "ExperienceLevel": "Entry",
            "RequirementsSummary": "Valid driver license and ability to follow testing procedures.",
        },
        {
            "RoleName": "Junior Software Developer",
            "RoleFamily": "Software",
            "ExperienceLevel": "Entry",
            "RequirementsSummary": "Foundational programming, Git, and relational database knowledge.",
        },
        {
            "RoleName": "Network Technician",
            "RoleFamily": "Network",
            "ExperienceLevel": "Intermediate",
            "RequirementsSummary": "Experience troubleshooting network connectivity and equipment.",
        },
        {
            "RoleName": "Systems Administrator",
            "RoleFamily": "Systems",
            "ExperienceLevel": "Experienced",
            "RequirementsSummary": "Experience administering servers, user access, and system backups.",
        },
        {
            "RoleName": "IT Support Technician",
            "RoleFamily": "IT",
            "ExperienceLevel": "Entry",
            "RequirementsSummary": "Foundational hardware, operating system, and troubleshooting knowledge.",
        },
        {
            "RoleName": "Security Analyst",
            "RoleFamily": "Security",
            "ExperienceLevel": "Intermediate",
            "RequirementsSummary": "Experience reviewing security alerts and investigating incidents.",
        },
    ]

    job_roles = []

    for role_id, definition in enumerate(role_definitions, start=1):
        role = {
            "JobRoleId": role_id,
            "RoleCode": f"ROLE-{role_id:04d}",
            "RoleName": definition["RoleName"],
            "RoleFamily": definition["RoleFamily"],
            "ExperienceLevel": definition["ExperienceLevel"],
            "RequirementsSummary": definition["RequirementsSummary"],
        }

        job_roles.append(role)

    return job_roles