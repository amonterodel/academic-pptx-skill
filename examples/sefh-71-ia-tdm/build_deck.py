"""Maqueta la ponencia sobre la plantilla SEFH «71-congreso-plantilla-ponencias.pptx».

    python3 build_deck.py <plantilla.pptx> <salida.pptx>

Trabaja sobre el propio paquete de la plantilla (patrón, diseño, tema y fondos),
de modo que el resultado se edita en PowerPoint como cualquier archivo SEFH.

Todos los valores de diseño (colores, tipografía, rejilla, radios, grosores y
componentes) se leen de design-systems/sefh/DESIGN.md: este archivo solo decide
la composición de cada diapositiva. Coordenadas en píxeles del lienzo 1920 × 1080.
"""

import copy
import random
import sys
from pathlib import Path

from lxml import etree
from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_LINE
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Pt

HERE = Path(__file__).parent
ASSETS = HERE / "assets"
sys.path.insert(0, str(HERE.parents[1] / "design-systems" / "sefh"))
from sefh_tokens import load  # noqa: E402

T = load()

# --- Lienzo y rejilla (DESIGN.md › spacing) -----------------------------------
SLIDE_W, SLIDE_H = 12192000, 6858000                  # 13,333 × 7,5 in
EMU = SLIDE_W / T.px("canvas-width")                  # EMU por píxel del lienzo
CANVAS_W = T.px("canvas-width")
MARGIN, GUTTER, COLW = T.px("margin"), T.px("gutter"), T.px("column")
TITLE_Y, TITLE_H = T.px("title-top"), T.px("title-height")
CONTENT_Y, CONTENT_B = T.px("content-top"), T.px("content-bottom")
SOURCE_Y, SOURCE_H = T.px("source-top"), T.px("source-height")
PAD, GAP = T.px("card-padding"), T.px("stack-gap")
R_MD = T.radius("md")
ICON_SM, ICON_MD, ICON_LG = T.px("icon-sm"), T.px("icon-md"), T.px("icon-lg")
# Grosores: tokens en px del lienzo -> puntos de PowerPoint
W_THIN, W_MD, W_STRONG = (T.px(k) / 2 for k in ("stroke-thin", "stroke-md", "stroke-strong"))

# --- Colores (DESIGN.md › colors) ---------------------------------------------
C = T.color
INK, GRAY, WHITE, SURFACE, RULE = C("primary"), C("secondary"), C("neutral"), C("surface"), C("outline")
ML, ML_D, ML_M, ML_S, ML_T = C("ml"), C("ml-dark"), C("ml-mid"), C("ml-soft"), C("ml-tint")
TOOL, TOOL_D, TOOL_T = C("tool"), C("tool-dark"), C("tool-tint")
HUMAN, HUMAN_D = C("human"), C("human-dark")
EMPH_D = C("emphasis-dark")
STRUCT = C("structure")
ERROR = C("error")
XBG, XLINE, XSOFT, MUTED = C("xray-surface"), C("xray-line"), C("xray-soft"), C("muted")
CHALKBOARD, CHALK = C("illus-chalkboard"), C("illus-chalk")

NB = " "   # espacio de no separación


def px(v):
    return Emu(int(round(v * EMU)))


def col(n):
    """x del borde izquierdo de la columna n (1-12)."""
    return MARGIN + (n - 1) * (COLW + GUTTER)


def cols(a, b):
    """(x, ancho) del tramo de columnas a..b."""
    return col(a), col(b) + COLW - col(a)


def rgb(h):
    return RGBColor.from_string(h)


def text_width(t, pt=20, bold=False):
    """Ancho del texto en px del lienzo (métrica de Calibri vía Carlito)."""
    try:
        from PIL import ImageFont
        f = ("/usr/share/fonts/truetype/crosextra/Carlito-Bold.ttf" if bold else
             "/usr/share/fonts/truetype/crosextra/Carlito-Regular.ttf")
        return ImageFont.truetype(f, int(pt * 20)).getlength(t) / 10
    except OSError:
        return len(t) * pt * (1.0 if bold else 0.95)


# --- Primitivas -----------------------------------------------------------------

def _strip_style(shape):
    st = shape._element.find(qn("p:style"))
    if st is not None:
        shape._element.remove(st)


def _name(shape, name):
    if name:
        shape._element.xpath("./*[1]/p:cNvPr")[0].set("name", name)


def _add_run(p, text, o, size, color, bold, italic):
    r_ = p.add_run()
    r_.text = text
    f = r_.font
    f.size = Pt(o.get("size", size))
    f.bold = o.get("bold", bold)
    f.italic = o.get("italic", italic)
    f.color.rgb = rgb(o.get("color", color))
    rpr = r_._r.get_or_add_rPr()
    rpr.set("lang", "es-ES")
    if o.get("sub"):
        rpr.set("baseline", "-25000")


def fill_text(tf, paras, size=20, color=INK, bold=False, italic=False, align="l",
              anchor="t", spacing=None, margins=(0, 0, 0, 0)):
    """Rellena un marco de texto.

    paras: lista de párrafos; cada uno es un str, una lista de runs
    (str | (texto, {opciones})) o un dict {"runs": [...], "align", "after", ...}.
    Un "\\n" dentro de un run es un salto de línea manual (mismo párrafo).
    """
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    l, t, r, b = margins
    tf.margin_left, tf.margin_top, tf.margin_right, tf.margin_bottom = (px(l), px(t), px(r), px(b))
    tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[anchor]
    if isinstance(paras, str):
        paras = [paras]
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        popts = para if isinstance(para, dict) else {}
        runs = para["runs"] if isinstance(para, dict) else para
        if isinstance(runs, str):
            runs = [runs]
        p.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[
            popts.get("align", align)]
        if "after" in popts:
            p.space_after = Pt(popts["after"])
        if popts.get("spacing", spacing):
            p.line_spacing = popts.get("spacing", spacing)
        for run in runs:
            txt, o = (run, {}) if isinstance(run, str) else run
            o = {**{k: popts[k] for k in ("size", "color", "bold", "italic") if k in popts}, **o}
            for j, piece in enumerate(txt.split("\n")):
                if j:
                    p.add_line_break()
                if piece:
                    _add_run(p, piece, o, size, color, bold, italic)
    return tf


