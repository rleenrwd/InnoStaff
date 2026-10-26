USE InnoStaff;
GO

CREATE TABLE dbo.CareerEvents
(
    CareerEventId INT NOT NULL,
    PlacementId INT NOT NULL,
    EventDate DATE NOT NULL,
    EventType VARCHAR(20) NOT NULL,
    TargetRoleId INT NULL,
    CareerGoalId INT NULL,
    ResultingPlacementId INT NULL,

    CONSTRAINT PK_CareerEvents
        PRIMARY KEY (CareerEventId),

    CONSTRAINT FK_CareerEvents_Placements
        FOREIGN KEY (PlacementId)
        REFERENCES dbo.Placements (PlacementId),

    CONSTRAINT FK_CareerEvents_JobRoles
        FOREIGN KEY (TargetRoleId)
        REFERENCES dbo.JobRoles (JobRoleId),

    CONSTRAINT FK_CareerEvents_CareerGoals
        FOREIGN KEY (CareerGoalId)
        REFERENCES dbo.CareerGoals (CareerGoalId),

    CONSTRAINT FK_CareerEvents_ResultingPlacement
        FOREIGN KEY (ResultingPlacementId)
        REFERENCES dbo.Placements (PlacementId),

    CONSTRAINT CK_CareerEvents_EventType
        CHECK (EventType IN
        (
            'Promotion',
            'ClientConversion',
            'LateralTransfer'
        )),

    CONSTRAINT CK_CareerEvents_DifferentResultingPlacement
        CHECK (
            ResultingPlacementId IS NULL
            OR ResultingPlacementId <> PlacementId
        ),

    CONSTRAINT CK_CareerEvents_ConversionPlacement
        CHECK (
            EventType <> 'ClientConversion'
            OR ResultingPlacementId IS NULL
        )
);
GO