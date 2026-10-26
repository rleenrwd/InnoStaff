USE InnoStaff;
GO

CREATE TABLE dbo.HiringCohorts 
(
	HiringCohortId INT NOT NULL,
	JobOrderId INT NOT NULL,
	CohortCode VARCHAR(30) NOT NULL,
	CohortStartDate DATE NOT NULL,

	CONSTRAINT PK_HiringCohorts
		PRIMARY KEY (HiringCohortId),

	CONSTRAINT UQ_HiringCohorts_CohortCode
		UNIQUE (CohortCode),

	CONSTRAINT FK_HiringCohorts_JobOrders
		FOREIGN KEY (JobOrderId)
		REFERENCES dbo.JobOrders(JobOrderId)
);
GO