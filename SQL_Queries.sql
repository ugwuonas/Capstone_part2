-- 1.) Retrieve the total confirmed, death, and recovered cases.
SELECT SUM(confirmed) AS TotalConfirmed, SUM(recovered) AS TotalRecoveries, SUM(deaths) AS TotalDeaths FROM covid_19_data;

-- 2.) Retrieve the total confirmed, deaths and recovered cases for the first quarter of each year of observation.
SELECT EXTRACT(YEAR FROM observationdate) AS year,
SUM(confirmed) AS TotalConfirmed_FirstQuarter, SUM(recovered) AS TotalRecoveries_FirstQuarter, SUM(deaths) AS TotalDeaths_FirstQuarter FROM covid_19_data WHERE 
EXTRACT(MONTH FROM observationdate) BETWEEN 1 AND 3 GROUP BY year; 

-- 3.) Retrieve a summary of all the records. This should include the following information for each country:
--  The total number of confirmed cases, The total number of deaths, The total number of recoveries
SELECT Country, SUM(confirmed) AS TotalConfirmed, SUM(recovered) AS TotalRecoveries, SUM(deaths) AS TotalDeaths FROM covid_19_data GROUP BY Country;


-- 4.) Retrieve the percentage increase in the number of death cases from 2019 to 2020.
WITH deaths_2019 AS (
    SELECT SUM(deaths) AS total_deaths_2019
    FROM covid_19_data
    WHERE EXTRACT(YEAR FROM observationdate) = 2019
),
deaths_2020 AS (
    SELECT SUM(deaths) AS total_deaths_2020
    FROM covid_19_data
    WHERE EXTRACT(YEAR FROM observationdate) = 2020
)
SELECT ROUND(((deaths_2020.total_deaths_2020 - deaths_2019.total_deaths_2019) ::DECIMAL / deaths_2019.total_deaths_2019) * 100, 3) AS percentage_increase
FROM deaths_2019, deaths_2020;


-- 5.) Retrieve information for the top 5 countries with the highest confirmed cases.
SELECT Country, SUM(confirmed) AS TotalConfirmed FROM covid_19_data GROUP BY Country ORDER BY TotalConfirmed DESC LIMIT 5; 


--6.) Compute the total number of drop (decrease) or increase in the confirmed cases from month to month in the 2 years of observation.
SELECT
    EXTRACT(MONTH FROM t1.observationdate) AS current_month,
    EXTRACT(YEAR FROM t1.observationdate) AS current_year,
    COUNT(*) AS count
FROM
    covid_19_data t1
JOIN
    covid_19_data t2 ON EXTRACT(MONTH FROM t1.observationdate) = EXTRACT(MONTH FROM t2.observationdate) + 1
                  AND EXTRACT(YEAR FROM t1.observationdate) = EXTRACT(YEAR FROM t2.observationdate)
WHERE
    t1.confirmed < t2.confirmed
GROUP BY
    EXTRACT(MONTH FROM t1.observationdate),
    EXTRACT(YEAR FROM t1.observationdate)
ORDER BY
    current_year, current_month;
