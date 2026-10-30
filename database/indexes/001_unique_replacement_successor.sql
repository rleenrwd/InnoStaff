USE InnoStaff;
GO

CREATE UNIQUE INDEX UX_Placements_ReplacesPlacementId
	ON dbo.Placements (ReplacesPlacementId)
	WHERE ReplacesPlacementId IS NOT NULL;
GO