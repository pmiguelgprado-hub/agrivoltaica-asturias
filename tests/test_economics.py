"""Tests del núcleo económico."""
import pytest

from app.core.economics import (
    consumo_granja,
    fraccion_autoconsumo,
    capex,
    lcoe,
    evaluar_economia,
    PREMIUM_AGRIVOLTAICO,
)


def test_consumo_escala_con_vacas():
    assert consumo_granja(40) == pytest.approx(40 * 516)
    assert consumo_granja(0) == 0


def test_autoconsumo_decrece_y_acotado():
    alto = fraccion_autoconsumo(5_000, 20_000)    # poco FV vs carga
    bajo = fraccion_autoconsumo(40_000, 20_000)   # mucho FV vs carga
    assert alto > bajo
    assert 0.25 <= bajo <= 0.90
    assert 0.25 <= alto <= 0.90


def test_capex_incluye_premium_agrivoltaico():
    assert capex(10, premium=1.0) < capex(10, premium=PREMIUM_AGRIVOLTAICO)


def test_lcoe_en_rango_plausible():
    # Sistema 15 kWp, ~18 MWh/año -> LCOE típico FV 0,05-0,15 €/kWh.
    cap = capex(15)
    opex = cap * 0.015
    val = lcoe(cap, opex, 18_000)
    assert 0.04 < val < 0.18, val


def test_payback_con_ayuda_menor():
    sin = evaluar_economia(15, 18_000, 40, ayuda_frac=0.0)
    con = evaluar_economia(15, 18_000, 40, ayuda_frac=0.40)
    assert con.payback_con_ayuda_anios < sin.payback_anios
    assert con.ayuda_eur > 0


def test_evaluar_economia_coherente():
    r = evaluar_economia(15, 18_000, 40)
    assert r.autoconsumida_kwh + r.excedente_kwh == pytest.approx(18_000)
    assert r.ahorro_anual_eur > 0
    assert r.payback_anios > 0
    assert r.consumo_anual_kwh == pytest.approx(40 * 516)
