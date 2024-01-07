SELECT
    p."PESEL",
    p."FirstName",
    p."LastName",
    c."CellNr",
    b."BlockName",
    p."AdmissionDate",
    StayDuration.StayDurationDays
FROM
    public."Prisoner" p
LEFT JOIN
    public."Prison" pr ON p."IdPrison" = pr."IdPrison"
LEFT JOIN
    public."Cell" c ON p."IdCell" = c."IdCell"
LEFT JOIN
    public."Block" b ON c."IdBlock" = b."IdBlock"
INNER JOIN (
    SELECT "IdPrisoner", SUM("StayDurationDays") AS StayDurationDays
    FROM public."Sentence"
    GROUP BY "IdPrisoner"
    HAVING SUM("StayDurationDays") > 1825
) StayDuration ON p."IdPrisoner" = StayDuration."IdPrisoner"
WHERE
    pr."PenitentiaryName" = 'Więzienie nr: 6'
ORDER BY
    p."PESEL";
