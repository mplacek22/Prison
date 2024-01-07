SELECT
    p."PESEL",
    p."FirstName",
    p."LastName",
    c."CellNr",
    b."BlockName",
    p."AdmissionDate",
    SUM(s."StayDurationDays") AS "StayDurationDays"
FROM
    public."Prisoner" p
INNER JOIN
    public."Sentence" s ON p."IdPrisoner" = s."IdPrisoner"
LEFT JOIN
    public."Prison" pr ON p."IdPrison" = pr."IdPrison"
LEFT JOIN
    public."Cell" c ON p."IdCell" = c."IdCell"
LEFT JOIN
    public."Block" b ON c."IdBlock" = b."IdBlock"
WHERE
    pr."PenitentiaryName" = 'Więzienie nr: 6'
GROUP BY
    p."PESEL", p."FirstName", p."LastName", c."CellNr", b."BlockName", p."AdmissionDate"
HAVING
    DATE_TRUNC('month', p."AdmissionDate" + SUM(s."StayDurationDays") * INTERVAL '1 day') = DATE_TRUNC('month', CURRENT_DATE + INTERVAL '1 month')
ORDER BY
    p."PESEL";
