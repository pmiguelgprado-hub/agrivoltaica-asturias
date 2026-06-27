---
type: spec
status: draft
tags: [agrivoltaica, fotovoltaica, ganaderia, asturias, beca, caja-rural]
created: 2026-06-27
updated: 2026-06-27
related: [PROJECT.md]
---

# Agrivoltaica ganadera asturiana — Spec de diseño (iteración 1)

> **⚠️ SUPUESTO DE PARTIDA (corregir en 1 vistazo si está mal):**
> La idea elegida es **A — agrivoltaica ganadera asturiana**: una **herramienta-calculadora**
> que estima energía + ahorro + dual-uso del suelo (pasto + PV) para una granja-tipo de
> Asturias rural. Si querías otra de las opciones (B atlas concejo / C kit PV+aerotermia),
> dilo y reescribo. Todo lo de abajo cuelga de este supuesto.

## 1. Qué es (una frase)

Calculadora web **precisa, visual y accesible** que, para una parcela ganadera asturiana,
estima producción FV, autoconsumo/ahorro y compatibilidad con el pasto bajo un sistema
**agrivoltaico** (paneles elevados sobre pradera), y genera una **memoria de proyecto**
para la convocatoria de innovación de la Fundación Caja Rural de Asturias (cierre 31-jul-2026).

## 2. Por qué (encaje y novedad)

- **Caja Rural = banco agrario-rural** → agricultura + energía + innovación + Asturias rural
  es el tema más alineado con su misión. Ventaja de jurado.
- **Novedad real:** la agrivoltaica española documentada es **sur seco sobre cultivo**.
  Vacuno + pradera + clima **oceánico húmedo** (cornisa cantábrica) = frontera poco explorada.
- **Diferencia de Sreca** (que fue PV-rural-Streamlit y le cansó): el foreground aquí es el
  **doble uso del suelo** (energía + ganadería en la misma parcela), no el reparto de una CEL.

## 3. Tensión simple ↔ preciso (resuelta)

| Eje | Decisión |
|---|---|
| **Uso** | SIMPLE. Pocos inputs, defaults sensatos, sin jerga. Ancianos y jóvenes. |
| **Scope** | ESTRECHO. 1 configuración en v1, 1 granja-tipo, 0 hardware, 0 diseño de planta. |
| **Núcleo ingeniería** | PRECISO + CITADO. Cada número con fuente y fórmula trazable. |

**Regla anti-rabbit-hole:** la investigación se acota a lo que (a) ancla los números y
(b) ancla la UX. Cuando ambos estén anclados → construir, no seguir leyendo.

## 4. Alcance IN / OUT

**IN (v1):**
- 1 configuración geométrica fija (ver §6).
- Producción FV anual horaria-agregada desde recurso solar (PVGIS/POA→NOCT→γ, reutiliza
  modelo físico validado de Sreca: yield ~1.100–1.150 kWh/kWp en Asturias).
- Fracción de autoconsumo contra **perfil de carga de granja láctea** (ordeño, refrigeración
  de leche, limpieza, iluminación).
- Balance dual-uso: GCR / altura / separación de hileras → **luz que llega al pasto** vs
  densidad energética (trade-off explícito, no oculto).
- Economía: CAPEX/OPEX con precios ES 2026 citados → ahorro anual, payback, LCOE.
- Salida: dashboard + **informe imprimible** (memoria de proyecto).

**OUT (v1, explícito):**
- Diseño estructural/mecánico detallado de la pérgola.
- Optimización multiobjetivo, ML, baterías.
- Tramitación legal / permitting real.
- Dependencia de ayudas PAC como cimiento (ver §5).
- Múltiples configuraciones (v2).

## 5. Riesgo regulatorio (lección Sreca)

La agrovoltaica es **elegible PAC en España desde oct-2025**, pero los criterios técnicos
(cobertura, altura, densidad máx.) están **"se definirán posteriormente"** → mismo olor a
norma pendiente que tumbó Sreca. **Decisión:** el valor de la herramienta se ancla en
**energía + ahorro de autoconsumo + doble uso del suelo**, que se sostienen sin PAC.
La ayuda PAC se muestra como **línea de upside**, nunca como cimiento del payback.

## 6. Fork de geometría (FIJADO para v1)

Dos arquetipos reales:
- **(a) Pastoreo BAJO panel elevado** — pérgola alta (≥2,1–4 m), estructura cara y exigente
  (cargas de viento), pero deja la parcela íntegra para pasto + da **refugio**.
- **(b) Ground-mount, pastoreo ENTRE hileras** — barato, pero el "solar grazing" real es
  casi siempre **ovino**; el vacuno daña panel bajo y resta pasto útil.

**v1 fija (a)** — pastoreo bajo panel elevado. Razón: es la configuración que justifica
"agrivoltaica **ganadera** (vacuno)" en minifundio asturiano y la que diferencia de un
huerto solar normal. Se documenta el trade económico con honestidad (puede NO amortizar sin
ayuda — y eso es un resultado válido y útil, como el titular honesto de Sreca). v2 añade (b).

## 7. Catch climático (verificar antes de codificar el beneficio ganadero)

Asturias = **oceánica, fresca, húmeda**. El beneficio dominante NO es sombra anti-calor
(eso es Minnesota / sur de España). Es **refugio de lluvia/viento** y protección del pasto.
**Tarea de build:** verificar si el estrés térmico (THI) del vacuno frisón aplica siquiera
en verano asturiano antes de usar ese argumento. Si no aplica, el beneficio se vende como
refugio + confort + protección de pradera, no como anti-calor.

## 8. Accesibilidad (REQUISITO DURO, se verifica)

- Texto grande, alto contraste, **español llano**, mínima jerga.
- Pocos inputs (deslizadores/desplegables con defaults), nada de configuración obligatoria.
- Resultado entendible de un vistazo (titulares en €/año y kWh, no solo gráficos).
- **Salida imprimible** (un anciano la imprime; un joven la comparte).
- Se verifica headless (Playwright/Chrome) como en Sreca.

## 9. Núcleo de ingeniería a computar (citado en la propia herramienta)

1. Recurso solar de la ubicación real (PVGIS) → POA.
2. Producción FV: POA → NOCT → corrección γ por temperatura → yield kWh/kWp.
3. GCR, altura, separación de hileras → fracción de luz al pasto (modelo de sombreado).
4. Fracción de autoconsumo vs perfil de carga láctea real.
5. CAPEX/OPEX precios ES 2026 (citados) → ahorro, payback, LCOE.
6. (Upside) línea PAC, separada.

## 10. Entregables (DOS)

1. **Calculadora** (app web, stack 0 € tipo Streamlit, reutiliza patrón Sreca pero distinto).
2. **Memoria de proyecto** para la beca (la herramienta genera el informe base).

## 11. Arquitectura (aislamiento/claridad)

- `app/core/` — backbone puro testeable (solar, agrivoltaico, economía). Sin UI. TDD.
- `app/ui/` — vista (dashboard + informe). Depende de core, no al revés.
- `data/` — perfiles de carga sintéticos paramétricos + precios citados.
- `tests/` — guard invariantes (p.ej. honestidad del trade-off, yield en rango asturiano).

## 12. Plan de iteraciones (cada una deja estado commiteado y revisable)

- **It-1 (esta):** spec + scaffold + slice ejecutable mínima con núcleo solar real.
- **It-2:** modelo agrivoltaico (trade luz-pasto) + economía citada + tests.
- **It-3:** UI accesible + informe imprimible + verificación headless.
- **It-4:** memoria de beca + pulido + README + push a GitHub (gated, pedir a Pablo).
