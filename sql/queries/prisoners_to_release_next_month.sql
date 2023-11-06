-- DONE
SELECT
   p."IdPrisoner",
    p."PESEL",
    p."FirstName",
    p."LastName",
    p."AdmissionDate",
    p."IdCell",
    p."IdContactPerson",
    p."Height",
    p."BloodGroup",
    p."Sex",
    SUM(s."StayDurationDays") AS "StayDurationDays"
FROM
    public."Prisoner" p
INNER JOIN
    public."Sentence" s ON p."IdPrisoner" = s."IdPrisoner"
LEFT JOIN
    public."Prison" pr ON p."IdPrison" = pr."IdPrison"
WHERE
    pr."PenitentiaryName" = 'Więzienie nr: 6'
GROUP BY
    p."IdPrisoner"
HAVING
    DATE_TRUNC('month', p."AdmissionDate" + SUM(s."StayDurationDays") * INTERVAL '1 day')
    = DATE_TRUNC('month', CURRENT_DATE + INTERVAL '1 month')
ORDER BY
    p."IdPrisoner";
