"""Calculadora agrivoltaica ganadera asturiana — vista (It-2).

Accesible: español llano, pocos inputs, titulares grandes, sin jerga obligatoria.
Núcleo: solar (PVGIS) + agrivoltaico (luz al pasto) + economía (ahorro/payback) + confort (THI).
"""
from __future__ import annotations

import pandas as pd
import streamlit as st

from app.core.solar import MESES, produccion_fv, ubicacion_asturias_central
from app.core.agrivoltaic import evaluar_por_potencia
from app.core.economics import evaluar_economia, consumo_granja, KWH_POR_VACA_ANIO
from app.core.confort import thi, clasifica_thi, ASTURIAS_VERANO_T, ASTURIAS_VERANO_RH

st.set_page_config(page_title="Agrivoltaica ganadera asturiana",
                   page_icon="🐄", layout="centered")

st.markdown(
    """
    <style>
      html, body, [class*="css"] { font-size: 18px; }
      .titular { font-size: 2.0rem; font-weight: 800; line-height: 1.15; }
      .sub { color: #5a6b3b; font-size: 1.05rem; }
      [data-testid="stMetricValue"] { font-size: 2.0rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="titular">🐄☀️ Sol y pasto en la misma finca</div>',
            unsafe_allow_html=True)
st.markdown('<div class="sub">Calculadora de agrivoltaica ganadera para la Asturias rural · '
            'datos solares reales de Tineo (PVGIS)</div>', unsafe_allow_html=True)
st.divider()

ubic = ubicacion_asturias_central()
yield_kwp = produccion_fv(1.0, ubic).yield_kwh_kwp   # kWh por kWp y año

# ---------------- 1 · Tu granja ----------------
st.subheader("1 · Cuéntanos de tu granja")
col_a, col_b = st.columns(2)
with col_a:
    vacas = st.slider("Número de vacas", 5, 200, 40, step=5,
                      help="Para estimar cuánta electricidad gasta la granja.")
with col_b:
    sugerido = max(3, round(consumo_granja(vacas) / yield_kwp))
    kwp = st.slider("Placas a instalar (kWp)", 3, 100, int(sugerido), step=1,
                    help=f"Sugerido para tu granja: ~{sugerido} kWp.")

gcr = st.select_slider(
    "¿Más pasto o más energía?",
    options=[0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50],
    value=0.35,
    format_func=lambda g: f"{int((1-g)*100)}% luz al pasto",
    help="Paneles más juntos = más energía pero menos luz al pasto.",
)
ayuda_pct = st.slider("Ayuda a fondo perdido (%)", 0, 65, 40, step=5,
                      help="Subvención posible (modernización agraria / upside PAC). Sin ella también se calcula.")

# ---------------- cálculo ----------------
ag = evaluar_por_potencia(kwp, gcr, ubic)
ec = evaluar_economia(kwp, ag.energia_anual_kwh, vacas, ayuda_frac=ayuda_pct / 100)

# ---------------- 2 · Lo que ganas ----------------
st.subheader("2 · Lo que ganarías al año")
c1, c2, c3 = st.columns(3)
c1.metric("Ahorro", f"{ec.ahorro_anual_eur:,.0f} €".replace(",", "."))
c2.metric("Cubre tu gasto", f"{ec.cobertura_demanda*100:,.0f} %")
c3.metric("Se paga en", f"{ec.payback_con_ayuda_anios:,.1f} años".replace(",", ","))
st.caption(f"Sin ninguna ayuda se pagaría en {ec.payback_anios:.1f} años. "
           f"Inversión ≈ {ec.capex_eur:,.0f} € · coste de tu kWh propio (LCOE) "
           f"{ec.lcoe_eur_kwh:.3f} € frente a ~0,18 € de la red.".replace(",", "."))

# ---------------- 3 · Sin renunciar al pasto ----------------
st.subheader("3 · Y sigues teniendo pasto")
d1, d2, d3 = st.columns(3)
d1.metric("Prado ocupado", f"{ag.area_terreno_m2:,.0f} m²".replace(",", "."))
d2.metric("Luz al pasto", f"{ag.transmitancia_pasto*100:,.0f} %")
d3.metric("Aprovechas la tierra", f"{ag.ler:.2f}×")
st.caption(f"Las placas van elevadas sobre una esquina del prado ({ag.area_terreno_m2:.0f} m², "
           f"{ag.area_terreno_m2/10000:.3f} ha). El ganado sigue pastando debajo y se "
           f"resguarda de la lluvia y el viento. «Aprovechas la tierra {ag.ler:.2f}×» "
           f"(LER) significa que sacas más del prado que dedicándolo solo a una cosa.")

# ---------------- 4 · El ganado, a gusto ----------------
valor_thi = thi(ASTURIAS_VERANO_T, ASTURIAS_VERANO_RH)
st.subheader("4 · El ganado, a gusto")
st.info(f"En Asturias el clima es fresco y húmedo: en un día caluroso de verano el índice "
        f"de estrés térmico (THI) ronda **{valor_thi:.0f}** (estrés *{clasifica_thi(valor_thi)}*, "
        f"no severo). Por eso aquí lo que más aporta la placa elevada es **refugio** de lluvia "
        f"y viento, no sombra contra el calor como en el sur.")

# ---------------- reparto mensual ----------------
st.subheader("5 · Energía mes a mes")
prod = produccion_fv(kwp, ubic)
df = pd.DataFrame({"Mes": MESES, "kWh": [round(x) for x in prod.energia_mensual_kwh]})
st.bar_chart(df, x="Mes", y="kWh", color="#7a9a3b", height=260)

st.divider()
st.caption("Fuentes: PVGIS v5.2 (recurso solar Tineo) · consumo 516 kWh/vaca·año (estudio "
           "Castilla y León) · CAPEX FV 800-1.400 €/kWp (mercado ES 2026) · THI NRC 1971. "
           "Modelo validado contra PVGIS (<1% de desvío). Versión It-2.")
