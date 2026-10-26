USE InnoStaff;
GO

CREATE TABLE dbo.JobOrders
(
    JobOrderId INT NOT NULL,
    JobOrderCode VARCHAR(20) NOT NULL,
    ClientSiteId INT NOT NULL,
    JobRoleId INT NOT NULL,
    RecruiterId INT NOT NULL,
    OpenDate DATE NOT NULL,
    CloseDate DATE NULL,
    AdvertisedHourlyWage DECIMAL(8,2) NOT NULL,
    AdvertisedWeeklyHours DECIMAL(8,2) NOT NULL,
    AdvertisedShift VARCHAR(15) NOT NULL,
    AdvertisedWeekendRequired BIT NOT NULL,
    AdvertisedHolidayRequired BIT NOT NULL,
    AdvertisedDuties NVARCHAR(1000) NOT NULL,
    TransferAvailable BIT NOT NULL,

    CONSTRAINT PK_JobOrders
        PRIMARY KEY (JobOrderId),

    CONSTRAINT UQ_JobOrders_JobOrderCode
        UNIQUE (JobOrderCode),

    CONSTRAINT FK_JobOrders_ClientSites
        FOREIGN KEY (ClientSiteId)
        REFERENCES dbo.ClientSites (ClientSiteId),

    CONSTRAINT FK_JobOrders_JobRoles
        FOREIGN KEY (JobRoleId)
        REFERENCES dbo.JobRoles (JobRoleId),

    CONSTRAINT FK_JobOrders_Recruiters
        FOREIGN KEY (RecruiterId)
        REFERENCES dbo.Recruiters (RecruiterId),

    CONSTRAINT CK_JobOrders_DateRange
        CHECK (CloseDate IS NULL OR CloseDate > OpenDate),

    CONSTRAINT CK_JobOrders_AdvertisedHourlyWage
        CHECK (AdvertisedHourlyWage > 0),

    CONSTRAINT CK_JobOrders_AdvertisedWeeklyHours
        CHECK (
            AdvertisedWeeklyHours > 0
            AND AdvertisedWeeklyHours <= 84
        ),

    CONSTRAINT CK_JobOrders_AdvertisedShift
        CHECK (AdvertisedShift IN
        (
            'Day',
            'Swing',
            'Overnight',
            'Rotating'
        ))
);
GO