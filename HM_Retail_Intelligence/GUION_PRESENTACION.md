# Guion de la presentación · H&M Retail Intelligence

**Duración total: 8:00 min** · [Diapositivas](https://claude.ai/artifact/XoVnxjusRMbLNh5mR4H4Jq)

| # | Bloque | Tiempo |
|:-:|---|:-:|
| 1 | Portada y contexto | 0:30 |
| 2 | Problema de negocio y destinatarios | 0:50 |
| 3 | Datos y metodología | 0:55 |
| 4 | Visión general del negocio | 1:05 |
| 5 | Clientes y fidelización | 1:15 |
| 6 | Productos y canales | 1:15 |
| 7 | Evolución del mix de productos | 1:30 |
| 8 | Decisiones estratégicas y cierre | 0:40 |

## 1. Portada y contexto · 0:30

Buenos días. Soy Beatriz y este es H&M Retail Intelligence. El objetivo del proyecto es convertir datos históricos de transacciones, casi 15 millones de artículos vendidos en un año, en información útil para tomar decisiones comerciales. Durante los próximos minutos os cuento cómo pasé de unos ficheros CSV en bruto a cinco dashboards y tres recomendaciones concretas.

## 2. Problema de negocio y destinatarios · 0:50

Me sitúo como Data Analyst del equipo de estrategia comercial de H&M. La pregunta que da sentido a todo es: ¿cómo identificar oportunidades comerciales a partir de los patrones de compra de clientes, productos y canales? El problema no es que H&M venda mal; eso no lo sabemos. El problema es que millones de registros, por sí solos, no ofrecen una visión integrada para orientar decisiones. Por eso esto es un diagnóstico comercial con datos históricos: no predigo ventas ni audito la rentabilidad. El destinatario principal es la dirección comercial, con aplicaciones directas para marketing y CRM, y para planificación de producto.

## 3. Datos y metodología · 0:55

Trabajé con el dataset público de H&M: más de 31 millones de transacciones, 1,4 millones de clientes y 105.000 artículos. Para que fuera manejable en MySQL me quedé con un ciclo anual completo, de septiembre de 2019 a septiembre de 2020: casi 15 millones de filas, sin muestrear clientes. Con Python exploré y limpié los datos, leyendo el fichero por bloques; en MySQL construí un modelo relacional con tres tablas y respondí las preguntas de negocio; y en Tableau lo convertí en cinco dashboards. Una aclaración esencial para todo lo que viene: cada fila es un artículo vendido, no un pedido. Y los precios vienen normalizados, así que no hablo de euros.

## 4. Visión general del negocio · 1:05

Primera pregunta: ¿qué está pasando en el negocio? En el año analizado se vendieron 14,9 millones de artículos a 994.320 compradores únicos. El gráfico muestra la evolución mensual: el mes completo más flojo es febrero de 2020, con un millón de artículos, y a partir de ahí la actividad sube hasta junio, que es el máximo con 1,76 millones; después se modera. ¿Por qué miro también los compradores? Porque vender más artículos no significa necesariamente tener más clientes: puede ser que los mismos clientes compren más. En junio coinciden ambos máximos, 305.018 compradores, así que el pico viene también de una base compradora más amplia. Los meses de septiembre son parciales y los excluyo de las comparaciones. Estas cifras agregadas no nos dicen quién está detrás de la actividad. Por eso el siguiente paso es la segmentación de clientes.

## 5. Clientes y fidelización · 1:15

Segunda pregunta: ¿quién está detrás de esa actividad? Por edad, el grupo de 25 a 34 años concentra el mayor volumen, 5,36 millones de artículos, y además es el que más compra por persona, 18,29 artículos. Aquí distingo dos ideas: volumen, cuánto compra un grupo en total, e intensidad, cuánto compra cada cliente. Por afiliación al club, los clientes ACTIVE compran de media 15,40 artículos frente a 5,48 de los PRE-CREATE. Pero no me quedé solo con la media: calculé también la mediana, 8 frente a 3, porque la distribución está muy sesgada y unos pocos clientes muy activos inflan el promedio. La diferencia se mantiene con las dos métricas. Eso sí, esto es una asociación: no puedo afirmar que pertenecer al club provoque más compras. Sabiendo quién compra, la siguiente pregunta es qué compran y por qué canal.

## 6. Productos y canales · 1:15

Tercera pregunta: ¿qué compran y por dónde? La demanda está muy concentrada: Garment Upper body supone el 38,62 % de los artículos vendidos y, junto con Lower body, el 60,45 %. Por canales, el canal 2 concentra el 71,85 % del volumen. Pero aquí hay una distinción importante: volumen y participación no son lo mismo. Aunque el canal 2 vende más en total, Upper body pesa más dentro del canal 1, un 42,93 %, que dentro del canal 2, un 36,94 %. Es decir, la composición de lo que se vende cambia según el canal. También cambia por edad: el grupo de 25 a 34 años es el que más usa el canal 2. Y una precaución: no identifico el canal 1 como tienda física ni el 2 como online, porque el dataset no lo documenta. Ahora bien, un análisis agregado puede ocultar cambios en el tiempo, y eso es lo que miramos a continuación.

## 7. Evolución del mix de productos · 1:30

Cuarta pregunta: ¿la composición de lo que se vende se mantiene estable? Este gráfico no repite el de ventas mensuales. Aquel respondía cuántos artículos se venden cada mes; este responde qué proporción del total mensual representa cada categoría. Y aquí aparece un cambio claro. Garment Upper body, la categoría principal, pasa de representar cerca del 50 % de los artículos en septiembre de 2019 a un 30 % en mayo y junio de 2020, y luego recupera peso. Ojo: eso es peso relativo, no necesariamente una caída de su volumen absoluto. En paralelo, Swimwear pasa de apenas un 1 % a un 15,6 % en mayo, justo en la primavera. Lower body, en cambio, se mantiene bastante estable, entre el 19 y el 24 %. ¿Para qué le sirve esto a un equipo comercial? Para revisar el calendario de campañas y la planificación del surtido según el periodo. Pero con prudencia: con un único año de datos no puedo afirmar que sea un patrón estacional que se repita. Con estas cuatro perspectivas ya podemos pasar a las decisiones.

## 8. Decisiones estratégicas y cierre · 0:40

Para cerrar, convierto los hallazgos en tres decisiones. Primera: planificar el surtido según la demanda, porque dos categorías concentran el 60 % y el mix cambia a lo largo del año. Segunda: probar campañas segmentadas por edad y afiliación, empezando por los segmentos con menor intensidad de compra. Tercera: diferenciar la estrategia por canal, porque cada canal vende un mix distinto. Cada una lleva un KPI para medir su efecto. Son recomendaciones basadas en patrones observados, no promesas de mejora: lo siguiente sería validarlas con pruebas controladas. Muchas gracias.

---

*≈971 palabras: ritmo de unas 130 palabras por minuto, con margen para las pausas.*

## Frases clave para defender el proyecto

- **Volumen ≠ intensidad:** un grupo puede comprar mucho en total porque tiene muchos clientes, no porque cada uno compre más.
- **Media ≠ mediana:** la distribución está sesgada; la mediana evita que unos pocos clientes muy activos distorsionen la conclusión.
- **Volumen ≠ participación:** el canal 2 vende más, pero Upper body pesa más dentro del canal 1.
- **Asociación ≠ causalidad:** ser ACTIVE no demuestra que el club haga comprar más.
- **Canales sin etiqueta:** no se afirma que el canal 1 sea tienda física ni el 2 online.
- **Un año ≠ estacionalidad:** los cambios del mix son compatibles con un patrón estacional, pero no lo confirman.
- **1 fila = 1 artículo:** no hay id de pedido y los precios están normalizados.
