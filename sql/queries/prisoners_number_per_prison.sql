SELECT
    p."PenitentiaryName" AS "PrisonName",
    COUNT(pr."IdPrisoner") AS "NumberOfPrisoners"
FROM
    public."Prison" p
LEFT JOIN
    public."Building" bu ON p."IdPrison" = bu."IdPrison"
LEFT JOIN
    public."Block" b ON bu."IdBuilding" = b."IdBuilding"
LEFT JOIN
    public."Cell" c ON b."IdBlock" = c."IdBlock"
LEFT JOIN
    public."Prisoner" pr ON c."IdCell" = pr."IdCell"
GROUP BY
    p."PenitentiaryName"
ORDER BY
    p."PenitentiaryName";
