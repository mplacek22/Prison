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
    p."Sex"
FROM
    public."Prisoner" p
LEFT JOIN
    public."Sentence" s ON p."IdPrisoner" = s."IdPrisoner"
LEFT JOIN
    public."Cell" c ON p."IdCell" = c."IdCell"
LEFT JOIN
    public."Block" b ON c."IdBlock" = b."IdBlok"
LEFT JOIN
    public."Building" bu ON b."IdBuilding" = bu."IdBuilding"
LEFT JOIN
    public."Prison" pr ON bu."IdPrison" = pr."IdPrison"
WHERE
    s."StayDurationDays" > 1825 -- 5 years in days
    AND pr."PenitentiaryName" = 'Więzienie nr: 6';
