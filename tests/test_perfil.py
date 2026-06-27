"""Tests del autoconsumo horario (perfil generación vs carga láctea)."""
import pytest

from app.core.perfil import (
    perfil_carga_diaria,
    generacion_horaria_dia,
    simular_autoconsumo,
    PESOS_CARGA_LACTEA,
    HORAS_LUZ_MES,
    DIAS_MES,
)


def test_carga_diaria_conserva_total():
    consumo_anual = 20_640.0
    carga = perfil_carga_diaria(consumo_anual)
    assert len(carga) == 24
    assert sum(carga) == pytest.approx(consumo_anual / 365.0)


def test_carga_tiene_dos_picos_ordeno():
    # Mañana (6-8) y tarde (18-20) deben superar el mínimo nocturno.
    assert max(PESOS_CARGA_LACTEA[6:9]) > PESOS_CARGA_LACTEA[3]
    assert max(PESOS_CARGA_LACTEA[18:21]) > PESOS_CARGA_LACTEA[3]


def test_generacion_diaria_conserva_energia_mes():
    e_mes = 120.0
    gen = generacion_horaria_dia(e_mes, dias_mes=30, horas_luz=14.0)
    assert sum(gen) == pytest.approx(e_mes / 30)
    # De noche no se genera.
    assert gen[0] == 0.0 and gen[23] == 0.0


def test_autoconsumo_en_rango_y_acotado():
    r = simular_autoconsumo(17, 20_640)
    assert 0.0 < r.fraccion_autoconsumo < 1.0
    assert r.autoconsumida_kwh + r.excedente_kwh == pytest.approx(r.generacion_anual_kwh)


def test_sobredimensionar_baja_autoconsumo():
    """Más FV sobre la misma carga -> menor fracción de autoconsumo (físico)."""
    poco = simular_autoconsumo(10, 20_640)
    mucho = simular_autoconsumo(40, 20_640)
    assert mucho.fraccion_autoconsumo < poco.fraccion_autoconsumo


def test_kwp_no_positivo_falla():
    with pytest.raises(ValueError):
        simular_autoconsumo(0, 20_640)


def test_constantes_coherentes():
    assert len(HORAS_LUZ_MES) == 12
    assert sum(DIAS_MES) == 365
