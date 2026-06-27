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

### It-3 (siguiente)
- [ ] Verificación headless real con captura (Playwright/Chrome) + check accesibilidad.
- [ ] Informe imprimible (memoria base para la beca) desde la propia app.
- [ ] Refinar autoconsumo con perfil horario de ordeño (sustituir heurística).
- [ ] Selector de ubicación (varios concejos) o entrada de coordenadas → PVGIS.

### It-4 (gated)
- [ ] Memoria de proyecto para la beca + README con capturas + push a GitHub (esperar OK Pablo).

## Checkpoints para Pablo (revisar cuando vuelva)
- ¿Idea A correcta? (si no, revertir barato — spec §0).
- ¿Geometría v1 = bajo-panel-elevado OK? (spec §6).
