SELECT
  P."PenitentiaryName" AS "PrisonName",
  COUNT(Pz."IdPrisoner") AS "NumberOfPrisoners"
FROM
  public."Prison" P
  LEFT JOIN public."Prisoner" Pz ON P."IdPrison" = Pz."IdPrison"
GROUP BY
  P."PenitentiaryName"
ORDER BY
  P."PenitentiaryName";

