"""Núcleo de cálculo solar fotovoltaico (modelo físico mensual).

Modelo: irradiación en plano (POA) -> corrección de temperatura de célula por el
modelo NOCT con coeficiente gamma -> pérdidas de sistema -> energía AC.

    E_ac = kWp * SUM_m [ H_poa,m * (1 - gamma*(Tcell,m - 25)) ] * k_system
    Tcell,m = Tamb,m + (NOCT - 20)/800 * G_ref

Referencias del modelo:
- Definición de kWp a STC (1000 W/m2, 25 C, AM1.5) -> E_dc_ideal = kWp * H_poa.
- Modelo NOCT para temperatura de célula (norma IEC 61215 / práctica habitual PVsyst).
- gamma_pmax típico de silicio cristalino ~ -0,0035 a -0,0040 /K.

PROVENANCIA DE DATOS (It-1): los perfiles mensuales de POA y Tamb son PROVISIONALES,
representativos de la Asturias central, a la espera de verificación con PVGIS para la
ubicación exacta (tarea It-2). Marcados con PROVISIONAL para no anclar números sin fuente.
"""
from __future__ import annotations

from dataclasses import dataclass, field

MESES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun",
         "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

# --- Constantes físicas del modelo (silicio cristalino moderno) ---
GAMMA_PMAX = -0.0037     # coef. de temperatura de potencia [1/K]
NOCT = 44.0              # Nominal Operating Cell Temperature [C]
G_REF = 500.0           # irradiancia efectiva media diurna mensual [W/m2] (modelo NOCT)
T_STC = 25.0            # temperatura de célula a STC [C]

# Pérdidas de sistema (factores multiplicativos, sin la térmica que es mensual).
# Categorías estándar de PVsyst. Valores ajustados a un clima OCEÁNICO NUBOSO
# (Asturias): la baja irradiancia/espectral y angular pesan más que en el sur seco.
# Producto -> k_system ~ 0,81  =>  PR global ~ 0,80 (coherente con Sreca: PR 76,5 %).
PERDIDAS_SISTEMA = {
    "suciedad_soiling": 0.97,                  # ensuciamiento
    "mismatch_modulos": 0.98,                  # dispersión entre módulos
    "perdidas_ohmicas_dc_ac": 0.98,            # cableado
    "eficiencia_inversor": 0.97,               # eficiencia europea media
    "baja_irradiancia_espectral": 0.96,        # clima nuboso: mucha luz difusa/baja
    "angular_iam": 0.97,                       # incidencia angular (IAM)
    "calidad_lid_degradacion_inicial": 0.98,   # calidad módulo + LID año 1
    "disponibilidad": 0.98,                    # availability
}


def k_system() -> float:
    """Producto de pérdidas de sistema (sin la térmica, que es mensual)."""
    k = 1.0
    for v in PERDIDAS_SISTEMA.values():
        k *= v
    return k


# --- Recurso solar REAL Asturias (Tineo, concejo ganadero SO) ---
# Fuente: PVGIS v5.2 (JRC, base SARAH3), lat 43,34 / lon -6,41, plano fijo óptimo
# (slope 37 deg, azimut sur). H(i)_m = irradiación mensual en plano [kWh/m2].
# Verificado 2026-06-27 vía API PVcalc. Sustituye los datos PROVISIONALES de It-1.
POA_TINEO_PVGIS = [80.5, 96.8, 132.7, 142.0, 154.3, 149.5,
                   167.1, 172.5, 151.2, 125.4, 83.4, 83.9]   # 1539,3 kWh/m2/año
# Energía PVGIS para 1 kWp con 14 % de pérdidas de sistema (referencia de validación).
PVGIS_YIELD_REF = 1219.5  # kWh/kWp/año

# Temperatura ambiente media mensual [C]. Fuente: AEMET, normales 1991-2020
# (Oviedo, estación de referencia; Tineo a mayor altitud es algo más fresco -> conservador
# para el derating térmico). El efecto térmico es de 2º orden frente a la POA.
TAMB_ASTURIAS = [7.6, 8.1, 9.9, 10.9, 13.7, 16.5,
                 18.5, 18.8, 16.8, 13.6, 10.0, 8.2]


@dataclass
class Ubicacion:
    """Recurso solar mensual de una ubicación."""
    nombre: str
    poa_mensual: list[float]      # kWh/m2/mes en plano
    tamb_mensual: list[float]     # C, media mensual
    provisional: bool = True

    def __post_init__(self) -> None:
        if len(self.poa_mensual) != 12 or len(self.tamb_mensual) != 12:
            raise ValueError("poa_mensual y tamb_mensual deben tener 12 valores")

    @property
    def poa_anual(self) -> float:
        return sum(self.poa_mensual)


def ubicacion_asturias_central() -> Ubicacion:
    """Tineo (Asturias) con recurso solar real de PVGIS v5.2."""
    return Ubicacion(
        nombre="Tineo, Asturias (PVGIS v5.2)",
        poa_mensual=list(POA_TINEO_PVGIS),
        tamb_mensual=list(TAMB_ASTURIAS),
        provisional=False,
    )


@dataclass
class ResultadoSolar:
    energia_anual_kwh: float
    energia_mensual_kwh: list[float]
    yield_kwh_kwp: float            # productividad específica
    performance_ratio: float        # PR global
    kwp: float


def t_celula(tamb: float) -> float:
    """Temperatura de célula por modelo NOCT a irradiancia de referencia."""
    return tamb + (NOCT - 20.0) / 800.0 * G_REF


def factor_temperatura(tamb: float) -> float:
    """Factor de derating térmico mensual (<=1 cuando Tcell>25)."""
    return 1.0 + GAMMA_PMAX * (t_celula(tamb) - T_STC)


def produccion_fv(kwp: float, ubic: Ubicacion | None = None) -> ResultadoSolar:
    """Producción FV anual de un sistema de `kwp` en una ubicación.

    >>> r = produccion_fv(1.0)
    >>> 1000 < r.yield_kwh_kwp < 1250   # rango Asturias plausible
    True
    """
    if kwp <= 0:
        raise ValueError("kwp debe ser > 0")
    ubic = ubic or ubicacion_asturias_central()
    ks = k_system()
    mensual: list[float] = []
    for poa_m, tamb_m in zip(ubic.poa_mensual, ubic.tamb_mensual):
        e_m = kwp * poa_m * factor_temperatura(tamb_m) * ks
        mensual.append(e_m)
    anual = sum(mensual)
    yield_esp = anual / kwp
    pr = yield_esp / ubic.poa_anual   # PR = yield / irradiación en plano
    return ResultadoSolar(
        energia_anual_kwh=anual,
        energia_mensual_kwh=mensual,
        yield_kwh_kwp=yield_esp,
        performance_ratio=pr,
        kwp=kwp,
    )
