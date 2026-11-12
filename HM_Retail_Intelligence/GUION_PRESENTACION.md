# Guion · *Muchos datos, poca visión*

**H&M Retail Intelligence** · Proyecto final Data Analytics · Duración: **8:00 min**

> **Título-problema:** *Muchos datos, poca visión: ¿cómo convertir millones de transacciones de H&M en decisiones sobre clientes, productos y canales?*

Diapositivas: https://claude.ai/artifact/XoVnxjusRMbLNh5mR4H4Jq

## Escaleta

| Tiempo | Pantalla | Bloque |
|---|---|---|
| 0:00 – 0:30 | Diapositiva 1 | Portada · el problema |
| 0:30 – 1:15 | Diapositiva 2 | Problema de negocio y destinatarios |
| 1:15 – 2:15 | Diapositiva 3 | Flujo de trabajo y técnicas |
| 2:15 – 6:15 | Diapositiva 4 → Tableau (Historia 1) | Dashboard en vivo · Tableau |
| 6:15 – 7:15 | Streamlit (diapositiva 5 de respaldo) | Demo en vivo · Streamlit |
| 7:15 – 8:00 | Diapositiva 6 | Aprendizajes y cierre |

## Antes de empezar (checklist)

- [ ] **Diapositivas** abiertas en modo presentación, en la portada.
- [ ] **Tableau**: `HM_Retail_Intelligence.twbx` → *Historia 1* → modo presentación (**F7**), en el punto 1.
- [ ] **Streamlit** ya arrancado (`python -m streamlit run app.py`) en el navegador, pestaña **① Campañas segmentadas**, con *Afiliación al club* → *PRE-CREATE*. Zoom del navegador al 110–125 %.
- [ ] Notificaciones desactivadas y cargador conectado.
- [ ] Practica el **Alt+Tab**: diapositivas → Tableau → Streamlit → diapositivas.
- [ ] Plan B: si algo falla, las diapositivas de **Respaldo** (después de *Respaldo y anexo*) muestran cada dashboard y la captura del simulador.

## Guion palabra por palabra

*Entre paréntesis, lo que haces; entre comillas, lo que dices.*

### 0:00 – 0:30 · Portada · el problema

**Pantalla:** Diapositiva 1

Buenos días. Soy Beatriz Fernández y mi proyecto se titula «Muchos datos, poca visión». H&M genera millones de transacciones, pero tener datos no es lo mismo que entender el negocio. En los próximos ocho minutos os enseño cómo convertí casi 15 millones de artículos vendidos en un año en un dashboard para la toma de decisiones y en un simulador de escenarios.

### 0:30 – 1:15 · Problema de negocio y destinatarios

**Pantalla:** Diapositiva 2

Me sitúo como Data Analyst del equipo de estrategia comercial. La pregunta que guía todo el trabajo es esta: ¿cómo puede H&M usar sus transacciones para detectar oportunidades en clientes, productos y canales? Una aclaración importante: el problema no es que H&M venda mal, eso no lo sabemos. El problema es que los datos transaccionales, por sí solos, no dan una visión integrada para decidir. Por eso esto es un diagnóstico comercial con datos históricos, no una predicción. Va dirigido a dirección comercial, a CRM y marketing, y a planificación de producto.

### 1:15 – 2:15 · Flujo de trabajo y técnicas

**Pantalla:** Diapositiva 3

Este es el flujo completo. Primero, la recopilación: el dataset público de H&M en Kaggle tiene 31,8 millones de transacciones. Como no era viable en MySQL en local, me quedé con un año completo, 14,9 millones de filas, que procesé en Python por bloques. Segundo, la limpieza: no inventé datos; las edades ausentes se etiquetan como desconocidas, y validé que todos los clientes y artículos existían en sus tablas. Tercero, creé variables nuevas: tramos de edad, artículos por comprador y el peso de cada categoría por mes y canal. Cuarto, en MySQL diseñé un modelo relacional con índices para trabajar con 15 millones de filas, y usé CTE y funciones de ventana para calcular la mediana. Y quinto, lo visualicé en Tableau y en Streamlit. Una clave para todo lo que viene: cada fila es un artículo vendido, no un pedido.

### 2:15 – 6:15 · Dashboard en vivo · Tableau

**Pantalla:** Diapositiva 4 → Tableau (Historia 1)

(Di la primera frase con esta diapositiva y pasa con Alt+Tab a Tableau: Historia 1, modo presentación.) «Para responder a esa pregunta construí cinco dashboards que cuentan una sola historia.»

▶ PUNTO 1 · VISIÓN GENERAL (0:45). «Primera pregunta: ¿qué está ocurriendo? En un año se vendieron 14,9 millones de artículos a 994.320 compradores. La actividad cae hasta febrero de 2020, el mes más flojo con un millón de artículos, y sube hasta junio, el máximo con 1,76 millones. Muestro artículos y compradores juntos porque vender más no significa tener más clientes; en junio coinciden ambos máximos. Pero estos totales no dicen quién compra.»

▶ PUNTO 2 · CLIENTES (0:55). «¿Quién está detrás? Aquí distingo volumen de intensidad. El grupo de 25 a 34 años concentra 5,36 millones de artículos y además es el que más compra por persona, 18,29 artículos. Por afiliación al club, los ACTIVE compran de media 15,40 artículos y los PRE-CREATE 5,48. Como la distribución está sesgada, calculé también la mediana en SQL: 8 frente a 3. La diferencia se mantiene. Eso sí, es una asociación: no demuestra que el club haga comprar más.»

