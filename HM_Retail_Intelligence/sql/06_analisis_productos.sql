USE hm_retail_intelligence;

-- =====================================================
-- BLOQUE 3. PRODUCT INTELLIGENCE
-- =====================================================
-- Objetivo: identificar los productos y categorías
-- con mayor volumen de artículos vendidos.
-- Periodo: 23/09/2019 - 22/09/2020.
-- Cada registro representa un artículo vendido.


-- SQL 10. Top 10 de artículos más vendidos
-- Objetivo: identificar los artículos con mayor demanda.

SELECT
    t.article_id,
    a.prod_name,
    a.product_type_name,
    COUNT(*) AS articulos_vendidos

FROM transacciones t

INNER JOIN articulos a
    ON t.article_id = a.article_id

GROUP BY
    t.article_id,
    a.prod_name,
    a.product_type_name

ORDER BY articulos_vendidos DESC

LIMIT 10;
-- RESULTADO SQL 10:
-- El artículo más vendido es 0706016001,
-- Jade HW Skinny Denim TRS, con 30.209 unidades.
-- El mismo nombre de producto aparece con diferentes
-- article_id, por lo que se consideran referencias distintas.
--
-- CONCLUSIÓN DE NEGOCIO:
-- Los pantalones, calcetines y otras prendas básicas
-- tienen presencia destacada en el Top 10.
-- Es necesario analizar todas las categorías para
-- identificar cuáles concentran mayor demanda.
--
-- LIMITACIÓN:
-- El ranking mide unidades vendidas, no ingresos
-- monetarios ni rentabilidad.
-- SQL 11. Categorías con mayor volumen de ventas
-- Objetivo: identificar las categorías de producto
-- que concentran más artículos vendidos.

SELECT
    a.product_group_name,

    COUNT(*) AS articulos_vendidos,

    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM transacciones),
        2
    ) AS porcentaje_total

FROM transacciones t

INNER JOIN articulos a
    ON t.article_id = a.article_id

GROUP BY a.product_group_name

ORDER BY articulos_vendidos DESC;
-- RESULTADO SQL 11:
-- La categoría Garment Upper body lidera las ventas
-- con 5.754.235 artículos (38,62% del total).
--
-- Garment Lower body ocupa el segundo lugar,
-- con 3.252.953 artículos (21,83%).
--
-- Ambas categorías representan conjuntamente
-- el 60,45% de los artículos vendidos.
--
-- CONCLUSIÓN:
-- La demanda está concentrada principalmente
-- en prendas de vestir para la parte superior
-- e inferior del cuerpo.
--
-- APLICACIÓN EN TABLEAU:
-- Gráfico de barras horizontales con las categorías
-- ordenadas de mayor a menor volumen de ventas.
-- SQL 12. Artículos vendidos por línea comercial
-- Objetivo: identificar las líneas comerciales
-- con mayor volumen de ventas.

SELECT
    a.index_group_name AS linea_comercial,
    COUNT(*) AS articulos_vendidos

FROM transacciones t

INNER JOIN articulos a
    ON t.article_id = a.article_id

GROUP BY a.index_group_name

ORDER BY articulos_vendidos DESC;
-- RESULTADO SQL 12:
-- Ladieswear lidera con 9.802.376 artículos vendidos (65,79%).
-- Divided ocupa la segunda posición con 3.298.129 (22,14%).
-- Ambas líneas concentran aproximadamente el 87,93%
-- del volumen total de artículos vendidos.
--
-- CONCLUSIÓN:
-- La demanda está muy concentrada en Ladieswear y Divided.
-- Este resultado puede ayudar a Dirección Comercial
-- a analizar el surtido y la distribución del inventario.
--
-- APLICACIÓN EN TABLEAU:
-- Gráfico de barras con el volumen de artículos
-- vendidos por línea comercial.
-- SQL 13. Preferencias de productos por grupo de edad
-- Objetivo: analizar qué categorías tienen más demanda
-- en cada segmento de edad.

SELECT
    CASE
        WHEN c.age BETWEEN 16 AND 24 THEN '16-24'
        WHEN c.age BETWEEN 25 AND 34 THEN '25-34'
        WHEN c.age BETWEEN 35 AND 44 THEN '35-44'
        WHEN c.age BETWEEN 45 AND 54 THEN '45-54'
        WHEN c.age >= 55 THEN '55+'
        ELSE 'Edad desconocida'
    END AS grupo_edad,

    a.product_group_name AS categoria,

    COUNT(*) AS articulos_vendidos

FROM transacciones t

STRAIGHT_JOIN articulos a
    ON t.article_id = a.article_id

STRAIGHT_JOIN clientes c
    ON t.customer_id = c.customer_id

GROUP BY
    grupo_edad,
    a.product_group_name

ORDER BY
    grupo_edad,
    articulos_vendidos DESC;
-- RESULTADO SQL 13:
-- Consulta ejecutada correctamente: 108 filas.
-- Tiempo de ejecución: 587,875 segundos.
--
-- La categoría Garment Upper body lidera las ventas
-- en todos los grupos de edad.
--
-- El grupo de 25-34 años registra el mayor volumen
-- de artículos vendidos de esta categoría: 2.005.774.
--
-- Garment Lower body ocupa el segundo lugar
-- en todos los segmentos de edad.
--
-- LIMITACIÓN:
-- El volumen absoluto depende del tamaño de cada
-- segmento. Para comparar preferencias relativas,
-- será necesario calcular porcentajes por grupo de edad.
--
-- OPTIMIZACIÓN:
-- Se utilizó STRAIGHT_JOIN para establecer el orden
-- de acceso a las tablas.
-- SQL 14. Tamaño del catálogo y volumen de ventas
-- Objetivo: comparar las referencias disponibles
-- con los artículos vendidos por categoría.

WITH catalogo AS (
    SELECT
        product_group_name AS categoria,
        COUNT(*) AS referencias_catalogo
    FROM articulos
    GROUP BY product_group_name
),

ventas AS (
    SELECT
        a.product_group_name AS categoria,
        COUNT(*) AS articulos_vendidos
    FROM articulos a
    INNER JOIN transacciones t
        ON a.article_id = t.article_id
    GROUP BY a.product_group_name
)

SELECT
    c.categoria,
    c.referencias_catalogo,
    COALESCE(v.articulos_vendidos, 0) AS articulos_vendidos

FROM catalogo c

LEFT JOIN ventas v
    ON c.categoria = v.categoria

ORDER BY articulos_vendidos DESC;
-- RESULTADO SQL 14:
-- Se compararon 19 categorías de productos.
-- Garment Upper body lidera tanto en referencias
-- del catálogo (42.741) como en artículos vendidos
-- (5.754.235).
--
-- Sin embargo, más referencias no implican
-- necesariamente un mayor volumen de ventas.
--
-- Swimwear registra 1.144.451 artículos vendidos
-- con 3.127 referencias, mientras que Accessories
-- registra 756.926 ventas con 11.158 referencias.
--
-- Conclusión: la variedad del catálogo no explica
-- por sí sola las diferencias de demanda.
