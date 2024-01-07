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
    public."Prison" pr ON p."IdPrison" = pr."IdPrison"
GROUP BY
    pr."IdPrison"
ORDER BY
    pr."PenitentiaryName";
