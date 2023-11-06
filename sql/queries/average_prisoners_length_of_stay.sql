SELECT
    pr."PenitentiaryName" AS "PrisonName",
    pr."City" AS "CityName",
    AVG(EXTRACT(DAY FROM (CURRENT_DATE - "AdmissionDate")) / 365.0) AS "AverageLengthOfStayInYears"
FROM
    public."Prisoner" p
LEFT JOIN
    public."Prison" pr ON p."IdPrison" = pr."IdPrison"
GROUP BY
    pr."PenitentiaryName", pr."City";
