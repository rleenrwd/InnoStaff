USE InnoStaff;
GO

CREATE TABLE dbo.Placements
(
    PlacementId INT NOT NULL,
    PlacementCode VARCHAR(20) NOT NULL,
    WorkerId INT NOT NULL,
    JobOrderId INT NOT NULL,
    HiringCohortId INT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE NULL,
    PlacementStatus VARCHAR(10) NOT NULL,
    HourlyWage DECIMAL(8,2) NOT NULL,
    ContractWeeklyHours DECIMAL(8,2) NOT NULL,
    PreferredShift VARCHAR(15) NOT NULL,
    HiringPurpose VARCHAR(15) NOT NULL,
    ReplacesPlacementId INT NULL,
    PreviousPlacementId INT NULL,
    RecruitmentCostUSD DECIMAL(12,2) NOT NULL,

    CONSTRAINT PK_Placements
        PRIMARY KEY (PlacementId),

    CONSTRAINT UQ_Placements_PlacementCode
        UNIQUE (PlacementCode),

    CONSTRAINT FK_Placements_Workers
        FOREIGN KEY (WorkerId)
        REFERENCES dbo.Workers (WorkerId),

    CONSTRAINT FK_Placements_JobOrders
        FOREIGN KEY (JobOrderId)
        REFERENCES dbo.JobOrders (JobOrderId),

    CONSTRAINT FK_Placements_HiringCohorts
        FOREIGN KEY (HiringCohortId)
        REFERENCES dbo.HiringCohorts (HiringCohortId),

    CONSTRAINT FK_Placements_ReplacesPlacement
        FOREIGN KEY (ReplacesPlacementId)
        REFERENCES dbo.Placements (PlacementId),

    CONSTRAINT FK_Placements_PreviousPlacement
        FOREIGN KEY (PreviousPlacementId)
        REFERENCES dbo.Placements (PlacementId),

    CONSTRAINT CK_Placements_DateRange
        CHECK (EndDate IS NULL OR EndDate > StartDate),

    CONSTRAINT CK_Placements_StatusAndEndDate
        CHECK (
            (PlacementStatus = 'Active' AND EndDate IS NULL)
            OR
            (PlacementStatus = 'Ended' AND EndDate IS NOT NULL)
        ),

    CONSTRAINT CK_Placements_HourlyWage
        CHECK (HourlyWage > 0),

    CONSTRAINT CK_Placements_ContractWeeklyHours
        CHECK (
            ContractWeeklyHours > 0
            AND ContractWeeklyHours <= 84
        ),

    CONSTRAINT CK_Placements_PreferredShift
        CHECK (PreferredShift IN
        (
            'Day',
            'Swing',
            'Overnight',
            'Rotating',
            'Any'
        )),

    CONSTRAINT CK_Placements_HiringPurpose
        CHECK (HiringPurpose IN
        (
            'Growth',
            'Replacement',
            'Transfer'
        )),

    CONSTRAINT CK_Placements_ReplacementReference
        CHECK (
            (
                HiringPurpose = 'Replacement'
                AND ReplacesPlacementId IS NOT NULL
            )
            OR
            (
                HiringPurpose IN ('Growth', 'Transfer')
                AND ReplacesPlacementId IS NULL
            )
        ),

    CONSTRAINT CK_Placements_NoSelfReplacement
        CHECK (
            ReplacesPlacementId IS NULL
            OR ReplacesPlacementId <> PlacementId
        ),

    CONSTRAINT CK_Placements_NoSelfPrevious
        CHECK (
            PreviousPlacementId IS NULL
            OR PreviousPlacementId <> PlacementId
        ),

    CONSTRAINT CK_Placements_RecruitmentCostUSD
        CHECK (RecruitmentCostUSD >= 0)
);
GO