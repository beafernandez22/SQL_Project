Felicidad y economía mundial: análisis de factores económicos y sociales

Objetivo del proyecto:
Analizar la relación entre el nivel de felicidad de los países y distintos factores económicos y sociales durante el periodo 2015–2019. El objetivo principal es estudiar si mayores niveles de riqueza están asociados con mayores niveles de felicidad y analizar cómo otros indicadores, como el desempleo y el gasto sanitario, pueden relacionarse con el bienestar de los países.

Contexto del negocio:
Este proyecto plantea un escenario de análisis socioeconómico internacional en el que se busca comprender qué factores están relacionados con mayores niveles de bienestar entre países.

El análisis puede servir como apoyo para identificar patrones entre felicidad,riqueza, empleo y gasto sanitario, así como diferencias entre regiones y niveles de ingresos.

Dataset: El proyecto combina dos fuentes de datos diferentes:

1. World Happiness Report

Datos correspondientes al periodo 2015–2019.

Principales variables:

- `country`: país
- `year`: año
- `happiness_rank`: posición del país en el ranking de felicidad
- `happiness_score`: puntuación de felicidad
- `gdp_score`: componente económico incluido en el World Happiness Report
- `social_support`: apoyo social
- `life_expectancy`: esperanza de vida saludable
- `freedom`: libertad para tomar decisiones
- `generosity`: generosidad
- `corruption`: percepción de corrupción


2. World Bank API

Los datos económicos se obtienen mediante la API del Banco Mundial.

Principales variables:

- `iso3_code`: código internacional del país
- `region`: región
- `income_level`: nivel de ingresos
- `gdp_per_capita`: PIB per cápita
- `unemployment_rate`: tasa de desempleo
- `health_expenditure`: gasto sanitario como porcentaje del PIB


Estructura de la base de datos: La base de datos se organiza en tres tablas relacionadas:

- `countries`
- `happiness_scores`
- `economic_indicators`

Las tablas se relacionan mediante `iso3_code`, utilizado como identificador común de los países.

Calidad de los datos:

Los archivos del World Happiness Report presentan diferencias en los nombres de las columnas entre los distintos años, por lo que fue necesario homogeneizar su estructura antes de combinarlos.

También se normalizaron los nombres de los países utilizando los códigos ISO3 del Banco Mundial para poder integrar ambas fuentes.

Los valores ausentes en los indicadores económicos se mantienen como valores nulos, ya que la ausencia de información no implica que el indicador tenga valor cero.


Preguntas clave:

1. ¿Qué relación existe entre el PIB per cápita y el nivel de felicidad de los países?

2. ¿Aumenta siempre la felicidad a medida que aumenta la riqueza o parece estabilizarse a partir de determinados niveles de PIB per cápita?

3. ¿Cómo ha evolucionado la felicidad de los países y regiones entre 2015 y 2019?

4. ¿Qué relación existe entre la felicidad y otros indicadores económicos como el desempleo y el gasto sanitario?

5. ¿Existen países con niveles similares de PIB per cápita pero niveles de felicidad muy diferentes?


Proceso de análisis:

1. Adquisición de datos

- Descarga de los archivos CSV del World Happiness Report.
- Obtención de indicadores económicos mediante la API del Banco Mundial.
- Almacenamiento local de los datos obtenidos mediante API.

2. Limpieza y transformación

- Exploración inicial de los datasets.
- Homogeneización de columnas entre los diferentes años.
- Tratamiento de valores nulos.
- Normalización de países mediante códigos ISO3.
- Eliminación de agregados regionales del Banco Mundial.
- Integración de las diferentes fuentes mediante país y año.

3. Diseño de la base de datos

Se diseñó un modelo relacional compuesto por tres tablas:

- `countries`
- `happiness_scores`
- `economic_indicators`

4. Análisis SQL

POR AQUI VAMOSSSS


Resultados / Insights → Los hallazgos más importantes, claros y accionables.
Recomendaciones de negocio → Tu interpretación profesional:qué decisión tomar, qué experimentos lanzar, qué optimizar, qué priorizar.
Limitaciones:
- Algunos indicadores presentan valores ausentes para determinados países y años.
- El periodo analizado está limitado a 2015–2019.
- Las relaciones observadas entre variables representan asociaciones y no permiten establecer causalidad.
Próximos pasos → Qué extenderías si tuvieras más datos o más tiempo.
Cómo replicar el proyecto → Enlace al notebook, queries SQL o dashboard.
