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

-- PREGUNTA 1. Relación entre el PIB per cápita y el nivel de felicidad
-- 1.A ¿Cuánto PIB y cuánta felicidad tiene cada país en cada año?

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

-- 1.B PIB per cápita medio y felicidad media de cada país durante el periodo 2015-2019

SELECT
    h.iso3_code,
    ROUND(AVG(e.gdp_per_capita), 2) AS avg_gdp_per_capita,
    ROUND(AVG(h.happiness_score), 2) AS avg_happiness

FROM happiness_rating AS h

INNER JOIN economic_indicators AS e
    ON h.iso3_code = e.iso3_code
    AND h.year = e.year

WHERE e.gdp_per_capita IS NOT NULL

GROUP BY h.iso3_code

ORDER BY avg_gdp_per_capita DESC;
-- 1.C Calculamos la correlación entre el PIB per cápita
-- y el nivel de felicidad

SELECT
    ROUND(
        (
            COUNT(*) * SUM(e.gdp_per_capita * h.happiness_score)
            - SUM(e.gdp_per_capita) * SUM(h.happiness_score)
        )
        /
        SQRT(
            (
                COUNT(*) * SUM(POWER(e.gdp_per_capita, 2))
                - POWER(SUM(e.gdp_per_capita), 2)
            )
            *
            (
                COUNT(*) * SUM(POWER(h.happiness_score, 2))
                - POWER(SUM(h.happiness_score), 2)
            )
        ),
        3
    ) AS correlation_gdp_happiness

FROM happiness_rating AS h

INNER JOIN economic_indicators AS e
    ON h.iso3_code = e.iso3_code
    AND h.year = e.year

WHERE e.gdp_per_capita IS NOT NULL
    AND h.happiness_score IS NOT NULL;
    
-- CONCLUSIÓN PREGUNTA 1:
-- El coeficiente de correlación de Pearson obtenido es 0.723,
-- lo que muestra una asociación positiva entre el PIB per cápita
-- y el nivel de felicidad.
-- En general, los países con mayor PIB per cápita tienden a presentar
-- puntuaciones de felicidad más altas.
-- Sin embargo, la relación no es perfecta, por lo que la riqueza
-- por sí sola no explica todas las diferencias de felicidad entre países.
-- Además, la correlación muestra una asociación entre ambas variables,
-- pero no implica una relación de causalidad.

-- 2. PREGUNTA 2
-- Agrupamos los países según su nivel de PIB per cápita
-- para comprobar cómo cambia la felicidad media

SELECT
    CASE
        WHEN e.gdp_per_capita < 10000 THEN '1. Menos de 10.000'
        WHEN e.gdp_per_capita < 30000 THEN '2. Entre 10.000 y 30.000'
        WHEN e.gdp_per_capita < 50000 THEN '3. Entre 30.000 y 50.000'
        ELSE '4. Más de 50.000'
    END AS gdp_group,

    COUNT(*) AS observations,

    ROUND(AVG(e.gdp_per_capita), 2) AS avg_gdp_per_capita,

    ROUND(AVG(h.happiness_score), 2) AS avg_happiness

FROM happiness_rating AS h

INNER JOIN economic_indicators AS e
    ON h.iso3_code = e.iso3_code
    AND h.year = e.year

WHERE e.gdp_per_capita IS NOT NULL
    AND h.happiness_score IS NOT NULL

GROUP BY gdp_group

ORDER BY avg_gdp_per_capita;

-- Analizamos la felicidad media por tramos de 10.000 dólares de PIB

SELECT
    FLOOR(e.gdp_per_capita / 10000) * 10000 AS gdp_range,

    COUNT(*) AS observations,

    ROUND(AVG(e.gdp_per_capita), 2) AS avg_gdp_per_capita,

    ROUND(AVG(h.happiness_score), 2) AS avg_happiness

FROM happiness_rating AS h

INNER JOIN economic_indicators AS e
    ON h.iso3_code = e.iso3_code
    AND h.year = e.year

