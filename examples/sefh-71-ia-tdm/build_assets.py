"""Ilustraciones de la ponencia (SVG -> PNG transparente).

Estilo único para todo el conjunto: contorno oscuro de grosor constante,
rellenos planos y colores de la plantilla SEFH. Cada pieza admite tres
variantes de paleta:

    color  -> versión normal
    gray   -> esquema atenuado (diapositiva 9)
    xray   -> radiografía: líneas claras azuladas sobre fondo oscuro (diapositiva 7)

Uso:  python3 build_assets.py   (escribe los PNG en ./assets)
"""

import math
import sys
from pathlib import Path

import cairosvg
from PIL import Image, ImageFilter

HERE = Path(__file__).parent
OUT_DIR = HERE / "assets"
sys.path.insert(0, str(HERE.parents[1] / "design-systems" / "sefh"))
from sefh_tokens import load  # noqa: E402

T = load()
IL = {k: "#" + v for k, v in T.palette("illus-").items()}


def _c(name):
    return "#" + T.color(name)


LIMA, VERDE, TURQUESA, MORADO, AZUL = (_c(n) for n in ("structure", "tool", "emphasis", "ml",
                                                         "human"))
INK = IL["ink"]

PALETTES = {
    "color": {
        "out": INK, "op": 1.0,
        "m1": IL["metal-1"], "m2": IL["metal-2"], "m3": IL["metal-3"], "m4": IL["metal-4"],
        "coat": IL["coat"], "coatS": IL["coat-shade"],
        "beak": "#46525F", "beakS": "#6C7884",
        "sock": "#1C2833", "glow": IL["glow"], "core": "#FFFFFF",
        "accent": MORADO, "paper": "#FFFFFF", "line": "#9AA6B2",
        "verde": VERDE, "verdeT": _c("tool-tint"), "morado": MORADO, "moradoT": _c("ml-tint"),
        "moradoS": _c("ml-soft"), "moradoM": _c("ml-mid"),
        "azul": AZUL, "azulT": _c("human-tint"), "turq": TURQUESA, "turqT": _c("emphasis-tint"),
        "lima": LIMA, "limaT": _c("structure-tint"), "skin": IL["skin"], "hair": "#3B3F4A",
        "shirt": TURQUESA, "plasma": "#E9D86A",
    },
    "gray": {
        "out": "#B4BCC5", "op": 1.0,
        "m1": "#F4F6F8", "m2": "#E9ECEF", "m3": "#DDE1E5", "m4": "#CDD3D9",
        "coat": "#FFFFFF", "coatS": "#F1F3F5",
        "beak": "#D2D8DE", "beakS": "#DEE3E7",
        "sock": "#C9D0D6", "glow": "#EEF1F4", "core": "#FFFFFF",
        "accent": "#D5DADF", "paper": "#FFFFFF", "line": "#D0D6DC",
        "verde": "#C9D0D6", "verdeT": "#F1F3F5", "morado": "#C9D0D6", "moradoT": "#F1F3F5",
        "moradoS": "#E3E7EB", "moradoM": "#D3D9DE",
        "azul": "#C9D0D6", "azulT": "#F1F3F5", "turq": "#C9D0D6", "turqT": "#F1F3F5",
        "lima": "#C9D0D6", "limaT": "#F1F3F5", "skin": "#ECEFF2", "hair": "#D3D9DE",
        "shirt": "#E3E7EB", "plasma": "#E9ECEF",
    },
}
# Radiografía: todo el dibujo en líneas claras; rellenos casi transparentes.
_X = _c("xray-line")
PALETTES["xray"] = {k: _X for k in PALETTES["color"]}
PALETTES["xray"].update({"op": 0.10, "out": _X, "glow": "#E8FBFF", "core": "#FFFFFF",
                          "sock": "#0B1626"})


