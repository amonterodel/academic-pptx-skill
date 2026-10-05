# Sistema de diseño SEFH

`DESIGN.md` describe el sistema visual de los materiales del 71 Congreso de la SEFH en el formato abierto [DESIGN.md de Google Labs](https://github.com/google-labs-code/design.md):

- **Bloque YAML inicial.** Los tokens normativos: colores con significado, tipografía, rejilla, radios, grosores y componentes.
- **Cuerpo en Markdown.** El porqué de cada decisión y las reglas de uso.

Los títulos de sección van en inglés (`Overview`, `Colors`…) porque son las palabras clave del formato. El contenido está en castellano.

## Usarlo en otro trabajo

| Destino | Cómo |
|---|---|
| Un agente de IA (Claude Code, Stitch…) | Copia `DESIGN.md` a la raíz del proyecto o cítalo en las instrucciones. |
| Python | `from sefh_tokens import load; T = load(); T.color("ml")`. Ejemplo completo en `examples/sefh-71-ia-tdm/build_deck.py`. |
| CSS o Tailwind | `npx @google/design.md export --format css-vars DESIGN.md` (o `css-tailwind`). |
| Variables de diseño W3C | `npx @google/design.md export --format dtcg DESIGN.md` |

Las medidas están en píxeles de un lienzo de 1920 × 1080. En una diapositiva de 13,333 × 7,5 in, 1 pt equivale a 2 px.

## Validar

```bash
npx @google/design.md lint DESIGN.md
```

Estado actual: 0 errores. Quedan 17 avisos `orphaned-tokens` aceptados: la paleta `illus-*`, que consume el generador de ilustraciones y no un componente, y los colores de marca de los que derivan los semánticos.