WHERE e.gdp_per_capita IS NOT NULL
    AND h.happiness_score IS NOT NULL

GROUP BY gdp_range

ORDER BY gdp_range;

-- CONCLUSIÓN PREGUNTA 2:
-- La felicidad media aumenta claramente en los niveles bajos de PIB per cápita.
-- Sin embargo, a medida que aumenta la riqueza, los incrementos de felicidad
-- son menores y dejan de seguir un crecimiento constante.
-- Los resultados sugieren una relación de rendimientos decrecientes:
-- a niveles elevados de PIB per cápita, mayores niveles de riqueza
-- no están asociados con aumentos igualmente grandes de felicidad.
-- No obstante, los resultados no permiten establecer un umbral exacto
-- a partir del cual la felicidad se estabilice.

-- 3. 
-- ¿Cómo ha evolucionado la felicidad de los países y regiones entre 2015 y 2019?
-- 3A. Evolución general de la felicidad entre 2015 y 2019
-- Analizamos cómo ha evolucionado la felicidad media entre 2015 y 2019

SELECT
    year,
    COUNT(*) AS observations,
    ROUND(AVG(happiness_score), 2) AS avg_happiness

FROM happiness_rating

GROUP BY year

ORDER BY year;
-- Entre 2015 y 2019, la felicidad media global se mantuvo prácticamente estable,
-- con pequeñas fluctuaciones y un ligero aumento de 5,37 a 5,40.

-- 3B. Evolución por regiones
SELECT
    c.region,
    h.year,
    COUNT(*) AS observations,
    ROUND(AVG(h.happiness_score), 2) AS avg_happiness

FROM happiness_rating AS h

INNER JOIN countries AS c
    ON h.iso3_code = c.iso3_code

GROUP BY
    c.region,
    h.year

ORDER BY
    c.region,
    h.year;

-- 3C. Comparamos la felicidad media de cada región
-- entre el primer año (2015) y el último año (2019)

SELECT
    c.region,

    ROUND(AVG(
        CASE
            WHEN h.year = 2015 THEN h.happiness_score
        END
    ), 2) AS happiness_2015,

    ROUND(AVG(
        CASE
            WHEN h.year = 2019 THEN h.happiness_score
        END
    ), 2) AS happiness_2019,

    ROUND(
        AVG(CASE WHEN h.year = 2019 THEN h.happiness_score END)
        -
        AVG(CASE WHEN h.year = 2015 THEN h.happiness_score END),
        2
    ) AS happiness_change

FROM happiness_rating AS h

INNER JOIN countries AS c
    ON h.iso3_code = c.iso3_code

GROUP BY c.region

ORDER BY happiness_change DESC;

-- 3D. Calculamos el cambio de felicidad de cada país
-- entre 2015 y 2019

SELECT
    country,
    happiness_2015,
    happiness_2019,
    ROUND(happiness_2019 - happiness_2015, 2) AS happiness_change

FROM (
    SELECT
        c.country,

        AVG(
            CASE
                WHEN h.year = 2015 THEN h.happiness_score
            END
        ) AS happiness_2015,

        AVG(
            CASE
                WHEN h.year = 2019 THEN h.happiness_score
            END
        ) AS happiness_2019

    FROM happiness_rating AS h

    INNER JOIN countries AS c
        ON h.iso3_code = c.iso3_code

    GROUP BY c.country

) AS country_changes

WHERE happiness_2015 IS NOT NULL
    AND happiness_2019 IS NOT NULL

ORDER BY happiness_change DESC;

