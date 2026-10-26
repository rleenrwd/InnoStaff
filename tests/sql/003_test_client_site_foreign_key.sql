USE InnoStaff;
GO

SET XACT_ABORT ON;

IF EXISTS (
    SELECT 1
    FROM dbo.Clients
    WHERE ClientId = -999
)
BEGIN
    THROW 50002, 'Test requires ClientId -999 to be absent.', 1;
END;

BEGIN TRY
    BEGIN TRANSACTION;

    INSERT INTO dbo.ClientSites
        (ClientSiteId, ClientId, SiteCode, SiteName, Region)
    VALUES
        (
            -1,
            -999,
            'TEST-SITE-001',
            N'Test Site',
            N'Alameda'
        );

    THROW 50003, 'FAIL: Site with a nonexistent client was accepted.', 1;
END TRY
BEGIN CATCH
    IF XACT_STATE() <> 0
        ROLLBACK TRANSACTION;

    IF ERROR_NUMBER() = 547
       AND ERROR_MESSAGE() LIKE '%FK_ClientSites_Clients%'
    BEGIN
        PRINT 'PASS: Site with a nonexistent client was rejected.';
    END
    ELSE
    BEGIN
        THROW;
    END;
END CATCH;
GO