class Pen:
    """Pequeño ayudante para escribir SVG con una paleta."""

    def __init__(self, pal, sw):
        self.p = PALETTES[pal]
        self.name = pal
        self.sw = sw
        self.parts = []

    def fill(self, key):
        if key is None or key == "none":
            return 'fill="none"'
        if self.name == "xray" and key not in ("glow", "core", "sock"):
            return f'fill="{_X}" fill-opacity="{self.p["op"]}"'
        return f'fill="{self.p[key]}"'

    def stroke(self, w=None, key="out", dash=None):
        w = self.sw if w is None else w
        d = f' stroke-dasharray="{dash}"' if dash else ""
        return (f'stroke="{self.p[key]}" stroke-width="{w}" '
                f'stroke-linejoin="round" stroke-linecap="round"{d}')

    def path(self, d, fill="none", w=None, skey="out", dash=None, extra=""):
        s = self.stroke(w, skey, dash) if w != 0 else 'stroke="none"'
        self.parts.append(f'<path d="{d}" {self.fill(fill)} {s} {extra}/>')

    def circle(self, cx, cy, r, fill="none", w=None, skey="out", extra=""):
        s = self.stroke(w, skey) if w != 0 else 'stroke="none"'
        self.parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" {self.fill(fill)} {s} {extra}/>')

    def rect(self, x, y, w_, h, rx=0, fill="none", w=None, skey="out", dash=None, extra=""):
        s = self.stroke(w, skey, dash) if w != 0 else 'stroke="none"'
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w_}" height="{h}" rx="{rx}" '
                          f'{self.fill(fill)} {s} {extra}/>')

    def raw(self, s):
        self.parts.append(s)

    def group(self, transform):
        self.parts.append(f'<g transform="{transform}">')

    def end(self):
        self.parts.append("</g>")

    def svg(self, w, h, vb=None):
        vb = vb or f"0 0 {w} {h}"
        body = "\n".join(self.parts)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
                f'viewBox="{vb}">{body}</svg>')


def tube(pen, d, w_out, w_in, key):
    """Trazo grueso con contorno: tubo metálico (dedos, varillas)."""
    pen.raw(f'<path d="{d}" fill="none" {pen.stroke(w_out)}/>')
    col = _X if pen.name == "xray" else pen.p[key]
    op = ' stroke-opacity="0.0"' if pen.name == "xray" else ""
    pen.raw(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w_in}" '
            f'stroke-linecap="round" stroke-linejoin="round"{op}/>')


def bolt(pen, x, y, r=6):
    pen.circle(x, y, r, "m2", w=pen.sw * 0.7)
    pen.circle(x, y, r * 0.35, "m4", w=0)


# ---------------------------------------------------------------------------
# Loro robótico
# ---------------------------------------------------------------------------

