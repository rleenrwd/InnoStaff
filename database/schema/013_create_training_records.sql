USE InnoStaff;
GO

CREATE TABLE dbo.TrainingRecords
(
    TrainingRecordId INT NOT NULL,
    PlacementId INT NOT NULL,
    TrainingDate DATE NOT NULL,
    TrainerCode VARCHAR(20) NOT NULL,
    TrainingType VARCHAR(20) NOT NULL,
    CompletionStatus VARCHAR(12) NOT NULL,
    DurationHours DECIMAL(8,2) NOT NULL,
    TrainingCostUSD DECIMAL(12,2) NOT NULL,
    ConflictingInstructionReported BIT NULL,

    CONSTRAINT PK_TrainingRecords
        PRIMARY KEY (TrainingRecordId),

    CONSTRAINT FK_TrainingRecords_Placements
        FOREIGN KEY (PlacementId)
        REFERENCES dbo.Placements (PlacementId),

    CONSTRAINT CK_TrainingRecords_TrainingType
        CHECK (TrainingType IN ('Onboarding', 'Refresher')),

    CONSTRAINT CK_TrainingRecords_CompletionStatus
        CHECK (CompletionStatus IN
        (
            'Completed',
            'Incomplete',
            'Cancelled'
        )),

    CONSTRAINT CK_TrainingRecords_DurationHours
        CHECK (DurationHours >= 0),

    CONSTRAINT CK_TrainingRecords_TrainingCostUSD
        CHECK (TrainingCostUSD >= 0)
);
GO