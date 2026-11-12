
-- =====================================================
-- H&M RETAIL INTELLIGENCE
-- VISTA 1: EXECUTIVE OVERVIEW
-- =====================================================

-- Público objetivo: Dirección Comercial de H&M
-- Periodo: 23/09/2019 - 22/09/2020
--
-- Pregunta de negocio:
-- ¿Cómo evoluciona la actividad comercial de H&M?
--
-- Indicadores:
-- 1. Total de artículos vendidos
-- 2. Compradores únicos
-- 3. Evolución mensual
-- 4. Meses de mayor y menor actividad
--
-- Cada registro representa un artículo vendido.
-- El precio está normalizado y no representa euros.

USE hm_retail_intelligence;

-- SQL 01. Validación del periodo y volumen de datos

SELECT
    MIN(t_dat) AS primera_fecha,
    MAX(t_dat) AS ultima_fecha,
    COUNT(*) AS total_articulos_vendidos
FROM transacciones;
-- RESULTADO SQL 01:
-- Periodo analizado: 23/09/2019 - 22/09/2020.
-- Total de artículos vendidos: 14.898.423.
-- Se confirma que los datos importados corresponden
-- al periodo de 12 meses seleccionado.
-- SQL 02. Número de compradores únicos
-- Objetivo: conocer cuántos clientes diferentes
-- realizaron compras durante el periodo analizado.

SELECT
    COUNT(DISTINCT customer_id) AS compradores_unicos
FROM transacciones;
-- RESULTADO SQL 02:
-- Compradores únicos: 994.320.
-- Durante el periodo analizado, 994.320 clientes
-- diferentes realizaron al menos una compra.
-- Se utiliza COUNT(DISTINCT customer_id) para evitar
-- contar varias veces a un mismo cliente.
-- SQL 03. Evolución mensual de artículos vendidos
-- Objetivo: analizar la actividad comercial mes a mes.

SELECT
    DATE_FORMAT(t_dat, '%Y-%m') AS mes,
    COUNT(*) AS articulos_vendidos
FROM transacciones
GROUP BY DATE_FORMAT(t_dat, '%Y-%m')
ORDER BY mes;
-- RESULTADO SQL 03:
-- Se analizó la evolución mensual de artículos vendidos.
--
-- Mes de mayor actividad: junio de 2020
-- Artículos vendidos: 1.764.507.
--
-- Mes completo de menor actividad: febrero de 2020
-- Artículos vendidos: 1.001.859.
--
-- Se observa un aumento de actividad entre febrero y junio.
-- Después de junio, el volumen mensual disminuye.
--
-- IMPORTANTE:
-- Septiembre de 2019 y septiembre de 2020 son meses
-- parciales y no deben compararse directamente
-- con meses completos.
-- Clientes únicos por mes
-- Objetivo: analizar la evolución mensual
-- del número de compradores diferentes.

SELECT
    DATE_FORMAT(t_dat, '%Y-%m') AS mes,
    COUNT(DISTINCT customer_id) AS clientes_unicos
FROM transacciones
GROUP BY DATE_FORMAT(t_dat, '%Y-%m')
ORDER BY mes;
-- KPI: Resumen general de ventas
-- Periodo: 23/09/2019 - 22/09/2020

SELECT
    COUNT(*) AS articulos_vendidos,
    COUNT(DISTINCT customer_id) AS compradores_unicos,
    ROUND(SUM(price), 2) AS precio_normalizado_total
FROM transacciones;
-- SQL 04. Meses de mayor y menor actividad
-- Se excluyen los meses parciales de septiembre.

WITH ventas_mensuales AS (
    SELECT
        DATE_FORMAT(t_dat, '%Y-%m') AS mes,
        COUNT(*) AS articulos_vendidos
    FROM transacciones
    WHERE t_dat >= '2019-10-01'
      AND t_dat < '2020-09-01'
    GROUP BY DATE_FORMAT(t_dat, '%Y-%m')
)

SELECT
    mes,
    articulos_vendidos,
    CASE
        WHEN articulos_vendidos = (
            SELECT MAX(articulos_vendidos)
            FROM ventas_mensuales
        ) THEN 'Mayor actividad'

        WHEN articulos_vendidos = (
            SELECT MIN(articulos_vendidos)
            FROM ventas_mensuales
        ) THEN 'Menor actividad'
    END AS clasificacion

FROM ventas_mensuales
WHERE articulos_vendidos = (
    SELECT MAX(articulos_vendidos)
    FROM ventas_mensuales
)
OR articulos_vendidos = (
    SELECT MIN(articulos_vendidos)
    FROM ventas_mensuales
);
-- RESULTADO SQL 04:
-- Mes de mayor actividad: junio de 2020.
-- Artículos vendidos: 1.764.507.
--
-- Mes de menor actividad: febrero de 2020.
-- Artículos vendidos: 1.001.859.
--
-- Se han excluido septiembre de 2019 y septiembre de 2020
-- porque son meses parciales.
--
-- La consulta utiliza una CTE, MAX, MIN y CASE WHEN.
-- SQL 05. Valor total de los precios normalizados
-- Objetivo: calcular el valor acumulado de los artículos vendidos.

SELECT
    ROUND(SUM(price), 2) AS valor_total_normalizado,
    ROUND(AVG(price), 4) AS precio_medio_normalizado
FROM transacciones;
-- RESULTADO SQL 05:
-- Valor total de los precios normalizados: 420.290,90.
-- Precio medio normalizado por artículo: 0,0282.
--
-- Los valores proceden de la variable price del dataset.
-- IMPORTANTE: los precios están normalizados.
-- No representan euros ni facturación real de H&M.