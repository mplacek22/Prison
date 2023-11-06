WITH PrisonStats AS (
  SELECT
    P."PenitentiaryName" AS "PrisonName",
    COUNT(DISTINCT Pz."IdPrisoner") AS "NumberOfPrisoners",
    COUNT(DISTINCT G."IdGuard") AS "NumberOfGuards"
  FROM
    public."Prison" P
    LEFT JOIN public."Prisoner" Pz ON P."IdPrison" = Pz."IdPrison"
    LEFT JOIN public."Guard" G ON P."IdPrison" = G."IdPrison"
  GROUP BY
    P."PenitentiaryName"
)
SELECT
  "PrisonName",
  "NumberOfPrisoners",
  "NumberOfGuards",
  "NumberOfGuards"::numeric / NULLIF("NumberOfPrisoners", 0) AS "NumberOfGuardsPerPrisoner"
FROM PrisonStats
ORDER BY "PrisonName";
