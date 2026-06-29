"""Calculadora agrivoltaica ganadera — dashboard visual (It-8).

Estilo enterprise (fondo blanco, verde/azul/naranja, tipografía IBM Plex Sans), sin emojis
ni imágenes. La información va en gráficas, gauges y modelos, no en prosa. Todo se calcula
desde los datos del concejo (PVGIS) y, opcionalmente, desde la factura/CSV que suba el usuario.
Núcleo de cálculo intacto en app/core/.
"""
from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from app.core.solar import MESES, produccion_fv, ubicacion, concejos
from app.core.agrivoltaic import evaluar_por_potencia
from app.core.economics import evaluar_economia, consumo_granja
from app.core.perfil import (simular_autoconsumo, matriz_generacion_horaria,
                             generacion_horaria_dia, perfil_carga_diaria,
                             DIAS_MES, HORAS_LUZ_MES)
from app.core.confort import thi, clasifica_thi, ASTURIAS_VERANO_T, ASTURIAS_VERANO_RH
from app.core.informe import DatosInforme, informe_html
from app.core.impacto import impacto_agregado, GRANJAS_LECHE_CONCEJO
from app.core.importador import parse_consumo

st.set_page_config(page_title="Agrivoltaica ganadera asturiana", layout="wide")

# ---- paleta enterprise (verde/azul/naranja sobre blanco) ----
VERDE = "#107c41"     # ahorro / energía / positivo
AZUL = "#0a6ed1"      # cobertura / estructura
NARANJA = "#ea7600"   # solar / generación / atención
GRIS = "#5b6b7b"
GRIS_CLARO = "#e3e8ee"
TINTA = "#1b2733"
PLOT = dict(paper_bgcolor="white", plot_bgcolor="white",
            font=dict(family="IBM Plex Sans, sans-serif", size=14, color=TINTA),
            margin=dict(l=10, r=10, t=40, b=10))

