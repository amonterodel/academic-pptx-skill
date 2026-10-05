---
version: alpha
name: Sistema de diseño SEFH · 71 Congreso
description: >-
  Sistema visual para materiales científicos de la Sociedad Española de Farmacia
  Hospitalaria (71 Congreso Nacional, Gran Canaria 2026): ponencias, carteles,
  informes y páginas. Colores de la plantilla oficial, Calibri, rejilla de 12
  columnas y un código de color con significado fijo. Las medidas están en
  píxeles de un lienzo de 1920 × 1080 (1 pt = 2 px en una diapositiva de
  13,333 × 7,5 in).
colors:
  primary: "#263445"
  secondary: "#5E6B78"
  neutral: "#FFFFFF"
  surface: "#F3F6F9"
  outline: "#C9D2DB"
  on-primary: "#FFFFFF"
  brand-lima: "#C3BF24"
  brand-verde: "#5BB46C"
  brand-turquesa: "#00B3B2"
  brand-morado: "#AD3B94"
  brand-azul: "#4A73A0"
  ml: "{colors.brand-morado}"
  ml-dark: "#8E2F79"
  ml-mid: "#C97AB5"
  ml-soft: "#E9C3DF"
  ml-tint: "#F8EAF4"
  tool: "{colors.brand-verde}"
  tool-dark: "#2B7D3D"
  tool-tint: "#E7F4E9"
  human: "{colors.brand-azul}"
  human-dark: "#2F5480"
  human-tint: "#E4EBF4"
  emphasis: "{colors.brand-turquesa}"
  emphasis-dark: "#007A79"
  emphasis-tint: "#E0F5F5"
  structure: "{colors.brand-lima}"
  structure-dark: "#77730E"
  structure-tint: "#F4F3D6"
  error: "#D42A3B"
  error-tint: "#FCE4E6"
  caution: "#F0A500"
  xray-surface: "#0E1B2C"
  xray-line: "#A9DBFF"
  xray-soft: "#DDE7F0"
  muted: "#C3CBD3"
  illus-ink: "{colors.primary}"
  illus-metal-1: "#E4E9EE"
  illus-metal-2: "#B9C3CD"
  illus-metal-3: "#8794A1"
  illus-metal-4: "#4E5B68"
  illus-coat: "#FFFFFF"
  illus-coat-shade: "#E3EAF0"
  illus-glow: "#5FF0EE"
  illus-skin: "#E3B48C"
  illus-chalkboard: "#31454F"
  illus-chalk: "#F4F1E6"
typography:
  headline-display:
    fontFamily: Calibri
    fontSize: 72px
    fontWeight: 400
    lineHeight: 1.0
  headline-lg:
    fontFamily: Calibri
    fontSize: 64px
    fontWeight: 400
    lineHeight: 1.0
  title-cover:
    fontFamily: Calibri
    fontSize: 72px
    fontWeight: 700
    lineHeight: 1.0
  stat-display:
    fontFamily: Calibri
    fontSize: 220px
    fontWeight: 700
    lineHeight: 1.0
  label-lg:
    fontFamily: Calibri
    fontSize: 48px
    fontWeight: 700
    lineHeight: 1.1
  body-lg:
    fontFamily: Calibri
    fontSize: 44px
    fontWeight: 400
    lineHeight: 1.15
  body-md:
    fontFamily: Calibri
    fontSize: 40px
    fontWeight: 400
    lineHeight: 1.15
  label-md:
    fontFamily: Calibri
    fontSize: 40px
    fontWeight: 700
    lineHeight: 1.0
  caption:
    fontFamily: Calibri
    fontSize: 24px
    fontWeight: 400
    lineHeight: 1.2
rounded:
  none: 0px
  md: 16px
  full: 9999px
spacing:
  canvas-width: 1920px
  canvas-height: 1080px
  columns: 12
  column: 124.67px
  gutter: 24px
  margin: 80px
  title-top: 118px
  title-height: 150px
  content-top: 290px
  content-bottom: 985px
  source-top: 998px
  source-height: 38px
  card-padding: 32px
  stack-gap: 24px
  section-gap: 48px
  icon-sm: 64px
  icon-md: 96px
  icon-lg: 120px
  stroke-thin: 3px
  stroke-md: 5px
  stroke-strong: 8px
