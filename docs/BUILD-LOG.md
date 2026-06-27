# BUILD-LOG — agrivoltaica ganadera asturiana

Registro vivo del loop autopautado. Cada entrada = un estado commiteado y revisable.

## 2026-06-27 · It-1 — arranque

- Decidida idea A (agrivoltaica ganadera) tras brainstorming (descartadas B atlas, C kit PV+aerotermia).
- Constraints fijados: PV+renovable, NO-EDP (independiente), simple de usar, núcleo preciso,
  visual, accesible ancianos+jóvenes, útil rural, innovador.
- Research inicial: casos ganado-PV (Minnesota dairy shade, reviews ScienceDirect, PVcase guide);
  agrovoltaica elegible PAC ES desde oct-2025 (criterios técnicos pendientes); calculadoras
  ref (PVGIS, Global Solar Atlas, ROI tools) para UX.
- Advisor pressure-test aplicado: spec-first + slice ejecutable temprano; clima oceánico
  (refugio, no calor); fork geometría fijado; accesibilidad como requisito duro; valor sin PAC.
- Escrito: spec de diseño, PROJECT.md, scaffold con git.

### It-1 hecho
- [x] Núcleo solar físico (POA→NOCT→γ→PR). yield 1070 kWh/kWp, PR 0,79 (realista Asturias).
- [x] 7 tests guard verde (rango yield, PR, linealidad, derating térmico, k_system).
- [x] Caché de bug propio: PR salía 0,90 (k_system optimista) → añadidas pérdidas baja-irradiancia/IAM/LID → 0,79. El guard lo cazó.
- [x] Slice Streamlit accesible (español, slider kWp, titulares grandes, gráfico mensual). Arranca HTTP 200.
- [x] Commit.

### It-2 hecho
- [x] **PVGIS real** (Tineo, API v5.2): POA 1.539 kWh/m², yield 1.219,5. Sustituye PROVISIONAL.
      Modelo físico propio cross-valida contra PVGIS con **0,65% de desvío** (test guard).
- [x] **Modelo agrivoltaico** (`agrivoltaic.py`): GCR→kWp/terreno vs luz al pasto (1-GCR), LER.
      Reconciliado escala: **kWp-first** (autoconsumo granja), área derivada = parche pequeño
      (cazado en sanity-check: 1 ha daba 735 kWp = utility, mal).
- [x] **Economía** (`economics.py`): consumo 516 kWh/vaca (scielo), CAPEX 1.000×1,3 €/kWp,
      autoconsumo heurístico, ahorro €, payback, LCOE, línea PAC upside separada.
- [x] **Confort/THI** (`confort.py`): catch clima verificado — verano asturiano THI~74
      (leve-moderado, NO severo) → beneficio = refugio, no sombra anti-calor. Test guard.
- [x] **App It-2**: calculadora completa (vacas+kWp+GCR+ayuda → ahorro/cobertura/payback/
      doble-uso/THI/mensual), accesible. Arranca HTTP 200. 27 tests verde.
- [x] Escenario 40 vacas: 17 kWp, 231 m² prado, luz 65%, LER 1,35, ahorro 2.160 €/año,
      payback 10,2 (6,1 con ayuda 40%), LCOE 0,084 €/kWh. Honesto y defendible.

### It-3 hecho
- [x] **Autoconsumo horario** (`perfil.py`): cruce generación FV (medio-seno por mes) vs
      carga láctea (2 picos ordeño, base refrigeración) sobre 12 días tipo. Sustituye la
      heurística. Da **42% autoconsumo** (vs 50% heurístico) = más honesto. Insight real:
      mismatch sol-mediodía / ordeño-alba-ocaso → argumenta batería o desplazar carga.
- [x] **Informe imprimible** (`informe.py`): HTML autocontenido con estilo print, formato
      número español, KPIs, fuentes. Botón de descarga en la app. Verificado por captura.
- [x] **Verificación headless real** (Playwright + Chrome sistema): desktop ✅ (captura
      `docs/screenshots/desktop.png`) + informe ✅ (`informe.png`). Accesible: titulares
      grandes, español llano, honesto.
- [x] App It-3 + 37 tests verde. Commit.
- [x] **Móvil verificado** (`docs/screenshots/movil.png`): renderiza accesible (columna única,
      texto grande). El blanco previo era artefacto MULTI-SESIÓN (2 páginas al mismo Streamlit
      → 2ª sesión vacía), no bug responsive. Captura en browser fresco = PASS.
- [ ] Selector de ubicación (varios concejos)→PVGIS. Diferido (opcional).

### It-3b — pase de honestidad (correcciones advisor)
- [x] **CAPEX premium = ASUNCIÓN, no dato**: estructura altura-vacuno real +50-100%, no +30%.
      Default subido a +60% y EXPUESTO como slider de sensibilidad. Headline honesto cambia:
      ahorro 1.897 €/año, payback **8,6 años con ayuda / 14,3 sin** (antes 6,7/11,2), LCOE 0,103.
- [x] **"Validado <1% vs PVGIS" era circular** (POA tomada de PVGIS + k_system ajustado a su
      modelo) → reescrito a "modelo de pérdidas coherente con PVGIS" en app, informe y test.
- [x] **LER 1,35× repositionado**: hueco en 231 m²; ahora se vende "esquina libre + refugio +
      ingreso extra", LER como métrica técnica secundaria. App + informe.
- [x] 37 tests verde. Commit.

### It-4 — HOLD (terminus esperar-a-Pablo; advisor: NO iterar autónomo más)
- [ ] **GATE 1 — confirmar idea A** (sin confirmar tras 3 iter; no escribir memoria a ciegas).
- [ ] **GATE 2 — conseguir las BASES reales de la convocatoria** (nunca verificadas, todo de
      memoria; formato/criterios/entregable desconocidos). Probablemente necesita a Pablo.
- [ ] Solo entonces: memoria de beca + README con capturas + push GitHub (GATED).

## Checkpoints para Pablo (revisar cuando vuelva)
- ¿Idea A correcta? (si no, revertir barato — spec §0).
- ¿Geometría v1 = bajo-panel-elevado OK? (spec §6).