def parrot(pal="color", pose="neutral"):
    """Loro robótico con bata de farmacia. Mira a la derecha.

    pose = "neutral"   -> de pie, ala recogida
           "confident" -> cabeza alta, párpado a media asta y ala señalando
    """
    pen = Pen(pal, 4)
    W, H = 440, 620

    # Cola (detrás)
    pen.path("M150,396 C126,440 104,486 92,528 C104,522 116,512 124,500 C140,470 160,434 178,404 Z",
             "m3")
    pen.path("M170,398 C158,448 146,500 142,548 C154,538 164,524 170,508 C180,474 190,438 198,406 Z",
             "m2")
    pen.path("M106,494 L126,484 M118,468 L138,458 M150,500 L170,494 M156,470 L176,464", w=3)

    # Patas: varillas con rodilla atornillada
    for x in (196, 240):
        pen.rect(x - 8, 420, 16, 92, rx=7, fill="m3")
        pen.circle(x, 462, 12, "m2")
        pen.circle(x, 462, 4, "m4", w=0)
        tube(pen, f"M{x},510 Q{x+20},508 {x+28},530", 12, 6, "m4")
        tube(pen, f"M{x},512 Q{x-12},516 {x-16},530", 12, 6, "m4")
    # Suelo de las patas
    pen.path("M166,536 L290,536", "none", w=4)

    # Bata
    pen.path("M204,214 C172,224 150,258 142,302 L126,444 Q214,458 304,444 "
             "L290,302 C284,258 264,226 240,214 Z", "coat")
    pen.path("M150,300 L136,438 Q150,442 166,444 L172,300 C170,272 176,250 186,236 "
             "C166,250 154,272 150,300 Z", "coatS", w=0)
    # Pecho metálico en la abertura
    pen.path("M206,220 L240,220 L226,306 Z", "m1")
    pen.path("M212,240 L236,240 M216,262 L233,262 M220,284 L230,284", w=3)
    # Solapas
    pen.path("M202,216 L216,220 L226,306 L194,262 Z", "coat")
    pen.path("M244,216 L234,220 L226,306 L258,258 Z", "coat")
    pen.path("M226,306 L222,450", w=4)
    # Botones y bolsillo con bolígrafo
    pen.circle(234, 338, 5.5, "m2")
    pen.circle(233, 382, 5.5, "m2")
    pen.rect(258, 314, 7, 26, rx=3, fill="accent")
    pen.rect(250, 332, 32, 30, rx=4, fill="coat")
    pen.rect(160, 330, 34, 22, rx=4, fill="turq")
    pen.path("M168,342 L186,342", w=3, skey="out")

    # Ala / manga
    if pose == "neutral":
        pen.path("M256,236 C290,246 304,296 300,356 L272,362 C270,320 262,288 248,262 Z", "coat")
        pen.path("M272,362 L298,356 L300,370 L274,376 Z", "m3")  # muñeca
        pen.path("M276,374 L292,428 L304,424 L298,370 Z", "m2")
        pen.path("M288,372 L314,418 L322,410 L300,368 Z", "m3")
        pen.path("M274,376 L276,420 L288,422 L286,374 Z", "m3")
        bolt(pen, 268, 262, 7)
    else:
        pen.path("M248,240 C282,222 318,202 346,180 L364,204 C334,230 300,254 266,272 Z", "coat")
        pen.path("M344,176 L368,200 L378,190 L354,166 Z", "m3")  # muñeca
        pen.path("M366,178 L420,140 L426,152 L376,192 Z", "m2")  # pluma que señala
        pen.path("M364,170 L404,128 L414,136 L372,182 Z", "m3")
        pen.path("M372,190 L414,168 L418,180 L378,200 Z", "m3")
        bolt(pen, 262, 252, 7)

    # Cabeza (en grupo para poder inclinarla)
    # Cuello articulado (visible entre cabeza y bata)
    pen.rect(200, 198, 44, 16, rx=6, fill="m3")
    pen.rect(204, 184, 36, 16, rx=6, fill="m2")
    tilt = "rotate(-9 222 200)" if pose == "confident" else ""
    pen.group(f"{tilt} translate(222 196) scale(1.12) translate(-222 -210)")
    # Cresta
    for d, tip in (
        ("M206,84 L166,30 L186,24 L226,78 Z", "M166,30 L186,24 L180,42 L172,44 Z"),
        ("M224,76 L206,14 L228,14 L244,74 Z", "M206,14 L228,14 L224,34 L212,34 Z"),
        ("M242,76 L252,22 L272,30 L258,82 Z", "M252,22 L272,30 L266,46 L256,42 Z"),
    ):
        pen.path(d, "m2")
        pen.path(tip, "accent")
    pen.path("M170,150 C166,96 206,70 242,72 C280,74 304,100 306,136 C307,168 288,196 254,206 "
             "C216,214 174,198 170,150 Z", "m2")
    # Placa facial
    pen.path("M222,102 C252,94 282,108 290,136 C294,162 278,184 250,188 C228,190 214,174 212,152 "
             "C210,128 212,108 222,102 Z", "m1")
    # Costura y remaches
    pen.path("M196,92 C186,124 188,166 214,200", w=3)
    for (x, y) in ((193, 112), (189, 140), (194, 168), (206, 188)):
        pen.circle(x, y, 3.2, "m4", w=0)
    bolt(pen, 246, 180, 7)
    # Pico
    pen.path("M286,118 C320,112 348,136 346,174 C345,192 336,204 326,208 C330,190 322,172 304,168 "
             "C296,167 288,168 282,170 Z", "beak")
    pen.path("M296,124 C318,124 334,140 336,160", "none", w=3, skey="out",
             extra='stroke-opacity="0.35"')
    pen.path("M282,172 C298,170 314,178 316,192 C306,200 292,200 282,192 Z", "beakS")
    # Ojo con luz
    if pal != "gray":
        pen.circle(250, 134, 30, "glow", w=0, extra='fill-opacity="0.28"')
    pen.circle(250, 134, 19, "sock")
    pen.circle(250, 134, 10, "glow", w=0)
    pen.circle(250, 134, 4.5, "core", w=0)
    if pose == "confident":
        # Párpado a media asta y ceja levantada: gesto de suficiencia
        pen.path("M229,136 A21,21 0 0 1 271,136 Z", "m2")
        pen.path("M222,100 L276,84 L280,96 L226,112 Z", "m4")
    pen.end()

    return pen.svg(W, H, vb="0 -36 440 620")


