-- DONE
SELECT
    pr."IdPrisoner",
    pr."FirstName",
    pr."LastName",
	pr."AdmissionDate"
FROM
    public."Prisoner" pr
LEFT JOIN
    public."Sentence" s ON pr."IdPrisoner" = s."IdPrisoner"
WHERE
    s."StayDurationDays" > 1825; -- 5 years in days
