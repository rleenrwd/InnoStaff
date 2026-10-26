USE InnoStaff;
GO

CREATE TABLE dbo.Attendance
(
    AttendanceId INT NOT NULL,
    PlacementId INT NOT NULL,
    WorkDate DATE NOT NULL,
    ScheduledHours DECIMAL(8,2) NOT NULL,
    WorkedHours DECIMAL(8,2) NOT NULL,
    AttendanceStatus VARCHAR(15) NOT NULL,

    CONSTRAINT PK_Attendance
        PRIMARY KEY (AttendanceId),

    CONSTRAINT FK_Attendance_Placements
        FOREIGN KEY (PlacementId)
        REFERENCES dbo.Placements (PlacementId),

    CONSTRAINT UQ_Attendance_PlacementDate
        UNIQUE (PlacementId, WorkDate),

    CONSTRAINT CK_Attendance_ScheduledHours
        CHECK (ScheduledHours BETWEEN 0 AND 24),

    CONSTRAINT CK_Attendance_WorkedHours
        CHECK (WorkedHours BETWEEN 0 AND 24),

    CONSTRAINT CK_Attendance_HoursWithinSchedule
        CHECK (WorkedHours <= ScheduledHours),

    CONSTRAINT CK_Attendance_Status
        CHECK (AttendanceStatus IN
        (
            'Present',
            'Late',
            'ExcusedAbsence',
            'UnexcusedAbsence'
        )),

    CONSTRAINT CK_Attendance_AbsenceHours
        CHECK (
            AttendanceStatus IN ('Present', 'Late')
            OR WorkedHours = 0
        )
);
GO