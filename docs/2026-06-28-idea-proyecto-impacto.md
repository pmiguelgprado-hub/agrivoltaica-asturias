---
type: deliverable
status: draft
tags: [beca, caja-rural, idea-proyecto, agrivoltaica, asturias]
created: 2026-06-28
updated: 2026-06-28
related: [2026-06-28-convocatoria-bases.md, PROJECT.md]
---

# Idea de proyecto de impacto — Becas Excelencia FCRA 2026 (Modalidad C)

> Borrador para el apartado "idea de proyecto" (15%, máx. 3.000 palabras) del Anexo 2.
> Marco: reto de despoblación y envejecimiento del medio rural · categoría **modernización
> y facilitación del sector primario** (implementación de tecnología, incorporación de
> jóvenes). Respaldo técnico: calculadora del repositorio (datos PVGIS, 37 tests).

## Título

**Sol y pasto en la misma finca: agrivoltaica ganadera para fijar jóvenes al campo asturiano**

## 1. La idea y su propuesta de valor

Las explotaciones de vacuno son el sostén económico de los concejos del interior y el
suroccidente de Asturias —Tineo, Somiedo, Teverga, Cangas del Narcea—, justamente los que
más población y relevo generacional están perdiendo. El joven que se plantea quedarse al
frente de la granja familiar se encuentra con dos costes que no controla: la factura
eléctrica (ordeño, refrigeración de la leche, limpieza) y la incertidumbre de unos ingresos
ligados al precio de la leche.

La propuesta es sencilla: **aprovechar el propio prado para producir electricidad sin dejar
de pastar**, mediante un sistema **agrivoltaico** —placas fotovoltaicas elevadas varios
metros sobre una esquina de la finca, de modo que el ganado siga pastando y se resguarde
debajo—. La granja autoconsume su energía, reduce su factura y diversifica sus ingresos, y
el suelo no se retira de la actividad agraria.

El proyecto no se queda en el concepto. Su núcleo es una **herramienta de cálculo accesible**
—pensada para que la entienda igual un ganadero mayor que un joven recién incorporado— que,
para una granja concreta, estima con datos reales cuánta energía produciría, cuánto ahorraría,
en cuántos años se pagaría y cuánta luz seguiría llegando al pasto. Convierte una idea
abstracta en una decisión informada para cada explotación.

A modo de ejemplo, para una granja típica de 40 vacas en Tineo, con un sistema de 17 kWp
elevado sobre unos 230 m² de prado (una esquina), la herramienta estima una producción de
unos 20.900 kWh al año —equivalente al consumo eléctrico de la propia explotación—, un ahorro
del orden de **1.900 €/año** y una amortización de unos **8–9 años** contando con ayudas a la
inversión. Bajo las placas, el pasto sigue recibiendo en torno al 65 % de la luz y el ganado
gana un refugio frente a la lluvia y el viento, que en el clima atlántico aportan más que la
sombra contra el calor.

## 2. Recursos necesarios para llevarlo a cabo

- **Herramienta de cálculo (ya desarrollada):** software de coste de licencia 0 € (Python,
  datos abiertos de PVGIS del Joint Research Centre europeo). Modelo físico de producción
  fotovoltaica, modelo agrivoltaico de reparto de luz entre placa y pasto, simulación horaria
  de autoconsumo frente a la curva de ordeño, y cálculo económico. Validada con 37 pruebas
  automáticas y coherente con la referencia oficial PVGIS.
- **Trabajo de campo:** uno o dos pilotos en granjas reales para contrastar consumos y
  curvas de carga, y afinar el modelo con datos medidos.
- **Inversión por explotación (la asume cada granja, no el proyecto):** del orden de
  20.000–30.000 € para un sistema de ~17 kWp con estructura elevada. Es el principal coste y
  la herramienta lo trata como variable, mostrando con honestidad cómo cambia la rentabilidad.
