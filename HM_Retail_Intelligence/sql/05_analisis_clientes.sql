-- =====================================================
-- H&M RETAIL INTELLIGENCE
-- BLOQUE 2: CUSTOMER INTELLIGENCE
-- =====================================================

USE hm_retail_intelligence;

-- SQL 06. Distribución de compradores por grupos de edad
-- Objetivo: identificar qué grupos de edad tienen
-- mayor número de compradores únicos.

SELECT
    CASE
        WHEN c.age < 25 THEN '16-24'
        WHEN c.age BETWEEN 25 AND 34 THEN '25-34'
        WHEN c.age BETWEEN 35 AND 44 THEN '35-44'
        WHEN c.age BETWEEN 45 AND 54 THEN '45-54'
        WHEN c.age >= 55 THEN '55+'
        ELSE 'Edad desconocida'
    END AS grupo_edad,

    COUNT(DISTINCT t.customer_id) AS compradores_unicos

FROM transacciones t

INNER JOIN clientes c
    ON t.customer_id = c.customer_id

GROUP BY grupo_edad

ORDER BY compradores_unicos DESC;
-- RESULTADO SQL 06:
-- Total de compradores únicos: 994.320.
-- El grupo de 25-34 años concentra más compradores (292.768).
-- Le sigue el grupo de 16-24 años (278.235).
-- Ambos grupos representan aproximadamente el 57,42 %
-- del total de compradores.
-- Existen 7.976 compradores sin edad registrada.
--
-- CONCLUSIÓN DE NEGOCIO:
-- Los compradores de 16 a 34 años constituyen el segmento
-- más numeroso de la base de compradores analizada.
-- Será necesario estudiar su volumen de artículos comprados
-- para determinar su peso real en la actividad comercial.
-- SQL 07. Artículos vendidos por grupo de edad
-- Objetivo: conocer el volumen de artículos comprados
-- por cada segmento de edad.

SELECT
    CASE
        WHEN c.age < 25 THEN '16-24'
        WHEN c.age BETWEEN 25 AND 34 THEN '25-34'
        WHEN c.age BETWEEN 35 AND 44 THEN '35-44'
        WHEN c.age BETWEEN 45 AND 54 THEN '45-54'
        WHEN c.age >= 55 THEN '55+'
        ELSE 'Edad desconocida'
    END AS grupo_edad,

    COUNT(*) AS articulos_vendidos

FROM transacciones t

INNER JOIN clientes c
    ON t.customer_id = c.customer_id

GROUP BY grupo_edad

ORDER BY articulos_vendidos DESC;
-- RESULTADO SQL 07:
-- Total de artículos vendidos: 14.898.423.
-- El grupo de 25-34 años lidera con 5.355.293 artículos.
-- Le sigue el grupo de 16-24 años con 3.411.052 artículos.
-- Los compradores de 16 a 34 años concentran aproximadamente
-- el 58,84 % del volumen total de artículos vendidos.
--
-- CONCLUSIÓN DE NEGOCIO:
-- El segmento de 25-34 años es el que genera mayor volumen
-- de artículos vendidos.
-- Es necesario calcular los artículos por comprador para
-- comparar la intensidad de compra entre segmentos.
-- SQL 08. Artículos por comprador según grupo de edad
-- Objetivo: comparar la intensidad de compra entre segmentos.

SELECT
    CASE
        WHEN c.age < 25 THEN '16-24'
        WHEN c.age BETWEEN 25 AND 34 THEN '25-34'
        WHEN c.age BETWEEN 35 AND 44 THEN '35-44'
        WHEN c.age BETWEEN 45 AND 54 THEN '45-54'
        WHEN c.age >= 55 THEN '55+'
        ELSE 'Edad desconocida'
    END AS grupo_edad,

    COUNT(*) AS articulos_vendidos,

    COUNT(DISTINCT t.customer_id) AS compradores_unicos,

    ROUND(
        COUNT(*) / COUNT(DISTINCT t.customer_id),
        2
    ) AS articulos_por_comprador

FROM transacciones t

INNER JOIN clientes c
    ON t.customer_id = c.customer_id

GROUP BY grupo_edad

ORDER BY articulos_por_comprador DESC;
-- RESULTADO SQL 08:
-- El grupo de 25-34 años presenta el mayor promedio
-- de artículos por comprador: 18,29.
-- Le siguen los grupos de 35-44 años (16,71)
-- y 45-54 años (15,18).
-- El grupo de 16-24 años registra 12,26 artículos
-- por comprador, a pesar de ser el segundo grupo
-- con mayor número de compradores únicos.
--
-- CONCLUSIÓN DE NEGOCIO:
-- El segmento de 25-34 años destaca tanto por volumen
-- de compradores como por intensidad de compra.
-- El grupo de 35-44 años también presenta una
-- intensidad de compra relativamente elevada.
--
-- LIMITACIÓN:
-- La métrica mide artículos por comprador durante
-- el periodo analizado, no pedidos ni visitas.
-- SQL 09. Comportamiento de compra según estado del club
-- Objetivo: comparar compradores, artículos vendidos
-- e intensidad de compra por estado de pertenencia.

SELECT
    c.club_member_status,

    COUNT(DISTINCT t.customer_id) AS compradores_unicos,

    COUNT(*) AS articulos_vendidos,

    ROUND(
        COUNT(*) / COUNT(DISTINCT t.customer_id),
        2
    ) AS articulos_por_comprador

FROM transacciones t

INNER JOIN clientes c
    ON t.customer_id = c.customer_id

GROUP BY c.club_member_status

ORDER BY articulos_vendidos DESC;
-- RESULTADO SQL 09:
-- ACTIVE: 951.428 compradores y 14.650.836 artículos.
-- PRE-CREATE: 39.875 compradores y 218.687 artículos.
-- UNKNOWN: 2.755 compradores y 26.533 artículos.
-- LEFT CLUB: 262 compradores y 2.367 artículos.
--
-- El grupo ACTIVE representa aproximadamente el 95,69 %
-- de los compradores y el 98,34 % de los artículos vendidos.
--
-- CONCLUSIÓN DE NEGOCIO:
-- Los compradores con estado ACTIVE concentran la mayor
-- parte de la actividad comercial y presentan un promedio
-- de 15,40 artículos por comprador.
--
-- LIMITACIÓN:
-- No podemos establecer una relación causal entre
-- pertenencia al club y comportamiento de compra.
-- Los estados corresponden a la información disponible
-- en el dataset y no a un historial de cambios.

-- ANÁLISIS ADICIONAL: ACTIVIDAD SEGÚN ESTADO DE AFILIACIÓN
-- Dashboard 2: Oportunidades de clientes
SELECT
    COALESCE(c.club_member_status, 'UNKNOWN') AS estado_afiliacion,
    COUNT(DISTINCT t.customer_id) AS compradores_unicos,
    COUNT(*) AS articulos_vendidos,
    ROUND(
        COUNT(*) / COUNT(DISTINCT t.customer_id),
        2
    ) AS articulos_por_comprador
FROM transacciones AS t
JOIN clientes AS c
    ON t.customer_id = c.customer_id
GROUP BY
    COALESCE(c.club_member_status, 'UNKNOWN')
ORDER BY articulos_vendidos DESC;