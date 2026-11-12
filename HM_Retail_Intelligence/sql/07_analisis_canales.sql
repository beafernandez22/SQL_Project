USE hm_retail_intelligence;

-- SQL 15. Distribución de artículos vendidos por canal
-- Objetivo: analizar el volumen y porcentaje de
-- artículos vendidos en cada canal de venta.

SELECT
    sales_channel_id AS canal_venta,

    COUNT(*) AS articulos_vendidos,

    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM transacciones),
        2
    ) AS porcentaje_total

FROM transacciones

GROUP BY sales_channel_id

ORDER BY articulos_vendidos DESC;
-- RESULTADO SQL 15:
-- Canal 2: 10.704.016 artículos vendidos (71,85%).
-- Canal 1: 4.194.407 artículos vendidos (28,15%).
--
-- El canal 2 concentra la mayor parte del volumen
-- de artículos vendidos durante el periodo analizado.
--
-- Los códigos 1 y 2 se mantienen sin asignar
-- etiquetas de canal físico u online.
-- SQL 16. Evolución mensual de artículos vendidos por canal
-- Objetivo: analizar cómo cambia la actividad
-- de cada canal durante el periodo estudiado.

SELECT
    DATE_FORMAT(t_dat, '%Y-%m') AS mes,

    sales_channel_id AS canal_venta,

    COUNT(*) AS articulos_vendidos

FROM transacciones

GROUP BY
    DATE_FORMAT(t_dat, '%Y-%m'),
    sales_channel_id

ORDER BY
    mes,
    canal_venta;
-- RESULTADO SQL 16:
-- Se analiza la evolución mensual de artículos
-- vendidos en los canales 1 y 2.
--
-- El canal 2 registra un volumen superior
-- al canal 1 durante todo el periodo.
--
-- En marzo de 2020, el canal 1 registra
-- 154.087 artículos vendidos.
--
-- En abril de 2020 no aparecen registros
-- correspondientes al canal 1.
-- El canal 2 alcanza 1.340.882 artículos.
--
-- A partir de mayo de 2020 vuelven a aparecer
-- registros del canal 1.
--
-- Este cambio podría estar relacionado con
-- circunstancias externas, pero el dataset
-- no permite confirmar sus causas.
--
-- Los meses de septiembre son parciales,
-- por lo que deben tratarse con precaución.
-- SQL 17. Categorías de productos por canal
-- Versión optimizada: agregación previa de transacciones.

SELECT
    t.sales_channel_id AS canal_venta,
    a.product_group_name AS categoria,
    SUM(t.total_articulos) AS articulos_vendidos

FROM (
    SELECT
        sales_channel_id,
        article_id,
        COUNT(*) AS total_articulos
    FROM transacciones
    GROUP BY
        sales_channel_id,
        article_id
) AS t

INNER JOIN articulos a
    ON t.article_id = a.article_id

GROUP BY
    t.sales_channel_id,
    a.product_group_name

ORDER BY
    canal_venta,
    articulos_vendidos DESC;
-- RESULTADO SQL 17:
-- Se analizaron 36 combinaciones de canal y categoría.
--
-- Garment Upper body es la categoría más vendida
-- en ambos canales:
-- Canal 1: 1.800.618 artículos.
-- Canal 2: 3.953.617 artículos.
--
-- El canal 2 concentra un volumen superior
-- en la mayoría de las categorías.
--
-- Sin embargo, Accessories y Socks & Tights
-- registran más artículos vendidos en el canal 1.
--
-- Se observan diferencias en la distribución
-- de categorías entre los canales.
--
-- Para Tableau será importante comparar
-- también porcentajes dentro de cada canal.
--
-- La consulta se optimizó agrupando primero
-- las transacciones por artículo y canal.
-- SQL 18. Artículos vendidos por grupo de edad y canal
-- Objetivo: comparar la distribución de artículos
-- vendidos según la edad de los compradores.

SELECT
    CASE
        WHEN c.age BETWEEN 16 AND 24 THEN '16-24'
        WHEN c.age BETWEEN 25 AND 34 THEN '25-34'
        WHEN c.age BETWEEN 35 AND 44 THEN '35-44'
        WHEN c.age BETWEEN 45 AND 54 THEN '45-54'
        WHEN c.age >= 55 THEN '55+'
        ELSE 'Edad desconocida'
    END AS grupo_edad,

    t.sales_channel_id AS canal_venta,

    SUM(t.total_articulos) AS articulos_vendidos

FROM (
    SELECT
        customer_id,
        sales_channel_id,
        COUNT(*) AS total_articulos
    FROM transacciones
    GROUP BY
        customer_id,
        sales_channel_id
) AS t

INNER JOIN clientes c
    ON t.customer_id = c.customer_id

GROUP BY
    grupo_edad,
    t.sales_channel_id

ORDER BY
    grupo_edad,
    canal_venta;

-- SQL 18. Artículos vendidos por edad y canal de venta

SELECT
    c.grupo_edad,
    t.sales_channel_id AS canal_venta,
    COUNT(*) AS articulos_vendidos

FROM transacciones t

INNER JOIN clientes_grupos_edad c
    ON t.customer_id = c.customer_id

GROUP BY
    c.grupo_edad,
    t.sales_channel_id

ORDER BY
    c.grupo_edad,
    canal_venta;
-- RESULTADOS SQL 18:
-- El canal 2 registra más artículos vendidos que el canal 1
-- en todos los grupos de edad.
--
-- El grupo de 25-34 años concentra el mayor volumen de ventas
-- en ambos canales.
--
-- Para mejorar el rendimiento se utilizó una tabla temporal
-- con los clientes clasificados por grupos de edad.
-- SQL 19. Distribución porcentual de ventas por edad y canal

WITH ventas_edad_canal AS (
    SELECT
        c.grupo_edad,
        t.sales_channel_id AS canal_venta,
        COUNT(*) AS articulos_vendidos

    FROM transacciones t

    INNER JOIN clientes_grupos_edad c
        ON t.customer_id = c.customer_id

    GROUP BY
        c.grupo_edad,
        t.sales_channel_id
)

SELECT
    grupo_edad,
    canal_venta,
    articulos_vendidos,

    ROUND(
        100.0 * articulos_vendidos /
        SUM(articulos_vendidos) OVER (
            PARTITION BY grupo_edad
        ),
        2
    ) AS porcentaje_grupo_edad

FROM ventas_edad_canal

ORDER BY
    grupo_edad,
    canal_venta;
-- RESULTADOS SQL 19:
-- El canal 2 predomina en todos los grupos de edad.
--
-- El grupo de 25-34 años presenta la mayor proporción
-- de artículos vendidos por el canal 2 (76.26%).
--
-- El grupo de 45-54 años presenta la mayor proporción
-- del canal 1 entre las edades conocidas (31.73%).
--
-- Los porcentajes se calculan sobre el total de
-- artículos vendidos dentro de cada grupo de edad.