- **Difusión y acompañamiento:** material divulgativo y sesiones con cooperativas y oficinas
  comarcales para que los ganaderos puedan usar la herramienta y entender los resultados.

## 3. Origen de los recursos y cómo conseguirlos

- **Beca Excelencia (6.000 €):** semilla para el trabajo de campo, la validación con granjas
  piloto y la difusión de la herramienta.
- **Ayudas a la modernización de explotaciones agrarias:** subvenciones a fondo perdido de
  hasta el 65 % de la inversión para jóvenes ganaderos, que reducen drásticamente el plazo de
  amortización del sistema en cada granja.
- **Política Agraria Común (PAC):** desde octubre de 2025 la agrovoltaica es elegible para las
  ayudas de la PAC en España (los criterios técnicos están aún por concretar); se contempla
  como recorrido adicional, no como base del proyecto.
- **Ahorro de la propia explotación:** una vez instalado, el sistema se financia en buena
  parte con la reducción de la factura eléctrica.
- **Cooperativas y entidades locales** (incluida la propia Caja Rural de Asturias como
  financiador del sector primario) como vía de financiación y de llegada a los ganaderos.

## 4. Grado de innovación y diferenciación en el territorio

- **Agrivoltaica adaptada a la cornisa cantábrica.** La agrivoltaica que se practica en España
  se concentra en el sur seco y sobre cultivos. Aplicarla a **pradera y vacuno en clima
  oceánico húmedo** es terreno casi inexplorado: aquí el valor para el animal no es la sombra
  contra el calor, sino el **refugio** frente a la lluvia y el viento, y la finca no se
  sustrae a la ganadería.
- **Una herramienta, no un folleto.** Frente a los estudios genéricos, el proyecto entrega un
  instrumento de cálculo que cualquier ganadero puede usar con los datos de **su** finca, con
  resultados trazables y citados. Está pensado para ser **accesible a todas las edades**
  —texto claro, pocos datos de entrada, informe imprimible—, de modo que no excluya a la
  población rural de más edad.
- **Honestidad como diferencia.** La herramienta no infla los números: muestra cuándo el
  sistema no se amortiza sin ayudas, expone el desajuste entre la generación al mediodía y el
  ordeño de mañana y tarde, y trata el sobrecoste de la estructura como una incertidumbre
  ajustable. Esa transparencia es lo que la hace creíble para quien tiene que invertir.

## 5. Impacto social generado

- **Fijar población joven al medio rural.** Mejorar la rentabilidad y reducir la factura de la
  granja hace más viable el relevo generacional: la condición para que un joven se quede al
  frente de la explotación.
- **Modernizar el sector primario.** Lleva tecnología energética útil y comprensible a
  explotaciones que hoy no tienen acceso a un análisis hecho a su medida.
- **Diversificar la renta agraria** y reducir su exposición al precio de la leche y de la
  electricidad, dando estabilidad a las familias ganaderas.
- **Energía limpia de proximidad** generada y consumida en el propio concejo.
- **Replicabilidad.** El mismo método y la misma herramienta sirven para cualquier concejo en
  reto demográfico; el piloto en Tineo es extensible a Somiedo, Teverga o Cangas del Narcea.

## Viabilidad y compromiso

La viabilidad técnica está demostrada con la herramienta ya construida y validada con datos
oficiales. La viabilidad económica depende de cada granja y de las ayudas disponibles, algo
que el proyecto no oculta sino que pone en manos del ganadero para que decida con criterio.
De concederse la beca, el compromiso es desarrollar los pilotos, afinar la herramienta con
datos reales de explotaciones asturianas y presentar los resultados en el encuentro de la
Comunidad Excellent antes de finalizar 2026.

---
*Respaldo técnico (no forma parte del texto de la beca): repositorio del proyecto con la
calculadora, el modelo de ingeniería y las fuentes citadas (PVGIS, consumo lácteo 516
kWh/vaca·año, CAPEX FV España 2026, THI NRC 1971).*
