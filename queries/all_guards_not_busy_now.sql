SELECT
    g."IdGuard",
    g."PESEL",
    g."Name",
    g."Surname",
    r."Rank" AS "RankName",
    p."PenitentiaryName" AS "PrisonName"
FROM
    public."Guard" g
LEFT JOIN
    public."Rank" r ON g."IdRank" = r."IdRank"
LEFT JOIN
    public."Prison" p ON g."IdPrison" = p."IdPrison"
WHERE
    g."IdGuard" NOT IN (
        SELECT gd."IdGuard"
        FROM public."GuardDuty" gd
        JOIN public."Duty" d ON gd."IdDuty" = d."IdDuty"
        WHERE DATE(NOW()) BETWEEN DATE(d."StartDate") AND DATE(d."EndDate")
    );