-- CONCLUSIÓN PREGUNTA 3:
-- Entre 2015 y 2019, la felicidad media global se mantuvo
-- prácticamente estable, pasando de 5.37 a 5.40.
-- Sin embargo, esta estabilidad global oculta diferencias
-- importantes entre regiones y países.
-- Europe & Central Asia aumentó aproximadamente +0.19 puntos
-- y Sub-Saharan Africa +0.12 puntos, mientras que otras regiones
-- presentaron pequeños descensos durante el periodo analizado.
-- A nivel de países, las diferencias fueron mucho mayores.
-- Benin presentó el mayor aumento observado (+1.54 puntos),
-- mientras que Venezuela presentó el mayor descenso (-2.10 puntos).
-- Por tanto, aunque la felicidad media mundial apenas cambió
-- entre 2015 y 2019, la evolución fue muy diferente dependiendo
-- de la región y del país analizado.

-- 4. ¿Qué relación existe entre la felicidad y otros indicadores económicos como el desempleo y el gasto sanitario?
-- 4A. Comparamos la felicidad de cada país
-- con su tasa de desempleo en cada año

SELECT
    c.country,
    h.year,
    h.happiness_score,
    e.unemployment_rate

FROM happiness_rating AS h

INNER JOIN economic_indicators AS e
    ON h.iso3_code = e.iso3_code
    AND h.year = e.year

INNER JOIN countries AS c
    ON h.iso3_code = c.iso3_code

WHERE e.unemployment_rate IS NOT NULL

ORDER BY e.unemployment_rate DESC;

-- 4B. Identificamos los países cuya tasa de desempleo
-- está por encima del desempleo medio del conjunto de datos

SELECT
    c.country,
    h.year,
    h.happiness_score,
    e.unemployment_rate

FROM happiness_rating AS h

INNER JOIN economic_indicators AS e
    ON h.iso3_code = e.iso3_code
    AND h.year = e.year

INNER JOIN countries AS c
    ON h.iso3_code = c.iso3_code

WHERE e.unemployment_rate > (
    SELECT AVG(unemployment_rate)
    FROM economic_indicators
    WHERE unemployment_rate IS NOT NULL
)

ORDER BY e.unemployment_rate DESC;

-- 4C. Calculamos la correlación entre el desempleo
-- y el nivel de felicidad

SELECT
    ROUND(
        (
            COUNT(*) * SUM(e.unemployment_rate * h.happiness_score)
            - SUM(e.unemployment_rate) * SUM(h.happiness_score)
        )
        /
        SQRT(
            (
                COUNT(*) * SUM(POWER(e.unemployment_rate, 2))
                - POWER(SUM(e.unemployment_rate), 2)
            )
            *
            (
                COUNT(*) * SUM(POWER(h.happiness_score, 2))
                - POWER(SUM(h.happiness_score), 2)
            )
        ),
        3
    ) AS correlation_unemployment_happiness

FROM happiness_rating AS h

INNER JOIN economic_indicators AS e
    ON h.iso3_code = e.iso3_code
    AND h.year = e.year

WHERE e.unemployment_rate IS NOT NULL
    AND h.happiness_score IS NOT NULL;

-- 4D. Calculamos la correlación entre el gasto sanitario
-- y el nivel de felicidad

SELECT
    ROUND(
        (
            COUNT(*) * SUM(e.health_expenditure * h.happiness_score)
            - SUM(e.health_expenditure) * SUM(h.happiness_score)
        )
        /
        SQRT(
            (
                COUNT(*) * SUM(POWER(e.health_expenditure, 2))
                - POWER(SUM(e.health_expenditure), 2)
            )
            *
            (
                COUNT(*) * SUM(POWER(h.happiness_score, 2))
                - POWER(SUM(h.happiness_score), 2)
            )
        ),
        3
    ) AS correlation_health_happiness

FROM happiness_rating AS h

INNER JOIN economic_indicators AS e
    ON h.iso3_code = e.iso3_code
    AND h.year = e.year

WHERE e.health_expenditure IS NOT NULL
    AND h.happiness_score IS NOT NULL;
    
