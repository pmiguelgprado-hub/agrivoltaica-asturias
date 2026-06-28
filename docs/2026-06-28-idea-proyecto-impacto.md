---
type: deliverable
status: draft
tags: [beca, caja-rural, idea-proyecto, agrivoltaica, asturias]
created: 2026-06-28
updated: 2026-06-28
related: [2026-06-28-convocatoria-bases.md, PROJECT.md]
---

# Idea de proyecto de impacto — Becas Excelencia FCRA 2026 (Modalidad C)

> Borrador para el apartado "idea de proyecto" (15 %, máx. 3.000 palabras) del Anexo 2.
> Marco: reto de despoblación y envejecimiento del medio rural, categoría de modernización
> del sector primario (tecnología e incorporación de jóvenes). Respaldo técnico: la
> calculadora del repositorio, con datos de PVGIS y 47 pruebas automáticas.

## Título

**Sol y pasto en la misma finca: agrivoltaica ganadera para fijar jóvenes al campo asturiano**

## 1. La idea y su propuesta de valor

Las explotaciones de vacuno sostienen la economía de los concejos del interior y el
suroccidente de Asturias, como Tineo, Somiedo, Teverga o Cangas del Narcea. Son también los
concejos que más población y relevo generacional pierden. El joven que se plantea quedarse al
frente de la granja familiar arrastra dos costes que no controla: la factura eléctrica del
ordeño, la refrigeración de la leche y la limpieza, y unos ingresos atados al precio que le
pague la industria por esa leche.

Mi propuesta parte de una idea sencilla: aprovechar el propio prado para producir
electricidad sin dejar de pastar. Se hace con un sistema agrivoltaico, placas fotovoltaicas
elevadas varios metros sobre una esquina de la finca, de modo que el ganado siga pastando y
se resguarde debajo. La granja consume su propia energía, baja la factura y diversifica los
ingresos, todo sin sacar el suelo de la actividad agraria.

La idea no se queda ahí. Su núcleo es una herramienta de cálculo que he construido y que
quiere ser fácil de usar, tanto para un ganadero mayor como para un joven recién incorporado.
Para una finca concreta estima, con datos reales, cuánta energía produciría, cuánto ahorraría,
en cuántos años se pagaría la inversión y cuánta luz seguiría llegando al pasto. Lo abstracto
se vuelve una decisión que cada explotación puede tomar con cifras delante.

Un ejemplo. Para una granja típica de 40 vacas en Tineo, con un sistema de 17 kWp elevado
sobre unos 230 m² de prado (una esquina), la herramienta estima una producción cercana a los
20.900 kWh al año, prácticamente el consumo eléctrico de la propia explotación. El ahorro
ronda los **1.900 €/año** y la inversión se amortiza en unos **8 o 9 años** si se cuenta con
ayudas. Bajo las placas, el pasto sigue recibiendo en torno al 65 % de la luz, y el ganado
gana un refugio frente a la lluvia y el viento, que en el clima atlántico pesan más que el
calor.

## 2. Recursos necesarios para llevarlo a cabo

La herramienta de cálculo ya está desarrollada y tiene coste de licencia cero: está hecha en
Python sobre los datos abiertos de PVGIS, el servicio solar del Joint Research Centre europeo.
Incluye el modelo físico de producción fotovoltaica, el reparto de luz entre placa y pasto, la
simulación hora a hora del autoconsumo frente a la curva de ordeño y el cálculo económico. La
respaldan 47 pruebas automáticas, y sus resultados coinciden con la referencia oficial de
PVGIS.

A partir de ahí, el proyecto necesita trabajo de campo: una o dos granjas piloto donde medir
consumos y curvas de carga reales y afinar el modelo con datos propios. La inversión en placas
la asume cada explotación, no el proyecto; ronda los 20.000 a 30.000 € para un sistema de unos
17 kWp con estructura elevada, y es el coste principal. La herramienta lo trata como una
variable y enseña sin maquillaje cómo cambia la rentabilidad según ese coste. Por último, hace
falta difusión: material divulgativo y sesiones con cooperativas y oficinas comarcales para
que los ganaderos manejen la herramienta y entiendan lo que les dice.

## 3. Origen de los recursos y cómo conseguirlos

