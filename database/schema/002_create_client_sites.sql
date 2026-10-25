USE InnoStaff;
GO

CREATE TABLE dbo.ClientSites 
(
	ClientSiteId INT NOT NULL,
	ClientId INT NOT NULL,
	SiteCode VARCHAR(20) NOT NULL,
	SiteName NVARCHAR(100) NOT NULL,
	Region NVARCHAR(60) NOT NULL,

	CONSTRAINT PK_ClientSites
		PRIMARY KEY (ClientSiteId),

	CONSTRAINT UQ_ClientSites_SiteCode
		UNIQUE (SiteCode),

	CONSTRAINT FK_ClientSites_Clients
		FOREIGN KEY (ClientId)
		REFERENCES dbo.Clients (ClientId)

);
GO