def text(slide, x, y, w, h, paras, name=None, **kw):
    tb = slide.shapes.add_textbox(px(x), px(y), px(w), px(h))
    _name(tb, name)
    fill_text(tb.text_frame, paras, **kw)
    return tb


def shape(slide, x, y, w, h, fill=None, line=None, lw=W_THIN, dash=None, radius=None,
          kind=MSO_SHAPE.RECTANGLE, name=None, paras=None, **tkw):
    """Forma con relleno plano. radius: px del lienzo o 'full' (píldora)."""
    if radius is not None and kind == MSO_SHAPE.RECTANGLE:
        kind = MSO_SHAPE.ROUNDED_RECTANGLE
    sp = slide.shapes.add_shape(kind, px(x), px(y), px(w), px(h))
    _strip_style(sp)
    _name(sp, name)
    if fill:
        sp.fill.solid()
        sp.fill.fore_color.rgb = rgb(fill)
    else:
        sp.fill.background()
    if line:
        sp.line.color.rgb = rgb(line)
        sp.line.width = Pt(lw)
        if dash:
            sp.line.dash_style = dash
    else:
        sp.line.fill.background()
    if radius is not None:
        sp.adjustments[0] = 0.5 if radius == "full" else min(0.5, radius / min(w, h))
    if paras is not None:
        fill_text(sp.text_frame, paras, **tkw)
    return sp


def _line_ends(ln, head=None, tail=None):
    for tag_, kind in (("a:headEnd", head), ("a:tailEnd", tail)):
        if kind:
            el = etree.SubElement(ln, qn(tag_))
            el.set("type", kind)
            el.set("w", "med")
            el.set("len", "med")


def line(slide, x1, y1, x2, y2, color=INK, lw=W_MD, dash=None, head=None, tail=None, name=None):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, px(x1), px(y1), px(x2), px(y2))
    _strip_style(c)
    _name(c, name)
    c.line.color.rgb = rgb(color)
    c.line.width = Pt(lw)
    if dash:
        c.line.dash_style = dash
    _line_ends(c.line._get_or_add_ln(), head, tail)
    return c


def polyline(slide, pts, color=INK, lw=W_MD, name="Perfil"):
    ff = slide.shapes.build_freeform(px(pts[0][0]), px(pts[0][1]))
    ff.add_line_segments([(px(x), px(y)) for x, y in pts[1:]], close=False)
    sh = ff.convert_to_shape()
    _strip_style(sh)
    sh.fill.background()
    sh.line.color.rgb = rgb(color)
    sh.line.width = Pt(lw)
    _name(sh, name)
    return sh


def polygon(slide, pts, fill, line_color=INK, lw=W_MD, name=None):
    ff = slide.shapes.build_freeform(px(pts[0][0]), px(pts[0][1]))
    ff.add_line_segments([(px(x), px(y)) for x, y in pts[1:]], close=True)
    sh = ff.convert_to_shape()
    _strip_style(sh)
    sh.fill.solid()
    sh.fill.fore_color.rgb = rgb(fill)
    sh.line.color.rgb = rgb(line_color)
    sh.line.width = Pt(lw)
    _name(sh, name)
    return sh


def curve(slide, p0, c1, c2, p1, color=INK, lw=W_MD, tail="triangle", name="Flecha curva"):
    """Flecha curva (Bézier cúbica) como forma libre editable."""
    xs = [p[0] for p in (p0, c1, c2, p1)]
    ys = [p[1] for p in (p0, c1, c2, p1)]
    x0, y0 = min(xs), min(ys)
    w, h = max(max(xs) - x0, 1), max(max(ys) - y0, 1)

    def pt(p):
        return f'<a:pt x="{int((p[0] - x0) * EMU)}" y="{int((p[1] - y0) * EMU)}"/>'

    sid = slide.shapes._next_shape_id
    xml = f"""
<p:sp xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
      xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
  <p:nvSpPr><p:cNvPr id="{sid}" name="{name}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="{int(x0 * EMU)}" y="{int(y0 * EMU)}"/><a:ext cx="{int(w * EMU)}" cy="{int(h * EMU)}"/></a:xfrm>
    <a:custGeom><a:avLst/><a:gdLst/><a:ahLst/><a:cxnLst/><a:rect l="0" t="0" r="r" b="b"/>
      <a:pathLst><a:path w="{int(w * EMU)}" h="{int(h * EMU)}" fill="none">
        <a:moveTo>{pt(p0)}</a:moveTo><a:cubicBezTo>{pt(c1)}{pt(c2)}{pt(p1)}</a:cubicBezTo>
      </a:path></a:pathLst></a:custGeom>
    <a:noFill/>
    <a:ln w="{int(Pt(lw))}" cap="rnd"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill>
      <a:round/><a:tailEnd type="{tail}" w="med" len="med"/></a:ln>
  </p:spPr>
</p:sp>"""
    el = etree.fromstring(xml)
    slide.shapes._spTree.append(el)
    return el


def image(slide, name, x, y, w, h, align="c", valign="m", rotation=0, label=None):
    """Coloca un PNG ajustado dentro de la caja sin deformarlo; devuelve la caja real."""
    path = ASSETS / f"{name}.png"
    iw, ih = Image.open(path).size
    s = min(w / iw, h / ih)
    dw, dh = iw * s, ih * s
    dx = {"l": 0, "c": (w - dw) / 2, "r": w - dw}[align]
    dy = {"t": 0, "m": (h - dh) / 2, "b": h - dh}[valign]
    pic = slide.shapes.add_picture(str(path), px(x + dx), px(y + dy), px(dw), px(dh))
    _name(pic, label or name)
    pic._element.xpath("./p:nvPicPr/p:cNvPr")[0].set("descr", label or name)
    if rotation:
        pic.rotation = rotation
    return x + dx, y + dy, dw, dh


# --- Componentes (DESIGN.md › components) ----------------------------------------

def headline(slide, paras, closing=False, align="l"):
    t = T.type("headline-display" if closing else "headline-lg")
    return text(slide, MARGIN, TITLE_Y, CANVAS_W - 2 * MARGIN, TITLE_H, paras, size=t["pt"],
                color=INK, align=align, anchor="t", spacing=0.92, name="Titular")