components:
  page:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.primary}"
  headline:
    textColor: "{colors.primary}"
    typography: "{typography.headline-lg}"
    height: 150px
  headline-closing:
    textColor: "{colors.primary}"
    typography: "{typography.headline-display}"
  source-note:
    textColor: "{colors.secondary}"
    typography: "{typography.caption}"
    height: 38px
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
    rounded: "{rounded.md}"
    padding: 32px
  card-stat:
    backgroundColor: "{colors.ml-tint}"
    textColor: "{colors.ml}"
    typography: "{typography.stat-display}"
    rounded: "{rounded.md}"
    padding: 48px
  card-tool:
    backgroundColor: "{colors.tool-tint}"
    textColor: "{colors.primary}"
    rounded: "{rounded.md}"
    padding: 32px
  card-tool-header:
    backgroundColor: "{colors.tool-dark}"
    textColor: "{colors.on-primary}"
    typography: "{typography.body-lg}"
  guide-question:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.emphasis-dark}"
    typography: "{typography.label-lg}"
    rounded: "{rounded.full}"
    height: 70px
  caveat-strip:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.body-lg}"
    rounded: "{rounded.md}"
    height: 70px
  tag:
    typography: "{typography.label-md}"
    rounded: "{rounded.full}"
    height: 46px
    padding: 30px
  tag-ok:
    backgroundColor: "{colors.tool}"
    textColor: "{colors.xray-surface}"
  tag-fail:
    backgroundColor: "{colors.error}"
    textColor: "{colors.on-primary}"
  tag-partial:
    backgroundColor: "{colors.caution}"
    textColor: "{colors.xray-surface}"
  tag-neutral:
    backgroundColor: "{colors.xray-soft}"
    textColor: "{colors.xray-surface}"
  scheme-frame:
    textColor: "{colors.primary}"
    rounded: "{rounded.md}"
    size: 5px
  arrow:
    textColor: "{colors.primary}"
    size: 5px
  label-ml:
    textColor: "{colors.ml-dark}"
    typography: "{typography.label-md}"
  label-human:
    textColor: "{colors.human-dark}"
    typography: "{typography.label-md}"
  label-emphasis:
    textColor: "{colors.emphasis-dark}"
    typography: "{typography.label-md}"
  ring-ml-outer:
    backgroundColor: "{colors.ml-soft}"
  ring-ml-middle:
    backgroundColor: "{colors.ml-mid}"
  ring-ml-inner:
    backgroundColor: "{colors.ml}"
  marker-ml:
    backgroundColor: "{colors.ml}"
    size: 16px
  marker-tool:
    backgroundColor: "{colors.tool}"
    size: 28px
  structure-band:
    backgroundColor: "{colors.structure}"
    height: 12px
  scheme-muted:
    textColor: "{colors.muted}"
  xray-panel:
    backgroundColor: "{colors.xray-surface}"
    textColor: "{colors.xray-line}"
    rounded: "{rounded.md}"
---

# Sistema de diseño SEFH · 71 Congreso

## Overview

Material científico para farmacéuticos de hospital que se proyecta en salas grandes. Tiene que leerse desde la última fila y no puede competir con la plantilla oficial del congreso: la banda superior con logotipos, el marco turquesa fino y la franja de triángulos del pie son intocables. Todo lo demás se compone dentro del marco.

El tono es sobrio y claro, con un punto de humor en las ilustraciones: un loro robótico con bata de farmacia representa al modelo de lenguaje. Cada pieza transmite una sola idea. En una diapositiva, el titular es una afirmación completa y no un rótulo.

Tres principios mandan sobre cualquier valor concreto:

1. **El color significa.** Cada color de marca tiene un único papel (ver *Colors*). Ningún color se usa de adorno.
2. **El texto es intocable.** El diseño se adapta al contenido: no se recortan, parafrasean ni reordenan textos validados. Si algo no cabe, se avisa.
3. **Un sistema, no piezas sueltas.** Tarjetas, etiquetas, flechas y marcos salen siempre de los componentes de este archivo, con el mismo radio, grosor y relleno.

## Colors

La paleta se toma de la propia plantilla del congreso: el morado (`#AD3B94`) y el turquesa (`#00B3B2`) están en sus textos, y el lima, el verde y el azul se muestrearon de sus triángulos. El fondo es siempre blanco y el texto, tinta (`#263445`).

**Código semántico.** Es fijo: no cambia entre piezas.

