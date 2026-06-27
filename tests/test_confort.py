"""Tests del confort animal (THI) — verifica el catch climático."""
import pytest

from app.core.confort import (
    thi,
    clasifica_thi,
    ASTURIAS_VERANO_T,
    ASTURIAS_VERANO_RH,
)


def test_thi_crece_con_temperatura():
    assert thi(30, 70) > thi(20, 70)


def test_thi_crece_con_humedad_en_calor():
    assert thi(30, 90) > thi(30, 50)


def test_humedad_fuera_de_rango_falla():
    with pytest.raises(ValueError):
        thi(25, 120)


def test_asturias_verano_no_es_estres_severo():
    """CATCH CLIMÁTICO: el verano asturiano NO da estrés severo => el beneficio
    dominante del panel es refugio, no sombra anti-calor (spec §7)."""
    valor = thi(ASTURIAS_VERANO_T, ASTURIAS_VERANO_RH)
    assert valor < 80, valor
    assert clasifica_thi(valor) in {"leve", "moderado"}


def test_clasificacion_umbrales():
    assert clasifica_thi(60) == "sin estrés"
    assert clasifica_thi(70) == "leve"
    assert clasifica_thi(75) == "moderado"
    assert clasifica_thi(82) == "severo"
