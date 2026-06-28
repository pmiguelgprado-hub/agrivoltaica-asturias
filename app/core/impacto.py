"""Impacto agregado y replicabilidad: de una granja al concejo.

Alimenta el apartado de IMPACTO SOCIAL de la idea de proyecto (beca). Disciplina de
honestidad (no inflar):
- NO se afirma "creación de empleo": la agrivoltaica sobre una granja existente no crea
  puestos, mejora el margen y hace **viable el relevo generacional** (retención de jóvenes).
  Eso es además la categoría exacta de la beca.
- El nº de granjas es un DATO con fuente, no inventado. La adopción se presenta como
  ESCENARIO transparente ("si X de las N granjas del concejo…").
- El CO₂ usa un factor de red oficial y se aplica solo a kWh que desplazan red.

Fuentes:
- Explotaciones de leche por concejo: estadística ganadera de Asturias (Tineo ~374 de leche
  + 32 mixtas; Tineo es el primer concejo ganadero de Asturias). Dato ~2016, orden de
  magnitud estable; se usa como denominador con cautela.
- Factor de emisión de la red eléctrica española: 0,258 kgCO2/kWh (mix nacional sin
  Garantías de Origen, 2025, MITECO). Conservador.
"""
from __future__ import annotations

from dataclasses import dataclass

FACTOR_CO2_RED = 0.258  # kgCO2/kWh, mix nacional ES sin GdO (MITECO 2025)

# Explotaciones de vacuno de LECHE por concejo (dato oficial). Solo los verificados; el
# resto se deja fuera para no inventar denominadores.
GRANJAS_LECHE_CONCEJO = {
    "Tineo": 374,
}


@dataclass
class ResultadoImpacto:
    n_granjas: int
    tasa_adopcion: float
    granjas_adoptan: float
    energia_limpia_anual_kwh: float
    co2_evitado_t_anio: float          # toneladas de CO2 al año
    ahorro_agregado_eur_anio: float    # € que quedan en la economía local


def impacto_agregado(generacion_por_granja_kwh: float, ahorro_por_granja_eur: float,
                     n_granjas: int, tasa_adopcion: float = 0.10) -> ResultadoImpacto:
    """Escala el resultado de una granja a un escenario de adopción en el concejo.

    `tasa_adopcion` es un supuesto explícito (p.ej. 0,10 = una de cada diez granjas).

    >>> r = impacto_agregado(20000, 1900, n_granjas=374, tasa_adopcion=0.10)
    >>> r.co2_evitado_t_anio > 0 and r.granjas_adoptan == 37.4
    True
    """
    if n_granjas < 0:
        raise ValueError("n_granjas debe ser >= 0")
    if not (0.0 <= tasa_adopcion <= 1.0):
        raise ValueError("tasa_adopcion debe estar en [0, 1]")
    adoptan = n_granjas * tasa_adopcion
    energia = generacion_por_granja_kwh * adoptan
    co2_t = energia * FACTOR_CO2_RED / 1000.0   # kg -> t
    ahorro = ahorro_por_granja_eur * adoptan
    return ResultadoImpacto(
        n_granjas=n_granjas,
        tasa_adopcion=tasa_adopcion,
        granjas_adoptan=adoptan,
        energia_limpia_anual_kwh=energia,
        co2_evitado_t_anio=co2_t,
        ahorro_agregado_eur_anio=ahorro,
    )
