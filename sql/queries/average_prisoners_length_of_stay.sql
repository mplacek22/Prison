SELECT
    pr."PenitentiaryName" AS "PrisonName",
    pr."City" AS "CityName",
    AVG(EXTRACT(DAY FROM (CURRENT_DATE - "AdmissionDate")) / 365.0) AS "AverageLengthOfStayInYears"
FROM
    public."Prisoner" p
LEFT JOIN
    public."Cell" c ON p."IdCell" = c."IdCell"
LEFT JOIN
    public."Block" b ON c."IdBlock" = b."IdBlok"
LEFT JOIN
    public."Building" bu ON b."IdBuilding" = bu."IdBuilding"
LEFT JOIN
    public."Prison" pr ON bu."IdPrison" = pr."IdPrison"
GROUP BY
    pr."PenitentiaryName", pr."City";
