USE InnoStaff;
GO

SET XACT_ABORT ON;

BEGIN TRY
    BEGIN TRANSACTION;

    INSERT INTO dbo.Workers
        (
            WorkerId,
            WorkerCode,
            DisplayName,
            HomeRegion,
            PriorWorkCategory,
            RegisteredDate
        )
    VALUES
        (
            -1,
            'TEST-WORKER-001',
            NULL,
            N'Oakland',
            'Gig',
            '20260101'
        );

    THROW 50005, 'FAIL: Worker without a name was accepted.', 1;
END TRY
BEGIN CATCH
    IF XACT_STATE() <> 0
        ROLLBACK TRANSACTION;

    IF ERROR_NUMBER() = 515
       AND ERROR_MESSAGE() LIKE '%DisplayName%'
       AND ERROR_MESSAGE() LIKE '%Workers%'
    BEGIN
        PRINT 'PASS: Worker without a name was rejected.';
    END
    ELSE
    BEGIN
        THROW;
    END;
END CATCH;
GO