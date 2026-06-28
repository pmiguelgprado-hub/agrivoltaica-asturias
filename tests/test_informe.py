"""Tests del informe imprimible."""
from app.core.informe import DatosInforme, informe_html, _es


def _datos():
    return DatosInforme(
        vacas=40, kwp=17.0, gcr=0.35, ubicacion="Tineo, Asturias",
        energia_anual_kwh=20866, yield_kwh_kwp=1227,
        area_m2=231, luz_pasto_pct=65, ler=1.35,
        consumo_anual_kwh=20640, autoconsumo_pct=42, cobertura_pct=43,
        ahorro_anual_eur=1973, capex_eur=22100, payback_anios=11.2,
        payback_ayuda_anios=6.7, lcoe_eur_kwh=0.084, thi=74, thi_nivel="moderado",
    )


def test_formato_espanol():
    assert _es(22100) == "22.100"
    assert _es(0.084, 3) == "0,084"
    assert _es(1.35, 2) == "1,35"


def test_informe_html_valido_y_con_cifras():
    html = informe_html(_datos())
    assert html.startswith("<!doctype html>")
    assert 'lang="es"' in html
    assert "22.100" in html        # CAPEX formateado
    assert "1.973 €" in html       # ahorro
    assert "refugio" in html       # mensaje clima correcto
    assert "PVGIS" in html         # fuentes citadas


def test_informe_imprimible_tiene_estilo_print():
    html = informe_html(_datos())
    assert "@media print" in html


def test_bloque_impacto_solo_si_hay_datos():
    # Sin datos de impacto: no aparece el bloque.
    sin = informe_html(_datos())
    assert "Y si el concejo se suma" not in sin
    # Con datos: aparece con cifras.
    d = _datos()
    d.impacto_granjas = 37
    d.impacto_mwh = 780
    d.impacto_co2_t = 201
    d.impacto_ahorro_eur = 70935
    d.impacto_concejo = "Tineo"
    con = informe_html(d)
    assert "Y si el concejo se suma" in con
    assert "780 MWh" in con
    assert "70.935" in con
