"""Marco legal y ayudas — datos con fuente oficial.

Disciplina del proyecto (verificada por test):
  - Cada afirmación legal se cita EN FUENTE oficial (BOE / administración), no de memoria.
  - Las ayudas son UPSIDE, no cimiento de la rentabilidad.
  - Los criterios técnicos de la agrivoltaica para la PAC están POR CONCRETAR: el
    RD 916/2025 fija el principio de elegibilidad, no los parámetros (altura, ocupación,
    merma admisible), que se definirán en desarrollo normativo posterior.

Fuentes consultadas (oct-2025):
  - RD 244/2019 (autoconsumo), modificado por RDL 7/2026.
  - RD 916/2025 (modifica art. 9.12 del RD 1048/2022): agrivoltaica elegible PAC.
  - AYUD0518T01 (Principado de Asturias): incorporación de jóvenes ganaderos.
"""
from __future__ import annotations

from dataclasses import dataclass

# Estados posibles de una norma, ordenados de más firme a más incierto.
ESTADOS: dict[str, tuple[str, str]] = {
    "vigente": ("Vigente", "#0f7a47"),          # verde bosque
    "principio": ("Principio aprobado", "#b8860b"),  # oro
    "por_concretar": ("Por concretar", "#a15c00"),   # ámbar oscuro = aviso
}

# Dominios oficiales admitidos como fuente (el test lo verifica).
DOMINIOS_OFICIALES: tuple[str, ...] = (
    "boe.es", "asturias.es", "europa.eu", "miteco.gob.es", "mapa.gob.es",
)


@dataclass(frozen=True)
class ItemLegal:
    tema: str
    resumen: str        # español llano, una idea clara
    estado: str         # clave de ESTADOS
    norma: str          # referencia corta de la norma
    fuente_label: str   # texto del enlace
    fuente_url: str     # URL a la fuente oficial


MARCO_LEGAL: tuple[ItemLegal, ...] = (
    ItemLegal(
        tema="Autoconsumo eléctrico",
        resumen=(
            "Puedes producir tu propia electricidad y verter el excedente a la red con "
            "compensación simplificada. Es el marco que hace rentable poner placas en la "
            "granja, con o sin ayudas."
        ),
        estado="vigente",
        norma="RD 244/2019, modificado por el RDL 7/2026",
        fuente_label="BOE · Real Decreto 244/2019",
        fuente_url="https://www.boe.es/buscar/act.php?id=BOE-A-2019-5089",
    ),
    ItemLegal(
        tema="Agrivoltaica elegible para la PAC",
        resumen=(
            "Desde octubre de 2025, una finca con placas elevadas mantiene el 100% de su "
            "superficie elegible para las ayudas de la PAC —en lugar de descontarse como "
            "suelo improductivo—, siempre que la actividad agraria siga siendo la principal."
        ),
        estado="principio",
        norma="RD 916/2025 (modifica el art. 9.12 del RD 1048/2022)",
        fuente_label="BOE · Real Decreto 916/2025",
        fuente_url="https://www.boe.es/buscar/doc.php?id=BOE-A-2025-20583",
    ),
    ItemLegal(
        tema="Criterios técnicos de la agrivoltaica",
        resumen=(
            "Los parámetros concretos (altura de las placas, ocupación máxima del suelo, "
            "merma de cosecha o pasto admisible) todavía no están publicados: se definirán "
            "en una norma de desarrollo posterior. Por eso este proyecto trata la ayuda "
            "como un extra, no como la base de la rentabilidad."
        ),
        estado="por_concretar",
        norma="Desarrollo pendiente del RD 916/2025",
        fuente_label="BOE · Real Decreto 916/2025",
        fuente_url="https://www.boe.es/buscar/doc.php?id=BOE-A-2025-20583",
    ),
    ItemLegal(
        tema="Ayuda a la inversión: modernización de la explotación (Asturias)",
        resumen=(
            "Es la ayuda que respalda el control de «ayuda a fondo perdido» de la calculadora: "
            "subvenciona hasta el 65% de la inversión en planes de mejora (hasta el 80% si la "
            "mejora es ambiental), con prioridad para jóvenes. La instalación agrivoltaica entra "
            "como inversión de modernización de la granja."
        ),
        estado="vigente",
        norma="Modernización de explotaciones · PEPAC 2023-2027 / Reg. (UE) 2021/2115",
        fuente_label="Principado de Asturias · bases de modernización",
        fuente_url=(
            "https://actualidad.asturias.es/-/medio-rural-publica-las-bases-reguladoras-de-las-"
            "ayudas-para-la-modernizaci%C3%B3n-la-mejora-ambiental-y-la-prevenci%C3%B3n-de-da"
            "%C3%B1os-en-las-explotaciones-agrarias"
        ),
    ),
    ItemLegal(
        tema="Prima de incorporación de jóvenes (Asturias)",
        resumen=(
            "Aparte de la inversión, hay una prima de 25.000 a 50.000 € por incorporarse por "
            "primera vez a una explotación (con incrementos por ganadería láctea, extensiva, "
            "titular mujer o ecológica). Es un pago único distinto del porcentaje de inversión: "
            "compatible con la ayuda de modernización, no la sustituye."
        ),
        estado="vigente",
        norma="AYUD0518T01 · PEPAC 2023-2027 / Reg. (UE) 2021/2115",
        fuente_label="Principado de Asturias · AYUD0518T01",
        fuente_url="https://miprincipado.asturias.es/-/dboid-6269000216071719207573",
    ),
)
