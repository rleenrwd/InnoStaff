USE InnoStaff;
GO

CREATE TABLE dbo.Clients 
(
	ClientId INT NOT NULL,
	ClientCode VARCHAR(20) NOT NULL,
	ClientName NVARCHAR(100) NOT NULL,
	IndustrySegment VARCHAR(40) NOT NULL,
	
	CONSTRAINT PK_Clients
		PRIMARY KEY (ClientId),

	CONSTRAINT UQ_Clients_ClientCode
		UNIQUE(ClientCode),

	CONSTRAINT UQ_Clients_ClientName
		UNIQUE(ClientName)
);
GO