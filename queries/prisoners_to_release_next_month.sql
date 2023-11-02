-- DONE
SELECT
    p."IdPrisoner",
    p."PESEL",
    p."FirstName",
    p."LastName",
    p."AdmissionDate",
    s."StayDurationDays" AS "StayDurationDays"
FROM
    public."Prisoner" p
JOIN
    public."Sentence" s ON p."IdPrisoner" = s."IdPrisoner"
WHERE
    DATE_TRUNC('month', p."AdmissionDate" + s."StayDurationDays" * INTERVAL '1 day') = DATE_TRUNC('month', CURRENT_DATE + INTERVAL '1 month');