-- CONCLUSIÓN PREGUNTA 4:
-- La correlación entre la tasa de desempleo y la felicidad es de -0.202,
-- lo que indica una relación negativa débil.
-- En general, mayores tasas de desempleo tienden a estar asociadas
-- con niveles ligeramente más bajos de felicidad, aunque la relación
-- no es fuerte.
-- Por otro lado, la correlación entre el gasto sanitario y la felicidad
-- es de 0.375, lo que indica una relación positiva moderada.
-- Los países con mayor gasto sanitario tienden a presentar niveles
-- de felicidad más altos, aunque existen importantes diferencias
-- entre países.
-- En comparación con el PIB per cápita, cuya correlación con la felicidad
-- fue de 0.723, tanto el desempleo como el gasto sanitario presentan
-- una relación menos fuerte con la felicidad.
-- Estas correlaciones muestran asociaciones entre las variables,
-- pero no implican relaciones de causalidad.


-- 5. ¿Existen países con niveles similares de PIB per cápita pero niveles de felicidad muy diferentes?
-- considerar "PIB similar" como una diferencia máxima del 10% y "felicidad muy diferente" como una diferencia de al menos 1 punto.

-- PREGUNTA 5:
-- ¿Existen países con niveles similares de PIB per cápita
-- pero niveles de felicidad muy diferentes?
-- Consideramos:
-- PIB similar = diferencia máxima del 10%
-- Felicidad muy diferente = diferencia mínima de 1 punto

SELECT
    c1.country AS country_1,
    c2.country AS country_2,
    e1.year,

    ROUND(e1.gdp_per_capita, 2) AS gdp_1,
    ROUND(e2.gdp_per_capita, 2) AS gdp_2,

    ROUND(h1.happiness_score, 2) AS happiness_1,
    ROUND(h2.happiness_score, 2) AS happiness_2,

    ROUND(
        ABS(h1.happiness_score - h2.happiness_score),
        2
    ) AS happiness_difference

FROM economic_indicators AS e1

-- Comparamos cada país con otros países del mismo año
INNER JOIN economic_indicators AS e2
    ON e1.year = e2.year
    AND e1.iso3_code < e2.iso3_code

-- Añadimos la felicidad del primer país
INNER JOIN happiness_rating AS h1
    ON e1.iso3_code = h1.iso3_code
    AND e1.year = h1.year

-- Añadimos la felicidad del segundo país
INNER JOIN happiness_rating AS h2
    ON e2.iso3_code = h2.iso3_code
    AND e2.year = h2.year

-- Obtenemos los nombres de los países
INNER JOIN countries AS c1
    ON e1.iso3_code = c1.iso3_code

INNER JOIN countries AS c2
    ON e2.iso3_code = c2.iso3_code

WHERE
    -- Los dos países deben tener un PIB similar
    ABS(e1.gdp_per_capita - e2.gdp_per_capita)
        <= ((e1.gdp_per_capita + e2.gdp_per_capita) / 2) * 0.10

    -- Pero una diferencia de felicidad de al menos 1 punto
    AND ABS(h1.happiness_score - h2.happiness_score) >= 1

ORDER BY happiness_difference DESC;

-- CONCLUSIÓN PREGUNTA 5:
-- Sí, existen países con niveles muy similares de PIB per cápita
-- que presentan diferencias importantes en sus niveles de felicidad.
-- Al considerar como PIB similar una diferencia máxima del 10%
-- y como diferencia relevante de felicidad al menos 1 punto,
-- encontramos varios pares de países que cumplen ambas condiciones.
-- Un ejemplo especialmente destacable es Finlandia y Hong Kong SAR, China
-- en 2019, cuyos niveles de PIB per cápita son prácticamente idénticos
-- (48,358.18 y 48,359), pero presentan una diferencia de felicidad
-- de al menos 1 punto según el criterio establecido en la consulta.
-- Por tanto, aunque existe una asociación positiva entre PIB per cápita
-- y felicidad, un nivel de riqueza similar no implica necesariamente
-- un nivel de felicidad similar.
-- Esto sugiere que existen otros factores, además del PIB per cápita,
-- asociados con las diferencias de felicidad entre países.