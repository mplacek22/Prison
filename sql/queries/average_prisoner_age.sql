SELECT
    pr."PenitentiaryName" AS "PrisonName",
    AVG(
        EXTRACT(YEAR FROM CURRENT_DATE)
        - CASE
            WHEN substring(p."PESEL", 3, 2)::integer > 20 THEN 2000 + substring(p."PESEL", 1, 2)::integer
            ELSE 1900 + substring(p."PESEL", 1, 2)::integer
        END
    )
FROM
    public."Prisoner" p
INNER JOIN
    public."Cell" c ON p."IdCell" = c."IdCell"
INNER JOIN
    public."Block" b ON c."IdBlock" = b."IdBlock"
INNER JOIN
    public."Building" bu ON b."IdBuilding" = bu."IdBuilding"
INNER JOIN
    public."Prison" pr ON bu."IdPrison" = pr."IdPrison"
GROUP BY
    pr."IdPrison";
ORDER BY
    p."PenitentiaryName";
