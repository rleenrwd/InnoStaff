USE InnoStaff;
GO

CREATE TABLE dbo.ShiftAssignments
(
    ShiftAssignmentId INT NOT NULL,
    PlacementId INT NOT NULL,
    RecordType VARCHAR(10) NOT NULL,
    ParentScheduleId INT NULL,
    EffectiveFrom DATE NULL,
    EffectiveTo DATE NULL,
    ShiftCode VARCHAR(15) NOT NULL,
    WeekendRequired BIT NULL,
    HolidayRequired BIT NULL,
    ScheduleConsistent BIT NULL,
    TransferAvailable BIT NULL,
    RequestedDate DATE NULL,
    ResolvedDate DATE NULL,
    RequestStatus VARCHAR(10) NULL,

    CONSTRAINT PK_ShiftAssignments
        PRIMARY KEY (ShiftAssignmentId),

    CONSTRAINT FK_ShiftAssignments_Placements
        FOREIGN KEY (PlacementId)
        REFERENCES dbo.Placements (PlacementId),

    CONSTRAINT FK_ShiftAssignments_ParentSchedule
        FOREIGN KEY (ParentScheduleId)
        REFERENCES dbo.ShiftAssignments (ShiftAssignmentId),

    CONSTRAINT CK_ShiftAssignments_RecordType
        CHECK (RecordType IN ('Schedule', 'Request')),

    CONSTRAINT CK_ShiftAssignments_ShiftCode
        CHECK (ShiftCode IN
        (
            'Day',
            'Swing',
            'Overnight',
            'Rotating'
        )),

    CONSTRAINT CK_ShiftAssignments_RecordShape
        CHECK (
            (
                RecordType = 'Schedule'
                AND ParentScheduleId IS NULL
                AND EffectiveFrom IS NOT NULL
                AND WeekendRequired IS NOT NULL
                AND HolidayRequired IS NOT NULL
                AND ScheduleConsistent IS NOT NULL
                AND TransferAvailable IS NOT NULL
                AND RequestedDate IS NULL
                AND ResolvedDate IS NULL
                AND RequestStatus IS NULL
            )
            OR
            (
                RecordType = 'Request'
                AND ParentScheduleId IS NOT NULL
                AND EffectiveFrom IS NULL
                AND EffectiveTo IS NULL
                AND WeekendRequired IS NULL
                AND HolidayRequired IS NULL
                AND ScheduleConsistent IS NULL
                AND TransferAvailable IS NULL
                AND RequestedDate IS NOT NULL
                AND RequestStatus IS NOT NULL
            )
        ),

    CONSTRAINT CK_ShiftAssignments_EffectiveDates
        CHECK (
            EffectiveTo IS NULL
            OR EffectiveTo > EffectiveFrom
        ),

    CONSTRAINT CK_ShiftAssignments_RequestStatus
        CHECK (
            RequestStatus IS NULL
            OR RequestStatus IN ('Pending', 'Approved', 'Denied')
        ),

    CONSTRAINT CK_ShiftAssignments_RequestResolution
        CHECK (
            RecordType = 'Schedule'
            OR
            (
                RequestStatus = 'Pending'
                AND ResolvedDate IS NULL
            )
            OR
            (
                RequestStatus IN ('Approved', 'Denied')
                AND ResolvedDate IS NOT NULL
                AND ResolvedDate >= RequestedDate
            )
        ),

    CONSTRAINT CK_ShiftAssignments_NoSelfParent
        CHECK (
            ParentScheduleId IS NULL
            OR ParentScheduleId <> ShiftAssignmentId
        )
);
GO