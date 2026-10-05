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
pip install python-pptx cairosvg pillow lxml pyyaml
python3 build_assets.py
python3 build_deck.py ruta/a/71-congreso-plantilla-ponencias.pptx salida/ponencia-ia-tdm-montero.pptx
```

Sistema de diseño: todos los valores visuales salen de [`design-systems/sefh/DESIGN.md`](../../design-systems/sefh/DESIGN.md). Los scripts lo leen a través de `sefh_tokens.py`, así que un cambio de color, radio o tamaño se hace en un solo sitio.

Decisiones de maquetación:

- Lienzo de 13,333 × 7,5 in (16:9). La plantilla viene a 10 × 5,625 in, y a ese tamaño los mínimos de letra pedidos (titular de 32 pt, cuerpo de 20 pt) no caben. Los fondos de la plantilla se escalan sin pérdida.
- Tipografía Calibri, la del tema de la plantilla.
- Código de color (ver `DESIGN.md › Colors`):

  | Color | Significado |
  |---|---|
  | Morado | Todo modelo aprendido de los datos: aprendizaje automático, redes neuronales, modelos de lenguaje e híbridos |
  | Verde | Herramienta validada y TDM |
  | Azul | La persona |
  | Turquesa | Énfasis editorial |
  | Rojo | Solo fallos demostrados |
  | Ámbar | Solo rendimiento parcial |

- Tras la auditoría de diseño:
  - titulares anclados arriba y cortados a mano;
  - un único esquema de cinco piezas a escala fija, con el loro como nodo mayor;
  - componentes comunes con dos radios de esquina (16 px y píldora) y sin sombras;
  - rótulos de la radiografía pegados a sus flechas;
  - escalera con perfil de huellas;
  - envase vertical y ficha plegada en tres paneles;
  - espacios de no separación entre cada cifra y su unidad.
