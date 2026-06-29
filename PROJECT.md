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
| Fase | Respaldo COMPLETO — calculadora + entregables de la beca listos |
| Hecho | Calculadora completa (núcleo solar PVGIS, modelo agrivoltaico, autoconsumo horario, economía, impacto de concejo, informe imprimible), **47 tests verde**; idea de proyecto redactada (≤3.000 palabras); guion del vídeo (2 min); bases oficiales verificadas; **vídeo animado en Remotion** (`video/`) |
| Siguiente (Pablo) | Grabar clip cara-a-cámara → `video/public/pablo.mp4` + render final; confirmar si el formulario admite adjunto/enlace; gate elegibilidad (residencia + matrícula + cuenta Caja Rural); rellenar formulario |
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
- **Entregable beca** (idea de proyecto, ≤3.000 palabras): `docs/2026-06-28-idea-proyecto-impacto.md`
- Guion del vídeo (2 min, Anexo 2): `docs/2026-06-28-guion-video.md`
- Bases oficiales de la convocatoria: `docs/2026-06-28-convocatoria-bases.md`

## Vídeo animado

`video/` — proyecto Remotion que genera el vídeo de 2 min (cabeza parlante + overlays
animados estilo Nate Herk; la app protagoniza el cierre). Ver `video/README.md`.
Pablo graba su clip → `video/public/pablo.mp4`, pone `hasFootage: true` y `npm run render`.
