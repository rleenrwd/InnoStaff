USE InnoStaff;
GO

SET XACT_ABORT ON;

BEGIN TRY
    BEGIN TRANSACTION;

    INSERT INTO dbo.Clients
        (ClientId, ClientCode, ClientName, IndustrySegment)
    VALUES
        (-1, 'TEST-CLIENT-001', N'Test Client One', 'Robotics');

    INSERT INTO dbo.Clients
        (ClientId, ClientCode, ClientName, IndustrySegment)
    VALUES
        (-2, 'TEST-CLIENT-001', N'Test Client Two', 'Robotics');

    THROW 50001, 'FAIL: Duplicate client code was accepted.', 1;
END TRY
BEGIN CATCH
    IF XACT_STATE() <> 0
        ROLLBACK TRANSACTION;

    IF ERROR_NUMBER() = 2627
       AND ERROR_MESSAGE() LIKE '%UQ_Clients_ClientCode%'
    BEGIN
        PRINT 'PASS: Duplicate client code was rejected.';
    END
    ELSE
    BEGIN
        THROW;
    END;
END CATCH;
GO