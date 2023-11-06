-- DONE
SELECT
    p."IdPrisoner",
    p."PESEL",
    p."FirstName",
    p."LastName",
    p."AdmissionDate",
    p."IdCell",
    p."Sex"
FROM
    public."Prisoner" p
LEFT JOIN
    public."Sentence" s ON p."IdPrisoner" = s."IdPrisoner"
LEFT JOIN
    public."Prison" pr ON p."IdPrison" = pr."IdPrison"
WHERE
    pr."PenitentiaryName" = 'Więzienie nr: 6'
GROUP BY
    p."IdPrisoner"
HAVING
    SUM(s."StayDurationDays") > 1825 -- 5 years in days
ORDER BY
    p."IdPrisoner";