# ---------------------------------------------------------------------------
# Iconos de línea (cuadrícula 120 x 120)
# ---------------------------------------------------------------------------

def icon_curva(pal="color"):
    pen = Pen(pal, 5)
    pen.path("M16,18 L16,104 L108,104", w=5)
    pen.path("M22,30 C34,62 44,74 62,82 C78,89 92,92 104,94", w=5.5, skey="out")
    # Compartimentos
    pen.rect(58, 14, 22, 22, rx=5, fill="verdeT")
    pen.rect(90, 14, 22, 22, rx=5, fill="verdeT")
    pen.path("M82,21 L88,21 M88,29 L82,29", w=4)
    pen.path("M69,36 L69,48", w=4)
    pen.path("M64,44 L69,50 L74,44", w=4)
    return pen.svg(120, 120)


def icon_campana(pal="color"):
    pen = Pen(pal, 5)
    pen.path("M10,100 L110,100", w=5)
    pen.path("M14,98 C34,96 42,52 60,52 C78,52 86,96 106,98", w=4, dash="7 7")
    pen.path("M34,99 C48,98 50,22 60,22 C70,22 72,98 86,99 Z", "verdeT", w=5)
    pen.path("M60,22 L60,99", w=3.5, dash="4 6")
    return pen.svg(120, 120)


def icon_red(pal="color"):
    pen = Pen(pal, 4)
    layers = [[(20, 34), (20, 86)], [(60, 20), (60, 60), (60, 100)], [(100, 60)]]
    for a, b in zip(layers, layers[1:]):
        for (x1, y1) in a:
            for (x2, y2) in b:
                pen.path(f"M{x1},{y1} L{x2},{y2}", w=3.5)
    for layer in layers:
        for (x, y) in layer:
            pen.circle(x, y, 11, "moradoT", w=5)
    return pen.svg(120, 120)


def icon_calculadora(pal="color", fill="azulT"):
    pen = Pen(pal, 5)
    pen.rect(24, 10, 72, 100, rx=10, fill=fill)
    pen.rect(34, 20, 52, 22, rx=4, fill="paper")
    pen.path("M70,31 L78,31", w=4)
    for r in range(3):
        for c in range(3):
            pen.rect(34 + c * 19, 52 + r * 17, 13, 11, rx=3, fill="paper", w=3.5)
    return pen.svg(120, 120)


def _gear_path(cx, cy, r_out, r_in, teeth):
    pts = []
    for i in range(teeth * 4):
        ang = 2 * math.pi * i / (teeth * 4)
        r = r_out if (i % 4) in (1, 2) else r_in
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"


