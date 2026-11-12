"""
H&M Retail Intelligence · Simulador de escenarios comerciales

App de Streamlit que acompaña al proyecto final. Usa los resultados agregados
de las consultas SQL (los mismos CSV que alimentan el libro de Tableau) para
explorar escenarios hipotéticos vinculados a las tres recomendaciones:

    1. Campañas segmentadas por edad y afiliación.
    2. Planificación del surtido según el peso mensual de cada categoría.
    3. Estrategia diferenciada por canal.

Importante: el análisis es descriptivo. Los escenarios son cálculos sobre lo
observado entre el 23/09/2019 y el 22/09/2020; no son predicciones ni efectos
causales.
"""

from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------------------------
# Configuración y estilo
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="H&M Retail Intelligence · Simulador",
    page_icon="📊",
    layout="wide",
)

RED = "#E50010"
BLACK = "#111111"
GREY = "#B0B0B0"
LIGHT_GREY = "#E6E6E6"
MUTED = "#555555"

DATA = Path(__file__).parent / "data"
TOTAL_ARTICULOS = 14_898_423
MESES_PARCIALES = {"2019-09", "2020-09"}
MESES_ES = {
    "01": "ene", "02": "feb", "03": "mar", "04": "abr", "05": "may", "06": "jun",
    "07": "jul", "08": "ago", "09": "sep", "10": "oct", "11": "nov", "12": "dic",
}

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"], .stMarkdown, .stText {{ font-family: 'Inter', Arial, sans-serif; }}
    .block-container {{ padding-top: 4rem; max-width: 1280px; }}
    h1, h2, h3 {{ font-family: 'Inter', Arial, sans-serif !important; font-weight: 800 !important; letter-spacing: -0.02em; color: {BLACK}; }}
    .hm-bar {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid {BLACK}; padding-bottom: .6rem; margin-bottom: 1.6rem; }}
    .hm-brand {{ font-weight: 800; font-size: 1.15rem; letter-spacing: -0.01em; }}
    .hm-brand span {{ color: {RED}; }}
    .hm-bar-r {{ font-size: .75rem; letter-spacing: .16em; text-transform: uppercase; color: {MUTED}; }}
    .hm-eyebrow {{ color: {RED}; font-weight: 700; letter-spacing: .18em; text-transform: uppercase; font-size: .8rem; }}
    .hm-title {{ font-family: 'Inter', Arial, sans-serif; font-size: 3.2rem; font-weight: 800; letter-spacing: -0.035em; line-height: 1.02; margin: .2rem 0 .4rem; color: {BLACK}; }}
    .hm-sub {{ color: {MUTED}; font-size: 1.05rem; max-width: 820px; }}
    .hm-kpi {{ border-top: 4px solid {BLACK}; padding: .8rem 0 .2rem; }}
    .hm-kpi.red {{ border-top-color: {RED}; }}
    .hm-kpi-value {{ font-family: 'Inter', Arial, sans-serif; font-size: 2.3rem; font-weight: 800; letter-spacing: -0.03em; line-height: 1.1; color: {BLACK}; }}
    .hm-kpi.red .hm-kpi-value {{ color: {RED}; }}
    .hm-kpi-label {{ color: {MUTED}; font-size: .9rem; }}
    .hm-result {{ background: {BLACK}; color: #FFFFFF; border-radius: 0px; padding: 1.1rem 1.3rem; height: 100%; }}
    .hm-result .v {{ font-family: 'Inter', Arial, sans-serif; font-size: 2rem; font-weight: 800; letter-spacing: -0.03em; color: #FF3341; line-height: 1.1; }}
    .hm-result .l {{ color: #BDBDBD; font-size: .88rem; }}
    .hm-note {{ border-left: 5px solid {RED}; background: #F7F7F7; padding: .8rem 1rem; color: {BLACK}; font-size: .92rem; margin: .6rem 0 1rem; }}
    .hm-insight {{ border-left: 5px solid {BLACK}; padding: .2rem 0 .2rem 1rem; font-size: 1.02rem; margin: .4rem 0 1rem; }}
    .stTabs [data-baseweb="tab-list"] {{ gap: 1.6rem; border-bottom: 1px solid {LIGHT_GREY}; }}
    .stTabs [data-baseweb="tab"] {{ font-weight: 600; padding-left: 0; padding-right: 0; }}
    footer {{ visibility: hidden; }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------

def fmt_int(n: float) -> str:
    """Entero con separador de miles español: 14898423 -> 14.898.423."""
    return f"{round(n):,}".replace(",", ".")


def fmt_dec(n: float, d: int = 2) -> str:
    """Decimal con coma: 15.4 -> 15,40."""
    s = f"{n:,.{d}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def fmt_pct(n: float, d: int = 2) -> str:
    return f"{fmt_dec(n, d)} %"


def etiqueta_mes(mes: str) -> str:
    """'2020-05' -> 'may 20'."""
    anio, m = mes[:4], mes[5:7]
    return f"{MESES_ES[m]} {anio[2:]}"


def kpi(col, valor: str, etiqueta: str, rojo: bool = False) -> None:
    clase = "hm-kpi red" if rojo else "hm-kpi"
    col.markdown(
        f'<div class="{clase}"><div class="hm-kpi-value">{valor}</div>'
        f'<div class="hm-kpi-label">{etiqueta}</div></div>',
        unsafe_allow_html=True,
    )


def resultado(col, valor: str, etiqueta: str) -> None:
    col.markdown(
        f'<div class="hm-result"><div class="v">{valor}</div><div class="l">{etiqueta}</div></div>',
        unsafe_allow_html=True,
    )


def estilo(fig: go.Figure, alto: int = 420) -> go.Figure:
    fig.update_layout(
        height=alto,
        template="simple_white",
        font=dict(family="Inter, Arial, sans-serif", size=13, color=BLACK),
        margin=dict(l=10, r=10, t=80, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.0, xanchor="left", x=0),
        title=dict(x=0, xanchor="left", y=0.98, yanchor="top"),
        hoverlabel=dict(bgcolor="white", font_size=13),
        separators=",.",
    )
    fig.update_xaxes(showgrid=False, linecolor=BLACK)
    fig.update_yaxes(gridcolor="#EEEEEE", linecolor="rgba(0,0,0,0)")
    return fig


# ---------------------------------------------------------------------------
# Datos (resultados agregados de las consultas SQL)
# ---------------------------------------------------------------------------

def leer(nombre: str) -> pd.DataFrame:
    """Lee un CSV exportado desde MySQL y limpia espacios y retornos de carro (\\r) en los textos."""
    df = pd.read_csv(DATA / nombre, dtype={"mes": str})
    for col in df.select_dtypes(include=["object", "string"]).columns:
        df[col] = df[col].str.strip()
    return df


@st.cache_data
def cargar_datos() -> dict:
    d = {}
    d["ventas_mes"] = leer("ventas_mensuales.csv")
    d["clientes_mes"] = leer("clientes_mensuales.csv")
    d["edad"] = leer("clientes_por_edad.csv")
    afil = leer("clientes_por_afiliacion.csv")
    act = leer("actividad_por_afiliacion.csv")
    d["afiliacion"] = afil.merge(
        act[["afiliacion", "mediana_articulos"]],
        left_on="estado_afiliacion", right_on="afiliacion", how="left",
    ).drop(columns="afiliacion")
    d["cat_canal"] = leer("categorias_por_canal.csv")
    d["edad_canal"] = leer("ventas_edad_canal.csv")
    vecm = leer("ventas_edad_categoria_mensual.csv")
    vecm["mes"] = vecm["mes"].str[:7]
    vecm["grupo_edad"] = vecm["grupo_edad"].replace({"Desconocida": "Edad desconocida"})
    d["edad_cat_mes"] = vecm
    # Serie mensual completa (sep 2018 – sep 2020) obtenida en el EDA de Python
    d["historico"] = leer("ventas_mensuales_historico.csv")
    d["cat_mes"] = leer("categorias_mensuales.csv")
    return d


datos = cargar_datos()

# ---------------------------------------------------------------------------
# Cabecera
# ---------------------------------------------------------------------------

st.markdown(
    '<div class="hm-bar"><div class="hm-brand">H&amp;M <span>Retail Intelligence</span></div>'
    '<div class="hm-bar-r">Simulador de decisiones comerciales</div></div>',
    unsafe_allow_html=True,
)
st.markdown('<div class="hm-eyebrow">Proyecto final · Data Analytics</div>', unsafe_allow_html=True)
st.markdown('<div class="hm-title">¿Y si…? Explora las decisiones con datos</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hm-sub">Escenarios hipotéticos construidos sobre 14,9 millones de artículos vendidos '
    "entre el 23/09/2019 y el 22/09/2020. Las pestañas ①–③ corresponden a las tres recomendaciones; la ④ proyecta la demanda de los próximos 12 meses.</div>",
    unsafe_allow_html=True,
)
st.write("")

k1, k2, k3, k4 = st.columns(4)
kpi(k1, fmt_int(TOTAL_ARTICULOS), "artículos vendidos")
kpi(k2, fmt_int(994_320), "compradores únicos")
kpi(k3, "71,85 %", "artículos vendidos por el canal 2", rojo=True)
kpi(k4, "60,45 %", "Upper + Lower body sobre el total", rojo=True)

st.write("")
tab0, tab1, tab2, tab3, tab4 = st.tabs(
    ["Visión general", "① Campañas segmentadas", "② Surtido y temporada", "③ Estrategia por canal",
     "④ Previsión de demanda"]
)

# ---------------------------------------------------------------------------
# Pestaña 0 · Visión general
# ---------------------------------------------------------------------------

with tab0:
    vm = datos["ventas_mes"].merge(datos["clientes_mes"], on="mes")
    vm["etiqueta"] = vm["mes"].map(etiqueta_mes)
    vm["parcial"] = vm["mes"].isin(MESES_PARCIALES)

    st.markdown("### Artículos y compradores por mes")
    st.markdown(
        '<div class="hm-insight">Más artículos no siempre significa más compradores. Junio de 2020 es el máximo en ambas métricas: '
        "<b>1.764.507 artículos</b> y <b>305.018 compradores</b>.</div>",
        unsafe_allow_html=True,
    )

    colores = [LIGHT_GREY if p else (RED if m == "2020-06" else GREY) for m, p in zip(vm["mes"], vm["parcial"])]
    fig = go.Figure()
    fig.add_bar(
        x=vm["etiqueta"], y=vm["articulos_vendidos"], name="Artículos vendidos",
        marker_color=colores, legendgroup="a",
        hovertemplate="%{x}<br>%{y:,.0f} artículos<extra></extra>",
    )
    fig.add_scatter(
        x=vm["etiqueta"], y=vm["clientes_unicos"], name="Compradores únicos", yaxis="y2",
        mode="lines+markers", line=dict(color=BLACK, width=3), marker=dict(size=7),
        hovertemplate="%{x}<br>%{y:,.0f} compradores<extra></extra>",
    )
    fig.update_layout(
        yaxis=dict(title="Artículos vendidos"),
        yaxis2=dict(title="Compradores únicos", overlaying="y", side="right", showgrid=False,
                    rangemode="tozero"),
        bargap=0.25,
    )
    st.plotly_chart(estilo(fig, 440), width="stretch")
    st.caption("Septiembre de 2019 y septiembre de 2020 son meses parciales (barras en gris claro).")

# ---------------------------------------------------------------------------
# Pestaña 1 · Campañas segmentadas
# ---------------------------------------------------------------------------

with tab1:
    st.markdown("### ¿Qué supondría aumentar la intensidad de compra de un segmento?")
    st.markdown(
        '<div class="hm-note"><b>Cómo leerlo.</b> Eliges un segmento, qué parte de sus compradores alcanza una campaña '
        "y cuántos artículos más compraría cada comprador alcanzado. El simulador calcula el volumen adicional. "
        "Supone que el incremento se produce: <b>no estima la probabilidad de conseguirlo</b>.</div>",
        unsafe_allow_html=True,
    )

    c_izq, c_der = st.columns([1, 2], gap="large")

    with c_izq:
        tipo = st.radio("Segmentar por", ["Grupo de edad", "Afiliación al club"], horizontal=True)

        if tipo == "Grupo de edad":
            seg = datos["edad"].rename(columns={"grupo_edad": "segmento"})
            seg = seg[seg["segmento"] != "Edad desconocida"]
            orden = ["16-24", "25-34", "35-44", "45-54", "55+"]
            seg = seg.set_index("segmento").loc[orden].reset_index()
            defecto = "16-24"
        else:
            seg = datos["afiliacion"].rename(columns={"estado_afiliacion": "segmento"})
            seg = seg[seg["segmento"].isin(["ACTIVE", "PRE-CREATE"])]
            defecto = "PRE-CREATE"

        segmentos = seg["segmento"].tolist()
        elegido = st.selectbox("Segmento objetivo", segmentos, index=segmentos.index(defecto))
        fila = seg.set_index("segmento").loc[elegido]

        compradores = float(fila["compradores_unicos"])
        articulos = float(fila["articulos_vendidos"])
        app_actual = articulos / compradores

        alcance = st.slider("Compradores alcanzados por la campaña (%)", 5, 100, 20, step=5)
        incremento = st.slider("Artículos adicionales por comprador alcanzado", 0.5, 10.0, 2.0, step=0.5, format="%.1f")

        ref = "media ACTIVE: 15,40 · media 25–34: 18,29"
        st.caption(
            f"Situación actual de **{elegido}**: {fmt_int(compradores)} compradores · "
            f"{fmt_dec(app_actual)} artículos por comprador"
            + (f" · mediana {fmt_dec(float(fila['mediana_articulos']), 0)}" if "mediana_articulos" in fila else "")
            + f". Referencias: {ref}."
        )

    alcanzados = compradores * alcance / 100
    extra = alcanzados * incremento
    app_nuevo = (articulos + extra) / compradores
    impacto_total = extra / TOTAL_ARTICULOS * 100
    impacto_segmento = extra / articulos * 100

    with c_der:
        r1, r2, r3 = st.columns(3)
        resultado(r1, fmt_int(alcanzados), "compradores alcanzados")
        resultado(r2, "+" + fmt_int(extra), "artículos adicionales en el año")
        resultado(r3, "+" + fmt_pct(impacto_total), "sobre el total de artículos vendidos")
        st.write("")

        etiquetas = seg["segmento"].tolist()
        actual = (seg["articulos_vendidos"] / seg["compradores_unicos"]).tolist()
        escenario = [app_nuevo if s == elegido else None for s in etiquetas]

        fig = go.Figure()
        fig.add_bar(
            x=etiquetas, y=actual, name="Actual",
            marker_color=[BLACK if s == elegido else GREY for s in etiquetas],
            text=[fmt_dec(v) for v in actual], textposition="outside",
            hovertemplate="%{x}<br>Actual: %{y:.2f}<extra></extra>",
        )
        fig.add_bar(
            x=etiquetas, y=escenario, name="Escenario", marker_color=RED,
            text=[fmt_dec(v) if v else "" for v in escenario], textposition="outside",
            hovertemplate="%{x}<br>Escenario: %{y:.2f}<extra></extra>",
        )
        fig.update_layout(
            barmode="group", bargap=0.3,
            yaxis=dict(title="Artículos por comprador", range=[0, max(actual + [app_nuevo]) * 1.18]),
            title=dict(text="Artículos por comprador: actual frente a escenario", font=dict(size=15)),
        )
        st.plotly_chart(estilo(fig, 400), width="stretch")

        st.markdown(
            f'<div class="hm-insight">Si el <b>{alcance} %</b> de los compradores <b>{elegido}</b> comprase '
            f"<b>{fmt_dec(incremento, 1)}</b> artículos más, el segmento pasaría de <b>{fmt_dec(app_actual)}</b> a "
            f"<b>{fmt_dec(app_nuevo)}</b> artículos por comprador (+{fmt_pct(impacto_segmento, 1)} en su volumen).</div>",
            unsafe_allow_html=True,
        )

# ---------------------------------------------------------------------------
# Pestaña 2 · Surtido y temporada
# ---------------------------------------------------------------------------

with tab2:
    st.markdown("### ¿Qué categorías ganan o pierden peso en cada mes?")
    st.markdown(
        '<div class="hm-note"><b>Cómo leerlo.</b> El peso de una categoría es su porcentaje sobre el total de '
        "artículos vendidos del mes. Compararlo con su peso anual muestra qué conviene reforzar en cada periodo. "
        "Con un solo año de datos <b>no se puede confirmar que el patrón sea estacional</b>.</div>",
        unsafe_allow_html=True,
    )

    df = datos["edad_cat_mes"]
    f1, f2 = st.columns([1, 1], gap="large")
    with f1:
        grupos = ["Todos", "16-24", "25-34", "35-44", "45-54", "55+"]
        grupo = st.selectbox("Grupo de edad", grupos, index=0)
    if grupo != "Todos":
        df = df[df["grupo_edad"] == grupo]

    cat_mes = df.groupby(["mes", "categoria"], as_index=False)["articulos_vendidos"].sum()
    cat_mes["peso"] = cat_mes["articulos_vendidos"] / cat_mes.groupby("mes")["articulos_vendidos"].transform("sum") * 100
    anual = df.groupby("categoria")["articulos_vendidos"].sum()
    anual = anual / anual.sum() * 100
    principales = anual[anual >= 1].sort_values(ascending=False).index.tolist()

    meses = sorted(cat_mes["mes"].unique())
    meses_completos = [m for m in meses if m not in MESES_PARCIALES]
    with f2:
        mes_sel = st.select_slider(
            "Mes a analizar", options=meses_completos, value="2020-05", format_func=etiqueta_mes,
        )

    cats = st.multiselect(
        "Categorías en el gráfico de evolución", principales,
        default=[c for c in ["Garment Upper body", "Garment Lower body", "Swimwear"] if c in principales],
    )

    g1, g2 = st.columns([3, 2], gap="large")

    with g1:
        paleta = [RED, BLACK, GREY, "#FF8A92", "#555555", "#7A0009", "#D9D9D9", "#333333"]
        fig = go.Figure()
        for i, c in enumerate(cats):
            serie = cat_mes[cat_mes["categoria"] == c].sort_values("mes")
            fig.add_scatter(
                x=serie["mes"].map(etiqueta_mes), y=serie["peso"], name=c, mode="lines+markers",
                line=dict(color=paleta[i % len(paleta)], width=3.5 if i == 0 else 2.5,
                          dash="dash" if c == "Garment Lower body" else "solid"),
                hovertemplate=f"{c}<br>%{{x}}: %{{y:.1f}} %<extra></extra>",
            )
        fig.add_vline(x=etiqueta_mes(mes_sel), line_color=RED, line_width=1, line_dash="dot")
        fig.update_layout(
            yaxis=dict(title="% del total mensual", ticksuffix=" %"),
            title=dict(text="Peso mensual de cada categoría", font=dict(size=15)),
        )
        st.plotly_chart(estilo(fig, 430), width="stretch")

    with g2:
        mes_df = cat_mes[cat_mes["mes"] == mes_sel].set_index("categoria")["peso"]
        dif = (mes_df.reindex(principales).fillna(0) - anual.reindex(principales)).sort_values()
        fig = go.Figure(go.Bar(
            x=dif.values, y=dif.index, orientation="h",
            marker_color=[RED if v > 0 else BLACK for v in dif.values],
            text=[("+" if v > 0 else "") + fmt_dec(v, 1) + " pp" for v in dif.values],
            textposition="outside", cliponaxis=False,
            hovertemplate="%{y}<br>%{x:+.1f} pp frente a la media anual<extra></extra>",
        ))
        lim = max(abs(dif.min()), abs(dif.max())) * 1.7
        fig.update_layout(
            xaxis=dict(title="pp frente a su peso anual", range=[-lim, lim], zeroline=True, zerolinecolor=BLACK),
            title=dict(text=f"{etiqueta_mes(mes_sel)} frente a la media anual", font=dict(size=15)),
            showlegend=False,
        )
        st.plotly_chart(estilo(fig, 430), width="stretch")

    sube, baja = dif.idxmax(), dif.idxmin()
    st.markdown(
        f'<div class="hm-insight">En <b>{etiqueta_mes(mes_sel)}</b>'
        + ("" if grupo == "Todos" else f" (grupo {grupo})")
        + f", <b>{sube}</b> es la categoría que más peso gana (+{fmt_dec(dif.max(), 1)} pp) y <b>{baja}</b> "
        f"la que más pierde ({fmt_dec(dif.min(), 1)} pp). Son señales para revisar el surtido y el calendario de campañas.</div>",
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Pestaña 3 · Estrategia por canal
# ---------------------------------------------------------------------------

with tab3:
    st.markdown("### ¿Cómo cambiaría el mix total si cambia el peso de cada canal?")
    st.markdown(
        '<div class="hm-note"><b>Cómo leerlo.</b> Cada canal vende un mix distinto de categorías. Al mover la cuota '
        "del canal 2 se recalcula el mix total, suponiendo que la composición interna de cada canal se mantiene. "
        "Los canales <b>no se identifican como tienda física u online</b>: el dataset no lo documenta.</div>",
        unsafe_allow_html=True,
    )

    cc = datos["cat_canal"].copy()
    cc["peso_canal"] = cc["articulos_vendidos"] / cc.groupby("canal_venta")["articulos_vendidos"].transform("sum") * 100
    mix = cc.pivot_table(index="categoria", columns="canal_venta", values="peso_canal", fill_value=0)
    mix.columns = ["canal_1", "canal_2"]
    top = (
        cc.groupby("categoria")["articulos_vendidos"].sum().sort_values(ascending=False).head(8).index.tolist()
    )
    otras = mix.drop(index=top).sum()
    mix = pd.concat([mix.loc[top], otras.to_frame("Otras categorías").T])

    p1, p2 = st.columns([1, 2], gap="large")
    with p1:
        cuota2 = st.slider("Cuota del canal 2 sobre los artículos vendidos (%)", 0.0, 100.0, 71.85, step=0.5, format="%.2f")
        st.caption("Valor observado: 71,85 % canal 2 · 28,15 % canal 1.")

        q = cuota2 / 100
        mix["actual"] = 0.7185 * mix["canal_2"] + 0.2815 * mix["canal_1"]
        mix["escenario"] = q * mix["canal_2"] + (1 - q) * mix["canal_1"]
        mix["dif"] = mix["escenario"] - mix["actual"]

        st.write("")
        resultado(st, fmt_pct(mix.loc["Garment Upper body", "escenario"], 1), "peso de Garment Upper body en el mix total")
        st.write("")
        mayor = mix["dif"].drop(index="Otras categorías").abs().idxmax()
        if abs(mix.loc[mayor, "dif"]) < 0.01:
            resultado(st, "Sin cambios", "mueve la cuota del canal 2 para simular otro reparto")
        else:
            resultado(
                st, ("+" if mix.loc[mayor, "dif"] > 0 else "") + fmt_dec(mix.loc[mayor, "dif"], 2) + " pp",
                f"mayor cambio de peso: {mayor}",
            )

    with p2:
        fig = go.Figure()
        fig.add_bar(
            y=mix.index, x=mix["actual"], name="Mix actual", orientation="h", marker_color=GREY,
            hovertemplate="%{y}<br>Actual: %{x:.2f} %<extra></extra>",
        )
        fig.add_bar(
            y=mix.index, x=mix["escenario"], name="Mix del escenario", orientation="h", marker_color=RED,
            text=[fmt_pct(v, 1) for v in mix["escenario"]], textposition="outside",
            hovertemplate="%{y}<br>Escenario: %{x:.2f} %<extra></extra>",
        )
        fig.update_layout(
            barmode="group", bargap=0.25,
            yaxis=dict(autorange="reversed"),
            xaxis=dict(title="% del total de artículos", ticksuffix=" %", range=[0, mix[["actual", "escenario"]].max().max() * 1.18]),
            title=dict(text="Mix de categorías: actual frente a escenario", font=dict(size=15)),
        )
        st.plotly_chart(estilo(fig, 470), width="stretch")

    st.markdown("#### Composición de cada canal")
    h1, h2 = st.columns([3, 2], gap="large")
    with h1:
        z = mix[["canal_1", "canal_2"]]
        fig = go.Figure(go.Heatmap(
            z=z.values, x=["Canal 1", "Canal 2"], y=z.index,
            colorscale=[[0, "#FFFFFF"], [0.5, "#FF8A92"], [1, RED]],
            text=[[fmt_pct(v, 1) for v in row] for row in z.values], texttemplate="%{text}",
            hovertemplate="%{y} · %{x}: %{z:.2f} %<extra></extra>", showscale=False,
        ))
        fig.update_layout(yaxis=dict(autorange="reversed"), title=dict(text="Peso de cada categoría dentro del canal", font=dict(size=15)))
        st.plotly_chart(estilo(fig, 420), width="stretch")
    with h2:
        ec = datos["edad_canal"]
        ec = ec[ec["grupo_edad"] != "Edad desconocida"]
        fig = go.Figure()
        for canal, color in [(1, GREY), (2, BLACK)]:
            s = ec[ec["canal_venta"] == canal]
            fig.add_bar(
                x=s["grupo_edad"], y=s["porcentaje_grupo_edad"], name=f"Canal {canal}", marker_color=color,
                text=[fmt_dec(v, 1) for v in s["porcentaje_grupo_edad"]], textposition="inside",
                hovertemplate=f"Canal {canal}<br>%{{x}}: %{{y:.2f}} %<extra></extra>",
            )
        fig.update_layout(
            barmode="stack", yaxis=dict(title="% de artículos del grupo", ticksuffix=" %", range=[0, 100]),
            title=dict(text="Uso de cada canal por edad", font=dict(size=15)),
        )
        st.plotly_chart(estilo(fig, 420), width="stretch")

# ---------------------------------------------------------------------------
# Pestaña 4 · Previsión de demanda
# ---------------------------------------------------------------------------


def prevision_estacional(serie: pd.Series, periodo: pd.Period, meses_tendencia: int = 3) -> float:
    """Mismo mes del año anterior × crecimiento de los últimos meses completos frente al año anterior."""
    previos = [periodo - i for i in range(1, meses_tendencia + 1)]
    pares = [(q, q - 12) for q in previos if q in serie.index and (q - 12) in serie.index]
    crecimiento = sum(serie[a] for a, _ in pares) / sum(serie[b] for _, b in pares) if pares else 1.0
    return serie[periodo - 12] * crecimiento


@st.cache_data
def validar_modelos(hist: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Backtest: predice cada mes de oct 2019 – ago 2020 solo con la información anterior a ese mes."""
    c = hist[hist["mes_completo"] == 1].set_index("mes")["articulos_vendidos"]
    c.index = pd.PeriodIndex(c.index, freq="M")
    test = c[c.index >= pd.Period("2019-10", "M")]
    pred = pd.DataFrame(index=test.index)
    pred["Real"] = test
    pred["Estacional ajustado"] = [prevision_estacional(c, p) for p in test.index]
    pred["Mismo mes año anterior"] = [c[p - 12] for p in test.index]
    pred["Último mes"] = [c[p - 1] for p in test.index]
    pred["Media móvil 3 meses"] = [c[[p - 1, p - 2, p - 3]].mean() for p in test.index]
    errores = pd.DataFrame({
        "Modelo": [m for m in pred.columns if m != "Real"],
        "MAPE (%)": [((pred[m] - pred["Real"]).abs() / pred["Real"]).mean() * 100 for m in pred.columns if m != "Real"],
    }).sort_values("MAPE (%)").reset_index(drop=True)
    return pred, errores


with tab4:
    st.markdown("### ¿Cuánta demanda cabe esperar en los próximos 12 meses?")

    hist = datos["historico"].copy()
    hist["periodo"] = pd.PeriodIndex(hist["mes"], freq="M")
    completos = hist[hist["mes_completo"] == 1].set_index("periodo")["articulos_vendidos"]
    pred_bt, errores = validar_modelos(datos["historico"])
    mape = float(errores.loc[errores["Modelo"] == "Estacional ajustado", "MAPE (%)"].iloc[0])
    mape_txt = {r["Modelo"]: fmt_dec(r["MAPE (%)"], 1) for _, r in errores.iterrows()}

    st.markdown(
        f'<div class="hm-note"><b>Método.</b> Cada mes se proyecta como <b>el mismo mes del año anterior × el crecimiento '
        f"reciente</b> (últimos 3 meses frente a los mismos meses del año previo). Validado sobre oct 2019 – ago 2020: "
        f"error medio <b>{mape_txt['Estacional ajustado']} %</b>, frente a {mape_txt['Último mes']} % repitiendo el último mes "
        f"y {mape_txt['Mismo mes año anterior']} % copiando el año anterior. Con dos años de datos, y uno afectado por la "
        "pandemia, la previsión es <b>orientativa</b>.</div>",
        unsafe_allow_html=True,
    )

    ultimo = completos.index.max()                      # ago 2020
    horizonte = pd.period_range(ultimo + 1, periods=12, freq="M")
    previos = [ultimo - i for i in range(3)]
    tendencia = sum(completos[q] for q in previos) / sum(completos[q - 12] for q in previos) - 1

    c_izq, c_der = st.columns([1, 2], gap="large")
    with c_izq:
        crecimiento = st.slider(
            "Crecimiento frente al año anterior (%)", -30.0, 30.0, float(round(tendencia * 100, 1)), step=0.5, format="%.1f",
        )
        st.caption(
            f"Tendencia observada: {fmt_pct(tendencia * 100, 1)} (jun–ago 2020 frente a jun–ago 2019). "
            "Muévelo para simular una recuperación o una caída."
        )
        meses_campania = st.multiselect(
            "Meses con campaña comercial", list(horizonte), default=[horizonte[8]] if len(horizonte) > 8 else [],
            format_func=lambda p: etiqueta_mes(str(p)),
        )
        impacto = st.slider("Impacto esperado de la campaña en esos meses (%)", 0.0, 20.0, 5.0, step=0.5, format="%.1f")

    base = pd.Series([completos[p - 12] for p in horizonte], index=horizonte)
    prevision = base * (1 + crecimiento / 100)
    prevision = prevision * [1 + impacto / 100 if p in meses_campania else 1 for p in horizonte]
    banda_inf, banda_sup = prevision * (1 - mape / 100), prevision * (1 + mape / 100)

    total_prev = prevision.sum()
    total_ult = completos[completos.index > ultimo - 12].sum()
    pico = prevision.idxmax()

    with c_der:
        r1, r2, r3 = st.columns(3)
        resultado(r1, f"{fmt_dec(total_prev / 1e6, 2)} M", f"artículos previstos ({etiqueta_mes(str(horizonte[0]))} – {etiqueta_mes(str(horizonte[-1]))})")
        resultado(r2, ("+" if total_prev >= total_ult else "") + fmt_pct((total_prev / total_ult - 1) * 100, 1), "frente a los últimos 12 meses completos")
        resultado(r3, etiqueta_mes(str(pico)), f"mes pico previsto · {fmt_dec(prevision[pico] / 1e6, 2)} M artículos")
        st.write("")

        x_hist = [etiqueta_mes(str(p)) for p in hist["periodo"]]
        x_prev = [etiqueta_mes(str(p)) for p in horizonte]
        fig = go.Figure()
        fig.add_scatter(
            x=x_prev + x_prev[::-1], y=list(banda_sup) + list(banda_inf[::-1]), fill="toself",
            fillcolor="rgba(229,0,16,0.10)", line=dict(width=0), hoverinfo="skip", name=f"Margen ±{fmt_dec(mape, 1)} %",
        )
        reales = hist[hist["mes_completo"] == 1]
        fig.add_scatter(
            x=[etiqueta_mes(m) for m in reales["mes"]], y=reales["articulos_vendidos"], name="Real",
            mode="lines+markers", line=dict(color=BLACK, width=3), marker=dict(size=6),
            hovertemplate="%{x}<br>%{y:,.0f} artículos<extra></extra>",
        )
        parciales = hist[hist["mes_completo"] == 0]
        fig.add_scatter(
            x=[etiqueta_mes(m) for m in parciales["mes"]], y=parciales["articulos_vendidos"], name="Mes parcial",
            mode="markers", marker=dict(color=GREY, size=9, symbol="circle-open", line=dict(width=2)),
            hovertemplate="%{x} (parcial)<br>%{y:,.0f} artículos<extra></extra>",
        )
        fig.add_scatter(
            x=[x_hist[hist.index[hist["periodo"] == ultimo][0]]] + x_prev,
            y=[completos[ultimo]] + list(prevision), name="Previsión",
            mode="lines+markers", line=dict(color=RED, width=3, dash="dash"), marker=dict(size=6),
            hovertemplate="%{x}<br>%{y:,.0f} artículos previstos<extra></extra>",
        )
        orden_x = list(dict.fromkeys(x_hist + x_prev))
        fig.update_layout(
            xaxis=dict(categoryorder="array", categoryarray=orden_x, tickangle=0,
                       tickmode="array", tickvals=orden_x[::3]),
            yaxis=dict(title="Artículos vendidos", rangemode="tozero"),
            title=dict(text="Demanda mensual: histórico y previsión", font=dict(size=15)),
        )
        st.plotly_chart(estilo(fig, 460), width="stretch")

    st.markdown("#### De la previsión total a la planificación por categoría")
    d1, d2 = st.columns([1, 2], gap="large")
    with d1:
        mes_plan = st.selectbox("Mes a planificar", list(horizonte), index=8, format_func=lambda p: etiqueta_mes(str(p)))
        cm = datos["cat_mes"]
        ref = str(mes_plan - 12)
        pesos = cm[cm["mes"] == ref].set_index("categoria")["articulos_vendidos"]
        pesos = pesos / pesos.sum()
        unidades = (pesos * prevision[mes_plan]).sort_values(ascending=False)
        top = unidades.head(8)
        st.caption(
            f"Reparte los {fmt_int(prevision[mes_plan])} artículos previstos para {etiqueta_mes(str(mes_plan))} "
            f"según el peso de cada categoría en {etiqueta_mes(ref)}."
        )
        resultado(st, fmt_int(top.iloc[0]), f"unidades previstas de {top.index[0]}")
    with d2:
        fig = go.Figure(go.Bar(
            x=top.values, y=top.index, orientation="h",
            marker_color=[RED if i == 0 else (BLACK if i < 3 else GREY) for i in range(len(top))],
            text=[fmt_int(v) for v in top.values], textposition="outside", cliponaxis=False,
            hovertemplate="%{y}<br>%{x:,.0f} unidades previstas<extra></extra>",
        ))
        fig.update_layout(
            yaxis=dict(autorange="reversed"), xaxis=dict(title="Unidades previstas", range=[0, top.max() * 1.22]),
            title=dict(text=f"Unidades previstas por categoría · {etiqueta_mes(str(mes_plan))}", font=dict(size=15)),
            showlegend=False,
        )
        st.plotly_chart(estilo(fig, 400), width="stretch")

    with st.expander("Validación del modelo (backtest)"):
        v1, v2 = st.columns([1, 2], gap="large")
        with v1:
            tabla = errores.copy()
            tabla["MAPE (%)"] = tabla["MAPE (%)"].map(lambda v: fmt_dec(v, 1))
            st.dataframe(tabla, hide_index=True, width="stretch")
            st.caption(
                "MAPE: error porcentual absoluto medio. Cada mes de oct 2019 – ago 2020 se predice solo con "
                "datos anteriores a ese mes. Se elige el modelo más sencillo con menor error."
            )
        with v2:
            fig = go.Figure()
            xs = [etiqueta_mes(str(p)) for p in pred_bt.index]
            fig.add_scatter(x=xs, y=pred_bt["Real"], name="Real", mode="lines+markers", line=dict(color=BLACK, width=3))
            fig.add_scatter(x=xs, y=pred_bt["Estacional ajustado"], name="Estacional ajustado", mode="lines+markers",
                            line=dict(color=RED, width=2.5, dash="dash"))
            fig.add_scatter(x=xs, y=pred_bt["Último mes"], name="Último mes", mode="lines",
                            line=dict(color=GREY, width=2))
            fig.update_layout(yaxis=dict(title="Artículos vendidos"), title=dict(text="Previsión frente a realidad", font=dict(size=15)))
            st.plotly_chart(estilo(fig, 360), width="stretch")

# ---------------------------------------------------------------------------
# Pie
# ---------------------------------------------------------------------------

st.divider()
with st.expander("Metodología y limitaciones"):
    st.markdown(
        """
- **Fuente:** dataset público *H&M Personalized Fashion Recommendations* (Kaggle). Periodo 23/09/2019 – 22/09/2020.
- **Pipeline:** Python (limpieza y preparación) → MySQL (modelo relacional y consultas) → CSV agregados → Tableau y esta app.
- **1 fila = 1 artículo vendido**, no un pedido. Los precios están normalizados, por lo que no se calculan ingresos.
- Los escenarios son **cálculos sobre patrones observados**, no predicciones ni efectos causales. Para validarlos harían falta pruebas controladas (A/B).
- Septiembre de 2019 y septiembre de 2020 son meses parciales.
- **Previsión:** modelo estacional ajustado validado con backtest (oct 2019 – ago 2020). Usa la serie mensual completa del EDA (sep 2018 – sep 2020). Dos años de datos, con 2020 afectado por la pandemia: la previsión es orientativa.
"""
    )
st.caption("H&M Retail Intelligence · Proyecto final Data Analytics · Ironhack · Beatriz Fernández")