def source(slide, s, two_lines=False):
    t = T.type("caption")
    y, h = (980, 56) if two_lines else (SOURCE_Y, SOURCE_H)
    return text(slide, MARGIN, y, CANVAS_W - 2 * MARGIN, h, s, size=t["pt"], color=GRAY,
                anchor="b", name="Fuente")


def card(slide, x, y, w, h, kind="card", name="Tarjeta"):
    c = T.comp(kind)
    border = TOOL if kind == "card-tool" else None
    return shape(slide, x, y, w, h, fill=c["backgroundColor"], line=border, lw=W_MD,
                 radius=R_MD, name=name)


def tag(slide, x, y, label, kind, w=None, h=None, center=False, lines=1, name="Etiqueta"):
    """Etiqueta de estado: ancho = texto + 60 px; alto 46 px por línea (sin autoajuste)."""
    base, c = T.comp("tag"), T.comp(kind)
    t = T.type("label-md")
    h = h or (base["height"] if lines == 1 else 2 * base["height"])
    w = w or text_width(label, t["pt"], True) + 2 * base["padding"]
    if center:
        x -= w / 2
    shape(slide, x, y, w, h, fill=c["backgroundColor"], radius="full", name=name,
          paras=[label], size=t["pt"], bold=True, color=c["textColor"], align="c", anchor="m",
          margins=(base["padding"] / 2, 0, base["padding"] / 2, 0))
    return x, y, w, h


def arrow(slide, x1, y1, x2, y2, both=False, color=INK, supervise=False, name="Flecha"):
    return line(slide, x1, y1, x2, y2, color=HUMAN if supervise else color, lw=W_MD,
                dash=MSO_LINE.ROUND_DOT if supervise else None,
                head="triangle" if both else None, tail="triangle", name=name)


def frame(slide, x, y, w, h, color=INK, name="Arnés"):
    return shape(slide, x, y, w, h, line=color, lw=W_MD, dash=MSO_LINE.DASH, radius=R_MD, name=name)


def icon_disc(slide, icon, cx, cy, d=ICON_LG, fill=WHITE):
    shape(slide, cx - d / 2, cy - d / 2, d, d, fill=fill, kind=MSO_SHAPE.OVAL, name=f"Fondo {icon}")
    image(slide, icon, cx - ICON_SM / 2, cy - ICON_SM / 2, ICON_SM, ICON_SM)


# --- Esquema de las cinco piezas (diapositivas 6, 7 y 9) --------------------------
FRAME_X, FRAME_W = cols(2, 11)
OFF = 511                                  # distancia de las piezas laterales al centro
PARROT_H, FICHA_H = 236, 150               # el loro es el nodo mayor (≈ 1,5×)


def scheme(slide, variant, fy, k=1.0, arrow_color=INK):
    """Dibujos y flechas del esquema. Devuelve la geometría para colocar rótulos."""
    cx = [960 - OFF * k, 960, 960 + OFF * k]
    ptop = fy + 24 * k
    ph = PARROT_H * k
    mid = ptop + ph / 2
    image(slide, f"loro-{variant}", 960 - ph / 2, ptop, ph, ph, label="Loro robótico (modelo de lenguaje)")
    fh = FICHA_H * k
    image(slide, f"ficha-caso-{variant}", cx[0] - fh / 2, mid - fh / 2, fh, fh, label="Ficha del caso")
    s_ = ICON_SM * k
    stack = 3 * s_ + 2 * 14 * k
    for i, ic in enumerate(("curva", "campana", "red")):
        image(slide, f"icono-{ic}-{variant}", cx[2] - s_ * 0.75, mid - stack / 2 + i * (s_ + 14 * k),
              s_ * 1.5, s_, label=f"Icono {ic}")
    arrow(slide, cx[0] + 80 * k, mid, 960 - 78 * k, mid, color=arrow_color, name="Contexto → modelo")
    arrow(slide, 960 + 78 * k, mid, cx[2] - 64 * k, mid, both=True, color=arrow_color,
          name="Modelo ↔ herramientas")
    return {"cx": cx, "mid": mid, "ptop": ptop, "bottom": ptop + ph}


def pharmacist(slide, variant, y, h, fy, ptop):
    """Farmacéutico centrado sobre el esquema, con flecha de supervisión al loro."""
    w = h * 1.146
    image(slide, f"farmaceutico-{variant}", 960 - w / 2, y, w, h, label="Farmacéutico con pluma")
    arrow(slide, 960, y + h + 4, 960, ptop - 6, supervise=True,
          color=XLINE if variant == "xray" else HUMAN, name="Supervisión")
    return 960 + w / 2


# --- Diapositivas -------------------------------------------------------------------

