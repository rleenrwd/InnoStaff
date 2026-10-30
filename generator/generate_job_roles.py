def generate_job_roles():
    role_definitions = [
        {
            "RoleName": "Autonomous Vehicle Operator",
            "RoleFamily": "Operations",
            "ExperienceLevel": "Entry",
            "RequirementsSummary": "Valid driver license and ability to follow vehicle testing and safety procedures.",
        },
        {
            "RoleName": "Robot Operator",
            "RoleFamily": "Operations",
            "ExperienceLevel": "Entry",
            "RequirementsSummary": "Basic computer skills and ability to follow robot operation and safety procedures.",
        },
        {
            "RoleName": "Teleoperator",
            "RoleFamily": "Operations",
            "ExperienceLevel": "Entry",
            "RequirementsSummary": "Basic computer skills, clear communication, and ability to follow remote operation procedures.",
        },
        {
            "RoleName": "Vehicle Test Operator",
            "RoleFamily": "Operations",
            "ExperienceLevel": "Entry",
            "RequirementsSummary": "Valid driver license and ability to perform scripted vehicle tests and record observations.",
        },
        {
            "RoleName": "Senior Operations Operator",
            "RoleFamily": "Operations",
            "ExperienceLevel": "Intermediate",
            "RequirementsSummary": "Prior technical operations experience and ability to handle escalations and support new operators.",
        },
        {
            "RoleName": "Operations Team Lead",
            "RoleFamily": "Operations",
            "ExperienceLevel": "Intermediate",
            "RequirementsSummary": "Prior operations experience and ability to coordinate shifts, coach operators, and communicate issues.",
        },
        {
            "RoleName": "Autonomous Vehicle Technician",
            "RoleFamily": "Operations",
            "ExperienceLevel": "Intermediate",
            "RequirementsSummary": "Experience inspecting vehicle hardware, troubleshooting equipment, and documenting maintenance.",
        },
        {
            "RoleName": "Software Engineer",
            "RoleFamily": "Software",
            "ExperienceLevel": "Experienced",
            "RequirementsSummary": "Professional experience developing, testing, and maintaining software using version control.",
        },
        {
            "RoleName": "Network Engineer",
            "RoleFamily": "Network",
            "ExperienceLevel": "Experienced",
            "RequirementsSummary": "Professional experience configuring and troubleshooting routing, switching, and network infrastructure.",
        },
        {
            "RoleName": "Systems Administrator",
            "RoleFamily": "Systems",
            "ExperienceLevel": "Experienced",
            "RequirementsSummary": "Professional experience administering servers, user access, backups, and system monitoring.",
        },
        {
            "RoleName": "IT Support Specialist",
            "RoleFamily": "IT",
            "ExperienceLevel": "Experienced",
            "RequirementsSummary": "Professional experience resolving hardware, operating system, and enterprise application issues.",
        },
        {
            "RoleName": "Cybersecurity Analyst",
            "RoleFamily": "Security",
            "ExperienceLevel": "Experienced",
            "RequirementsSummary": "Professional experience investigating security alerts, assessing threats, and documenting incidents.",
        }
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