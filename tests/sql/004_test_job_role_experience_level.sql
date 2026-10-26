USE InnoStaff;
GO

SET XACT_ABORT ON;

BEGIN TRY
    BEGIN TRANSACTION;

    INSERT INTO dbo.JobRoles
        (
            JobRoleId,
            RoleCode,
            RoleName,
            RoleFamily,
            ExperienceLevel,
            RequirementsSummary
        )
    VALUES
        (
            -1,
            'TEST-ROLE-001',
            N'Test Operator',
            'Operations',
            'Beginner',
            N'Test role for constraint verification.'
        );

    THROW 50004, 'FAIL: Invalid experience level was accepted.', 1;
END TRY
BEGIN CATCH
    IF XACT_STATE() <> 0
        ROLLBACK TRANSACTION;

    IF ERROR_NUMBER() = 547
       AND ERROR_MESSAGE() LIKE '%CK_JobRoles_ExperienceLevel%'
    BEGIN
        PRINT 'PASS: Invalid experience level was rejected.';
    END
    ELSE
    BEGIN
        THROW;
    END;
END CATCH;
GO