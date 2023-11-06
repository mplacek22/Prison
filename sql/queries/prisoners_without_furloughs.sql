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
    public."Furlough" fur ON p."IdPrisoner" = fur."IdPrisoner"
LEFT JOIN
    public."Cell" c ON p."IdCell" = c."IdCell"
LEFT JOIN
    public."Block" b ON c."IdBlock" = b."IdBlok"
LEFT JOIN
    public."Building" bu ON b."IdBuilding" = bu."IdBuilding"
LEFT JOIN
    public."Prison" pr ON bu."IdPrison" = pr."IdPrison"
WHERE
    fur."IdFurlough" IS NULL
    AND pr."PenitentiaryName" = 'Więzienie nr: 6';