def slide_cover(s):
    """Rellena los cuadros de texto de la portada de la plantilla."""
    sp = {shp.name: shp for shp in s.shapes}

    def retext(shp, paras, x, y, w, h):
        shp.left, shp.top, shp.width, shp.height = px(x), px(y), px(w), px(h)
        tf = shp.text_frame
        bp = tf._txBody.find(qn("a:bodyPr"))
        for child in list(bp):
            bp.remove(child)                              # tamaño fijo, sin autoajuste
        p0 = tf.paragraphs[0]
        rpr_tpl = copy.deepcopy(p0.runs[0]._r.find(qn("a:rPr")))
        for r in list(p0._p.findall(qn("a:r"))):
            p0._p.remove(r)
        txt, opts = paras
        p0.alignment = PP_ALIGN.CENTER
        if "spacing" in opts:
            p0.line_spacing = opts["spacing"]
        for j, piece in enumerate(txt.split("\n")):
            if j:
                p0.add_line_break()
            r = p0.add_run()
            r.text = piece
            rpr = copy.deepcopy(rpr_tpl)
            old = r._r.find(qn("a:rPr"))
            if old is not None:
                r._r.remove(old)
            r._r.insert(0, rpr)
            rpr.set("lang", "es-ES")
            rpr.set("sz", str(int(opts["size"] * 100)))
            for k_, attr in (("bold", "b"), ("italic", "i")):
                if k_ in opts:
                    rpr.set(attr, "1" if opts[k_] else "0")
            if "color" in opts:
                for f in rpr.findall(qn("a:solidFill")):
                    rpr.remove(f)
                sf = etree.Element(qn("a:solidFill"))
                etree.SubElement(sf, qn("a:srgbClr")).set("val", opts["color"])
                ln = rpr.find(qn("a:ln"))
                (ln.addnext(sf) if ln is not None else rpr.insert(0, sf))
        tf.word_wrap = True

    retext(sp["TextBox 12"], ("CURSO PRECONGRESO · INTELIGENCIA ARTIFICIAL APLICADA A LA "
                              "FARMACOCINÉTICA CLÍNICA", {"size": 20, "bold": True}),
           100, 360, 1720, 56)
    retext(sp["TextBox 4"], ("«Qué puede aportar realmente la IA\n"
                             "a la TDM y a la farmacocinética clínica»",
                             {"size": 36, "bold": True, "spacing": 0.95}), 200, 440, 1520, 180)
    retext(sp["TextBox 6"], ("ALFREDO MONTERO DELGADO", {"size": 24, "bold": True, "color": INK}),
           260, 690, 1400, 50)
    retext(sp["TextBox 7"], (f"Farmacéutico especialista en Farmacia{NB}Hospitalaria ·\n"
                             f"Hospital Universitario Nuestra{NB}Señora{NB}de{NB}Candelaria · "
                             f"Grupo{NB}DIGIFHAR{NB}(SEFH)", {"size": 20, "color": GRAY}),
           200, 752, 1520, 110)


def slide_hook(s):
    headline(s, [[("ChatGPT sabe hablar de farmacocinética,\npero no ", {}),
                  ("hacer", {"bold": True, "color": EMPH_D}), (" farmacocinética.", {})]])

    x0, w0 = cols(1, 7)
    floor_y = 972
    line(s, x0 + 10, floor_y, x0 + w0, floor_y, color=RULE, lw=W_THIN, name="Suelo")
    # Pizarra con fórmulas impecables (texto editable)
    bx, by, bw, bh = 480, 300, 610, 318
    shape(s, bx, by, bw, bh, fill=CHALKBOARD, line=INK, lw=W_MD, radius=R_MD, name="Pizarra")
    shape(s, bx + 40, by + bh, bw - 80, 12, fill=C("illus-metal-2"), line=INK, lw=W_THIN, name="Repisa")
    shape(s, bx + 430, by + bh - 10, 38, 10, fill=WHITE, line=INK, lw=W_THIN, name="Tiza")
    text(s, bx + 50, by + 24, bw - 90, bh - 40, [
        ["CL = k", ("e", {"sub": True}), " · V", ("d", {"sub": True})],
        ["t½ = 0,693 / k", ("e", {"sub": True})],
        ["V", ("d", {"sub": True}), " = Dosis / C", ("0", {"sub": True})],
        ["k", ("e", {"sub": True}), " = ln(C", ("1", {"sub": True}), " / C", ("2", {"sub": True}),
         ") / Δt"],
    ], size=26, color=CHALK, italic=True, spacing=1.0, anchor="m", name="Fórmulas")
    # Loro muy seguro de sí mismo
    image(s, "loro-seguro", 90, 392, 380, floor_y - 392 + 6, valign="b",
          label="Loro robótico con bata señalando la pizarra")
    # Bocadillo alineado con la pizarra; cola corta hacia el pico
    bub_x, bub_y, bub_w, bub_h = bx, 650, 560, 130
    bub = shape(s, bub_x, bub_y, bub_w, bub_h, fill=WHITE, line=INK, lw=W_MD,
                kind=MSO_SHAPE.ROUNDED_RECTANGULAR_CALLOUT, name="Bocadillo",
                paras=["aclaramiento… volumen de distribución… semivida…"],
                size=22, italic=True, color=INK, anchor="m", margins=(28, 10, 28, 10))
    tip = (bub_x - 34, bub_y - 26)                    # cola corta hacia el pico
    bub.adjustments[0] = (tip[0] - (bub_x + bub_w / 2)) / bub_w
    bub.adjustments[1] = (tip[1] - (bub_y + bub_h / 2)) / bub_h
    # Calculadora boca abajo, tirada en el suelo junto al loro
    image(s, "icono-calculadora", 520, floor_y - 110, 110, 110, valign="b", rotation=200,
          label="Calculadora boca abajo en el suelo")

    # Tarjeta de dato: columnas 8-12, centrada en vertical
    cx, cw = cols(8, 12)
    ch = 600
    cy = CONTENT_Y + (CONTENT_B - CONTENT_Y - ch) / 2
    card(s, cx, cy, cw, ch, kind="card-stat", name="Tarjeta dato")
    t = T.type("stat-display")
    text(s, cx + 48, cy + 24, cw - 96, 214, f"37{NB}%", size=t["pt"], bold=True, color=ML,
         anchor="m", name="Cifra")
    text(s, cx + 48, cy + 250, cw - 96, 214,
         f"de las predicciones de valle de vancomicina de ChatGPT quedaron a ±2{NB}mg/L "
         f"del valor medido", size=T.type("body-lg")["pt"], color=INK, name="Lectura")
    line(s, cx + 48, cy + 474, cx + cw - 48, cy + 474, color=ML_S, lw=W_THIN)
    text(s, cx + 48, cy + 490, cw - 96, 100,
         f"717 predicciones · 239{NB}ingresos{NB}en{NB}UCI · Grok: 29{NB}%", size=20,
         color=GRAY, name="Detalle")
    source(s, "Ishaqui et al., Expert Rev Anti Infect Ther, 2026")


