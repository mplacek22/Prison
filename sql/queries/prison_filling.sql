SELECT
    pr."PenitentiaryName" AS "PrisonName",
    COUNT(p."IdPrisoner") AS "NumberOfPrisoners",
    SUM(c."CellCapacity") AS "Capacity",
    COUNT(p."IdPrisoner")::float / SUM(c."CellCapacity") AS "Filling"
FROM
    "Prisoner" p
INNER JOIN
    "Cell" p ON p."IdCell" = c."IdCell"
INNER JOIN
    "Block" b ON c."IdBlock" = b."IdBlock"
INNER JOIN
    "Building" bu ON b."IdBuilding" = bu."IdBuilding"
INNER JOIN
    "Prison" pr ON bu."IdPrison" = pr."IdPrison"

GROUP BY
    pr."IdPrison"
HAVING
    COUNT(p."IdPrisoner")::float / SUM(c."CellCapacity") >= 0.15
ORDER BY
    pr."PenitentiaryName";