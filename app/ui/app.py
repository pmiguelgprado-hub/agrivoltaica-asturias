"""Calculadora agrivoltaica ganadera asturiana — vista (It-1, slice mínima).

Accesible: español llano, pocos inputs, titulares grandes. La economía y el modelo
agrivoltaico (luz al pasto) llegan en It-2; aquí solo el núcleo solar para que se vea correr.
"""
from __future__ import annotations

import pandas as pd
import streamlit as st

from app.core.solar import MESES, produccion_fv, ubicacion_asturias_central

st.set_page_config(page_title="Agrivoltaica ganadera asturiana",
                   page_icon="🐄", layout="centered")

# --- Estilo accesible: texto grande, alto contraste ---
st.markdown(
    """
    <style>
      html, body, [class*="css"] { font-size: 18px; }
      .titular { font-size: 2.1rem; font-weight: 800; line-height: 1.1; }
      .sub { color: #5a6b3b; font-size: 1.05rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="titular">🐄☀️ Energía solar en tu finca, sin renunciar al pasto</div>',
            unsafe_allow_html=True)
st.markdown('<div class="sub">Calculadora de agrivoltaica ganadera para la Asturias rural · '
            'versión inicial (It-1)</div>', unsafe_allow_html=True)
st.divider()

# --- Entrada simple ---
st.subheader("1 · ¿Cuánta placa solar quieres poner?")
kwp = st.slider("Potencia instalada (kWp)", min_value=3.0, max_value=100.0,
                value=15.0, step=1.0,
                help="A más kWp, más energía. 15 kWp ≈ una granja pequeña.")

ubic = ubicacion_asturias_central()
r = produccion_fv(kwp, ubic)

# --- Titulares grandes ---
st.subheader("2 · Lo que produciría al año")
c1, c2, c3 = st.columns(3)
c1.metric("Energía al año", f"{r.energia_anual_kwh:,.0f} kWh".replace(",", "."))
c2.metric("Productividad", f"{r.yield_kwh_kwp:,.0f} kWh/kWp".replace(",", "."))
c3.metric("Rendimiento (PR)", f"{r.performance_ratio*100:,.0f} %")

hogares = r.energia_anual_kwh / 3500  # consumo medio hogar ES ~3500 kWh/año
st.info(f"Equivale al consumo eléctrico de unos **{hogares:.0f} hogares** al año.")

# --- Reparto mensual ---
st.subheader("3 · Reparto a lo largo del año")
df = pd.DataFrame({"Mes": MESES, "kWh": [round(x) for x in r.energia_mensual_kwh]})
st.bar_chart(df, x="Mes", y="kWh", color="#7a9a3b", height=260)

st.divider()
if ubic.provisional:
    st.warning("⚠️ Datos solares **provisionales** (Asturias central). Se afinarán con PVGIS "
               "para tu ubicación exacta en la próxima versión.")
st.caption("Próximo (It-2): ahorro en € · doble uso pasto+placa · informe imprimible para la beca.")
