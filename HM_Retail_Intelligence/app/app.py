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
    @import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:wght@600;700&family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"], .stMarkdown, .stText {{ font-family: 'Inter', Arial, sans-serif; }}
    .block-container {{ padding-top: 4rem; max-width: 1280px; }}
    h1, h2, h3 {{ font-family: 'Bodoni Moda', Georgia, serif !important; color: {BLACK}; }}
    .hm-eyebrow {{ color: {RED}; font-weight: 700; letter-spacing: .18em; text-transform: uppercase; font-size: .8rem; }}
    .hm-title {{ font-family: 'Bodoni Moda', Georgia, serif; font-size: 3rem; font-weight: 700; line-height: 1.05; margin: .2rem 0 .4rem; color: {BLACK}; }}
    .hm-sub {{ color: {MUTED}; font-size: 1.05rem; max-width: 820px; }}
    .hm-kpi {{ border-top: 4px solid {BLACK}; padding: .8rem 0 .2rem; }}
    .hm-kpi.red {{ border-top-color: {RED}; }}
    .hm-kpi-value {{ font-family: 'Bodoni Moda', Georgia, serif; font-size: 2.3rem; font-weight: 700; line-height: 1.1; color: {BLACK}; }}
    .hm-kpi.red .hm-kpi-value {{ color: {RED}; }}
    .hm-kpi-label {{ color: {MUTED}; font-size: .9rem; }}
    .hm-result {{ background: {BLACK}; color: #FFFFFF; border-radius: 10px; padding: 1.1rem 1.3rem; height: 100%; }}
    .hm-result .v {{ font-family: 'Bodoni Moda', Georgia, serif; font-size: 2rem; font-weight: 700; color: #FF3341; line-height: 1.1; }}
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
    return d


datos = cargar_datos()

# ---------------------------------------------------------------------------
# Cabecera
# ---------------------------------------------------------------------------

st.markdown('<div class="hm-eyebrow">H&amp;M Retail Intelligence · Simulador de escenarios</div>', unsafe_allow_html=True)
st.markdown('<div class="hm-title">¿Y si…? Explora las decisiones con datos</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hm-sub">Escenarios hipotéticos construidos sobre 14,9 millones de artículos vendidos '
    "entre el 23/09/2019 y el 22/09/2020. Cada pestaña corresponde a una de las tres recomendaciones del proyecto.</div>",
    unsafe_allow_html=True,
)
st.write("")

k1, k2, k3, k4 = st.columns(4)
kpi(k1, fmt_int(TOTAL_ARTICULOS), "artículos vendidos")
kpi(k2, fmt_int(994_320), "compradores únicos")
kpi(k3, "71,85 %", "artículos vendidos por el canal 2", rojo=True)
kpi(k4, "60,45 %", "Upper + Lower body sobre el total", rojo=True)

st.write("")
tab0, tab1, tab2, tab3 = st.tabs(
    ["Visión general", "① Campañas segmentadas", "② Surtido y temporada", "③ Estrategia por canal"]
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
"""
    )
st.caption("H&M Retail Intelligence · Proyecto final Data Analytics · Ironhack · Beatriz Fernández")
