"""Núcleo agrivoltaico: el trade-off explícito entre energía y pasto.

La variable de diseño clave es el **GCR** (Ground Coverage Ratio = área de módulo /
área de terreno). Subirlo da más kWp por hectárea (más energía) pero deja menos luz al
pasto. Esta tensión es el corazón del proyecto y se muestra abierta, no oculta.

Modelo (primer orden, documentado):
- kWp por terreno:   kWp = area_modulo * eta ;  area_modulo = GCR * area_terreno
- Luz al pasto:      transmitancia = 1 - GCR   (fracción de PAR que llega al suelo)
- LER (Land Equivalent Ratio) = pasto_relativo + energia_relativa  (IEA-PVPS T13, 2025)
  LER > 1  =>  el doble uso produce más que cualquiera de los usos por separado.

Simplificaciones y referencias:
- transmitancia = 1 - GCR es la aproximación de primer orden habitual para la luz que
  llega al cultivo bajo hileras; la ALTURA del panel redistribuye la sombra de forma más
  uniforme (mejora calidad, no cambia mucho el total). Refs: InSPIRE Agrivoltaics Shading
  Tool (NREL), IEA-PVPS T13-29 "Dual Land Use" (2025), MDPI Energies 18(14):3877.
- El pasto atlántico asturiano rara vez está limitado por luz (mucha difusa, agua
  abundante); modelar pasto_relativo = transmitancia es CONSERVADOR (probablemente
  tolera mejor la sombra parcial y gana por menor estrés hídrico/térmico).
"""
from __future__ import annotations

from dataclasses import dataclass

from app.core.solar import Ubicacion, produccion_fv, ubicacion_asturias_central

ETA_MODULO_KWP_M2 = 0.21    # kWp por m2 de módulo (silicio ~21 % a STC)
GCR_REF_HUERTO = 0.50       # GCR de referencia de un huerto solar comercial (para LER)

# Rango sensato de GCR para agrivoltaica sobre pradera (dejar pasar luz al pasto)
GCR_MIN = 0.20
GCR_MAX = 0.55


@dataclass
class ResultadoAgrivoltaico:
    area_terreno_m2: float
    gcr: float
    kwp: float
    area_modulo_m2: float
    transmitancia_pasto: float     # fracción de luz que llega al pasto (0-1)
    pasto_relativo: float          # rendimiento de pasto vs campo abierto (0-1)
    energia_relativa: float        # energía vs huerto solar de referencia
    ler: float                     # Land Equivalent Ratio
    energia_anual_kwh: float       # producción FV anual del sistema


def kwp_desde_terreno(area_terreno_m2: float, gcr: float,
                      eta: float = ETA_MODULO_KWP_M2) -> float:
    """kWp instalables en un terreno dado un GCR."""
    _validar(area_terreno_m2, gcr)
    return gcr * area_terreno_m2 * eta


def area_terreno_desde_kwp(kwp: float, gcr: float,
                           eta: float = ETA_MODULO_KWP_M2) -> float:
    """Terreno (m2) necesario para `kwp` a un GCR dado. Inverso de kwp_desde_terreno.

    Para autoconsumo de granja el sistema se dimensiona por POTENCIA (consumo), y el
    terreno ocupado es un PARCHE pequeño de prado, no una hectárea entera.
    """
    if kwp <= 0:
        raise ValueError("kwp debe ser > 0")
    if not (GCR_MIN <= gcr <= GCR_MAX):
        raise ValueError(f"gcr fuera de rango [{GCR_MIN}, {GCR_MAX}]: {gcr}")
    return kwp / (eta * gcr)


def transmitancia_pasto(gcr: float) -> float:
    """Fracción de luz (PAR) que llega al pasto. Primer orden: 1 - GCR."""
    _validar(1.0, gcr)
    return 1.0 - gcr


def land_equivalent_ratio(gcr: float, gcr_ref: float = GCR_REF_HUERTO) -> float:
    """LER = pasto_relativo + energia_relativa. >1 => el doble uso gana terreno."""
    pasto_rel = transmitancia_pasto(gcr)
    energia_rel = min(gcr / gcr_ref, 1.0)
    return pasto_rel + energia_rel


def evaluar(area_terreno_m2: float, gcr: float = 0.35,
            ubic: Ubicacion | None = None) -> ResultadoAgrivoltaico:
    """Evalúa el sistema agrivoltaico completo para un terreno y GCR.

    >>> r = evaluar(10_000, gcr=0.35)   # 1 ha
    >>> r.kwp > 0 and 0 < r.transmitancia_pasto < 1 and r.ler > 1
    True
    """
    _validar(area_terreno_m2, gcr)
    ubic = ubic or ubicacion_asturias_central()
    area_modulo = gcr * area_terreno_m2
    kwp = area_modulo * ETA_MODULO_KWP_M2
    transm = transmitancia_pasto(gcr)
    energia_rel = min(gcr / GCR_REF_HUERTO, 1.0)
    ler = transm + energia_rel
    prod = produccion_fv(kwp, ubic)
    return ResultadoAgrivoltaico(
        area_terreno_m2=area_terreno_m2,
        gcr=gcr,
        kwp=kwp,
        area_modulo_m2=area_modulo,
        transmitancia_pasto=transm,
        pasto_relativo=transm,          # conservador (ver docstring del módulo)
        energia_relativa=energia_rel,
        ler=ler,
        energia_anual_kwh=prod.energia_anual_kwh,
    )


def evaluar_por_potencia(kwp: float, gcr: float = 0.35,
                         ubic: Ubicacion | None = None) -> ResultadoAgrivoltaico:
    """Evalúa dimensionando por POTENCIA (autoconsumo granja). Deriva el terreno.

    >>> r = evaluar_por_potencia(17, gcr=0.35)
    >>> r.area_terreno_m2 < 300 and r.ler > 1   # parche pequeño, doble uso gana
    True
    """
    area = area_terreno_desde_kwp(kwp, gcr)
    return evaluar(area, gcr, ubic)


def _validar(area: float, gcr: float) -> None:
    if area <= 0:
        raise ValueError("area_terreno_m2 debe ser > 0")
    if not (GCR_MIN <= gcr <= GCR_MAX):
        raise ValueError(f"gcr fuera de rango agrivoltaico [{GCR_MIN}, {GCR_MAX}]: {gcr}")
