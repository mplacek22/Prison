SELECT
    p."PESEL",
    p."FirstName",
    p."LastName",
    c."CellNr",
    b."BlockName",
	p."AdmissionDate"

FROM
    public."Prisoner" p
LEFT JOIN
    public."Furlough" fur ON p."IdPrisoner" = fur."IdPrisoner"
LEFT JOIN
    public."Prison" pr ON p."IdPrison" = pr."IdPrison"
LEFT JOIN
    public."Cell" c ON p."IdCell" = c."IdCell"
LEFT JOIN
    public."Block" b ON c."IdBlock" = b."IdBlock"
WHERE
    fur."IdFurlough" IS NULL
    AND pr."PenitentiaryName" = 'Więzienie nr: 6';
