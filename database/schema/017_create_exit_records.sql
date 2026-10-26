USE InnoStaff;
GO

CREATE TABLE dbo.ExitRecords
(
    ExitRecordId INT NOT NULL,
    PlacementId INT NOT NULL,
    ExitClass VARCHAR(20) NOT NULL,
    PrimaryReason VARCHAR(30) NOT NULL,
    AgencyDeparture BIT NOT NULL,
    ExitNotes NVARCHAR(500) NULL,

    CONSTRAINT PK_ExitRecords
        PRIMARY KEY (ExitRecordId),

    CONSTRAINT UQ_ExitRecords_PlacementId
        UNIQUE (PlacementId),

    CONSTRAINT FK_ExitRecords_Placements
        FOREIGN KEY (PlacementId)
        REFERENCES dbo.Placements (PlacementId),

    CONSTRAINT CK_ExitRecords_ExitClass
        CHECK (ExitClass IN
        (
            'Voluntary',
            'Involuntary',
            'ContractCompleted',
            'ClientConversion',
            'Transfer'
        )),

    CONSTRAINT CK_ExitRecords_PrimaryReason
        CHECK (PrimaryReason IN
        (
            'Commute',
            'Schedule',
            'JobFit',
            'Training',
            'Career',
            'Personal',
            'Performance',
            'ContractEnd',
            'Conversion',
            'Transfer',
            'Unknown'
        )),

    CONSTRAINT CK_ExitRecords_TransferDeparture
        CHECK (
            ExitClass <> 'Transfer'
            OR AgencyDeparture = 0
        ),

    CONSTRAINT CK_ExitRecords_ConversionDeparture
        CHECK (
            ExitClass <> 'ClientConversion'
            OR AgencyDeparture = 1
        )
);
GO