def icon_engranaje(pal="color"):
    pen = Pen(pal, 5)
    pen.path(_gear_path(52, 62, 36, 27, 8), "azulT", w=5)
    pen.circle(52, 62, 10, "paper", w=5)
    # Flecha que sale: la regla se ejecuta sola
    pen.path("M80,26 C96,30 106,42 108,58", w=5)
    pen.path("M98,52 L108,62 L114,48", w=5)
    return pen.svg(120, 120)


def icon_gotero(pal="color"):
    pen = Pen(pal, 5)
    # Gotero vacío: sin líquido y con la gota en contorno discontinuo
    pen.path("M46,12 C46,4 74,4 74,12 L74,30 L46,30 Z", "azulT", w=5)
    pen.rect(40, 30, 40, 10, rx=3, fill="paper", w=5)
    pen.path("M50,40 L50,78 L60,94 L70,78 L70,40", "paper", w=5)
    pen.path("M60,102 C54,110 52,114 52,118", w=0)
    pen.path("M60,100 C66,108 68,112 68,114 C68,119 52,119 52,114 C52,112 54,108 60,100 Z",
             w=3.5, dash="4 5")
    return pen.svg(120, 120)


def icon_tubo(pal="color"):
    pen = Pen(pal, 5)
    pen.rect(40, 8, 40, 16, rx=4, fill="turqT", w=5)
    pen.path("M46,24 L46,98 C46,116 74,116 74,98 L74,24", "paper", w=5)
    pen.path("M46,62 L74,62 L74,98 C74,116 46,116 46,98 Z", "plasma", w=0)
    pen.path("M46,24 L46,98 C46,116 74,116 74,98 L74,24", w=5)
    pen.path("M46,62 L74,62", w=4)
    pen.path("M58,36 L58,52", w=3.5, extra='stroke-opacity="0.5"')
    return pen.svg(120, 120)


def icon_escalera(pal="color"):
    pen = Pen(pal, 5)
    pen.path("M10,106 L10,86 L34,86 L34,66 L58,66 L58,46 L82,46 L82,26 L106,26 L106,106 Z",
             "limaT", w=5)
    pen.path("M96,12 L106,22 L116,12", w=0)
    return pen.svg(120, 120)


def pharmacist(pal="color"):
    """Farmacéutico con pluma: busto con bata, firmando."""
    pen = Pen(pal, 4.5)
    W, H = 220, 220
    # Hombros y bata
    pen.path("M30,212 C32,160 62,138 110,138 C158,138 188,160 190,212 Z", "coat")
    pen.path("M92,140 L110,180 L128,140 C122,138 98,138 92,140 Z", "shirt")
    pen.path("M92,140 L110,180 L96,212 M128,140 L110,180 L124,212", w=4)
    pen.path("M110,180 L110,212", w=4)
    # Cabeza
    pen.rect(98, 116, 24, 26, rx=8, fill="skin")
    pen.circle(110, 92, 32, "skin")
    pen.path("M78,90 C76,60 96,52 112,54 C134,54 146,68 142,92 C134,78 120,72 104,74 "
             "C92,76 84,82 78,90 Z", "hair")
    # Mano con pluma
    pen.path("M150,196 C148,182 156,170 168,168 C178,168 184,178 182,190 C180,200 168,206 158,204 Z",
             "skin")
    pen.path("M166,176 C178,148 196,124 214,108 C212,132 196,156 172,182 Z", "turqT")
    pen.path("M168,178 L206,118", w=3)
    pen.path("M164,190 L156,206", w=4)
    return pen.svg(W, H)


def case_sheet(pal="color"):
    """Ficha del caso: carpeta con hoja y una curva de concentraciones."""
    pen = Pen(pal, 4.5)
    pen.rect(14, 14, 112, 144, rx=10, fill="m2")
    pen.rect(26, 28, 88, 120, rx=4, fill="paper")
    pen.rect(46, 8, 48, 18, rx=6, fill="m3")
    pen.rect(36, 40, 30, 8, rx=3, fill="turq", w=0)
    for y in (60, 74, 88):
        pen.path(f"M36,{y} L104,{y}", w=3.5, skey="line")
    pen.path("M36,136 L36,104 M36,136 L104,136", w=3)
    pen.path("M40,108 C52,124 66,130 100,132", w=3.5)
    for (x, y) in ((52, 120), (74, 129)):
        pen.circle(x, y, 3.5, "turq", w=0)
    return pen.svg(140, 166)


