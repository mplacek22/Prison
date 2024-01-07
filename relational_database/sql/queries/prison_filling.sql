WITH "SumCells" AS (
    SELECT
		pr."IdPrison",
		SUM("CellCapacity") AS "Capacity"
    FROM "Cell"
    INNER JOIN
        "Block" b ON "Cell"."IdBlock" = b."IdBlock"
    INNER JOIN
        "Building" bu ON b."IdBuilding" = bu."IdBuilding"
    INNER JOIN
        "Prison" pr ON bu."IdPrison" = pr."IdPrison"
    GROUP BY
        pr."IdPrison"
)

SELECT
    pr."PenitentiaryName" AS "PrisonName",
    pr."City" AS "City",
    COUNT(p."IdPrisoner")::float / sc."Capacity" AS "Filling"
FROM
    "Prison" pr
INNER JOIN
    "Prisoner" p ON pr."IdPrison" = p."IdPrison"
INNER JOIN
    "SumCells" sc ON pr."IdPrison" = sc."IdPrison"
GROUP BY
    pr."IdPrison", sc."Capacity"
HAVING
    COUNT(p."IdPrisoner")::float / sc."Capacity" <= 0.7
ORDER BY
    "Filling" DESC;