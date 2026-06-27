"""Genera un informe imprimible (HTML autocontenido) del escenario calculado.

Sirve de memoria base para la beca y de hoja que el ganadero puede imprimir/compartir.
Función pura: recibe los resultados ya calculados y devuelve HTML. Sin dependencias de UI.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass
class DatosInforme:
    vacas: int
    kwp: float
    gcr: float
    ubicacion: str
    # solar / energía
    energia_anual_kwh: float
    yield_kwh_kwp: float
    # agrivoltaico
    area_m2: float
    luz_pasto_pct: float
    ler: float
    # economía
    consumo_anual_kwh: float
    autoconsumo_pct: float
    cobertura_pct: float
    ahorro_anual_eur: float
    capex_eur: float
    payback_anios: float
    payback_ayuda_anios: float
    lcoe_eur_kwh: float
    # confort
    thi: float
    thi_nivel: str


def _es(n: float, dec: int = 0) -> str:
    """Formato número español (miles con punto, decimales con coma)."""
    s = f"{n:,.{dec}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def informe_html(d: DatosInforme) -> str:
    """Construye el HTML imprimible del informe."""
    hoy = date.today().isoformat()
    return f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<title>Informe agrivoltaica — {d.ubicacion}</title>
<style>
 @media print {{ .noprint {{ display:none }} }}
 body {{ font-family: Georgia, serif; font-size: 15pt; color:#222; max-width: 820px;
        margin: 2rem auto; line-height: 1.5; padding: 0 1rem; }}
 h1 {{ font-size: 24pt; color:#3d5220; margin-bottom:0 }}
 h2 {{ font-size: 17pt; color:#5a6b3b; border-bottom:2px solid #cdd9b0; padding-bottom:.2rem }}
 .kpi {{ display:inline-block; min-width: 30%; margin:.4rem 1rem .4rem 0 }}
 .kpi b {{ font-size: 20pt; color:#3d5220; display:block }}
 .src {{ font-size: 11pt; color:#666 }}
</style></head><body>
<h1>🐄☀️ Sol y pasto en la misma finca</h1>
<p class="src">Estudio de agrivoltaica ganadera · {d.ubicacion} · {hoy}</p>

<h2>La granja</h2>
<p>{d.vacas} vacas · sistema fotovoltaico de <b>{_es(d.kwp)} kWp</b> elevado sobre el prado.</p>

<h2>Lo que produce y ahorra</h2>
<div class="kpi">Energía al año<b>{_es(d.energia_anual_kwh)} kWh</b></div>
<div class="kpi">Cubre tu gasto<b>{_es(d.cobertura_pct)} %</b></div>
<div class="kpi">Ahorro anual<b>{_es(d.ahorro_anual_eur)} €</b></div>
<div class="kpi">Inversión<b>{_es(d.capex_eur)} €</b></div>
<div class="kpi">Se paga en<b>{_es(d.payback_ayuda_anios,1)} años*</b></div>
<div class="kpi">Coste de tu kWh<b>{_es(d.lcoe_eur_kwh,3)} €</b></div>
<p class="src">*Con ayuda a fondo perdido. Sin ninguna ayuda: {_es(d.payback_anios,1)} años.
 Autoconsumo {_es(d.autoconsumo_pct)} % (calculado hora a hora). Red ~0,18 €/kWh.</p>

<h2>Y sigues teniendo pasto</h2>
<div class="kpi">Prado ocupado<b>{_es(d.area_m2)} m²</b></div>
<div class="kpi">Luz al pasto<b>{_es(d.luz_pasto_pct)} %</b></div>
<div class="kpi">Aprovechas la tierra<b>{_es(d.ler,2)}×</b></div>
<p>Solo se ocupa una esquina del prado: el resto sigue dando pasto y, bajo las placas
 elevadas, el ganado se resguarda de la lluvia y el viento. La ventaja no es optimizar el
 suelo sino un ingreso extra y refugio sin perder pradera. En la franja ocupada, el índice
 de doble uso (LER) es {_es(d.ler,2)}× (métrica técnica, no clave del proyecto).</p>

<h2>El ganado, a gusto</h2>
<p>En el verano asturiano el índice de estrés térmico (THI) ronda {_es(d.thi)}
 (estrés {d.thi_nivel}, no severo). El beneficio principal de la placa elevada aquí es
 el <b>refugio</b> de lluvia y viento, no la sombra contra el calor.</p>

<p class="src">Fuentes: recurso solar de PVGIS v5.2 · consumo 516 kWh/vaca·año (estudio
 Castilla y León) · CAPEX FV 800-1.400 €/kWp (mercado ES 2026) · THI NRC 1971.
 Modelo de pérdidas coherente con PVGIS. El sobrecoste de la estructura elevada es una
 asunción ajustable, no un dato.</p>
</body></html>"""
