"""Guards del importador de consumo (factura/CSV)."""
from app.core.importador import parse_consumo, ConsumoImportado
from app.core.perfil import simular_autoconsumo


def test_curva_diaria_24h():
    csv = "\n".join(str(x) for x in ([1.0] * 24))
    r = parse_consumo(csv)
    assert r.n_valores == 24
    assert r.perfil_24h is not None and len(r.perfil_24h) == 24
    assert abs(r.consumo_anual_kwh - 24 * 365) < 1e-6


def test_coma_decimal_y_punto_coma():
    csv = "hora;kWh\n0;1,5\n1;2,5"
    r = parse_consumo(csv)
    # cabecera no numérica se ignora; 2 valores
    assert r.n_valores == 2
    assert abs(r.consumo_anual_kwh - 4.0) < 1e-6


def test_horario_anual_agrega_perfil():
    csv = "\n".join(str(1.0) for _ in range(8760))
    r = parse_consumo(csv)
    assert r.n_valores == 8760
    assert r.perfil_24h is not None
    assert abs(sum(r.perfil_24h) - 8760) < 1e-6   # 365 por hora * 24 = 8760


def test_vacio():
    assert parse_consumo("").consumo_anual_kwh is None
    assert parse_consumo("texto,sin,numeros").n_valores == 0


def test_perfil_real_alimenta_autoconsumo():
    # un perfil plano vs el láctea dan fracciones distintas -> el override se usa
    plano = [1.0] * 24
    base = simular_autoconsumo(17, 20000)
    real = simular_autoconsumo(17, 20000, pesos_carga=plano)
    assert real.fraccion_autoconsumo != base.fraccion_autoconsumo


def test_glue_import_a_calculo_mueve_resultados():
    """Integración: la ruta de la app (parse CSV -> overrides -> núcleo) mueve los KPI."""
    from app.core.solar import ubicacion
    from app.core.agrivoltaic import evaluar_por_potencia
    from app.core.economics import evaluar_economia, consumo_granja

    ubic = ubicacion("Tineo"); kwp = 17; vacas = 40
    ag = evaluar_por_potencia(kwp, 0.35, ubic)

    def cobertura_ahorro(consumo, pesos):
        sc = simular_autoconsumo(kwp, consumo, ubic, pesos_carga=pesos)
        ec = evaluar_economia(kwp, ag.energia_anual_kwh, vacas,
                              fraccion_autoconsumo_override=sc.fraccion_autoconsumo,
                              consumo_anual_override=consumo)
        return ec.cobertura_demanda, ec.ahorro_anual_eur

    base = cobertura_ahorro(consumo_granja(vacas), None)

    csv24 = "hora;kWh\n" + "\n".join(f"{h};{v}" for h, v in
                                     enumerate([2, 2, 2, 2, 3, 5, 9, 10, 8, 5, 4, 4,
                                                4, 4, 4, 5, 7, 10, 11, 9, 6, 4, 3, 2]))
    imp = parse_consumo(csv24)
    assert imp.consumo_anual_kwh and imp.perfil_24h
    con_csv = cobertura_ahorro(imp.consumo_anual_kwh, imp.perfil_24h)
    assert con_csv != base   # el consumo y la forma importados cambian el resultado
