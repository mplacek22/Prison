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
    s."StayDurationDays" AS "StayDurationDays"
FROM
    public."Prisoner" p
JOIN
    public."Sentence" s ON p."IdPrisoner" = s."IdPrisoner"
LEFT JOIN
    public."Cell" c ON p."IdCell" = c."IdCell"
LEFT JOIN
    public."Block" b ON c."IdBlock" = b."IdBlock"
LEFT JOIN
    public."Building" bu ON b."IdBuilding" = bu."IdBuilding"
LEFT JOIN
    public."Prison" pr ON bu."IdPrison" = pr."IdPrison"
WHERE
    DATE_TRUNC('month', p."AdmissionDate" + s."StayDurationDays" * INTERVAL '1 day') = DATE_TRUNC('month', CURRENT_DATE + INTERVAL '1 month')
    AND pr."PenitentiaryName" = 'Więzienie nr: 6';
