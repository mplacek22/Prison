SELECT
    pr."PenitentiaryName" AS "PrisonName",
    COUNT(p."IdPrisoner")::float / SUM(c."CellCapacity") AS "Filling"
FROM
    "Prisoner" p
RIGHT JOIN
    "Cell" c ON p."IdCell" = c."IdCell"
INNER JOIN
    "Prison" pr ON p."IdPrison" = pr."IdPrison"
GROUP BY
    pr."IdPrison"
HAVING
    COUNT(p."IdPrisoner")::float / SUM(c."CellCapacity") <= 0.15
ORDER BY
    "Filling" DESC;