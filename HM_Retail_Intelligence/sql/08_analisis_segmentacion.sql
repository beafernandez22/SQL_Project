USE hm_retail_intelligence;

CREATE TABLE IF NOT EXISTS ventas_edad_categoria_mensual (
    mes DATE NOT NULL,
    grupo_edad VARCHAR(20) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    articulos_vendidos BIGINT NOT NULL,
    PRIMARY KEY (mes, grupo_edad, categoria)
);

INSERT INTO ventas_edad_categoria_mensual
    (mes, grupo_edad, categoria, articulos_vendidos)

SELECT
    '2019-10-01' AS mes,

    CASE
        WHEN c.age BETWEEN 16 AND 24 THEN '16-24'
        WHEN c.age BETWEEN 25 AND 34 THEN '25-34'
        WHEN c.age BETWEEN 35 AND 44 THEN '35-44'
        WHEN c.age BETWEEN 45 AND 54 THEN '45-54'
        WHEN c.age >= 55 THEN '55+'
        ELSE 'Desconocida'
    END AS grupo_edad,

    a.product_group_name AS categoria,

    COUNT(*) AS articulos_vendidos

FROM transacciones t

JOIN clientes c
    ON t.customer_id = c.customer_id

JOIN articulos a
    ON t.article_id = a.article_id

WHERE t.t_dat >= '2019-10-01'
  AND t.t_dat < '2019-11-01'

GROUP BY grupo_edad, categoria;

SELECT
    mes,
    COUNT(*) AS combinaciones,
    SUM(articulos_vendidos) AS total_articulos
FROM ventas_edad_categoria_mensual
GROUP BY mes
ORDER BY mes;

SELECT DISTINCT mes
FROM ventas_edad_categoria_mensual
ORDER BY mes;

INSERT INTO ventas_edad_categoria_mensual
    (mes, grupo_edad, categoria, articulos_vendidos)

SELECT
    '2019-11-01' AS mes,

    CASE
        WHEN c.age BETWEEN 16 AND 24 THEN '16-24'
        WHEN c.age BETWEEN 25 AND 34 THEN '25-34'
        WHEN c.age BETWEEN 35 AND 44 THEN '35-44'
        WHEN c.age BETWEEN 45 AND 54 THEN '45-54'
        WHEN c.age >= 55 THEN '55+'
        ELSE 'Desconocida'
    END AS grupo_edad,

    a.product_group_name AS categoria,

    COUNT(*) AS articulos_vendidos

FROM transacciones t

JOIN clientes c
    ON t.customer_id = c.customer_id

JOIN articulos a
    ON t.article_id = a.article_id

WHERE t.t_dat >= '2019-11-01'
  AND t.t_dat < '2019-12-01'

GROUP BY grupo_edad, categoria;

SELECT
    mes,
    COUNT(*) AS combinaciones,
    SUM(articulos_vendidos) AS total_articulos
FROM ventas_edad_categoria_mensual
GROUP BY mes
ORDER BY mes;

DELIMITER $$

CREATE PROCEDURE procesar_ventas_edad_categoria(
    IN fecha_inicio DATE,
    IN fecha_fin DATE
)
BEGIN
    DECLARE mes_actual DATE;

    SET mes_actual = fecha_inicio;

    WHILE mes_actual < fecha_fin DO

        IF NOT EXISTS (
            SELECT 1
            FROM ventas_edad_categoria_mensual
            WHERE mes = mes_actual
        ) THEN

            INSERT INTO ventas_edad_categoria_mensual
                (mes, grupo_edad, categoria, articulos_vendidos)

            SELECT
                mes_actual,

                CASE
                    WHEN c.age BETWEEN 16 AND 24 THEN '16-24'
                    WHEN c.age BETWEEN 25 AND 34 THEN '25-34'
                    WHEN c.age BETWEEN 35 AND 44 THEN '35-44'
                    WHEN c.age BETWEEN 45 AND 54 THEN '45-54'
                    WHEN c.age >= 55 THEN '55+'
                    ELSE 'Desconocida'
                END,

                COALESCE(a.product_group_name, 'Unknown'),

                COUNT(*)

            FROM transacciones t

            JOIN clientes c
                ON t.customer_id = c.customer_id

            JOIN articulos a
                ON t.article_id = a.article_id

            WHERE t.t_dat >= mes_actual
              AND t.t_dat < DATE_ADD(mes_actual, INTERVAL 1 MONTH)

            GROUP BY 2, 3;

        END IF;

        SET mes_actual = DATE_ADD(mes_actual, INTERVAL 1 MONTH);

    END WHILE;
END$$

DELIMITER ;

CALL procesar_ventas_edad_categoria(
    '2019-12-01',
    '2020-01-01'
);

SELECT
    mes,
    COUNT(*) AS combinaciones,
    SUM(articulos_vendidos) AS total_articulos
FROM ventas_edad_categoria_mensual
GROUP BY mes
ORDER BY mes;

CALL procesar_ventas_edad_categoria(
    '2020-01-01',
    '2020-03-01'
);
SELECT
    mes,
    COUNT(*) AS combinaciones,
    SUM(articulos_vendidos) AS total_articulos
FROM ventas_edad_categoria_mensual
GROUP BY mes
ORDER BY mes;

CALL procesar_ventas_edad_categoria(
    '2020-03-01',
    '2020-05-01'
);

SELECT
    mes,
    COUNT(*) AS combinaciones,
    SUM(articulos_vendidos) AS total_articulos
