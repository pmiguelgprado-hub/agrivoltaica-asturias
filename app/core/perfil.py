"""Autoconsumo horario: cruce real entre la curva de generación FV y la de la granja.

Sustituye la heurística de economics.fraccion_autoconsumo por una simulación hora a hora
sobre 12 días representativos (uno por mes), que es lo defendible en una memoria de máster.

Generación: la energía mensual (PVGIS) se reparte en las horas de luz con una forma de
medio-seno centrada en el mediodía solar (~13 h en hora local ES), con la duración del día
propia de cada mes a 43 N.

Carga láctea: dos picos de ORDEÑO (mañana y tarde) sobre una base de refrigeración del
tanque de leche que es ~continua. Forma coherente con el reparto diario descrito en la
literatura (ITEA, "Consumo eléctrico diario en granjas de vacuno lechero").
"""
from __future__ import annotations

import math
from dataclasses import dataclass

from app.core.solar import Ubicacion, produccion_fv, ubicacion_asturias_central

DIAS_MES = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# Duración del día (horas) media por mes a ~43 N.
HORAS_LUZ_MES = [9.3, 10.4, 11.9, 13.5, 14.8, 15.4, 15.1, 13.9, 12.3, 10.8, 9.5, 8.9]
MEDIODIA_SOLAR_LOCAL = 13.0   # hora local aproximada del mediodía solar en España

# Pesos relativos de la carga eléctrica de una granja láctea hora a hora (se normaliza).
# Picos de ordeño ~6-8 h y ~18-20 h; base de refrigeración el resto.
PESOS_CARGA_LACTEA = [
    0.025, 0.020, 0.020, 0.020, 0.025, 0.040,   # 0-5
    0.075, 0.085, 0.070, 0.050, 0.040, 0.035,   # 6-11
    0.035, 0.035, 0.030, 0.030, 0.035, 0.050,   # 12-17
    0.075, 0.080, 0.060, 0.040, 0.030, 0.025,   # 18-23
]


def perfil_carga_diaria(consumo_anual_kwh: float) -> list[float]:
    """Reparte el consumo diario (consumo_anual/365) en 24 horas según la curva láctea."""
    total = sum(PESOS_CARGA_LACTEA)
    diario = consumo_anual_kwh / 365.0
    return [diario * p / total for p in PESOS_CARGA_LACTEA]


def generacion_horaria_dia(energia_mes_kwh: float, dias_mes: int,
                           horas_luz: float) -> list[float]:
    """Generación de un día representativo del mes, repartida en 24 h (medio-seno)."""
    e_dia = energia_mes_kwh / dias_mes
    amanecer = MEDIODIA_SOLAR_LOCAL - horas_luz / 2.0
    ocaso = MEDIODIA_SOLAR_LOCAL + horas_luz / 2.0
    forma = []
    for h in range(24):
        centro = h + 0.5
        if amanecer <= centro <= ocaso:
            forma.append(math.sin(math.pi * (centro - amanecer) / horas_luz))
        else:
            forma.append(0.0)
    s = sum(forma) or 1.0
    return [e_dia * f / s for f in forma]


def matriz_generacion_horaria(kwp: float, ubic: Ubicacion | None = None) -> list[list[float]]:
    """Matriz 12x24 (mes x hora) de generación de un día medio del mes [kWh/h].

    Es la 'firma solar' de la instalación: visualiza cuándo se produce la energía.

    >>> M = matriz_generacion_horaria(17)
    >>> len(M) == 12 and len(M[0]) == 24
    True
    """
    if kwp <= 0:
        raise ValueError("kwp debe ser > 0")
    ubic = ubic or ubicacion_asturias_central()
    prod = produccion_fv(kwp, ubic)
    return [generacion_horaria_dia(prod.energia_mensual_kwh[m], DIAS_MES[m], HORAS_LUZ_MES[m])
            for m in range(12)]


@dataclass
class ResultadoAutoconsumo:
    fraccion_autoconsumo: float     # autoconsumida / generada
    autoconsumida_kwh: float
    excedente_kwh: float
    generacion_anual_kwh: float
    cobertura_demanda: float        # autoconsumida / consumo


def simular_autoconsumo(kwp: float, consumo_anual_kwh: float,
                        ubic: Ubicacion | None = None) -> ResultadoAutoconsumo:
    """Cruza generación y carga hora a hora sobre 12 días tipo. Autoconsumo sin batería.

    >>> r = simular_autoconsumo(17, 20640)
    >>> 0.0 < r.fraccion_autoconsumo < 1.0
    True
    """
    if kwp <= 0:
        raise ValueError("kwp debe ser > 0")
    ubic = ubic or ubicacion_asturias_central()
    prod = produccion_fv(kwp, ubic)
    carga_dia = perfil_carga_diaria(consumo_anual_kwh)

    autoc = 0.0
    gen_total = 0.0
    for m in range(12):
        gen_dia = generacion_horaria_dia(prod.energia_mensual_kwh[m], DIAS_MES[m],
                                         HORAS_LUZ_MES[m])
        autoc_dia = sum(min(g, c) for g, c in zip(gen_dia, carga_dia))
        autoc += autoc_dia * DIAS_MES[m]
        gen_total += sum(gen_dia) * DIAS_MES[m]

    sc = autoc / gen_total if gen_total > 0 else 0.0
    autoc_kwh = prod.energia_anual_kwh * sc
    exced = prod.energia_anual_kwh - autoc_kwh
    cobertura = autoc_kwh / consumo_anual_kwh if consumo_anual_kwh > 0 else 0.0
    return ResultadoAutoconsumo(
        fraccion_autoconsumo=sc,
        autoconsumida_kwh=autoc_kwh,
        excedente_kwh=exced,
        generacion_anual_kwh=prod.energia_anual_kwh,
        cobertura_demanda=cobertura,
    )
