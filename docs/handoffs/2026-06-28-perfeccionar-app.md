---
type: handoff
status: active
tags: [agrivoltaica, app, streamlit, ui, legal, benchmark, handoff]
created: 2026-06-28
related: [../../PROJECT.md, ../BUILD-LOG.md, ../2026-06-28-idea-proyecto-impacto.md]
---

# Handoff — perfeccionar la app agrivoltaica

## Goal de la próxima sesión

Trabajar **en `/loop`** hasta **perfeccionar la aplicación** (Streamlit) de
`~/AIOS/projects/agrivoltaica-asturias/`:

1. **Más amigable y profesional** — UI/UX a nivel producto, no demo.
2. **Lectura de decretos y leyes** — que la app incorpore/consulte el marco legal real
   (RD agrovoltaica/PAC, ayudas a modernización de explotaciones para jóvenes ganaderos,
   normativa de autoconsumo, PVPC) con fuentes citadas, no de memoria.
3. **Benchmark en internet** — buscar apps/calculadoras similares (interfaz + lo que
   tienen "detrás": modelo, datos, features, flujo) y subir el listón a partir de ellas.

## State of play

- **App YA funciona y está completa** — núcleo de cálculo en `app/core/` (7 módulos:
  `solar.py`, `agrivoltaic.py`, `perfil.py`, `economics.py`, `confort.py`, `impacto.py`,
  `informe.py`), UI en `app/ui/app.py`, entry `streamlit_app.py`. **47/47 tests verde**
  (`python -m pytest -q`, hay `.venv`). Datos PVGIS reales por concejo. Licencia 0 €.
- Arquitectura, decisiones y cifras: NO duplicar — ver `PROJECT.md` + `docs/BUILD-LOG.md`.
- Lanzar local: `cd ~/AIOS/projects/agrivoltaica-asturias && source .venv/bin/activate &&
  streamlit run streamlit_app.py` (histórico en :8521).
- **Vídeos del proyecto ya hechos** (no es el foco ahora, pero contexto de marca/estética):
  `video/` (Remotion). El vídeo de estructura usa estilo hand-drawn Excalidraw/Nate Herk —
  ver `video/README.md`. Decidir si la app adopta esa identidad visual o mantiene Streamlit
  limpio (ver Open decisions).
- **Caveat legal heredado (importante):** los criterios técnicos de la agrovoltaica para
  la PAC en España están **"por concretar"** (desde oct-2025). El proyecto trata las ayudas
  como *upside, no cimiento* — mantener esa disciplina; las leyes se leen y citan, pero la
  viabilidad no debe depender de norma pendiente. Verificar TODA cita legal EN LA FUENTE
  (BOE/EUR-Lex), no de memoria.

## Open decisions (las decide el próximo agente / Pablo)

1. **Cómo surfacear el marco legal en la app** — ¿pestaña "Marco legal / ayudas" con
   resumen + enlaces a BOE? ¿Panel de fuentes? ¿Tooltip por cifra que dependa de norma?
   ¿Parser de PDFs de decretos (pdftotext) para extraer importes/porcentajes de ayuda?
2. **Qué competidores benchmarkear** — candidatos: PVGIS, Global Solar Atlas, Otovo,
   EnergySage, SamSolar, calculadoras de autoconsumo ES. Sacar de cada una: features, flujo
   de entrada, cómo muestran resultados, qué datos usan.
3. **Identidad visual de la app** — ¿alinear con la estética hand-drawn de los vídeos, o
   UI profesional limpia (PowerBI/Fiori)? Pablo valoró "preciso, visual, accesible
   ancianos+jóvenes" — accesibilidad es requisito DURO (texto grande, español llano).
4. **Deploy** — ¿Streamlit Community Cloud 1-click para que el jurado lo abra? (cloud-ready
   ya verificado históricamente).

## Skills to use

- **`solar-fotovoltaica`** + **`pv-valuation`** — dominio FV/económico (validar modelo, LCOE).
- **`impeccable`** / **`ui-ux-pro-max`** / **`taste`** — rediseño UI/UX profesional.
- **`investigador`** + `firecrawl_search` + **`watch`** + **`browser`** — buscar/inspeccionar
  apps competidoras (UI y "lo de detrás").
- **`redactor-tecnico`** + **`humanizer`** — redactar el marco legal en lenguaje claro.
- **`browser`** (CDP) — verificar la app headless tras cada cambio (Playwright/Chrome).
- **`advisor`** — antes de comprometer enfoque y antes de declarar done (red-team las cifras
  y las citas legales; histórico: cazó "de-memoria ≠ fuente" y bugs de half-fix).
- **`loop`** — el modo de trabajo pedido (dynamic, autopautado).

## Artifacts (referencias, NO duplicar)

- Proyecto: `~/AIOS/projects/agrivoltaica-asturias/` (git propio).
- Estado/decisiones: `PROJECT.md`, `docs/BUILD-LOG.md`.
- Entregable beca + cifras citadas: `docs/2026-06-28-idea-proyecto-impacto.md`.
- Bases de la convocatoria: `docs/2026-06-28-convocatoria-bases.md`.
- Código: `app/core/*.py`, `app/ui/app.py`, `streamlit_app.py`, `tests/`.
- Vídeos/estética: `video/README.md` + skill `~/.claude/skills/video-animado/`.
- Memoria viva del proyecto: `project-agrivoltaica-asturias` (auto-memory).
- Registro: `~/AIOS/registry/projects.md`.

## Notas de arranque

- Empezar por leer `PROJECT.md` + `docs/BUILD-LOG.md` (no re-derivar lo hecho).
- Correr los 47 tests antes de tocar para tener línea base.
- Reuse-first: el cálculo es correcto y testeado — extender, no reescribir.
- Pablo: caveman mode; pide evidencia, no sycophancy; commit solo cuando lo pida.
