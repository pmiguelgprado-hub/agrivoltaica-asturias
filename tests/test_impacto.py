"""Tests del impacto agregado."""
import pytest

from app.core.impacto import (
    impacto_agregado,
    FACTOR_CO2_RED,
    GRANJAS_LECHE_CONCEJO,
)


def test_escala_lineal_con_adopcion():
    poco = impacto_agregado(20_000, 1_900, n_granjas=374, tasa_adopcion=0.05)
    mucho = impacto_agregado(20_000, 1_900, n_granjas=374, tasa_adopcion=0.20)
    assert mucho.energia_limpia_anual_kwh == pytest.approx(4 * poco.energia_limpia_anual_kwh)
    assert mucho.co2_evitado_t_anio > poco.co2_evitado_t_anio


def test_co2_usa_factor_oficial():
    r = impacto_agregado(20_000, 1_900, n_granjas=100, tasa_adopcion=1.0)
    esperado_t = 100 * 20_000 * FACTOR_CO2_RED / 1000.0
    assert r.co2_evitado_t_anio == pytest.approx(esperado_t)


def test_tasa_fuera_de_rango_falla():
    with pytest.raises(ValueError):
        impacto_agregado(20_000, 1_900, n_granjas=374, tasa_adopcion=1.5)


def test_cero_granjas_cero_impacto():
    r = impacto_agregado(20_000, 1_900, n_granjas=0, tasa_adopcion=0.10)
    assert r.energia_limpia_anual_kwh == 0
    assert r.co2_evitado_t_anio == 0


def test_denominador_tineo_es_dato():
    assert GRANJAS_LECHE_CONCEJO["Tineo"] == 374
