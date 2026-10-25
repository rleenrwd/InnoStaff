USE InnoStaff;
GO

CREATE TABLE dbo.CareerGoals
(
    CareerGoalId INT NOT NULL,
    WorkerId INT NOT NULL,
    RecordedDate DATE NOT NULL,
    GoalFamily VARCHAR(30) NOT NULL,
    GoalDescription NVARCHAR(200) NULL,

    CONSTRAINT PK_CareerGoals
        PRIMARY KEY (CareerGoalId),

    CONSTRAINT FK_CareerGoals_Workers
        FOREIGN KEY (WorkerId)
        REFERENCES dbo.Workers (WorkerId),

    CONSTRAINT CK_CareerGoals_GoalFamily
        CHECK (GoalFamily IN
        (
            'Operations',
            'Software',
            'Network',
            'Systems',
            'IT',
            'Security',
            'StableEmployment',
            'Other'
        ))
);
GO