def slide_not_ai(s):
    headline(s, "No todo lo que calcula es inteligencia artificial.")
    gq = T.comp("guide-question")
    shape(s, MARGIN, 288, CANVAS_W - 2 * MARGIN, gq["height"], fill=gq["backgroundColor"],
          radius="full", name="Pregunta guía",
          paras=["¿Quién decide la forma del modelo: una persona o los datos?"],
          size=T.type("label-lg")["pt"], bold=True, color=gq["textColor"], align="c", anchor="m")

    lx, lw_ = cols(1, 6)
    rx, rw = cols(7, 12)
    head_y = 384
    lab = T.type("label-lg")["pt"]
    text(s, lx, head_y, lw_, 46, "La decide una persona", size=lab, bold=True, color=HUMAN_D)
    text(s, rx, head_y, rw, 46, "La aprenden los datos", size=lab, bold=True, color=ML_D)
    line(s, 960, 392, 960, 965, color=RULE, lw=W_THIN, dash=MSO_LINE.DASH, name="Separador")

    items = [("icono-curva-color", "Modelos poblacionales y estimación bayesiana"),
             ("icono-calculadora", "Calculadoras y nomogramas"),
             ("icono-engranaje", "Automatizaciones por reglas")]
    cy, chh = 450, 150
    for i, (ic, label) in enumerate(items):
        y = cy + i * (chh + GAP)
        card(s, lx, y, lw_ - GAP, chh, name=f"Tarjeta {i + 1}")
        icon_disc(s, ic, lx + PAD + ICON_LG / 2, y + chh / 2)
        text(s, lx + 2 * PAD + ICON_LG, y, lw_ - GAP - 3 * PAD - ICON_LG, chh, label,
             size=T.type("body-lg")["pt"], color=INK, anchor="m", bold=True)

    # Conjuntos anidados: todo es aprendizaje automático (morado de claro a intenso)
    ccx, ccy = rx + 222, 712
    rings = [(222, ML_S, "Aprendizaje automático"),
             (150, ML_M, "Aprendizaje profundo\n(redes neuronales)"),
             (80, ML, "Modelos de lenguaje\n(IA generativa)")]
    for r, c, _ in rings:
        shape(s, ccx - r, ccy - r, 2 * r, 2 * r, fill=c, line=WHITE, lw=W_MD, kind=MSO_SHAPE.OVAL,
              name="Círculo")
    lab_x = rx + 452
    anchors = [((ccx + 120, ccy - 140), ccy - 140),
               ((ccx + 115, ccy - 6), ccy - 6),
               ((ccx + 30, ccy + 40), ccy + 136)]
    for (r, c, label), ((dx, dy), ly) in zip(rings, anchors):
        shape(s, dx - 9, dy - 9, 18, 18, fill=WHITE, line=INK, lw=W_THIN, kind=MSO_SHAPE.OVAL,
              name="Marca")
        if abs(ly - dy) < 1:
            line(s, dx + 9, dy, lab_x - 12, ly, color=INK, lw=W_THIN)
        else:
            line(s, dx + 6, dy + 6, lab_x - 70, ly, color=INK, lw=W_THIN)
            line(s, lab_x - 70, ly, lab_x - 12, ly, color=INK, lw=W_THIN)
        text(s, lab_x, ly - 52, rx + rw - lab_x, 104, label, size=20, bold=True, color=ML_D,
             anchor="m")
    source(s, "Keutzer et al., Pharmaceutics, 2022")


def slide_thirty_years(s):
    headline(s, "Treinta años de estudios: predice parecido al bayesiano,\n"
                "pero apenas ha llegado al día a día.")
    ty = 312
    line(s, MARGIN, ty, CANVAS_W - MARGIN, ty, color=INK, lw=W_MD, tail="triangle",
         name="Línea de tiempo")
    lx, lw_ = cols(1, 6)
    rx, rw = cols(7, 12)
    for (x, w, yr, rest) in (
        (lx, lw_, "1995", " · Red neuronal frente a NONMEM (gentamicina, 111 pacientes)"),
        (rx, rw, "2025", " · 58 estudios: el aprendizaje automático rinde igual o mejor "
                         "que los modelos poblacionales"),
    ):
        shape(s, x, ty - 13, 26, 26, fill=WHITE, line=INK, lw=W_MD, kind=MSO_SHAPE.OVAL,
              name=f"Hito {yr}")
        text(s, x, ty + 26, w - GAP, 130, [[(yr, {"bold": True, "size": 24}), (rest, {})]],
             size=20, color=INK, name=f"Texto {yr}")

    cy, chh = 470, 360
    body = T.type("body-lg")["pt"]
    for x, w, ic, head, lbl in ((lx, lw_, "icono-gotero", "Sin concentraciones del paciente",
                                 "Gotero vacío"),
                                (rx, rw, "icono-tubo", "Con concentraciones del paciente",
                                 "Tubo de análisis")):
        card(s, x, cy, w, chh, name=f"Tarjeta {head}")
        image(s, ic, x + PAD, cy + PAD, ICON_SM, ICON_MD, label=lbl)
        text(s, x + PAD + ICON_SM + 16, cy + PAD, w - 2 * PAD - ICON_SM - 16, ICON_MD, head,
             size=24, bold=True, color=INK, anchor="m")
    text(s, lx + PAD, cy + 150, lw_ - 2 * PAD, chh - 150 - PAD, [[
        ("El modelo híbrido mejora un ", {}), (f"17{NB}%", {"bold": True, "color": ML}),
        (f" el error del bayesiano · vancomicina en sepsis, 4059{NB}pacientes", {})]],
        size=body, color=INK, anchor="m")
    for i, (c, dark, runs) in enumerate((
        (TOOL, TOOL_D, [("Gana el bayesiano: ", {"bold": True}),
                        (f"13{NB}% de error frente{NB}a{NB}34{NB}%", {})]),
        (ML, ML_D, [("Gana el aprendizaje automático: ", {"bold": True}),
                    ("ABC de tacrolimus en 6 series externas", {})]),
    )):
        yy = cy + 140 + i * 110
        shape(s, rx + PAD, yy + 12, 20, 20, fill=c, kind=MSO_SHAPE.OVAL, name="Marca color")
        text(s, rx + PAD + 36, yy, rw - 2 * PAD - 36, 96, [runs], size=body, color=dark)

    cv = T.comp("caveat-strip")
    shape(s, MARGIN, 852, CANVAS_W - 2 * MARGIN, cv["height"], fill=cv["backgroundColor"],
          radius=R_MD, name="Advertencia",
          paras=["Casi todo retrospectivo · La IA y los híbridos siguen en investigación"],
          size=body, bold=True, color=cv["textColor"], align="c", anchor="m")
    source(s, "Brier et al., Pharm Res, 1995 · Methaneethorn et al., Clin Pharmacokinet, 2025 · "
              "Chen et al., Microbiol Spectr, 2025 · Woillard et al., Clin Pharmacol Ther, 2021 · "
              "Altynova et al., Pharmaceuticals, 2026", two_lines=True)