La beca de 6.000 € sería la semilla para el trabajo de campo, la validación con las granjas
piloto y la difusión. La inversión de cada granja se apoya en las ayudas a la modernización de
explotaciones agrarias, subvenciones a fondo perdido de hasta el 65 % para jóvenes ganaderos,
que recortan mucho el plazo de amortización. Desde octubre de 2025 la agrovoltaica también es
elegible para las ayudas de la Política Agraria Común en España, aunque sus criterios técnicos
aún están por concretar; lo dejo como recorrido adicional, nunca como base del proyecto. Una
vez instalado, el sistema se paga en buena parte solo, con la reducción de la factura. Y para
llegar a los ganaderos cuento con las cooperativas y entidades del territorio, entre ellas la
propia Caja Rural de Asturias por su papel de financiación del sector primario.

## 4. Grado de innovación y diferenciación en el territorio

Lo más diferencial es llevar la agrivoltaica a la cornisa cantábrica. La que se practica en
España se concentra en el sur seco y sobre cultivos. Aplicarla a pradera y vacuno en un clima
oceánico húmedo es terreno casi inexplorado: aquí la placa no da sombra contra el calor, da
refugio frente a la lluvia y el viento, y la finca no se retira de la ganadería.

El proyecto entrega una herramienta, no un folleto. Cualquier ganadero puede usarla con los
datos de su propia finca y obtener resultados trazables y con fuentes. La he pensado para que
la entienda gente de cualquier edad, con lenguaje claro, pocos datos de entrada y un informe
imprimible, de manera que la población rural más mayor no quede fuera.

Y hay una decisión de fondo: la herramienta no infla los números. Avisa de cuándo el sistema
no se amortiza sin ayudas, enseña el desfase entre el sol del mediodía y el ordeño de mañana y
tarde, y trata el sobrecoste de la estructura elevada como una incertidumbre que el usuario
ajusta. Esa transparencia es justo lo que la hace creíble para quien tiene que poner el dinero.

## 5. Impacto social generado

Aquí no vendo creación de empleo. La agrivoltaica sobre una granja que ya existe no inventa
puestos de trabajo, pero mejora el margen y baja la factura, y con eso hace viable que un
joven se quede al frente de la explotación. En un territorio que envejece, ese relevo es el
impacto que de verdad cuenta. De paso, lleva tecnología energética útil y comprensible a
explotaciones que hoy no tienen acceso a un análisis hecho a su medida, y da a las familias
ganaderas una renta menos expuesta al vaivén del precio de la leche y de la luz.

Conviene mirarlo también a escala de concejo. Tineo tiene del orden de 370 explotaciones de
leche y es el primer concejo ganadero de Asturias. Como escenario ilustrativo, si solo una de
cada diez adoptara el sistema, unas 37 granjas, el conjunto generaría cerca de **780 MWh de
energía limpia al año**, evitaría alrededor de **200 toneladas de CO₂** anuales (con el factor
de la red eléctrica española, 0,258 kgCO₂/kWh, MITECO 2025) y dejaría cerca de **70.000 €
anuales** de ahorro dentro del concejo, en vez de marcharse en la factura. Son cifras de un
supuesto de adopción declarado, no una garantía.

Y es replicable de verdad. La herramienta ya trae los datos solares de PVGIS de varios
concejos en reto demográfico, cada uno con su propio resultado. Para la misma granja de 40
vacas y 17 kWp, Tineo y Cangas del Narcea rondan los 1.900 €/año de ahorro y 8 años y medio de
amortización con ayuda; Teverga y Grado, unos 1.815 €/año y nueve años; Somiedo, con menos sol
de invierno por su horizonte de montaña, unos 1.670 €/año y diez años. El piloto de Tineo se
extiende, por tanto, al resto del territorio.

## Viabilidad y compromiso

La viabilidad técnica ya está demostrada con la herramienta construida y contrastada con datos
oficiales. La económica depende de cada granja y de las ayudas de cada momento, y el proyecto
no lo esconde: pone esa cuenta en manos del ganadero para que decida con criterio. Si la beca
sale adelante, me comprometo a desarrollar los pilotos, afinar la herramienta con datos reales
de explotaciones asturianas y presentar los resultados con el resto de becados antes de cerrar
2026.

---
*Respaldo técnico (no forma parte del texto de la beca): repositorio del proyecto con la
calculadora, el modelo de ingeniería y las fuentes citadas (PVGIS, consumo lácteo 516
kWh/vaca·año, CAPEX FV España 2026, THI NRC 1971, factor CO₂ red española MITECO 2025).*