st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&display=swap');
      html, body, [class*="css"], [class*="st-"] { font-family: 'IBM Plex Sans', sans-serif; }
      .stApp { background: #ffffff; }
      .block-container { max-width: 1180px; padding-top: 2rem; }
      .dash-title { font-size: 1.9rem; font-weight: 700; color: #1b2733; letter-spacing: -.01em; }
      .dash-sub { color: #5b6b7b; font-size: 1rem; margin-top: .15rem; }
      .sech { font-size: 1.15rem; font-weight: 600; color: #1b2733; margin: 1.4rem 0 .2rem 0;
              padding-left: .55rem; border-left: 4px solid #0a6ed1; }
      .kpi { background:#fff; border:1px solid #e3e8ee; border-top:4px solid #5b6b7b;
             border-radius:.6rem; padding:1rem 1.1rem; box-shadow:0 1px 2px rgba(27,39,51,.05); }
      .kpi.green { border-top-color:#107c41; } .kpi.blue { border-top-color:#0a6ed1; }
      .kpi.orange{ border-top-color:#ea7600; }
      .kpi-l { font-size:.8rem; font-weight:600; color:#5b6b7b; text-transform:uppercase;
               letter-spacing:.04em; }
      .kpi-v { font-size:2.05rem; font-weight:700; color:#1b2733; line-height:1.1; margin-top:.1rem; }
      .kpi-u { font-size:.85rem; color:#5b6b7b; }
      [data-testid="stMetricValue"] { font-size:1.7rem; }
      /* oculta el texto en inglés del file_uploader (drag-drop, "200MB per file") */
      [data-testid="stFileUploaderDropzoneInstructions"] { display:none; }
      [data-testid="stFileUploaderDropzone"] { padding:.5rem 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)


def es(n: float, dec: int = 0) -> str:
    s = f"{n:,.{dec}f}"
    return s.replace(",", "·").replace(".", ",").replace("·", ".")


def kpi(col, clase, label, value, unit=""):
    col.markdown(f'<div class="kpi {clase}"><div class="kpi-l">{label}</div>'
                 f'<div class="kpi-v">{value}</div><div class="kpi-u">{unit}</div></div>',
                 unsafe_allow_html=True)


def sech(t):
    st.markdown(f'<div class="sech">{t}</div>', unsafe_allow_html=True)


def donut(pct, color, titulo):
    pct = max(0.0, min(100.0, pct))
    fig = go.Figure(go.Pie(values=[pct, 100 - pct], hole=.72, sort=False,
                           marker=dict(colors=[color, GRIS_CLARO]),
                           textinfo="none", hoverinfo="skip"))
    fig.update_layout(showlegend=False, height=200, title=dict(text=titulo, x=.5, y=.97,
                      font=dict(size=14, color=TINTA)),
                      annotations=[dict(text=f"<b>{es(pct)}%</b>", x=.5, y=.5,
                                        font=dict(size=30, color=TINTA), showarrow=False)],
                      **PLOT)
    return fig


def gauge_thi(valor):
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=valor,
        number=dict(font=dict(size=34, color=TINTA), valueformat=".0f"),
        gauge=dict(
            axis=dict(range=[50, 100], tickwidth=1, tickcolor=GRIS),
            bar=dict(color=TINTA, thickness=.18),
            steps=[dict(range=[50, 72], color="#c6e7d4"),
                   dict(range=[72, 80], color="#ffe08a"),
                   dict(range=[80, 90], color="#f6b26b"),
                   dict(range=[90, 100], color="#e06666")],
            threshold=dict(line=dict(color=TINTA, width=4), value=valor))))
    fig.update_layout(height=240, title=dict(
        text="Estrés térmico del ganado (THI)", x=.5, font=dict(size=14, color=TINTA)), **PLOT)
    return fig


# ===================== cabecera =====================
st.markdown('<div class="dash-title">Agrivoltaica ganadera · Asturias rural</div>'
            '<div class="dash-sub">Doble uso del suelo: energía solar sobre pasto. '
            'Cálculo con recurso solar real de PVGIS por concejo.</div>',
            unsafe_allow_html=True)
st.divider()

# ===================== controles =====================
sech("Parámetros")
c1, c2, c3 = st.columns(3)
with c1:
    concejo = st.selectbox("Concejo", concejos(), index=0)
    ubic = ubicacion(concejo)
    yield_kwp = produccion_fv(1.0, ubic).yield_kwh_kwp
with c2:
    vacas = st.slider("Vacas", 5, 200, 40, step=5)
    sugerido = max(3, round(consumo_granja(vacas) / yield_kwp))
    kwp = st.slider("Potencia FV (kWp)", 3, 100, int(sugerido), step=1)
with c3:
    gcr = st.select_slider("Luz al pasto", options=[0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50],
                           value=0.35, format_func=lambda g: f"{int((1-g)*100)} %")
    ayuda_pct = st.slider("Ayuda inversión (%)", 0, 65, 40, step=5)
    premium_pct = st.slider("Sobrecoste pérgola (%)", 30, 100, 60, step=5)

up = st.file_uploader("Factura / CSV de consumo (opcional) — afina el cálculo con tus datos reales",
                      type=["csv", "txt"])

# ---- consumo: importado si hay CSV, si no estimado por nº de vacas ----
consumo_anual = consumo_granja(vacas)
pesos_carga = None
fuente_consumo = f"Estimado: {es(consumo_anual)} kWh/año ({vacas} vacas)"
if up is not None:
    try:
        imp = parse_consumo(up.getvalue().decode("utf-8", errors="ignore"))
        if imp.consumo_anual_kwh and imp.consumo_anual_kwh > 0:
            consumo_anual = imp.consumo_anual_kwh
            pesos_carga = imp.perfil_24h
            fuente_consumo = f"Importado ({imp.fuente}): {es(consumo_anual)} kWh/año"
    except Exception:
        fuente_consumo = "No se pudo leer el archivo — usando estimación por vacas"
st.caption(fuente_consumo)

# ===================== cálculo (núcleo intacto) =====================
ag = evaluar_por_potencia(kwp, gcr, ubic)
sc = simular_autoconsumo(kwp, consumo_anual, ubic, pesos_carga=pesos_carga)
ec = evaluar_economia(kwp, ag.energia_anual_kwh, vacas, ayuda_frac=ayuda_pct / 100,
                      premium=1 + premium_pct / 100,
                      fraccion_autoconsumo_override=sc.fraccion_autoconsumo,
                      consumo_anual_override=consumo_anual)

# ===================== KPIs =====================
sech("Resultado")
k1, k2, k3, k4 = st.columns(4)
kpi(k1, "green", "Ahorro anual", f"{es(ec.ahorro_anual_eur)} €", "factura eléctrica")
kpi(k2, "blue", "Cobertura demanda", f"{es(ec.cobertura_demanda*100)} %", "de tu consumo")
kpi(k3, "orange", "Retorno (con ayuda)", f"{es(ec.payback_con_ayuda_anios,1)}", "años")
kpi(k4, "green", "Coste kWh propio", f"{es(ec.lcoe_eur_kwh,3)} €", f"red ≈ 0,18 €")

# ===================== gauges =====================
g1, g2, g3 = st.columns(3)
g1.plotly_chart(donut(ec.cobertura_demanda * 100, AZUL, "Cobertura de la demanda"),
                use_container_width=True)
g2.plotly_chart(donut(sc.fraccion_autoconsumo * 100, NARANJA, "Autoconsumo directo"),
                use_container_width=True)
valor_thi = thi(ASTURIAS_VERANO_T, ASTURIAS_VERANO_RH)
g3.plotly_chart(gauge_thi(valor_thi), use_container_width=True)

# ===================== uso del suelo + LER =====================
sech("Uso del suelo")
u1, u2 = st.columns([3, 1])
ocup = ag.area_terreno_m2
luz = ag.transmitancia_pasto * 100
land = go.Figure()
land.add_bar(y=["Finca"], x=[100 - (100 - luz)], orientation="h", name="Pasto con luz",
             marker_color=VERDE, hovertemplate="Luz al pasto %{x:.0f}%<extra></extra>")
land.add_bar(y=["Finca"], x=[100 - luz], orientation="h", name="Sombra de placa",
             marker_color=NARANJA, hovertemplate="Sombra %{x:.0f}%<extra></extra>")
land.update_layout(barmode="stack", height=160, xaxis=dict(range=[0, 100], ticksuffix=" %"),
                   yaxis=dict(showticklabels=False), legend=dict(orientation="h", y=-.3),
                   title=dict(text="Reparto de luz en la franja con placas", font=dict(size=14)),
                   **PLOT)
u1.plotly_chart(land, use_container_width=True)
kpi(u2, "green", "Doble uso (LER)", f"{es(ag.ler,2)}×", "índice técnico")
u2.metric("Prado ocupado", f"{es(ocup)} m²")

# ===================== generación vs consumo (día medio) =====================
sech("Cuándo se produce y cuándo se consume")
prod = produccion_fv(kwp, ubic)
gen_dia = [sum(generacion_horaria_dia(prod.energia_mensual_kwh[m], DIAS_MES[m],
              HORAS_LUZ_MES[m])[h] for m in range(12)) / 12 for h in range(24)]
carga = perfil_carga_diaria(consumo_anual, pesos_carga)
horas = list(range(24))
curva = go.Figure()
curva.add_scatter(x=horas, y=gen_dia, name="Generación solar", mode="lines",
                  line=dict(color=NARANJA, width=3), fill="tozeroy",
                  fillcolor="rgba(234,118,0,.12)")
curva.add_scatter(x=horas, y=carga, name="Consumo de la granja", mode="lines",
                  line=dict(color=AZUL, width=3))
curva.update_layout(height=300, xaxis=dict(title="Hora del día", dtick=3, ticksuffix="h"),
                    yaxis=dict(title="kWh/h"), legend=dict(orientation="h", y=-.25),
                    title=dict(text="Día medio: el sol pega al mediodía, el ordeño al alba y al ocaso",
                               font=dict(size=14)), **PLOT)
st.plotly_chart(curva, use_container_width=True)

# ===================== energía mensual + firma solar =====================
m1, m2 = st.columns(2)
barras = go.Figure(go.Bar(x=MESES, y=[round(x) for x in prod.energia_mensual_kwh],
                          marker_color=VERDE, hovertemplate="%{x}<br>%{y} kWh<extra></extra>"))
barras.update_layout(height=320, xaxis=dict(categoryorder="array", categoryarray=MESES),
                     yaxis=dict(title="kWh"),
                     title=dict(text="Energía generada por mes", font=dict(size=14)), **PLOT)
m1.plotly_chart(barras, use_container_width=True)

M = matriz_generacion_horaria(kwp, ubic)
heat = go.Figure(go.Heatmap(z=M, x=[f"{h}h" for h in range(24)], y=MESES,
                            colorscale=[[0, "#ffffff"], [.5, NARANJA], [1, "#7a2e00"]],
                            colorbar=dict(title="kWh"),
                            hovertemplate="%{y} · %{x}<br>%{z:.1f} kWh<extra></extra>"))
heat.update_layout(height=320, yaxis=dict(autorange="reversed"),
                   title=dict(text="Firma solar (hora × mes)", font=dict(size=14)), **PLOT)
m2.plotly_chart(heat, use_container_width=True)

# ===================== impacto del concejo =====================
imp_obj = None
if concejo in GRANJAS_LECHE_CONCEJO:
    n_granjas = GRANJAS_LECHE_CONCEJO[concejo]
    sech(f"Impacto si {concejo} se suma")
    adopcion = st.slider(f"Adopción en {concejo} (% de ~{n_granjas} granjas de leche)",
                         5, 100, 10, step=5)
    imp_obj = impacto_agregado(ag.energia_anual_kwh, ec.ahorro_anual_eur, n_granjas, adopcion / 100)
    i1, i2, i3 = st.columns(3)
    kpi(i1, "green", "Energía limpia", f"{es(imp_obj.energia_limpia_anual_kwh/1000)}", "MWh/año")
    kpi(i2, "blue", "CO₂ evitado", f"{es(imp_obj.co2_evitado_t_anio)}", "t/año")
    kpi(i3, "orange", "Queda en el concejo", f"{es(imp_obj.ahorro_agregado_eur_anio)} €", "al año")

# ===================== informe =====================
sech("Informe")
_datos = DatosInforme(
    vacas=int(vacas), kwp=float(kwp), gcr=float(gcr), ubicacion=ubic.nombre,
    energia_anual_kwh=ag.energia_anual_kwh, yield_kwh_kwp=yield_kwp,
    area_m2=ag.area_terreno_m2, luz_pasto_pct=ag.transmitancia_pasto * 100, ler=ag.ler,
    consumo_anual_kwh=ec.consumo_anual_kwh, autoconsumo_pct=sc.fraccion_autoconsumo * 100,
    cobertura_pct=ec.cobertura_demanda * 100, ahorro_anual_eur=ec.ahorro_anual_eur,
    capex_eur=ec.capex_eur, payback_anios=ec.payback_anios,
    payback_ayuda_anios=ec.payback_con_ayuda_anios, lcoe_eur_kwh=ec.lcoe_eur_kwh,
    thi=valor_thi, thi_nivel=clasifica_thi(valor_thi),
    impacto_granjas=int(imp_obj.granjas_adoptan) if imp_obj else 0,
    impacto_mwh=(imp_obj.energia_limpia_anual_kwh / 1000) if imp_obj else 0,
    impacto_co2_t=imp_obj.co2_evitado_t_anio if imp_obj else 0,
    impacto_ahorro_eur=imp_obj.ahorro_agregado_eur_anio if imp_obj else 0,
    impacto_concejo=concejo,
)
st.download_button("Descargar informe (HTML)", data=informe_html(_datos),
                   file_name=f"informe_agrivoltaica_{int(vacas)}vacas_{int(kwp)}kWp.html",
                   mime="text/html")
