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
WHERE
    fur."IdFurlough" IS NULL;
