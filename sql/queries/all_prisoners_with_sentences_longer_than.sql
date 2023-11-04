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
WHERE
    s."StayDurationDays" > 1825; -- 5 years in days
