SELECT
    e."ExaminationDate" AS "ExaminationDate",
    et."ExaminationType" AS "ExaminationType",
    e."ExaminationResult" AS "ExaminationResult"
FROM
    public."Examination" e
INNER JOIN
    public."ExaminationType" et ON e."IdExaminationType" = et."IdExaminationType"
INNER JOIN
    public."Doctor" d ON e."IdDoctor" = d."IdDoctor"
INNER JOIN
    public."Specialization" s ON d."IdSpecialization" = s."IdSpecialization"
INNER JOIN
    public."Prisoner" p ON e."IdPrisoner" = p."IdPrisoner"
WHERE
    s."Specialization" = 'Kardiolog' AND p."FirstName" = 'Konrad' AND p."LastName" = 'Skutnik'
ORDER BY
    e."ExaminationDate" DESC;