FROM ventas_edad_categoria_mensual
GROUP BY mes
ORDER BY mes;

CALL procesar_ventas_edad_categoria(
    '2020-05-01',
    '2020-07-01'
);

SELECT
    mes,
    COUNT(*) AS combinaciones,
    SUM(articulos_vendidos) AS total_articulos
FROM ventas_edad_categoria_mensual
GROUP BY mes
ORDER BY mes;

CALL procesar_ventas_edad_categoria(
    '2020-07-01',
    '2020-09-01'
);

SELECT
    mes,
    COUNT(*) AS combinaciones,
    SUM(articulos_vendidos) AS total_articulos
FROM ventas_edad_categoria_mensual
GROUP BY mes
ORDER BY mes;

CALL procesar_ventas_edad_categoria(
    '2019-09-01',
    '2019-10-01'
);

CALL procesar_ventas_edad_categoria(
    '2020-09-01',
    '2020-10-01'
);

SELECT
    mes,
    COUNT(*) AS combinaciones,
    SUM(articulos_vendidos) AS total_articulos
FROM ventas_edad_categoria_mensual
GROUP BY mes
ORDER BY mes;

SELECT
    mes,
    grupo_edad,
    categoria,
    articulos_vendidos
FROM ventas_edad_categoria_mensual
ORDER BY mes, grupo_edad, articulos_vendidos DESC;

SELECT COUNT(*) AS total_filas
FROM ventas_edad_categoria_mensual;

SELECT
    mes,
    grupo_edad,
    categoria,
    articulos_vendidos
FROM ventas_edad_categoria_mensual
ORDER BY mes, grupo_edad, articulos_vendidos DESC;


SELECT
    COALESCE(c.club_member_status, 'UNKNOWN') AS estado_afiliacion,
    t.customer_id,
    COUNT(*) AS articulos_comprados
FROM transacciones AS t
INNER JOIN clientes AS c
    ON t.customer_id = c.customer_id
GROUP BY
    COALESCE(c.club_member_status, 'UNKNOWN'),
    t.customer_id
ORDER BY articulos_comprados DESC
LIMIT 20;


-- PASO 2: Mediana de artículos por comprador
-- según el estado de afiliación

WITH compras_por_cliente AS (
    SELECT
        COALESCE(c.club_member_status, 'UNKNOWN') AS afiliacion,
        t.customer_id,
        COUNT(*) AS articulos_comprados
    FROM transacciones AS t
    INNER JOIN clientes AS c
        ON t.customer_id = c.customer_id
    GROUP BY
        COALESCE(c.club_member_status, 'UNKNOWN'),
        t.customer_id
),
clientes_ordenados AS (
    SELECT
        afiliacion,
        articulos_comprados,
        ROW_NUMBER() OVER (
            PARTITION BY afiliacion
            ORDER BY articulos_comprados
        ) AS posicion,
        COUNT(*) OVER (
            PARTITION BY afiliacion
        ) AS total_clientes
    FROM compras_por_cliente
)
SELECT
    afiliacion,
    COUNT(*) AS compradores_unicos,
    ROUND(AVG(articulos_comprados), 2) AS media_articulos,
    ROUND(
        AVG(
            CASE
                WHEN posicion IN (
                    FLOOR((total_clientes + 1) / 2),
                    FLOOR((total_clientes + 2) / 2)
                )
                THEN articulos_comprados
            END
        ), 2
    ) AS mediana_articulos,
    MAX(articulos_comprados) AS maximo_articulos
FROM clientes_ordenados
GROUP BY afiliacion
ORDER BY compradores_unicos DESC;


-- PASO 3: Comprobar las columnas disponibles
-- para analizar categorías por afiliación

SHOW COLUMNS FROM articulos;


-- PASO 4: Categorías de producto por afiliación

SELECT
    COALESCE(c.club_member_status, 'UNKNOWN') AS afiliacion,
    a.product_group_name AS categoria,
    COUNT(*) AS articulos_vendidos
FROM transacciones AS t
INNER JOIN clientes AS c
    ON t.customer_id = c.customer_id
INNER JOIN articulos AS a
    ON t.article_id = a.article_id
GROUP BY
    COALESCE(c.club_member_status, 'UNKNOWN'),
    a.product_group_name
ORDER BY
    afiliacion,
    articulos_vendidos DESC;

-- PASO 39: Evolución mensual de las categorías
-- Objetivo: identificar patrones temporales
-- que ayuden a planificar campañas de Marketing.

USE hm_retail_intelligence;

SELECT
    DATE_FORMAT(t.t_dat, '%Y-%m') AS mes,
    COALESCE(a.product_type_name, 'Unknown') AS categoria,
    COUNT(*) AS articulos_vendidos
FROM transacciones AS t
INNER JOIN articulos AS a
    ON t.article_id = a.article_id
GROUP BY
    DATE_FORMAT(t.t_dat, '%Y-%m'),
    COALESCE(a.product_type_name, 'Unknown')
ORDER BY
    mes,
    articulos_vendidos DESC;


SELECT
    DATE_FORMAT(t.t_dat, '%Y-%m') AS mes,
    COALESCE(a.product_group_name, 'Unknown') AS categoria,
    COUNT(*) AS articulos_vendidos
FROM transacciones AS t
INNER JOIN articulos AS a
    ON t.article_id = a.article_id
GROUP BY
    DATE_FORMAT(t.t_dat, '%Y-%m'),
    COALESCE(a.product_group_name, 'Unknown')
ORDER BY
    mes,
    articulos_vendidos DESC;