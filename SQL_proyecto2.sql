USE base_datos_genérica;

-- Número de países
SELECT COUNT(*) AS total_countries
FROM countries;

-- Número de registros de felicidad
SELECT COUNT(*) AS total_happiness
FROM happiness_rating;

-- Número de registros económicos
SELECT COUNT(*) AS total_economic
FROM economic_indicators;

-- Relación entre el PIB per cápita y el nivel de felicidad

SELECT
    h.iso3_code,
    h.year,
    h.happiness_score,
    e.gdp_per_capita
FROM happiness_rating AS h

INNER JOIN economic_indicators AS e
    ON h.iso3_code = e.iso3_code
    AND h.year = e.year

WHERE e.gdp_per_capita IS NOT NULL

ORDER BY e.gdp_per_capita DESC;