def slide_ladder(s):
    headline(s, "Predecir bien no es lo mismo que mejorar al paciente.")
    x_end = col(8) + COLW              # la tarjeta ocupa las columnas 9-12
    base, rise, run, x0 = 965, 128, 150, MARGIN
    steps = [("Estudio retrospectivo", None),
             ("Validación externa", "10 de 115 estudios de tacrolimus"),
             ("Estudio prospectivo", "pocos, pequeños, sin comparador (CURATE.AI: 10 pacientes)"),
             ("Ensayo con desenlace de proceso", None),
             ("Ensayo con desenlace clínico", None)]
    tints = ["EEF2F6", "E4EAF0", "DAE2EA", "D0DAE4", "C6D2DE"]

    def tread(i):
        return base - (i + 1) * rise

    for i, (name, detail) in enumerate(steps):
        x = x0 + i * run
        shape(s, x, tread(i), x_end - x, rise, fill=tints[i], line=WHITE, lw=W_THIN,
              name=f"Peldaño {i + 1}")
        runs = [(name, {"bold": True})] + ([(": " + detail, {})] if detail else [])
        text(s, x + 22, tread(i) + 6, x_end - x - 44, rise - 12, [runs], size=20, color=INK,
             anchor="m", name=f"Rótulo peldaño {i + 1}")
    # Perfil de la escalera: huellas y contrahuellas en tinta
    prof = [(x0, base)]
    for i in range(5):
        prof += [(x0 + i * run, tread(i)), (x0 + (i + 1) * run if i < 4 else x_end, tread(i))]
    polyline(s, prof, color=INK, lw=W_MD, name="Perfil escalera")

    # Marcador morado: mancha densa en 1, se estrecha en 2, un punto en 3
    rnd = random.Random(11)
    for i, n, spread in ((0, 70, 54), (1, 14, 30), (2, 1, 0)):
        cxp = x0 + i * run + run / 2
        if n > 1:
            shape(s, cxp - spread - 16, tread(i) - spread * 1.35 - 26, 2 * spread + 32,
                  spread * 1.35 + 24, fill=ML_T, line=ML_S, lw=W_THIN, kind=MSO_SHAPE.OVAL,
                  name="Mancha")
        for _ in range(n):
            dx = rnd.uniform(-spread, spread)
            dy = -abs(rnd.gauss(0, spread * 0.5)) - 10
            r = rnd.uniform(5, 8.5) if n > 1 else 14
            shape(s, cxp + dx - r, tread(i) + dy - r, 2 * r, 2 * r, fill=ML, line=WHITE,
                  lw=0.75 if n > 1 else W_THIN, kind=MSO_SHAPE.OVAL, name="Estudio")
    text(s, x0, 470, 290, 100, "Aprendizaje automático", size=22, bold=True, color=ML,
         anchor="b", name="Rótulo marcador")
    line(s, x0 + 50, 576, x0 + 50, 730, color=ML, lw=W_THIN, dash=MSO_LINE.ROUND_DOT,
         name="Guía marcador")

    # Tarjeta verde unida al quinto peldaño por un marcador verde
    cx, cw = cols(9, 12)
    cy, chh, head_h = 296, 650, 196
    card(s, cx, cy, cw, chh, kind="card-tool", name="Tarjeta TDM")
    hc = T.comp("card-tool-header")
    shape(s, cx, cy, cw, head_h, fill=hc["backgroundColor"], radius=R_MD, name="Cabecera tarjeta")
    shape(s, cx, cy + head_h - 40, cw, 40, fill=hc["backgroundColor"], name="Cabecera (base)")
    text(s, cx + PAD, cy + 16, cw - 2 * PAD, head_h - 32,
         f"Dosificación individualizada\nde antimicrobianos\n(TDM{NB}o{NB}MIPD)", size=22,
         bold=True, color=hc["textColor"], anchor="m")
    text(s, cx + PAD, cy + head_h + 16, cw - 2 * PAD, 44, "10 ensayos · 1241 pacientes",
         size=20, color=TOOL_D, bold=True)
    rows_ = [[("Fracaso terapéutico ", {}), (f"−30{NB}%", {"bold": True}), (f" (RR{NB}0,70)", {})],
             [("Nefrotoxicidad ", {}), (f"−45{NB}%", {"bold": True}), (f" (RR{NB}0,55)", {})],
             [("Mortalidad: sin cambio significativo", {})]]
    for i, r in enumerate(rows_):
        yy = cy + head_h + 76 + i * 122
        if i:
            line(s, cx + PAD, yy - 10, cx + cw - PAD, yy - 10, color=C("tool-tint"), lw=W_THIN)
        text(s, cx + PAD, yy, cw - 2 * PAD, 108, [r], size=22, color=INK, anchor="m")
    mk = T.comp("marker-tool")
    my = tread(4) - mk["size"] / 2 - 4
    mx = x_end - 60
    line(s, mx, my, cx, my, color=TOOL, lw=W_STRONG, name="Unión peldaño 5")
    shape(s, mx - mk["size"] / 2, my - mk["size"] / 2, mk["size"], mk["size"], fill=TOOL,
          line=WHITE, lw=W_THIN, kind=MSO_SHAPE.OVAL, name="Marcador TDM en peldaño 5")
    source(s, "Amooei et al., Pharmaceutics, 2026 · Blasiak et al., NPJ Precis Oncol, 2025 · "
              "Sanz-Codina et al., Clin Microbiol Infect, 2023")


# Columnas de rótulos del esquema (mismas en las diapositivas 6 y 7)
LCOLS = [(960 - OFF - 205, 410), (960 - 300, 600), (960 + OFF - 205, 410)]


