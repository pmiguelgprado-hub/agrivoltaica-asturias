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

### It-4 — bases verificadas + entregable redactado (2026-06-28)
- [x] **GATE 1 resuelto:** Pablo confirma idea A.
- [x] **GATE 2 resuelto:** bases reales obtenidas (PDF oficial vía pdftotext). RECALIBRACIÓN:
      es **Beca Excelencia** (no "convocatoria de proyecto"). Modalidad C máster = 12×6.000 €,
      **80% expediente + 5% vídeo + 15% idea de proyecto** (texto ≤3.000 palabras). Marco
      obligatorio = despoblación rural / **modernización sector primario + tecnología +
      jóvenes** (encaje pleno). Plazo 31-jul-2026. Doc: `docs/2026-06-28-convocatoria-bases.md`.
- [x] **Entregable real redactado:** `docs/2026-06-28-idea-proyecto-impacto.md` — idea de
      proyecto a los 5 puntos de Anexo 2 (1.105/3.000 palabras), con números de la calculadora
      como respaldo. La calculadora = soporte de credibilidad, NO el entregable.

### It-5 — perfeccionar el RESPALDO (Pablo: "que funcione e impresione")
- [x] **It-5a multi-concejo**: 5 concejos ganaderos con PVGIS real (Tineo, Cangas, Somiedo,
      Teverga, Grado), coherentes con PVGIS <3%. Selector en la app.
- [x] **It-5b pulido visual**: tema rural cálido + **heatmap hora×mes "firma solar"** (Plotly)
      + barras mensuales en orden cronológico (st.bar_chart las ordenaba alfabético).
- [x] **It-5c módulo de impacto** (`impacto.py`): escala 1 granja → concejo con disciplina de
      honestidad (advisor): **retención/relevo, NO empleo creado**; denominador real (Tineo
      ~374 granjas leche, dato oficial); CO₂ con factor red ES 0,258 kg/kWh (MITECO 2025).
      Escenario 10% Tineo = **780 MWh/año, 201 t CO₂/año, 70.935 €/año** en el concejo.
      Sección en la app (hero figure para el vídeo) + bloque en el informe imprimible.
- [x] **Reconciliado pitch ↔ herramienta**: §5 del entregable reescrito con impacto agregado
      (retención no empleo) + replicabilidad con números reales por concejo. Cifras §1/§3
      verificadas contra la salida actual. 47 tests verde.

### Definición de DONE del respaldo (advisor)
Acabado cuando cada cifra del texto ≤3.000 palabras esté (a) producida por la herramienta y
(b) citada o marcada como asunción. ✅ cumplido. Más gráficos = rendimientos decrecientes.

### It-6 — pulido de entregables (a petición de Pablo)
- [x] **Pitch humanizado + más cercano**: pasada anti-IA (paralelismos negativos rotos,
      0 guiones largos, menos negrita, reglas de tres deshechas) + voz de autor en 1ª persona
      + tono más cercano en intro y cierre. 1.335/3.000 palabras. Commits `b70befa` + (este).
- [x] **Guion del vídeo de motivación** (`docs/2026-06-28-guion-video.md`): plantilla a la
      estructura del Anexo 2 (presentación, criterios máster, valor para él y su entorno,
      planes, CV no académico), con tiempos, versión seguida y notas de grabación. Huecos
      `[PABLO: ...]` para datos personales reales (NO inventados).

### Pendiente (de Pablo, no autónomo)
- [ ] Rellenar los huecos `[PABLO: ...]` del guion con datos reales + grabar (≤2 min).
- [ ] Leer/validar el pitch (¿voz OK?).
- [ ] **VERIFICAR si el formulario FCRA admite adjunto/enlace** (decide si el jurado ve la app).
- [ ] **GATE elegibilidad (duro):** residencia Asturias + matrícula ≥60 cr + cuenta/ruralvia/
      débito Caja Rural antes del cierre (o Fyin).
- [ ] Rellenar el formulario telemático FCRA.
- [ ] Opcional: push GitHub (GATED, esperar OK Pablo).

