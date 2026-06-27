"""Calculadora agrivoltaica ganadera asturiana — vista (It-2).

Accesible: español llano, pocos inputs, titulares grandes, sin jerga obligatoria.
Núcleo: solar (PVGIS) + agrivoltaico (luz al pasto) + economía (ahorro/payback) + confort (THI).
"""
from __future__ import annotations

import pandas as pd
import streamlit as st

from app.core.solar import MESES, produccion_fv, ubicacion, concejos
from app.core.agrivoltaic import evaluar_por_potencia
from app.core.economics import evaluar_economia, consumo_granja, KWH_POR_VACA_ANIO
from app.core.perfil import simular_autoconsumo
from app.core.confort import thi, clasifica_thi, ASTURIAS_VERANO_T, ASTURIAS_VERANO_RH
from app.core.informe import DatosInforme, informe_html

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
            'datos solares reales de PVGIS por concejo</div>', unsafe_allow_html=True)
st.divider()

# ---------------- 1 · Tu granja ----------------
st.subheader("1 · Cuéntanos de tu granja")
concejo = st.selectbox("¿En qué concejo está tu finca?", concejos(), index=0,
                       help="Datos solares reales de PVGIS para cada concejo.")
ubic = ubicacion(concejo)
yield_kwp = produccion_fv(1.0, ubic).yield_kwh_kwp   # kWh por kWp y año

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
col_c, col_d = st.columns(2)
with col_c:
    ayuda_pct = st.slider("Ayuda a fondo perdido (%)", 0, 65, 40, step=5,
                          help="Subvención posible (modernización agraria / upside PAC). Sin ella también se calcula.")
with col_d:
    premium_pct = st.slider("Sobrecoste estructura elevada (%)", 30, 100, 60, step=5,
                            help="ASUNCIÓN, no dato: encarecer la pérgola alta para vacuno. "
                                 "Mueve este control para ver cuánto cambia el payback.")

# ---------------- cálculo ----------------
ag = evaluar_por_potencia(kwp, gcr, ubic)
sc = simular_autoconsumo(kwp, consumo_granja(vacas), ubic)   # autoconsumo hora a hora
ec = evaluar_economia(kwp, ag.energia_anual_kwh, vacas, ayuda_frac=ayuda_pct / 100,
                      premium=1 + premium_pct / 100,
                      fraccion_autoconsumo_override=sc.fraccion_autoconsumo)

# ---------------- 2 · Lo que ganas ----------------
st.subheader("2 · Lo que ganarías al año")
c1, c2, c3 = st.columns(3)
c1.metric("Ahorro", f"{ec.ahorro_anual_eur:,.0f} €".replace(",", "."))
c2.metric("Cubre tu gasto", f"{ec.cobertura_demanda*100:,.0f} %")
c3.metric("Se paga en", f"{ec.payback_con_ayuda_anios:,.1f} años".replace(",", ","))
st.caption(f"Sin ninguna ayuda se pagaría en {ec.payback_anios:.1f} años. "
           f"Inversión ≈ {ec.capex_eur:,.0f} € · coste de tu kWh propio (LCOE) "
           f"{ec.lcoe_eur_kwh:.3f} € frente a ~0,18 € de la red.".replace(",", "."))
st.caption(f"Aprovechas en directo el **{sc.fraccion_autoconsumo*100:.0f}%** de lo que generas "
           f"(calculado hora a hora). El sol pega al mediodía y el ordeño es al alba y al "
           f"atardecer, por eso parte se vierte a la red; una batería o mover tareas al "
           f"mediodía subiría este número.")

# ---------------- 3 · Sin renunciar al pasto ----------------
st.subheader("3 · Y sigues teniendo pasto")
d1, d2, d3 = st.columns(3)
d1.metric("Prado ocupado", f"{ag.area_terreno_m2:,.0f} m²".replace(",", "."))
d2.metric("Luz al pasto", f"{ag.transmitancia_pasto*100:,.0f} %")
d3.metric("Doble uso (LER)", f"{ag.ler:.2f}×")
st.caption(f"Solo se usa una **esquina del prado** ({ag.area_terreno_m2:.0f} m², "
           f"{ag.area_terreno_m2/10000:.3f} ha): el resto sigue dando pasto y, bajo las placas "
           f"elevadas, el ganado se resguarda de la lluvia y el viento. Lo que ganas no es "
           f"optimizar el suelo, sino **un ingreso extra + refugio sin perder pradera**. "
           f"En la franja ocupada, el índice de doble uso (LER) es {ag.ler:.2f}× — métrica "
           f"técnica, no clave del proyecto.")

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

# ---------------- informe imprimible ----------------
st.subheader("6 · Llévate el informe")
_datos = DatosInforme(
    vacas=int(vacas), kwp=float(kwp), gcr=float(gcr), ubicacion=ubic.nombre,
    energia_anual_kwh=ag.energia_anual_kwh, yield_kwh_kwp=yield_kwp,
    area_m2=ag.area_terreno_m2, luz_pasto_pct=ag.transmitancia_pasto * 100, ler=ag.ler,
    consumo_anual_kwh=ec.consumo_anual_kwh, autoconsumo_pct=sc.fraccion_autoconsumo * 100,
    cobertura_pct=ec.cobertura_demanda * 100, ahorro_anual_eur=ec.ahorro_anual_eur,
    capex_eur=ec.capex_eur, payback_anios=ec.payback_anios,
    payback_ayuda_anios=ec.payback_con_ayuda_anios, lcoe_eur_kwh=ec.lcoe_eur_kwh,
    thi=valor_thi, thi_nivel=clasifica_thi(valor_thi),
)
st.download_button("📄 Descargar informe imprimible (HTML)",
                   data=informe_html(_datos),
                   file_name=f"informe_agrivoltaica_{int(vacas)}vacas_{int(kwp)}kWp.html",
                   mime="text/html",
                   help="Ábrelo en el navegador e imprímelo o guárdalo en PDF.")

st.caption("Fuentes: recurso solar de PVGIS v5.2 (Tineo) · consumo 516 kWh/vaca·año (estudio "
           "Castilla y León) · CAPEX FV 800-1.400 €/kWp (mercado ES 2026) · THI NRC 1971. "
           "El modelo físico de pérdidas es coherente con el de PVGIS (mismo recurso, mismo "
           "orden de pérdidas). El sobrecoste de la estructura elevada es una asunción "
           "ajustable, no un dato. Versión It-3.")
