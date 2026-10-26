USE InnoStaff;
GO

CREATE TABLE dbo.Workers
(
    WorkerId INT NOT NULL,
    WorkerCode VARCHAR(20) NOT NULL,
    DisplayName NVARCHAR(100) NOT NULL,
    HomeRegion NVARCHAR(60) NOT NULL,
    PriorWorkCategory VARCHAR(30) NOT NULL,
    RegisteredDate DATE NOT NULL,

    CONSTRAINT PK_Workers
        PRIMARY KEY (WorkerId),

    CONSTRAINT UQ_Workers_WorkerCode
        UNIQUE (WorkerCode),

    CONSTRAINT CK_Workers_PriorWorkCategory
        CHECK (PriorWorkCategory IN
        (
            'Gig',
            'Operations',
            'Technical',
            'Other'
        ))
);
GO