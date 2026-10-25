USE InnoStaff;
GO

CREATE TABLE dbo.JobRoles
(
    JobRoleId INT NOT NULL,
    RoleCode VARCHAR(30) NOT NULL,
    RoleName NVARCHAR(100) NOT NULL,
    RoleFamily VARCHAR(30) NOT NULL,
    ExperienceLevel VARCHAR(20) NOT NULL,
    RequirementsSummary NVARCHAR(500) NOT NULL,

    CONSTRAINT PK_JobRoles
        PRIMARY KEY (JobRoleId),

    CONSTRAINT UQ_JobRoles_RoleCode
        UNIQUE (RoleCode),

    CONSTRAINT CK_JobRoles_RoleFamily
        CHECK (RoleFamily IN
        (
            'Operations',
            'Software',
            'Network',
            'Systems',
            'IT',
            'Security',
            'Other'
        )),

    CONSTRAINT CK_JobRoles_ExperienceLevel
        CHECK (ExperienceLevel IN
        (
            'Entry',
            'Intermediate',
            'Experienced'
        ))
);
GO