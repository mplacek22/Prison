SELECT
    g."IdGuard",
    g."PESEL",
    g."Name",
    g."Surname",
    g."IdRank",
    g."IdPrison",

    DATE_TRUNC('month', d."StartDate") AS Month,
    SUM(EXTRACT(EPOCH FROM (d."EndDate" - d."StartDate")) / 3600) AS WorkHours
FROM
    public."Guard" g
JOIN
    public."GuardDuty" gd ON g."IdGuard" = gd."IdGuard"
JOIN
    public."Duty" d ON gd."IdDuty" = d."IdDuty"
JOIN
    public."Prison" p ON g."IdPrison" = p."IdPrison"
WHERE
    DATE_TRUNC('month', d."StartDate") = DATE_TRUNC('month', '2023-02-01'::date) -- Change the date to the selected month
    AND p."PenitentiaryName" = 'Więzienie nr: 6'  -- Rename to the prison name of your choice
GROUP BY
    g."IdGuard", Month
ORDER BY
    WorkHours DESC
LIMIT 3;