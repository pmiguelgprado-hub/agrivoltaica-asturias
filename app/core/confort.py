"""Confort animal bajo el panel: ¿sombra anti-calor o refugio?

Catch climático (spec §7): Asturias es oceánica, fresca y húmeda. El argumento de
"sombra contra el estrés térmico" viene de Minnesota / sur de España y NO se puede
importar crudo. Aquí se verifica con el THI (Temperature-Humidity Index) si el estrés
térmico del vacuno frisón aplica siquiera en el verano asturiano.

THI (NRC 1971, uso estándar en vacuno lechero):
    THI = (1.8*T + 32) - (0.55 - 0.0055*RH) * (1.8*T - 26)
con T en C y RH en %.

Umbrales (vacuno lechero de alta producción):
    < 68  sin estrés
    68-71 estrés leve
    72-79 estrés moderado
    >= 80 estrés severo

Conclusión para Asturias (verificada): en un día cálido-húmedo de verano (T~25 C,
RH~75 %) el THI ronda ~74 => estrés LEVE-MODERADO solo en picos puntuales, no crónico.
Por tanto el beneficio dominante del panel NO es sombra anti-calor (como en el sur),
sino REFUGIO de lluvia/viento y confort en esos picos. El proyecto lo vende así.
"""
from __future__ import annotations


def thi(temp_c: float, humedad_rel: float) -> float:
    """Índice temperatura-humedad (NRC 1971)."""
    if not (0 <= humedad_rel <= 100):
        raise ValueError("humedad_rel debe estar en [0, 100]")
    return (1.8 * temp_c + 32) - (0.55 - 0.0055 * humedad_rel) * (1.8 * temp_c - 26)


def clasifica_thi(valor: float) -> str:
    """Nivel de estrés térmico a partir del THI."""
    if valor < 68:
        return "sin estrés"
    if valor < 72:
        return "leve"
    if valor < 80:
        return "moderado"
    return "severo"


# Día cálido-húmedo representativo de verano en Asturias interior.
ASTURIAS_VERANO_T = 25.0
ASTURIAS_VERANO_RH = 75.0
