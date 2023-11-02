SELECT
    p."PenitentiaryName" AS "PrisonName",
    COUNT(g."IdGuard") AS "GuardCount",
    COUNT(pri."IdPrisoner") AS "PrisonerCount",
    COUNT(g."IdGuard") / COUNT(pri."IdPrisoner") AS "GuardsPerPrisoner"
FROM
    public."Prison" p
LEFT JOIN
    public."Guard" g ON p."IdPrison" = g."IdPrison"
LEFT JOIN
    public."Prisoner" pri ON g."IdPrison" = pri."IdPrisoner"
GROUP BY
    "PrisonName"
ORDER BY
    "PrisonName";
