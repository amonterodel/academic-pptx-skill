# Ponencia «Qué puede aportar realmente la IA a la TDM y a la farmacocinética clínica»

Curso precongreso del 71 Congreso Nacional SEFH. Nueve diapositivas fijas (sin animaciones ni transiciones) maquetadas sobre la plantilla oficial `71-congreso-plantilla-ponencias.pptx`.

| Archivo | Qué es |
|---|---|
| `salida/ponencia-ia-tdm-montero.pptx` | Presentación editable (todo el texto es texto) |
| `salida/vista-previa.pdf` | Vista previa renderizada con LibreOffice |
| `assets/*.png` | Ilustraciones sueltas (loro, iconos, farmacéutico, ficha del caso) en variantes color, gris y radiografía |
| `build_assets.py` | Genera las ilustraciones (SVG → PNG) |
| `build_deck.py` | Monta la presentación sobre la plantilla |

Reconstruir (la plantilla SEFH no se incluye en el repositorio):

```bash
pip install python-pptx cairosvg pillow lxml
python3 build_assets.py
python3 build_deck.py ruta/a/71-congreso-plantilla-ponencias.pptx salida/ponencia-ia-tdm-montero.pptx
```

Decisiones de maquetación:

- Lienzo de 13,333 × 7,5 in (16:9). La plantilla venía a 10 × 5,625 in, tamaño al que los mínimos de letra pedidos (titular de 32 pt, cuerpo de 20 pt) no caben; los fondos de la plantilla se escalan sin pérdida.
- Tipografía Calibri, la del tema de la plantilla.
- Colores muestreados de la plantilla: lima `C3BF24`, verde `5BB46C`, turquesa `00B3B2`, morado `AD3B94`, azul `4A73A0`. Morado = aprendizaje automático; verde = TDM y herramienta validada; rojo `D42A3B` solo para fallos; ámbar solo para el estado «interpreta» del modelo (diapositiva 7).
