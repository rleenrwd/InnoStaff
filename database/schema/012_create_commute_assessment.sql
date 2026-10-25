USE InnoStaff;
GO

CREATE TABLE dbo.CommuteAssessments
(
    CommuteAssessmentId INT NOT NULL,
    PlacementId INT NOT NULL,
    AssessmentDate DATE NOT NULL,
    AssessmentType VARCHAR(12) NOT NULL,
    HomeRegion NVARCHAR(60) NOT NULL,
    OneWayMiles DECIMAL(8,2) NOT NULL,
    OneWayMinutes SMALLINT NOT NULL,
    FuelDailyUSD DECIMAL(8,2) NOT NULL,
    TollsDailyUSD DECIMAL(8,2) NOT NULL,
    ParkingDailyUSD DECIMAL(8,2) NOT NULL,
    CommuteDaysPerWeek TINYINT NOT NULL,

    CONSTRAINT PK_CommuteAssessments
        PRIMARY KEY (CommuteAssessmentId),

    CONSTRAINT FK_CommuteAssessments_Placements
        FOREIGN KEY (PlacementId)
        REFERENCES dbo.Placements (PlacementId),

    CONSTRAINT UQ_CommuteAssessments_PlacementTypeDate
        UNIQUE (PlacementId, AssessmentType, AssessmentDate),

    CONSTRAINT CK_CommuteAssessments_AssessmentType
        CHECK (AssessmentType IN ('Expected', 'Experienced')),

    CONSTRAINT CK_CommuteAssessments_OneWayMiles
        CHECK (OneWayMiles >= 0),

    CONSTRAINT CK_CommuteAssessments_OneWayMinutes
        CHECK (OneWayMinutes >= 0),

    CONSTRAINT CK_CommuteAssessments_FuelDailyUSD
        CHECK (FuelDailyUSD >= 0),

    CONSTRAINT CK_CommuteAssessments_TollsDailyUSD
        CHECK (TollsDailyUSD >= 0),

    CONSTRAINT CK_CommuteAssessments_ParkingDailyUSD
        CHECK (ParkingDailyUSD >= 0),

    CONSTRAINT CK_CommuteAssessments_CommuteDaysPerWeek
        CHECK (CommuteDaysPerWeek BETWEEN 1 AND 7)
);
GO