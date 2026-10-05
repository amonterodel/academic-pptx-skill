# Personaje: el loro estocástico

Mascota de la ponencia «Qué puede aportar realmente la IA a la TDM y a la farmacocinética clínica» (71 Congreso SEFH). Es la referencia canónica del personaje: cualquier ilustración nueva, sea a mano, generada por IA o vectorial, debe cumplir esta ficha. Los colores salen de `../DESIGN.md` (paleta `illus-*`).

## Concepto

Un loro robótico con bata de farmacia. Encarna al **modelo de lenguaje**: habla de farmacocinética con fluidez y una seguridad excesiva, pero no calcula. El nombre alude al «loro estocástico», la metáfora del modelo que encadena palabras probables sin entenderlas. Resulta simpático, no ridículo: un colega brillante que se pasa de listo.

## Anatomía (de arriba abajo)

| Parte | Descripción | Color |
|---|---|---|
| Cresta | Tres placas metálicas alargadas en abanico hacia arriba y atrás; la punta de cada una, en morado | Metal medio `#B9C3CD`; puntas `#AD3B94` |
| Cabeza | Redondeada y algo mayor de lo natural (proporción de mascota); una costura curva en la nuca con cuatro remaches | Metal medio `#B9C3CD` |
| Placa facial | Placa clara y lisa alrededor del ojo, como el parche blanco de un guacamayo | Metal claro `#E4E9EE` |
| Ojo | Una cuenca oscura con una luz cian en el centro, un punto blanco de brillo y un halo cian suave alrededor | Cuenca `#1C2833`; luz `#5FF0EE` |
| Ceja | Placa metálica oscura e inclinada sobre el ojo. En el gesto de suficiencia se levanta por fuera y el párpado metálico cubre media pupila | `#4E5B68` |
| Pico | Grande y ganchudo, de loro, en grafito; la mandíbula inferior es más pequeña y algo más clara | Superior `#46525F`; inferior `#6C7884` |
| Bisagra | Un tornillo visible en la unión del pico con la cara | Metal medio con centro oscuro |
| Cuello | Dos anillos metálicos segmentados entre la cabeza y el cuello de la bata | `#B9C3CD` y `#8794A1` |
| Pecho | Placa metálica clara con tres ranuras horizontales, visible en la abertura en V de la bata | `#E4E9EE` |
| Bata | Bata de farmacia blanca, hasta media pierna, con solapas, dos botones grises y una sombra lateral muy suave | `#FFFFFF`; sombra `#E3EAF0` |
| Identificación | Tarjeta turquesa rectangular en el pecho, a la izquierda de quien mira en la vista de frente, con una raya oscura (sin texto) | `#00B3B2` |
| Bolsillo | Bolsillo en el pecho, a la derecha de quien mira, con un bolígrafo morado asomando | Bolígrafo `#AD3B94` |
| Alas | Salen de las mangas de la bata; en el puño, un anillo metálico (muñeca articulada); las «manos» son tres plumas metálicas planas que hacen de dedos | `#8794A1` y `#B9C3CD` |
| Hombros | Un tornillo visible en el hombro, sobre la manga | Metal medio |
| Cola | Dos o tres plumas metálicas largas y ahusadas que asoman bajo la bata, inclinadas hacia atrás y abajo, con estrías finas | `#8794A1` y `#B9C3CD` |
| Patas | Dos varillas metálicas con la rodilla atornillada (círculo con centro oscuro) | `#8794A1` |
| Pies | Zigodáctilos, como los de un loro: dos dedos adelante y uno atrás, gruesos y curvos | `#4E5B68` |

## Estilo gráfico

- **Ilustración plana vectorial.** Contorno de tinta `#263445` de grosor constante y uniforme (unas 4 unidades por cada 120 de altura del personaje), con juntas redondeadas.
- **Rellenos lisos** de la tabla. Sin degradados, texturas, brillos realistas ni volumen 3D; el único efecto es el halo cian del ojo.
- **Proporciones.** Unas tres cabezas de altura. La bata ocupa la mitad central del cuerpo; las patas y la cola, el cuarto inferior.
- **Mira a la derecha** en su postura de referencia (vista de tres cuartos).
- **Coherencia con los iconos de línea** del proyecto: misma tinta y mismo grosor de trazo.

## Variantes que ya existen en el proyecto

| Variante | Archivo | Uso |
|---|---|---|
| Neutra en color | `examples/sefh-71-ia-tdm/assets/loro-color.png` | Esquemas |
| Segura de sí misma | `assets/loro-seguro.png` | Señala con el ala, ceja levantada y párpado a media asta |
| Atenuada | `assets/loro-gray.png` | Esquemas secundarios |
| Radiografía | `assets/loro-xray.png` | Líneas azul claro `#A9DBFF` con resplandor sobre fondo `#0E1B2C` |

Origen vectorial: función `parrot()` en `examples/sefh-71-ia-tdm/build_assets.py`.

## Personalidad y gestos

- **Neutro:** de pie, erguido, ojo abierto y luminoso, alas recogidas.
- **Seguro de sí mismo:** pecho fuera, cabeza ligeramente alzada, ceja levantada, párpado a media asta y un ala señalando con suficiencia.
- **Hablando:** pico entreabierto, ala que gesticula y un bocadillo vacío.
- **Pillado:** ojo muy abierto, cresta algo caída y una gota de sudor metálica (para fallos y errores de cálculo).