▶ PUNTO 3 · PRODUCTOS Y CANALES (0:55). «¿Qué compran y por dónde? Upper body y Lower body suman el 60,45 % de los artículos, y el canal 2 concentra el 71,85 %. (CLIC: filtro de canal del Top 10, selecciona canal 1.) Al filtrar por canal, el peso cambia: Upper body es el 42,93 % del canal 1 y el 36,94 % del canal 2. Volumen y participación no son lo mismo. Y no etiqueto los canales como tienda u online, porque los datos no lo documentan.»

▶ PUNTO 4 · EVOLUCIÓN DEL MIX (0:45). «Un total anual puede esconder cambios. Este gráfico no repite el de ventas: muestra qué porcentaje del mes representa cada categoría. Upper body baja del 50 al 30 % en primavera y Swimwear sube hasta el 15,6 % en mayo. Es útil para planificar surtido y campañas, aunque con un solo año no puedo confirmar que sea estacional.»

▶ PUNTO 5 · DECISIONES ESTRATÉGICAS (0:40). «Con las cuatro perspectivas, propongo tres decisiones, cada una con su KPI: planificar el surtido según la demanda, probar campañas segmentadas por edad y afiliación, y diferenciar la estrategia por canal. Son recomendaciones basadas en patrones observados, no promesas. Y para no quedarme en la recomendación, construí un simulador.» (Alt+Tab a Streamlit.)

### 6:15 – 7:15 · Demo en vivo · Streamlit

**Pantalla:** Streamlit (diapositiva 5 de respaldo)

(Antes de empezar la presentación, deja la app abierta en la pestaña ①, con «Afiliación al club» y «PRE-CREATE» seleccionados.) «Con los mismos resultados de SQL construí esta app en Streamlit, con una pestaña por cada decisión. Por ejemplo, campañas segmentadas. (Sube «Compradores alcanzados» del 20 al 50 %.) Si la mitad de los clientes PRE-CREATE comprara dos artículos más, serían unos 40.000 artículos adicionales. Es un escenario, no una promesa. (Clic en la pestaña ④ Previsión de demanda.) Además, añadí una previsión de demanda a doce meses. Comparé cuatro modelos con un backtest, prediciendo cada mes solo con datos anteriores, y elegí el más sencillo con menor error: un 10,5 %. (Sube el crecimiento de −12 % a 0 %.) Así se ve cómo cambiaría la demanda si se recuperara el nivel del año anterior, y cómo se repartiría por categoría. Es orientativa: solo hay dos años de datos, uno de ellos con pandemia.» (Alt+Tab a las diapositivas.)

### 7:15 – 8:00 · Aprendizajes y cierre

**Pantalla:** Diapositiva 6

Para cerrar, tres aprendizajes. El técnico: con 15 millones de filas, optimizar no es opcional; los índices y la pre-agregación convirtieron consultas inviables en consultas útiles, y validé cada paso antes de avanzar. El analítico: una sola métrica nunca basta; hay que mirar media y mediana, volumen y peso relativo, y no confundir asociación con causa. Y el de negocio: un buen dashboard no termina en gráficos, sino en decisiones medibles. Por eso cierro con tres: surtido según la demanda, campañas segmentadas y estrategia por canal. Muchas gracias; quedo abierta a vuestras preguntas.

## Frases clave para defender el proyecto

- **Diagnóstico, no predicción:** el objetivo es entender patrones históricos para decidir mejor, no adivinar ventas.
- **Volumen ≠ intensidad:** un grupo puede comprar mucho en total porque tiene muchos clientes.
- **Media ≠ mediana:** la distribución está sesgada; la mediana evita que unos pocos clientes muy activos distorsionen la conclusión.
- **Volumen ≠ participación:** el canal 2 vende más, pero Upper body pesa más dentro del canal 1.
- **Asociación ≠ causalidad:** ser ACTIVE no demuestra que el club haga comprar más.
- **Canales sin etiqueta:** no afirmo que el canal 1 sea tienda física ni el 2 online.
- **Un año ≠ estacionalidad:** los cambios del mix son compatibles con un patrón estacional, pero no lo confirman.
- **Escenario ≠ promesa:** el simulador calcula qué pasaría *si* ocurre un cambio, no la probabilidad de lograrlo.

## Preguntas probables del tribunal

**¿Por qué solo un año de datos?**  
Porque 31,8 M de filas no eran viables en MySQL en local. Elegí un ciclo anual completo en lugar de muestrear filas, para no romper el historial de cada cliente.

**¿Por qué no hay ingresos en euros?**  
Porque el dataset trae los precios normalizados. Por eso trabajo en unidades y lo digo desde el principio.

**¿Cómo calculaste la mediana en MySQL?**  
Con una CTE y funciones de ventana: `ROW_NUMBER()` para ordenar y `COUNT(*) OVER` para localizar la posición central, porque MySQL no tiene una función MEDIAN.

**¿Qué problemas técnicos tuviste?**  
La importación de artículos solo cargaba 4 filas, por los saltos de línea `\r\n`. Además, los JOIN sobre 15 M de filas eran inviables sin un índice en `customer_id`, y una consulta tardó 588 s hasta que la optimicé.

**¿Qué tan fiable es la previsión?**  
Comparé cuatro modelos con un backtest. El elegido tiene un error medio del 10,5 %. Es orientativa: solo hay dos años de datos y uno está afectado por la pandemia.

**¿Qué harías con más tiempo?**  
Segmentación RFM y cohortes, usar los dos años para comparar temporadas, y validar las recomendaciones con pruebas A/B.
