"""Tests guard del núcleo solar. Verifican el rango físico, no un número mágico."""
import pytest

from app.core.solar import (
    produccion_fv,
    ubicacion_asturias_central,
    factor_temperatura,
    k_system,
    PVGIS_YIELD_REF,
)


def test_yield_asturias_en_rango_plausible():
    """Yield específico de Asturias (Tineo) debe caer en rango oceánico plausible."""
    r = produccion_fv(1.0)
    assert 1150 < r.yield_kwh_kwp < 1280, r.yield_kwh_kwp


def test_coherencia_con_pvgis():
    """El yield del modelo debe quedar dentro de ±5 % del de PVGIS v5.2.

    NO es validación independiente: la POA se toma de PVGIS y k_system está ajustado
    al orden de pérdidas de PVGIS (14 %), así que el acuerdo es en parte por construcción.
    Sirve como guard de regresión y como chequeo de coherencia, no como prueba de exactitud.
    """
    r = produccion_fv(1.0)
    desvio = abs(r.yield_kwh_kwp - PVGIS_YIELD_REF) / PVGIS_YIELD_REF
    assert desvio < 0.05, f"desvío {desvio:.1%} vs PVGIS"


def test_performance_ratio_en_rango():
    """PR de un sistema FV bien diseñado: ~0,72-0,84."""
    r = produccion_fv(1.0)
    assert 0.72 < r.performance_ratio < 0.84, r.performance_ratio


def test_energia_escala_lineal_con_kwp():
    r1 = produccion_fv(1.0)
    r10 = produccion_fv(10.0)
    assert r10.energia_anual_kwh == pytest.approx(10 * r1.energia_anual_kwh, rel=1e-9)


def test_kwp_no_positivo_falla():
    with pytest.raises(ValueError):
        produccion_fv(0.0)


def test_factor_temperatura_penaliza_calor():
    """Mas calor ambiente -> menor factor (derating térmico)."""
    assert factor_temperatura(25.0) > factor_temperatura(30.0)


def test_k_system_en_rango():
    # Clima oceánico nuboso: pérdidas de sistema mayores que en el sur seco.
    assert 0.78 < k_system() < 0.85


def test_doce_meses():
    u = ubicacion_asturias_central()
    assert len(u.poa_mensual) == 12
    assert len(u.tamb_mensual) == 12