def slide_pieces(s):
    headline(s, "El fallo no es de la IA: es de usar una sola pieza.")
    fy, fh = 420, 460
    # Rótulo del arnés, fuera del marco y alineado con él
    text(s, FRAME_X, 296, 640, 100, [[("Arnés (el protocolo)", {"bold": True})],
                                    [("procedimiento normalizado de trabajo", {"color": GRAY})]],
         size=20, color=INK, anchor="b", name="Rótulo arnés")
    frame(s, FRAME_X, fy, FRAME_W, fh)
    shape(s, 960 - 220, fy + fh - 22, 440, 44, fill=WHITE, name="Borde arnés",
          paras=["reglas · límites · registro"], size=20, italic=True, color=INK, align="c",
          anchor="m")
    g = scheme(s, "color", fy)
    right = pharmacist(s, "color", 290, 104, fy, g["ptop"])
    text(s, right + 18, 290, 760, 104, [
        [("Farmacéutico", {"bold": True, "color": HUMAN_D}), (" · supervisa y aporta criterio", {})],
        [("firma del informe", {"color": GRAY})]], size=20, color=INK, anchor="m")
    lab_y = g["bottom"] + 14
    labels = [
        [[("Contexto", {"bold": True}), (" · lo que le das del caso", {})],
         [("historia clínica", {"color": GRAY})]],
        [[("Modelo de lenguaje", {"bold": True, "color": ML_D}), (" · predice texto", {})],
         [("lee, llama a la herramienta y redacta el borrador", {"color": GRAY})]],
        [[("Herramientas", {"bold": True, "color": TOOL_D}),
          (" · código y programas validados", {})],
         [("programa bayesiano", {"color": GRAY})]],
    ]
    for (x, w), lab in zip(LCOLS, labels):
        text(s, x, lab_y, w, 150, lab, size=20, color=INK, align="c")
    text(s, MARGIN, 914, CANVAS_W - 2 * MARGIN, 60, [[
        ("El modelo de lenguaje no da siempre la misma respuesta; ", {}),
        ("la herramienta validada, sí.", {"bold": True, "color": TOOL_D})]],
        size=24, color=INK, align="c", anchor="m", name="Frase de pie")
    source(s, "Pritchard-Bell et al., CPT Pharmacometrics Syst Pharmacol, 2026")


def slide_xray(s):
    headline(s, "La lección de TDM-AID: cada tarea, a la pieza que mejor la hace.")
    xp = T.comp("xray-panel")
    shape(s, MARGIN, 282, CANVAS_W - 2 * MARGIN, 700, fill=xp["backgroundColor"], radius=R_MD,
          name="Fondo radiografía")
    fy, fh = 420, 480
    text(s, 112, 300, 760, 92, [[(
        "Prepublicación · 30 casos retrospectivos ·\nfunción renal estable", {})]],
        size=20, italic=True, color=XSOFT, anchor="m", name="Franja")
    frame(s, FRAME_X, fy, FRAME_W, fh, color=ERROR)
    text(s, FRAME_X + 20, fy + 14, 160, 44, "Arnés", size=20, bold=True, color=WHITE,
         name="Rótulo arnés")
    g = scheme(s, "xray", fy, arrow_color=XLINE)
    right = pharmacist(s, "xray", 290, 104, fy, g["ptop"])
    text(s, right + 18, 292, 300, 44, "Farmacéutico", size=20, bold=True, color=WHITE)
    tag(s, right + 18, 342, "borrador + revisión obligatoria", "tag-neutral",
        name="Estado farmacéutico")

    ny = g["bottom"] + 14
    cx = g["cx"]
    # Contexto
    text(s, LCOLS[0][0], ny, LCOLS[0][1], 44, "Contexto", size=20, bold=True, color=WHITE, align="c")
    tag(s, cx[0], ny + 50, "guías locales\nrecuperadas", "tag-neutral", w=300, lines=2,
        center=True, name="Estado contexto")
    # Modelo
    text(s, LCOLS[1][0], ny, LCOLS[1][1], 44, "Modelo (GPT-4o)", size=20, bold=True, color=WHITE,
         align="c")
    tag(s, 960, ny + 50, f"interpreta: 83{NB}%", "tag-partial", center=True, name="Estado modelo")
    f1 = tag(s, 960, ny + 100, f"predice concentraciones: 58{NB}%", "tag-fail", center=True,
             name="Fallo 1")
    tag(s, 960, ny + 150, "cuándo extraer: 0 de 30", "tag-fail", center=True, name="Fallo 2")
    # Herramienta
    tx = LCOLS[2][0] + 24
    text(s, tx, ny, LCOLS[2][1] - 24, 140, [
        [("Herramienta", {"bold": True, "color": WHITE})],
        [("(motor de ecuaciones de primer orden)", {"color": XSOFT})]], size=20, align="c")
    tag(s, cx[2] + 12, ny + 150, "cálculos sin errores", "tag-ok", center=True,
        name="Estado herramienta")

    # «esto es cálculo»: de los fallos del modelo a la herramienta
    fx_r = f1[0] + f1[2]
    p0 = (fx_r + 6, ny + 100 + 23)
    p1 = (cx[2] - 70, g["mid"] + 60)
    curve(s, p0, (fx_r + 24, ny + 40), (fx_r + 10, p1[1] + 10), p1, color=WHITE)
    text(s, 960 + 66, g["mid"] + 28, 270, 44, "esto es cálculo", size=20, italic=True,
         color=WHITE, name="Rótulo cálculo")
    # «esto es un límite»: de «> 4 g/día» al arnés
    lx, ly, lw_, lh = tag(s, FRAME_X, fy + fh + 18, f"sin tope de dosis · 1 de cada 6 casos "
                          f">{NB}4{NB}g/día", "tag-fail", name="Estado arnés")
    end = (lx + lw_ + 70, fy + fh)
    curve(s, (lx + lw_ + 6, ly + lh / 2), (lx + lw_ + 40, ly + lh / 2), (end[0], ly + 6),
          (end[0], end[1] + 4), color=WHITE)
    text(s, end[0] + 20, ly, 300, lh, "esto es un límite", size=20, italic=True, color=WHITE,
         anchor="m", name="Rótulo límite")
    source(s, "Hassan et al., medRxiv, 2026 (prepublicación)")


