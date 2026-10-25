USE InnoStaff;
GO

CREATE TABLE dbo.Recruiters
(
    RecruiterId INT NOT NULL,
    BranchId INT NOT NULL,
    RecruiterCode VARCHAR(20) NOT NULL,
    DisplayName NVARCHAR(100) NOT NULL,

    CONSTRAINT PK_Recruiters
        PRIMARY KEY (RecruiterId),

    CONSTRAINT UQ_Recruiters_RecruiterCode
        UNIQUE (RecruiterCode),

    CONSTRAINT FK_Recruiters_Branches
        FOREIGN KEY (BranchId)
        REFERENCES dbo.Branches (BranchId)
);
GO