## 2026-06-28 · Vídeo animado (Remotion) + limpieza de proyectos

- [x] **Vídeo de 2 min animado estilo Nate Herk** en `video/` (Remotion + ffmpeg, node ya
      instalado). Composición `BecaVideo` (120 s, 1920×1080, 30 fps): cabeza parlante +
      overlays (chips de sección, titulares, palabras-clave con *pop* escalonado, **mapa
      mental** Máster→Energía/Sistemas/Inversiones/Territorio, rótulo, barra de progreso) +
      **cierre con la app** (capturas con zoom Ken Burns). Estilo **Equilibrado** (Pablo lo
      eligió): los overlays ilustran SU historia; el proyecto protagoniza solo el final
      (respeta el baremo personal del Anexo 2).
- [x] Cámara: `OffthreadVideo` de `public/pablo.mp4`, *gated* por prop `hasFootage`
      (placeholder con instrucciones mientras no haya clip).
- [x] **Bug cazado por advisor + corregido:** la cámara se montaba dentro de cada `<Sequence>`
      → el clip se **reiniciaba en cada sección** (y se perdía el audio del cierre). Arreglo:
      una sola instancia a nivel raíz, 120 s; el cierre la tapa con fondo opaco pero el audio
      sigue. **Verificado** con un clip-señuelo cronometrado: el contador sube 14→15 cruzando
      el límite de los 15 s (antes se reiniciaba a 0).
- [x] Verificación empírica: `Sample` 5 s → mp4 (ffprobe h264/aac); `BecaVideo` completo →
      `out/beca-video.mp4` (120,04 s, 1920×1080); stills de intro/mapa-mental/cierre revisados.
- [x] `README.md` de uso + skill global reutilizable `~/.claude/skills/video-animado/`.
- [x] **Limpieza AIOS** (fuera de este proyecto): borrados `sreca` (reemplazado por este),
      `synertia` y `aios-second-brain` (Pablo aprobó); `kinesis` conservado (sin backup).
- [x] Calculadora sigue **47/47 tests verde**; PROJECT.md actualizado.

### Pendiente de Pablo (vídeo)
- [ ] Grabar el clip (horizontal, cara y hombros, 2 min) → `video/public/pablo.mp4`.
- [ ] Poner `hasFootage: true` en `src/Root.tsx` y `npm run render`.
- [ ] Ajustar tiempos de sección en `src/script.ts` para que cuadren con su locución real
      (previsualizar con `npm run studio`).

## 2026-06-29 · It-7 — perfeccionar la app (UI pro-limpia + marco legal con fuentes)

Foco del handoff `docs/handoffs/2026-06-28-perfeccionar-app.md`: app más amigable+pro,
lectura del marco legal con fuentes, benchmark de competidores. Trabajo **view-only**
(núcleo de cálculo intacto → los 47 tests siguen verde).

- [x] **Investigación legal verificada EN FUENTE** (no de memoria; el caveat del handoff se
      confirmó, no estaba stale):
  - Autoconsumo: **RD 244/2019** (BOE-A-2019-5089), vigente, modificado por **RDL 7/2026**.
  - Agrivoltaica + PAC: **RD 916/2025** (14-oct-2025, BOE-A-2025-20583) modifica el art.
    9.12 del RD 1048/2022 → la parcela agrivoltaica mantiene el **100% de superficie
    elegible** (vs solar normal = improductiva) *si la agricultura sigue siendo la principal*.
    **Criterios técnicos (altura, ocupación, merma) = POR CONCRETAR** por desarrollo posterior
    → confirma la disciplina "ayuda = upside, no cimiento".
  - Ayudas jóvenes Asturias: **AYUD0518T01** (oficial) — prima 25.000-50.000 € + incrementos
    (láctea, extensiva, mujer, ecológica); marco PEPAC 2023-27 / Reg. (UE) 2021/2115.
- [x] **Benchmark de competidores** (firecrawl): EnergySage (dirección→factura→ahorro, ultra
      simple, lidera con el ahorro), Clean Energy Project Builder (payback + valor 10 años +
      TIR). Patrón adoptado: **pocos inputs + resultado-primero + transparencia de fuentes**.