## Prohibido

- Texto, logotipos o marcas reales en la bata o en la tarjeta.
- Plumas de colores naturales: el cuerpo es metálico y gris.
- Rasgos humanos (manos, dientes, cejas de pelo).
- Gafas, estetoscopio u otros accesorios fuera de esta ficha.
- Sombras proyectadas en el suelo.

## Prompt para generar la hoja de personaje (ChatGPT Images 2)

```
Crea una hoja de personaje profesional (model sheet / turnaround) de una mascota para una ponencia científica de farmacia hospitalaria. Formato horizontal 3:2, fondo blanco liso, sin sombras proyectadas.

EL PERSONAJE: «el loro estocástico», un loro robótico con bata blanca de farmacia que representa a un modelo de lenguaje: habla de farmacocinética con fluidez y demasiada seguridad, pero no sabe calcular. Simpático y algo creído, nunca ridículo.

ESTILO: ilustración plana vectorial, como un icono editorial moderno. Contorno de tinta azul noche #263445 de grosor constante en todo el dibujo, juntas redondeadas, rellenos lisos sin degradados, sin texturas, sin brillos realistas, sin 3D. Proporción de mascota: unas tres cabezas de altura, cabeza algo grande.

ANATOMÍA EXACTA (debe ser idéntica en todas las vistas):
- Cresta: tres placas metálicas alargadas en abanico hacia arriba y atrás, gris medio #B9C3CD, con la punta de cada placa en morado #AD3B94.
- Cabeza redondeada gris medio #B9C3CD con una costura curva en la nuca y cuatro remaches.
- Placa facial lisa y clara #E4E9EE alrededor del ojo.
- Ojo: cuenca oscura #1C2833, luz cian #5FF0EE en el centro, punto blanco de brillo y halo cian suave alrededor.
- Pico de loro grande y ganchudo en grafito #46525F, mandíbula inferior más pequeña #6C7884, tornillo visible en la bisagra del pico.
- Cuello: dos anillos metálicos segmentados visibles entre la cabeza y la bata.
- Bata de farmacia blanca hasta media pierna, con solapas, dos botones grises y abertura en V que deja ver una placa metálica clara en el pecho con tres ranuras horizontales.
- En la vista de frente, a la izquierda de quien mira, una tarjeta de identificación turquesa #00B3B2 sin texto sobre el pecho; a la derecha de quien mira, un bolsillo con un bolígrafo morado #AD3B94 asomando.
- Alas dentro de las mangas; en cada puño, un anillo metálico articulado y tres plumas metálicas planas que hacen de dedos (#8794A1 y #B9C3CD). Tornillo visible en el hombro.
- Cola: dos o tres plumas metálicas largas y ahusadas que asoman por detrás bajo la bata, inclinadas hacia atrás y abajo, con estrías finas.
- Patas: varillas metálicas grises #8794A1 con la rodilla atornillada; pies de loro con dos dedos adelante y uno atrás, gruesos y curvos, gris oscuro #4E5B68.

COMPOSICIÓN DE LA HOJA:
Fila superior, de izquierda a derecha, el personaje de cuerpo entero en postura neutra (erguido, alas recogidas, ojo abierto) y a la misma altura exacta, con líneas guía horizontales finas en gris claro a la altura de la cresta, el ojo, el bajo de la bata y los pies:
1. Frente
2. Tres cuartos de frente, mirando a la derecha
3. Perfil derecho
4. Tres cuartos de espalda
5. Espalda (se ven la costura de la nuca, la espalda de la bata y la cola)
Bajo cada vista, un rótulo pequeño en mayúsculas grises con este texto exacto: FRENTE · TRES CUARTOS · PERFIL · TRES CUARTOS ESPALDA · ESPALDA.

Fila inferior izquierda, tres bustos de expresión a la misma escala, con rótulo debajo: NEUTRO (ojo abierto y luminoso); SEGURO DE SÍ MISMO (pecho fuera, cabeza alzada, placa de ceja oscura levantada, párpado metálico cubriendo media pupila, un ala señalando hacia arriba con suficiencia); HABLANDO (pico entreabierto, ala gesticulando y un bocadillo de diálogo vacío, sin texto).

Fila inferior derecha, tres detalles ampliados dentro de círculos con fino borde gris: el ojo con su halo cian, la cresta con las puntas moradas y un pie con su rodilla atornillada. Debajo, una fila de muestras de color planas, cuadradas, con su código hexadecimal en gris: #B9C3CD, #E4E9EE, #8794A1, #4E5B68, #46525F, #5FF0EE, #AD3B94, #00B3B2, #263445.

PROHIBIDO: plumas de colores naturales, rasgos humanos (manos, dientes, cejas de pelo), gafas, estetoscopio, logotipos, marcas, texto en la bata o en la tarjeta, fondos decorativos, sombras en el suelo, cualquier texto distinto de los rótulos indicados.

Antes de terminar, comprueba que el personaje es idéntico en todas las vistas (número de placas de la cresta, color de cada pieza, posición de la tarjeta y del bolsillo, número de dedos en pies y alas) y que todos los rótulos están escritos sin errores.
```
