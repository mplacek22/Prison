SELECT
    p."PESEL",
    p."FirstName" AS "PrisonerFirstName",
    p."LastName" AS "PrisonerLastName",
    c."CellNr",
    b."BlockName",
    p."AdmissionDate",
    CONCAT(cp."Name", ' ', cp."Surname") AS "ContactPersonFullName",
    p."Height",
    p."BloodGroup",
    p."Sex",
    e."ExaminationDate" AS "ExaminationDate",
    e."ExaminationType",
    e."ExaminationResult" AS "ExaminationResult"
FROM
    public."Prisoner" p
LEFT JOIN
    public."Examination" e ON p."IdPrisoner" = e."IdPrisoner"
LEFT JOIN
    public."Cell" c ON p."IdCell" = c."IdCell"
LEFT JOIN
    public."Block" b ON c."IdBlock" = b."IdBlock"
LEFT JOIN
    public."ContactPerson" cp ON p."IdContactPerson" = cp."IdContactPerson"
WHERE
    p."FirstName" = 'Arkadiusz' AND p."LastName" = 'Glaza'
    AND e."ExaminationType" = 'Masa ciała'
ORDER BY
    e."ExaminationDate" DESC
LIMIT 1;