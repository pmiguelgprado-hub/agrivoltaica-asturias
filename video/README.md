# Vídeo animado de la beca (Remotion)

Vídeo de motivación de **2 min** para las Becas Excelencia FCRA 2026 (Anexo 2, 5 %).
Estilo YouTuber de IA (Nate Herk): tú hablando + overlays animados que ilustran tu
historia (chips de sección, titulares, palabras-clave, mapa mental) y, **al cierre**,
la app del proyecto. Decisión de estilo: *Equilibrado* — el vídeo es de motivación
personal; el proyecto solo protagoniza el final.

## Uso rápido

```bash
cd video
npm install              # solo la 1ª vez
npm run studio           # previsualizar en el navegador (recomendado para iterar)
npm run render           # vídeo de la beca → out/beca-video.mp4 (2 min, necesita tu clip)
npm run render:estructura # vídeo corto de estructura → out/estructura-proyecto.mp4 (1 min, sin cámara)
npm run render:sample    # vídeo de prueba (5 s) para verificar que todo va
```

## Composiciones

| ID | Qué es | Necesita tu clip |
|---|---|---|
| `Estructura` | Vídeo corto (1 min) que explica la **estructura del proyecto** en diapositivas animadas estilo **Excalidraw/Nate Herk** (portada → qué es → mapa mental del cálculo → app en iPhone → cifras → cierre). Solo motion graphics. | No |
| `BecaVideo` | Vídeo de motivación de 2 min (Anexo 2): cabeza parlante + overlays. | Sí (`pablo.mp4`) |
| `Sample` | Prueba de 5 s del pipeline de render. | No |
| `StyleTest` | Una sola slide (el mapa mental) para iterar el estilo a mano. | No |

## Estilo hand-drawn (Excalidraw / Nate Herk)

`Estructura` usa **rough.js** (el mismo motor de dibujo a mano de Excalidraw) +
fuente manuscrita **Kalam** (`@remotion/google-fonts`) sobre canvas negro con tarjetas
blancas tipo infografía. Cajas y flechas imperfectas a propósito = look NO-IA.
La app se presenta dentro de un **iPhone** (`PhoneMockup`) con scroll vertical de la
captura móvil real. Componentes: `rough.ts`, `RoughMindMap`, `RoughStats`, `HandSlide`,
`PhoneMockup`. Gotcha: los trazos rough se calculan con `seed` fijo en `useMemo` sin
depender del frame, si no "hierven" en movimiento.

## Meter tu grabación

1. Graba en horizontal (cara y hombros, luz por delante, audio limpio).
2. Guarda el clip como `public/pablo.mp4`.
3. En `src/Root.tsx`, cambia `defaultProps={{hasFootage: false}}` → `true`.
   (O en Studio, edita la prop `hasFootage` y dale a render.)
4. `npm run render`.

Mientras no haya clip, el hueco de la cámara muestra un marcador. El resto del vídeo
(overlays, mapa mental, app) ya funciona y se puede renderizar.

## Estructura

| Archivo | Qué hace |
|---|---|
| `src/script.ts` | Guion → bloques con tiempos. **Edita aquí los textos.** |
| `src/Root.tsx` | Registra las composiciones (`BecaVideo` 2 min, `Sample` 5 s). |
| `src/BecaVideo.tsx` | Monta las escenas en el tiempo. |
| `src/components/` | Fondo, cámara, panel de historia, mapa mental, app, rótulo, barra. |
| `public/` | Capturas de la app (`desktop/impacto/informe/movil.png`) y tu `pablo.mp4`. |

## Ajustes frecuentes

- **Cambiar textos:** `src/script.ts` (chips, titulares, palabras-clave, mapa mental).
- **Más/menos duración de un bloque:** edita `from`/`to` (segundos) en `script.ts` y
  `durationInFrames` total en `Root.tsx` si cambias el total.
- **Revisar un fotograma sin render completo:**
  `npx remotion still src/index.ts BecaVideo out/f.png --frame=100`

El guion hablado completo está en `../docs/2026-06-28-guion-video.md` (los `[PABLO: …]`
son huecos con tus datos reales).
