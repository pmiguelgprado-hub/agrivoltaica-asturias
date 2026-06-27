"""Núcleo económico: ahorro, payback y LCOE para la granja.

Valor anclado en INGENIERÍA + ECONOMÍA (no en ayudas pendientes). La línea PAC se
calcula aparte como UPSIDE, nunca como cimiento del payback (lección Sreca, spec §5).

Fuentes de los datos (ES 2026):
- Consumo eléctrico granja vacuno lechero: 516 kWh/vaca·año (estudio Castilla y León,
  scielo S0004-05922013000300013; ~51 kWh por 1.000 kg de leche).
- CAPEX FV autoconsumo: 800-1.400 €/kWp (Cambio Energético 2026); base media usada 1.000.
- Precio compra electricidad agraria/PVPC ~0,18 €/kWh; excedente compensado ~0,06 €/kWh.

ASUNCIÓN (no citada, expuesta como sensibilidad en la UI): el sobrecoste de la estructura
agrivoltaica ELEVADA a altura de vacuno (pérgola alta ~4 m, cargas de viento, protección
frente al ganado) NO está tomado de una fuente. La literatura sitúa el premium entre +50 %
y +100 % sobre ground-mount; aquí el default es +60 % y el usuario lo ajusta con un control
de sensibilidad. Es el número que más afecta al payback -> se trata como variable, no dato.
"""
from __future__ import annotations

from dataclasses import dataclass

# --- Defaults (editables en la UI) ---
KWH_POR_VACA_ANIO = 516.0       # consumo eléctrico medio por vaca productora (citado)
CAPEX_BASE_KWP = 1000.0         # €/kWp instalación FV estándar (citado)
PREMIUM_AGRIVOLTAICO = 1.60     # ASUNCIÓN: sobrecoste estructura elevada (rango 1,3-2,0)
OPEX_FRAC_CAPEX = 0.015         # O&M anual como fracción del CAPEX
PRECIO_COMPRA = 0.18            # €/kWh
PRECIO_EXCEDENTE = 0.06         # €/kWh
VIDA_UTIL_ANIOS = 25
TASA_DESCUENTO = 0.04


@dataclass
class ResultadoEconomico:
    consumo_anual_kwh: float
    energia_anual_kwh: float
    fraccion_autoconsumo: float     # fracción de la GENERACIÓN autoconsumida
    autoconsumida_kwh: float
    excedente_kwh: float
    cobertura_demanda: float        # autoconsumida / consumo
    capex_eur: float
    opex_anual_eur: float
    ahorro_anual_eur: float
    payback_anios: float            # simple, sin ayudas
    lcoe_eur_kwh: float
    # Upside (separado): con ayuda a fondo perdido
    payback_con_ayuda_anios: float
    ayuda_eur: float


def consumo_granja(n_vacas: float, kwh_vaca: float = KWH_POR_VACA_ANIO) -> float:
    if n_vacas < 0:
        raise ValueError("n_vacas debe ser >= 0")
    return n_vacas * kwh_vaca


def fraccion_autoconsumo(generacion_kwh: float, consumo_kwh: float) -> float:
    """Fracción de la generación que se autoconsume (heurística sin batería).

    Decrece al sobredimensionar el FV respecto a la carga. Aproximación documentada
    (a refinar con perfil horario de ordeño en It-3). Acotada a [0,25 ; 0,90].
    """
    if generacion_kwh <= 0 or consumo_kwh <= 0:
        return 0.0
    ratio = generacion_kwh / consumo_kwh
    return max(0.25, min(0.90, 0.95 - 0.45 * ratio))


def capex(kwp: float, base_kwp: float = CAPEX_BASE_KWP,
          premium: float = PREMIUM_AGRIVOLTAICO) -> float:
    if kwp <= 0:
        raise ValueError("kwp debe ser > 0")
    return kwp * base_kwp * premium


def factor_recuperacion_capital(r: float = TASA_DESCUENTO, n: int = VIDA_UTIL_ANIOS) -> float:
    if r == 0:
        return 1.0 / n
    return r * (1 + r) ** n / ((1 + r) ** n - 1)


def lcoe(capex_eur: float, opex_anual_eur: float, energia_anual_kwh: float,
         r: float = TASA_DESCUENTO, n: int = VIDA_UTIL_ANIOS) -> float:
    """Coste nivelado de la energía [€/kWh]."""
    if energia_anual_kwh <= 0:
        raise ValueError("energia_anual_kwh debe ser > 0")
    crf = factor_recuperacion_capital(r, n)
    return (capex_eur * crf + opex_anual_eur) / energia_anual_kwh


def evaluar_economia(kwp: float, energia_anual_kwh: float, n_vacas: float,
                     precio_compra: float = PRECIO_COMPRA,
                     precio_excedente: float = PRECIO_EXCEDENTE,
                     base_kwp: float = CAPEX_BASE_KWP,
                     premium: float = PREMIUM_AGRIVOLTAICO,
                     ayuda_frac: float = 0.0,
                     fraccion_autoconsumo_override: float | None = None) -> ResultadoEconomico:
    """Economía completa. `ayuda_frac` = fracción de CAPEX a fondo perdido (upside).

    `fraccion_autoconsumo_override`: si se pasa (p.ej. de la simulación horaria en
    perfil.simular_autoconsumo), se usa en vez de la heurística.
    """
    consumo = consumo_granja(n_vacas)
    sc = (fraccion_autoconsumo_override if fraccion_autoconsumo_override is not None
          else fraccion_autoconsumo(energia_anual_kwh, consumo))
    autoc = energia_anual_kwh * sc
    exced = energia_anual_kwh * (1 - sc)
    cobertura = (autoc / consumo) if consumo > 0 else 0.0

    cap = capex(kwp, base_kwp, premium)
    opex = cap * OPEX_FRAC_CAPEX
    ahorro = autoc * precio_compra + exced * precio_excedente - opex
    payback = cap / ahorro if ahorro > 0 else float("inf")

    ayuda = cap * max(0.0, min(ayuda_frac, 0.65))   # tope 65 % fondo perdido
    cap_neto = cap - ayuda
    payback_ayuda = cap_neto / ahorro if ahorro > 0 else float("inf")

    return ResultadoEconomico(
        consumo_anual_kwh=consumo,
        energia_anual_kwh=energia_anual_kwh,
        fraccion_autoconsumo=sc,
        autoconsumida_kwh=autoc,
        excedente_kwh=exced,
        cobertura_demanda=cobertura,
        capex_eur=cap,
        opex_anual_eur=opex,
        ahorro_anual_eur=ahorro,
        payback_anios=payback,
        lcoe_eur_kwh=lcoe(cap, opex, energia_anual_kwh),
        payback_con_ayuda_anios=payback_ayuda,
        ayuda_eur=ayuda,
    )
