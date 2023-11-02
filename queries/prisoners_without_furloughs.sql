-- DONE
SELECT
    pr."IdPrisoner",
    pr."FirstName",
    pr."LastName"
FROM
    public."Prisoner" pr
LEFT JOIN
    public."Furlough" fur ON pr."IdPrisoner" = fur."IdPrisoner"
WHERE
    fur."IdFurlough" IS NULL;