def slide_label(s):
    headline(s, "Leemos la ficha técnica de lo que dispensamos;\n"
                "leamos también la de la IA que usamos.")
    lx, lw_ = cols(6, 12)
    top, bottom = 298, 968
    # Envase genérico vertical (proyección oblicua), alineado con la ficha
    dx, dy = 120, 70
    fx0, fw0 = MARGIN + 16, 470
    fy0, fh0 = top + dy, bottom - top - dy
    polygon(s, [(fx0, fy0), (fx0 + dx, fy0 - dy), (fx0 + fw0 + dx, fy0 - dy), (fx0 + fw0, fy0)],
            C("illus-metal-1"), name="Caja: tapa")
    polygon(s, [(fx0 + fw0, fy0), (fx0 + fw0 + dx, fy0 - dy), (fx0 + fw0 + dx, fy0 + fh0 - dy),
                (fx0 + fw0, fy0 + fh0)], C("illus-metal-2"), name="Caja: lateral")
    lat = text(s, fx0 + fw0 + dx / 2 - 260, fy0 + fh0 / 2 - dy / 2 - 50, 520, 100,
               "Lea la ficha técnica\nantes de usar", size=20, bold=True, color=INK, align="c",
               anchor="m", name="Caja: texto lateral")
    lat.rotation = 270
    shape(s, fx0, fy0, fw0, fh0, fill=WHITE, line=INK, lw=W_MD, name="Caja: frontal")
    sb = T.comp("structure-band")
    shape(s, fx0 + 1.5, fy0 + 34, fw0 - 3, 18, fill=C("emphasis"), name="Caja: banda")
    shape(s, fx0 + 1.5, fy0 + 58, fw0 - 3, sb["height"] / 2, fill=STRUCT, name="Caja: banda fina")
    text(s, fx0 + PAD, fy0 + 96, fw0 - 2 * PAD, 90, "Dosifica-IA", size=40, bold=True, color=INK,
         anchor="m", name="Caja: nombre")
    text(s, fx0 + PAD, fy0 + 196, fw0 - 2 * PAD, 110, "Contiene:\n1 modelo de lenguaje", size=22,
         color=INK, name="Caja: contenido")
    d = 168
    shape(s, fx0 + fw0 / 2 - d / 2, fy0 + fh0 - d - 40, d, d, fill=C("emphasis-tint"),
          kind=MSO_SHAPE.OVAL, name="Caja: fondo pictograma")
    image(s, "loro-pictograma", fx0 + fw0 / 2 - 60, fy0 + fh0 - d - 30, 120, d - 20,
          label="Pictograma: loro")

    # Ficha técnica desplegada en tres paneles plegados (sin sombra)
    sections = [
        ("icono-dos-columnas", "Composición", "¿Qué hay dentro?",
         " Estadística con modelo, aprendizaje automático o modelo de lenguaje."),
        ("icono-esquema", "Mecanismo de acción", "¿Quién hace el cálculo?",
         " Una herramienta validada o el modelo de lenguaje."),
        ("icono-escalera", "Eficacia clínica y seguridad", "¿Qué ha demostrado, y frente a qué?",
         " Aciertos en una base de datos o resultados en pacientes; frente a un bayesiano con "
         "concentraciones o frente a un rival débil."),
    ]
    heights = [190, 190, bottom - top - 380]
    y = top
    for k, ((ic, head, q, ans), h) in enumerate(zip(sections, heights)):
        shape(s, lx, y, lw_, h, fill=WHITE if k % 2 == 0 else SURFACE, line=RULE, lw=W_THIN,
              name=f"Ficha: panel {k + 1}")
        image(s, ic, lx + PAD, y + PAD, ICON_MD, ICON_MD * 0.85, label=f"Icono {head}")
        text(s, lx + 2 * PAD + ICON_MD, y + 22, lw_ - 3 * PAD - ICON_MD, h - 30, [
            {"runs": [(head, {"bold": True, "color": EMPH_D, "size": 22})], "after": 2},
            [(q, {"bold": True}), (ans, {})]], size=20, color=INK)
        y += h


def slide_close(s):
    headline(s, [[("La ", {}), ("herramienta", {"bold": True, "color": TOOL_D}),
                  (" calcula, el ", {}), ("modelo", {"bold": True, "color": ML}),
                  (" explica\ny el ", {}), ("farmacéutico", {"bold": True, "color": HUMAN_D}),
                  (" decide.", {})]], closing=True, align="c")
    fx, fw = cols(3, 10)
    k = fw / FRAME_W
    fy = 470
    g_top = fy + 24 * k
    pharmacist(s, "color", 300, 140, fy, g_top)
    fh = (24 + PARROT_H + 24) * k + 24
    shape(s, fx, fy, fw, fh, line=MUTED, lw=W_MD, dash=MSO_LINE.DASH, radius=R_MD,
          name="Arnés (gris)")
    scheme(s, "gray", fy, k=k, arrow_color=MUTED)
    shape(s, MARGIN, 868, CANVAS_W - 2 * MARGIN, 100, fill=SURFACE, radius=R_MD, name="Relevo",
          paras=[[("A continuación: ", {"bold": True, "color": EMPH_D}),
                  ("Emilio Monte Boquet", {"bold": True}),
                  (" · Competencias y habilidades en IA para el farmacéutico hospitalario: de "
                   "usuario a supervisor experto", {})]],
          size=20, color=INK, align="l", anchor="m", margins=(PAD, 4, PAD, 4))


# --- Montaje ------------------------------------------------------------------------

def build(template, out):
    prs = Presentation(template)
    prs.slide_width, prs.slide_height = Emu(SLIDE_W), Emu(SLIDE_H)
    sld_ids = prs.slides._sldIdLst
    for sld_id in list(sld_ids)[1:]:                 # se conserva solo la portada
        prs.part.drop_rel(sld_id.get(qn("r:id")))
        sld_ids.remove(sld_id)
    slide_cover(prs.slides[0])
    layout = prs.slide_layouts[0]                    # fondo de contenido de la plantilla
    for builder in (slide_hook, slide_not_ai, slide_thirty_years, slide_ladder,
                    slide_pieces, slide_xray, slide_label, slide_close):
        builder(prs.slides.add_slide(layout))
    prs.save(out)
    print(f"Escrito {out}")


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2])
