"""Tests del núcleo agrivoltaico (trade energía<->pasto)."""
import pytest

from app.core.agrivoltaic import (
    evaluar,
    evaluar_por_potencia,
    kwp_desde_terreno,
    area_terreno_desde_kwp,
    transmitancia_pasto,
    land_equivalent_ratio,
    GCR_MIN,
    GCR_MAX,
)


def test_kwp_escala_con_gcr_y_area():
    assert kwp_desde_terreno(10_000, 0.40) > kwp_desde_terreno(10_000, 0.20)
    assert kwp_desde_terreno(20_000, 0.30) == pytest.approx(2 * kwp_desde_terreno(10_000, 0.30))


def test_transmitancia_decrece_con_gcr():
    assert transmitancia_pasto(0.25) > transmitancia_pasto(0.45)
    assert 0 < transmitancia_pasto(0.35) < 1


def test_ler_mayor_que_uno_en_rango_util():
    # El doble uso debe ganar terreno frente a monocultivo en el rango agrivoltaico.
    assert land_equivalent_ratio(0.35) > 1.0


def test_trade_explicito_mas_gcr_menos_pasto_mas_energia():
    bajo = evaluar(10_000, gcr=0.25)
    alto = evaluar(10_000, gcr=0.45)
    assert alto.kwp > bajo.kwp                      # más energía
    assert alto.transmitancia_pasto < bajo.transmitancia_pasto  # menos pasto


def test_gcr_fuera_de_rango_falla():
    with pytest.raises(ValueError):
        evaluar(10_000, gcr=GCR_MAX + 0.1)
    with pytest.raises(ValueError):
        evaluar(10_000, gcr=GCR_MIN - 0.05)


def test_evaluar_consistente():
    r = evaluar(10_000, gcr=0.35)
    assert r.area_modulo_m2 == pytest.approx(0.35 * 10_000)
    assert r.energia_anual_kwh > 0
    assert r.pasto_relativo == r.transmitancia_pasto


def test_area_desde_kwp_es_inverso():
    # kwp -> area -> kwp debe cerrar el círculo.
    area = area_terreno_desde_kwp(17, 0.35)
    assert kwp_desde_terreno(area, 0.35) == pytest.approx(17)


def test_escala_granja_no_utility():
    """Dimensionar por potencia de granja ocupa un PARCHE, no una hectárea."""
    r = evaluar_por_potencia(17, gcr=0.35)   # ~granja 40 vacas
    assert r.kwp == pytest.approx(17, rel=1e-6)
    assert r.area_terreno_m2 < 300            # < 0,03 ha, una esquina del prado
    assert r.ler > 1.0
