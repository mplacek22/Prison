-- DONE
SELECT
    g."IdGuard",
    g."Name",
    g."Surname",
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
LIMIT 1;