- [x] **Identidad visual = pro-limpia** (Pablo lo eligió; hand-drawn se queda en el vídeo).
      Diseño con `ui-ux-pro-max`: paleta verde bosque #0f7a47 + oro solar + crema, fuente
      **Fira Sans**, KPI cards (borde lateral de color, label en mayúsculas + valor grande),
      chips numerados de sección. Accesibilidad mantenida como **suelo duro** (columna única,
      texto grande, español llano) — NO se convirtió en rejilla BI densa.
- [x] **Nuevo `.streamlit/config.toml`** (tema pro), **vista `app/ui/app.py` rediseñada**
      (8 secciones, banda hero de 3 KPI, inputs en card, panel legal).
- [x] **NUEVO `app/core/legal.py`** — marco legal como datos estructurados (tema/resumen/
      estado/norma/fuente_url) con etiqueta de estado (`vigente`/`principio`/`por_concretar`)
      y enlace a la fuente oficial. La rentabilidad se sostiene **sin** ayudas (texto explícito).
- [x] **NUEVO `tests/test_legal.py`** (4 guards): toda entrada con fuente https, dominio
      oficial (boe.es/asturias.es/europa.eu/…), estado válido, y el caveat agrivoltaico
      presente y etiquetado. Blinda la disciplina "citar en fuente". **51/51 tests verde.**
- [x] **Verificación headless** (Playwright bundled + Chrome vía CDP): desktop ✅
      (hero, KPI band 1.897 €/43%/8,6 años, secciones 3-5, cards legales con badges+enlaces
      BOE, informe, footer) + **móvil** ✅ (reflow a columna única, cards apiladas, texto
      grande). Capturas en `/tmp/agri-final-*.png`, `/tmp/agri-mobile*.png`.
      GOTCHA observado: Streamlit 1.58.0 sirve UNA sesión buena y al hacer `reload` se queda
      en blanco → verificar siempre en **primer load** de un server fresco, sin recargar.

### Done-bar de "perfeccionar" (cumplido salvo visto bueno de Pablo)
(a) lee pro Y pasa accesibilidad ✅ · (b) panel legal con cada cifra en fuente + estado +
"upside" explícito ✅ · (c) 51/51 verde + guard legal ✅ · (d) **Pablo aprueba el look**
(pendiente — revisar capturas).

### Pendiente / posible siguiente iteración
- [ ] Visto bueno de Pablo al look pro-limpio.
- [ ] (opcional) Subir más el listón del benchmark: comparador lado a lado, o un “¿y si…?”
      con escenarios guardados.
- [ ] (opcional) Deploy 1-click a Streamlit Community Cloud para que el jurado lo abra.

## 2026-06-29 · It-8 — rediseño VISUAL-FIRST enterprise (Pablo redirigió)

Pablo, tras pedir verla: **"demasiado texto; todo implícito en gráficas/modelos; nada de
prosa; fondo blanco, verde/azul/naranja tipo EDP/PowerBI/AWS/Oracle; sin emojis ni imágenes;
todo calculado desde los datos que se importen".** Forks clavados con él (AskUserQuestion):
import = mínimos + CSV opcional · texto = visual puro 0 prosa · legal = FUERA de la app
(va al informe). It-7 (panel legal en la app, look cálido) → descartado.

- [x] **Tema enterprise** (`.streamlit/config.toml` + CSS): fondo BLANCO, **IBM Plex Sans**,
      paleta verde `#107c41` / azul `#0a6ed1` / naranja `#ea7600` sobre blanco. Sin emojis,
      sin imágenes. `layout="wide"`.
- [x] **`app/ui/app.py` reescrita visual-first** — fuera TODA la prosa (`st.caption`/`st.info`/
      párrafos). La información vive en gráficas + títulos cortos + leyendas:
      KPI cards (borde superior de color) · **donuts** cobertura/autoconsumo (Plotly) ·
      **gauge THI** con zonas verde/ámbar/naranja/rojo + aguja · **barra de uso del suelo**
      (pasto con luz vs sombra) + LER · **curva generación-vs-consumo** del día medio (el
      desfase sol-mediodía / ordeño-alba-ocaso se VE, sin explicarlo) · barras mensuales ·
      heatmap firma solar · KPIs de impacto. Botón de informe sin emoji.
