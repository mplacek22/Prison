-- DONE
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
WHERE
    DATE_TRUNC('month', d."StartDate") = DATE_TRUNC('month', '2023-02-01'::date) -- Replace '2023-02-01' with your desired month
GROUP BY
    g."IdGuard", Month
ORDER BY
    WorkHours DESC
LIMIT 3;

--
-- SELECT
--     g."IdGuard",
--     g."PESEL",
--     g."Name",
--     g."Surname",
--     g."IdRank",
--     g."IdPrison",
--
--     DATE_TRUNC('month', d."StartDate") AS Month,
--     SUM(EXTRACT(EPOCH FROM (d."EndDate" - d."StartDate")) / 3600) AS WorkHours
-- FROM
--     public."Guard" g
-- JOIN
--     public."GuardDuty" gd ON g."IdGuard" = gd."IdGuard"
-- JOIN
--     public."Duty" d ON gd."IdDuty" = d."IdDuty"
-- JOIN
--     public."Prison" p ON g."IdPrison" = p."IdPrison"
-- WHERE
--     DATE_TRUNC('month', d."StartDate") = DATE_TRUNC('month', '2023-02-01'::date) -- Zmień datę na wybrany miesiąc
--     AND p."PenitentiaryName" = :PrisonName  -- Tu wprowadź nazwę więzienia
-- GROUP BY
--     g."IdGuard", Month
-- ORDER BY
--     WorkHours DESC
-- LIMIT 3;
