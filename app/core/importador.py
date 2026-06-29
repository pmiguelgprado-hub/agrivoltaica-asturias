"""Importador de consumo real de la granja (factura / CSV).

Acepta un CSV sencillo con una columna numérica de consumo en kWh y deduce:
  - el consumo anual total (para dimensionar mejor),
  - una curva de carga de 24 h (forma horaria real, para el autoconsumo).

Robusto a separadores (`,` o `;`), a coma decimal española y a una posible cabecera.
Sin dependencias de pandas: parser propio testeable.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ConsumoImportado:
    consumo_anual_kwh: float | None      # None si no se puede deducir un anual fiable
    perfil_24h: list[float] | None       # forma horaria (24 valores) o None
    n_valores: int
    fuente: str                          # descripción corta de lo detectado


def _a_float(tok: str) -> float | None:
    tok = tok.strip().strip('"').strip()
    if not tok:
        return None
    # coma decimal española -> punto; quita separador de millar
    if "," in tok and "." in tok:
        tok = tok.replace(".", "").replace(",", ".")
    elif "," in tok:
        tok = tok.replace(",", ".")
    try:
        return float(tok)
    except ValueError:
        return None


def _numeros(texto: str) -> list[float]:
    """Extrae la primera columna numérica plausible de un CSV de texto."""
    nums: list[float] = []
    for linea in texto.splitlines():
        if not linea.strip():
            continue
        # separa por ; o , o tabulador o espacios
        sep = ";" if ";" in linea else ("," if linea.count(",") and "\t" not in linea else None)
        celdas = linea.split(sep) if sep else linea.split()
        # el consumo suele ir en la última columna (hora/fecha primero, kWh después)
        ultimo = None
        for celda in celdas:
            v = _a_float(celda)
            if v is not None and v >= 0:
                ultimo = v
        if ultimo is not None:
            nums.append(ultimo)
    return nums


def parse_consumo(texto: str) -> ConsumoImportado:
    """Parsea el contenido de un CSV/exportación de consumo en kWh.

    Heurística por nº de valores:
      - 24            -> curva diaria; anual = suma*365
      - 8760 / 8784   -> horario anual; anual = suma, perfil = media por hora del día
      - 12            -> mensual; anual = suma; sin perfil horario
      - otro (>0)     -> trata la suma como anual; sin perfil horario
    """
    nums = _numeros(texto)
    n = len(nums)
    if n == 0:
        return ConsumoImportado(None, None, 0, "sin datos numéricos")

    if n == 24:
        anual = sum(nums) * 365.0
        return ConsumoImportado(anual, list(nums), n, "curva diaria (24 h)")

    if n in (8760, 8784):
        perfil = [0.0] * 24
        for i, v in enumerate(nums):
            perfil[i % 24] += v
        return ConsumoImportado(sum(nums), perfil, n, "horario anual (8760 h)")

    if n == 12:
        return ConsumoImportado(sum(nums), None, n, "mensual (12 meses)")

    return ConsumoImportado(sum(nums), None, n, f"{n} valores (suma = anual)")
