USE InnoStaff;
GO

SET XACT_ABORT ON;

BEGIN TRY
    BEGIN TRANSACTION;

    INSERT INTO dbo.Clients
        (ClientId, ClientCode, ClientName, IndustrySegment)
    VALUES
        (-1, 'TEST-CLIENT-001', N'Test Client', 'Robotics');

    INSERT INTO dbo.ClientSites
        (ClientSiteId, ClientId, SiteCode, SiteName, Region)
    VALUES
        (-1, -1, 'TEST-SITE-001', N'Test Site', N'Alameda');

    IF NOT EXISTS (
        SELECT 1
        FROM dbo.ClientSites AS cs
        INNER JOIN dbo.Clients AS c
            ON c.ClientId = cs.ClientId
        WHERE cs.ClientSiteId = -1
          AND c.ClientId = -1
    )
    BEGIN
        THROW 50006, 'FAIL: Expected client-site relationship was not found.', 1;
    END;

    ROLLBACK TRANSACTION;

    PRINT 'PASS: Valid client-site relationship was accepted.';
END TRY
BEGIN CATCH
    IF XACT_STATE() <> 0
        ROLLBACK TRANSACTION;

    THROW;
END CATCH;
GO