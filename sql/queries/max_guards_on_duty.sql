SELECT
    "City",
    "Street",
    "BuildingNumber",
    "BlockName",
    MAX("NumberOfGuards") AS "MaxNumberOfGuardsOnDuty"
FROM (
    SELECT
        bu."City",
        bu."Street",
        bu."BuildingNr" AS "BuildingNumber",
        b."BlockName",
        COUNT(gd."IdGuard") AS "NumberOfGuards"
    FROM
        public."GuardDuty" gd
    INNER JOIN
        public."Duty" d ON gd."IdDuty" = d."IdDuty"
    RIGHT JOIN
        public."Block" b ON d."IdBlock" = b."IdBlock"
    INNER JOIN
        public."Building" bu ON b."IdBuilding" = bu."IdBuilding"
    INNER JOIN
        public."Prison" pr ON bu."IdPrison" = pr."IdPrison"
    WHERE
        pr."PenitentiaryName" = 'Więzienie nr: 9'
    GROUP BY
        bu."City", bu."Street", bu."BuildingNr", b."BlockName", d."IdDuty"
)
GROUP BY
    "City", "Street", "BuildingNumber", "BlockName"
ORDER BY
    "MaxNumberOfGuardsOnDuty" DESC;
