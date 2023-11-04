-- DONE
SELECT
    AVG(EXTRACT(DAY FROM (CURRENT_DATE - "AdmissionDate")) / 365.0) AS "AverageLengthOfStayInYears"
FROM
    public."Prisoner";