- **Morado: aprendizaje automático (`ml`).** Todo modelo cuya forma aprenden los datos: aprendizaje automático, redes neuronales, modelos de lenguaje e híbridos. Las variantes `ml-soft` y `ml-mid` sirven para anidar conjuntos (anillos concéntricos), siempre de claro (fuera) a intenso (dentro).
- **Verde: herramienta validada y TDM (`tool`).** Modelos poblacionales, estimación bayesiana, programas validados y resultados de la dosificación individualizada.
- **Azul: la persona (`human`).** El farmacéutico, el criterio humano y «la decide una persona».
- **Turquesa: énfasis editorial (`emphasis`).** La palabra clave de un titular, una pregunta guía, los apartados de una ficha o el aviso de relevo. Como mucho un uso por pieza; nunca codifica una categoría.
- **Lima: estructura (`structure`).** Solo ecos de la plantilla (bandas finas, peldaños, decoración del envase). No lleva texto.
- **Rojo: fallo (`error`).** Solo para un fallo demostrado: un dato erróneo o una pieza que falla en un estudio. Nunca para advertencias genéricas.
- **Ámbar: rendimiento parcial (`caution`).** Solo para el estado intermedio de una pieza evaluada («interpreta: 83 %»). No se usa para avisos metodológicos.

**Radiografía.** `xray-surface` y `xray-line` sirven para la vista de «rayos X» de un esquema: fondo azul noche y líneas claras azuladas con un leve resplandor.

**Contraste.** El texto normal necesita al menos 4,5:1 y el grande (≥ 24 pt, o ≥ 18,7 pt en negrita) al menos 3:1. El turquesa puro y el verde puro no pasan sobre blanco: para texto se usan sus variantes `-dark`. La única excepción tolerada es el título de la portada, que conserva el turquesa de la plantilla (2,6:1).

## Typography

Una sola familia, **Calibri**, que es la del tema de la plantilla y viene en Windows y en Office para macOS. La jerarquía se construye con tamaño y peso, nunca con otra tipografía. En equipos sin Calibri, el sustituto métrico es **Carlito**: las comprobaciones de ajuste del texto se hacen con él.

| Nivel | px (lienzo) | pt (diapositiva) | Uso |
|---|---|---|---|
| `headline-display` | 72 | 36 | Titular de cierre y título de portada |
| `headline-lg` | 64 | 32 | Titular de cada diapositiva, en redonda, con la palabra clave en negrita de color |
| `stat-display` | 220 | 110 | Cifra destacada (de 96 a 120 pt) |
| `label-lg` | 48 | 24 | Encabezados de columna y pregunta guía |
| `body-lg` | 44 | 22 | Texto principal de tarjetas |
| `body-md` | 40 | 20 | Mínimo para cualquier texto proyectado |
| `label-md` | 40 | 20 | Etiquetas de estado |
| `caption` | 24 | 12 | Pie de fuente bibliográfica, y nada más |

**Composición del texto.**

- Los titulares tienen como máximo dos líneas, cortadas a mano en una pausa natural: tras una coma, un punto y coma o un «pero».
- Entre cifra y unidad va un espacio de no separación (`37 %`, `4 g/día`, `RR 0,55`). También se protegen los nombres propios compuestos (`Nuestra Señora de Candelaria`).
- Nunca queda una palabra sola en la última línea de un titular o de una tarjeta.
- Texto alineado a la izquierda. Solo se centran el titular de cierre, la portada y los rótulos que van bajo un dibujo.

## Layout

Lienzo de 1920 × 1080 px (16:9), equivalente a 13,333 × 7,5 in. Rejilla de **12 columnas** de 124,67 px, con medianil de 24 px y márgenes laterales de 80 px.

Franjas verticales:

| Franja | Desde | Hasta | Contenido |
|---|---|---|---|
| Banda de la plantilla | 0 | 112 | Logotipos (no se toca) |
| Titular | 118 | 268 | Anclado arriba: un titular de una línea y otro de dos empiezan a la misma altura |
| Contenido | 290 | 985 | Todo lo demás |
| Fuente | 998 | 1036 | Pie de 12 pt, a la izquierda; si no cabe en una línea, se permiten dos desde y = 980 |
| Triángulos de la plantilla | 1042 | 1080 | No se toca |

Relleno interior de tarjeta: 32 px. Separación entre bloques apilados: 24 px. Separación entre secciones: 48 px. Los iconos se colocan solo a tres tamaños (64, 96 y 120 px) para que su trazo se vea siempre igual de grueso.

## Elevation & Depth

Diseño plano. La jerarquía se marca con tinte de fondo, peso tipográfico y color semántico, no con sombras: **no hay sombras paralelas en ningún elemento**. La única excepción es la portada, que conserva la sombra de texto que trae la propia plantilla del congreso. La única profundidad permitida es la de las ilustraciones, por ejemplo la proyección oblicua de un envase. La vista de radiografía añade un resplandor suave a las líneas claras, nunca una sombra.