- [x] **Import de consumo real** (lo que pidió): `app/core/importador.py` `parse_consumo()`
      (CSV robusto: `;`/`,`, coma decimal ES, cabecera; toma la última columna numérica; 24
      valores→curva diaria, 8760→horario anual con perfil medio, 12→mensual, otro→suma anual).
      `st.file_uploader` → si hay CSV, **consumo y forma horaria reales** alimentan autoconsumo
      y economía; si no, estimación por vacas. Caption "Importado/Estimado".
- [x] **Núcleo extendido (aditivo, núcleo de cálculo intacto):** `perfil.simular_autoconsumo`
      acepta `pesos_carga` (curva 24 h real); `economics.evaluar_economia` acepta
      `consumo_anual_override`. Nuevos tests: `test_importador.py` (6, incl. **integración
      glue import→cálculo mueve KPI**) + `test_consumo_override_se_usa`. **58/58 verde.**
- [x] **Legal movido al INFORME** (Pablo): `informe.py` ahora monta `MARCO_LEGAL` (badges de
      estado + enlaces oficiales) → `legal.py` deja de estar huérfano y `test_legal` sigue vivo.
      Emoji del título del informe quitado.
- [x] **Advisor cazó 4 (corregidos):** (1) **CSV sin probar e2e** → verificado la ruta exacta
      de la app en Python (24h: autoconsumo 42→74%, ahorro 1.897→2.696 €; 8760: cobertura
      42,5→43,9%) + test de integración; (2) THI gauge "74.4"→`valueformat=".0f"`="74";
      (3) texto inglés del uploader ("200MB per file") → CSS oculta las instrucciones;
      (4) `legal.py` huérfano → cableado al informe.
- [x] **Verificación visual** (browser-harness, first-load): dashboard enterprise OK — KPIs,
      donuts (cobertura azul / autoconsumo naranja), gauge THI con zonas, barra uso del suelo,
      **curva gen-vs-consumo** (el money shot), barras + heatmap. Capturas `/tmp/it8-1..4.png`.

### BLOQUEO de visualización (importante)
Streamlit 1.58.0 en esta máquina sirve **UNA sesión buena**; cualquier **rerun o reload**
(incluido subir un CSV) deja el server **en blanco** para todos. Verificado con flags
robustos (CORS/XSRF off, fileWatcher none) — persiste. Por eso:
- **Para ver la app local:** abrir un server **recién arrancado, primer load, SIN recargar**.
- **Fix permanente recomendado:** desplegar a **Streamlit Community Cloud** (URL estable, sin
  el quirk de WS local, el jurado la abre). Requiere push a GitHub público = **GATED** (OK Pablo).
- browser-harness usa el Chrome REAL de Pablo (tabs privados Alpaca/Gmail/trading) → NO usar
  `ensure_real_tab`; targetear con `new_tab`+`current_tab`. La conexión CDP pide "Allow" en
  chrome://inspect (acción manual de Pablo). Móvil = CDP `setDeviceMetricsOverride`.

### Done-bar It-8: (a) visual-first 0 prosa ✅ (b) enterprise blanco+verde/azul/naranja, sin
emojis/imágenes ✅ (c) import CSV funcionando+probado ✅ (d) legal en el informe ✅ (e) 58/58 ✅
(f) **Pablo aprueba el look + decide deploy = PENDIENTE.**

## Checkpoints para Pablo (revisar cuando vuelva)
- ¿Idea A correcta? (si no, revertir barato — spec §0).
- ¿Geometría v1 = bajo-panel-elevado OK? (spec §6).
- **¿Aprobado el look enterprise visual-first (It-8)?**
- **¿Desplegar a Streamlit Cloud (push GitHub público) para verla/que la abra el jurado?**
