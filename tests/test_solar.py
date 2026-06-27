"""Tests guard del núcleo solar. Verifican el rango físico, no un número mágico."""
import pytest

from app.core.solar import (
    produccion_fv,
    ubicacion_asturias_central,
    factor_temperatura,
    k_system,
)


def test_yield_asturias_en_rango_plausible():
    """Yield específico de Asturias debe caer en rango oceánico plausible."""
    r = produccion_fv(1.0)
    assert 1000 < r.yield_kwh_kwp < 1250, r.yield_kwh_kwp


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