# Iconos pequeños que remiten a diapositivas anteriores (diapositiva 8)

def icon_dos_columnas(pal="color"):
    pen = Pen(pal, 4.5)
    for i in range(3):
        pen.rect(8, 16 + i * 32, 44, 24, rx=5, fill="azulT")
    pen.circle(86, 60, 30, "moradoS", w=4)
    pen.circle(86, 60, 20, "moradoM", w=4)
    pen.circle(86, 60, 10, "morado", w=4)
    return pen.svg(120, 120)


def icon_esquema(pal="color"):
    pen = Pen(pal, 4.5)
    pen.rect(8, 44, 104, 66, rx=8, w=4, dash="7 6")
    pen.rect(18, 66, 20, 24, rx=3, fill="paper", w=4)
    pen.circle(60, 78, 13, "m2", w=4)
    for i in range(3):
        pen.rect(84, 58 + i * 14, 18, 10, rx=3, fill="verdeT", w=3.5)
    pen.path("M40,78 L44,78", w=4)
    pen.path("M75,78 L82,78", w=4)
    pen.circle(60, 18, 9, "skin", w=4)
    pen.path("M46,40 C46,30 74,30 74,40", "coat", w=4)
    return pen.svg(120, 120)


def render(name, svg, width):
    """Rasteriza y recorta el margen transparente (deja 2 % de aire)."""
    OUT_DIR.mkdir(exist_ok=True)
    out = OUT_DIR / f"{name}.png"
    cairosvg.svg2png(bytestring=svg.encode(), write_to=str(out), output_width=width)
    im = Image.open(out)
    x0, y0, x1, y1 = im.getbbox()
    pad = int(0.02 * max(im.size))
    im = im.crop((max(0, x0 - pad), max(0, y0 - pad),
                  min(im.width, x1 + pad), min(im.height, y1 + pad)))
    if name.endswith("-xray"):
        im = _glow(im)
    im.save(out)


def _glow(im):
    """Halo cian suave detrás de las líneas: aspecto de placa iluminada."""
    im = im.convert("RGBA")
    r = max(6, im.width // 60)
    canvas = Image.new("RGBA", (im.width + 4 * r, im.height + 4 * r), (0, 0, 0, 0))
    canvas.paste(im, (2 * r, 2 * r), im)
    alpha = canvas.split()[3].filter(ImageFilter.GaussianBlur(r))
    halo = Image.new("RGBA", canvas.size, (120, 210, 255, 0))
    halo.putalpha(alpha.point(lambda a: int(a * 0.55)))
    halo.alpha_composite(canvas)
    return halo


def main():
    render("loro-seguro", parrot("color", "confident"), 1320)
    for pal in ("color", "gray", "xray"):
        render(f"loro-{pal}", parrot(pal, "neutral"), 880)
        render(f"farmaceutico-{pal}", pharmacist(pal), 660)
        render(f"ficha-caso-{pal}", case_sheet(pal), 420)
        for nm, fn in (("curva", icon_curva), ("campana", icon_campana), ("red", icon_red)):
            render(f"icono-{nm}-{pal}", fn(pal), 360)
    for nm, fn in (("calculadora", icon_calculadora), ("engranaje", icon_engranaje),
                   ("gotero", icon_gotero), ("tubo", icon_tubo), ("escalera", icon_escalera),
                   ("dos-columnas", icon_dos_columnas), ("esquema", icon_esquema)):
        render(f"icono-{nm}", fn("color"), 360)
    render("loro-pictograma", parrot("color", "neutral"), 600)


if __name__ == "__main__":
    main()