## Shapes

Solo tres radios: `none` para las bandas que forman escaleras y diagramas de barras, `md` (16 px) para tarjetas, paneles y marcos, y `full` para etiquetas y la pregunta guía. Los grosores de línea son tres: fino (3 px = 1,5 pt) para filetes, medio (5 px = 2,5 pt) para flechas y marcos, y fuerte (8 px = 4 pt) para conectores que unen un dato con su tarjeta.

El marco discontinuo está reservado al «arnés» (protocolo o procedimiento) que envuelve un sistema. Un rótulo puede abrir un hueco deliberado en el borde, centrado en el borde inferior; el resto del marco no se interrumpe.

**Ilustración.** Estilo plano con contorno de tinta de grosor constante (5 px a 120 px de alto) y rellenos lisos de la paleta `illus-*`. Personajes recurrentes:

- **El loro robótico.** Cuerpo metálico, articulaciones atornilladas, luz cian en el ojo y bata blanca. Es el modelo de lenguaje y, en un esquema, el nodo más grande (unas 1,5 veces los demás). Su ficha canónica, con el prompt para generar la hoja de personaje, está en `personajes/loro-estocastico.md`.
- **El farmacéutico con pluma.** Busto con bata. Es el criterio humano y va siempre por encima del esquema que supervisa.

Los iconos son de línea con la misma tinta y, como mucho, un relleno de tinte semántico. Cada uno tiene tres variantes: color, gris (atenuado) y radiografía. Sin logotipos ni marcas reales.

## Components

- **Titular (`headline`).** Va a x = 80 y y = 118, anclado arriba, en 64 px redonda tinta. La palabra que lleva la tesis se marca en negrita y con el color semántico que le corresponda, o con el énfasis turquesa si no tiene categoría.
- **Pie de fuente (`source-note`).** 24 px en gris, alineado a la izquierda en x = 80, con el borde inferior en y = 1036. Las referencias se separan con « · ».
- **Tarjeta (`card`).** Tinte `surface`, radio de 16 px, relleno de 32 px y sin borde. Es la unidad básica para agrupar contenido.
- **Tarjeta de dato (`card-stat`).** Tinte del color semántico del dato, cifra en `stat-display` y lectura en `body-lg` debajo.
- **Tarjeta de herramienta (`card-tool`).** Tinte verde con borde verde de 5 px y cabecera sólida `tool-dark` con texto blanco. Es la única tarjeta con borde: señala lo validado.
- **Pregunta guía (`guide-question`).** Píldora `surface` a todo el ancho, con el texto centrado en turquesa oscuro.
- **Franja de advertencia (`caveat-strip`).** Banda sólida de tinta con texto blanco en negrita. Va en las advertencias metodológicas que matizan el titular.
- **Etiqueta (`tag`, `tag-ok`, `tag-fail`, `tag-partial`, `tag-neutral`).** Píldora de 46 px de alto (92 px si ocupa dos líneas), con un ancho que es el del texto más 60 px y sin ajuste automático.
- **Flecha (`arrow`).** Línea recta o curva de 5 px en tinta, con punta triangular. Las flechas de supervisión son punteadas y en azul. Una flecha mide al menos 40 px y su rótulo va pegado a ella.
- **Marco de esquema (`scheme-frame`).** Discontinuo, de 5 px y radio de 16 px. Representa el arnés.
- **Panel de radiografía (`xray-panel`).** Ocupa el área de contenido con radio de 16 px. Repite el esquema en líneas `xray-line` y las etiquetas de estado según el código semántico.

## Do's and Don'ts

- Usa el morado para todo modelo aprendido de los datos, incluidos los modelos de lenguaje y los híbridos.
- Ancla el titular arriba y corta a mano las líneas de titulares y tarjetas.
- Une con un espacio de no separación cada cifra con su unidad y cada abreviatura con su número.
- Mantén el texto a 20 pt o más (12 pt solo en el pie de fuente).
- Haz que el loro sea el nodo más grande del esquema y conserva la escala del esquema en todas las piezas.
- No uses el rojo para nada que no sea un fallo demostrado, ni el ámbar para avisos.
- No pongas sombras, bandas de acento ni filetes bajo el titular.
- No tapes un borde del marco con un recuadro de fondo para colocar un rótulo, salvo el hueco centrado del borde inferior.
- No mezcles radios fuera de 0, 16 px y píldora.
- No escales un icono a un tamaño intermedio: usa 64, 96 o 120 px.
- No dejes rayas de relleno ni objetos sin significado en una ilustración.
