USE InnoStaff;
GO

CREATE TABLE dbo.WorkerSurveys
(
    WorkerSurveyId INT NOT NULL,
    PlacementId INT NOT NULL,
    SurveyDate DATE NOT NULL,
    ExpectationFitScore TINYINT NULL,
    TrainingConsistencyScore TINYINT NULL,
    ConfidenceScore TINYINT NULL,
    JobSatisfactionScore TINYINT NULL,
    ExperiencedDuties NVARCHAR(500) NULL,
    StableEmploymentPreferred BIT NULL,

    CONSTRAINT PK_WorkerSurveys
        PRIMARY KEY (WorkerSurveyId),

    CONSTRAINT FK_WorkerSurveys_Placements
        FOREIGN KEY (PlacementId)
        REFERENCES dbo.Placements (PlacementId),

    CONSTRAINT UQ_WorkerSurveys_PlacementDate
        UNIQUE (PlacementId, SurveyDate),

    CONSTRAINT CK_WorkerSurveys_ExpectationFitScore
        CHECK (
            ExpectationFitScore IS NULL
            OR ExpectationFitScore BETWEEN 1 AND 5
        ),

    CONSTRAINT CK_WorkerSurveys_TrainingConsistencyScore
        CHECK (
            TrainingConsistencyScore IS NULL
            OR TrainingConsistencyScore BETWEEN 1 AND 5
        ),

    CONSTRAINT CK_WorkerSurveys_ConfidenceScore
        CHECK (
            ConfidenceScore IS NULL
            OR ConfidenceScore BETWEEN 1 AND 5
        ),

    CONSTRAINT CK_WorkerSurveys_JobSatisfactionScore
        CHECK (
            JobSatisfactionScore IS NULL
            OR JobSatisfactionScore BETWEEN 1 AND 5
        ),

    CONSTRAINT CK_WorkerSurveys_HasResponse
        CHECK (
            ExpectationFitScore IS NOT NULL
            OR TrainingConsistencyScore IS NOT NULL
            OR ConfidenceScore IS NOT NULL
            OR JobSatisfactionScore IS NOT NULL
            OR ExperiencedDuties IS NOT NULL
            OR StableEmploymentPreferred IS NOT NULL
        )
);
GO