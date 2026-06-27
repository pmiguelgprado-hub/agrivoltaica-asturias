---
type: project
status: active
tags: [agrivoltaica, fotovoltaica, ganaderia, asturias, beca, caja-rural, energia]
created: 2026-06-27
updated: 2026-06-27
related: [docs/2026-06-27-design-spec.md]
---

# AGRIVOLTAICA GANADERA ASTURIANA — PROJECT

Documento de proyecto. El código vive en este repositorio (git propio).

## Qué es

Herramienta-calculadora **precisa, visual y accesible** (ancianos + jóvenes) que estima,
para una granja ganadera de la Asturias rural, la producción fotovoltaica, el autoconsumo/
ahorro y el **doble uso del suelo** (pasto + PV elevada = agrivoltaica). Genera la memoria
base para la **convocatoria de innovación (máster) de la Fundación Caja Rural de Asturias**
(cierre 31-jul-2026). Stack coste-licencia 0 €.

## Por qué (vs Sreca)

Sreca (CEL rural PV) cansó por poco innovador + riesgo legal + scope. Aquí el foco es el
**doble uso del suelo agrícola-energético**, ángulo de frontera en la cornisa cantábrica
húmeda (la agrivoltaica española es sur seco). Independiente de EDP. Valor anclado en
ingeniería + economía, no en norma pendiente.

## Estado

| | |
|---|---|
| Fase | It-1 — spec aprobada (supuesto A) + scaffold + slice en construcción |
| Hecho | Research inicial (casos ganado-PV, elegibilidad PAC ES, calculadoras ref); spec de diseño |
| Siguiente | Núcleo solar testeable → modelo agrivoltaico → UI accesible → memoria beca |
| Dinero/despliegue | N/A (proyecto de estudiante, multi-sesión, loop autopautado) |

## Decisiones clave (2026-06-27)

1. **Idea = A** agrivoltaica ganadera (supuesto explícito, barato de revertir — ver spec §0).
2. **Geometría v1 = pastoreo bajo panel elevado** (no entre-hileras). Spec §6.
3. **Beneficio ganadero = refugio lluvia/viento** (clima oceánico), NO sombra anti-calor; THI a verificar. Spec §7.
4. **PAC = upside, no cimiento** (riesgo regulatorio tipo-Sreca). Spec §5.
5. **Accesibilidad = requisito duro verificable** (texto grande, español llano, imprimible). Spec §8.

## Docs

- Spec de diseño (iter-1): `docs/2026-06-27-design-spec.md`
- Build-log / estado vivo: `docs/BUILD-LOG.md`
