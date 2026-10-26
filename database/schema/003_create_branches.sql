USE InnoStaff;
GO

CREATE TABLE dbo.Branches
(
    BranchId INT NOT NULL,
    BranchCode VARCHAR(20) NOT NULL,
    BranchName NVARCHAR(100) NOT NULL,
    Region NVARCHAR(60) NOT NULL,

    CONSTRAINT PK_Branches
        PRIMARY KEY (BranchId),

    CONSTRAINT UQ_Branches_BranchCode
        UNIQUE (BranchCode)
);
GO