"""Lee los tokens del DESIGN.md del sistema SEFH y resuelve sus referencias.

    from sefh_tokens import load
    T = load()                       # DESIGN.md junto a este archivo
    T.color("ml")                    # 'AD3B94'  (hex sin '#', listo para OOXML)
    T.px("margin")                   # 80.0      (píxeles del lienzo 1920 × 1080)
    T.type("headline-lg")            # {'pt': 32.0, 'bold': False, 'line': 1.0, ...}
    T.comp("tag-fail")               # {'backgroundColor': 'D42A3B', ...}

Formato: https://github.com/google-labs-code/design.md (versión alpha).
"""

import re
from pathlib import Path

import yaml

DEFAULT = Path(__file__).with_name("DESIGN.md")
_REF = re.compile(r"^\{([a-zA-Z0-9_.-]+)\}$")
PX_PER_PT = 2.0                    # lienzo de 1920 px sobre una diapositiva de 960 pt


class Tokens:
    def __init__(self, data):
        self.raw = data

    # -- resolución ---------------------------------------------------------
    def _get(self, path):
        node = self.raw
        for part in path.split("."):
            node = node[part]
        return self._resolve(node)

    def _resolve(self, value):
        if isinstance(value, str):
            m = _REF.match(value.strip())
            if m:
                return self._get(m.group(1))
        if isinstance(value, dict):
            return {k: self._resolve(v) for k, v in value.items()}
        return value

    # -- accesos ------------------------------------------------------------
    def color(self, name):
        return str(self._get(f"colors.{name}")).lstrip("#").upper()

    def px(self, name):
        return _dim(self._get(f"spacing.{name}"))

    def radius(self, name):
        return _dim(self._get(f"rounded.{name}"))

    def type(self, name):
        t = self._get(f"typography.{name}")
        return {"font": t["fontFamily"], "pt": _dim(t["fontSize"]) / PX_PER_PT,
                "bold": int(t.get("fontWeight", 400)) >= 600,
                "line": float(t.get("lineHeight", 1.0))}

    def comp(self, name):
        out = {}
        for k, v in self._get(f"components.{name}").items():
            if isinstance(v, str) and v.startswith("#"):
                v = v.lstrip("#").upper()
            elif isinstance(v, str) and v.endswith("px"):
                v = _dim(v)
            out[k] = v
        return out

    def palette(self, prefix):
        """Todos los colores cuyo nombre empieza por `prefix`, sin el prefijo."""
        return {k[len(prefix):]: self.color(k) for k in self.raw["colors"]
                if k.startswith(prefix)}


def _dim(v):
    if isinstance(v, (int, float)):
        return float(v)
    v = str(v).strip()
    if v.endswith("px"):
        return float(v[:-2])
    if v.endswith("rem") or v.endswith("em"):
        return float(v.rstrip("rem").rstrip("em")) * 16
    return float(v)


def load(path=DEFAULT):
    text = Path(path).read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError(f"{path} no tiene bloque YAML inicial")
    front = text.split("---", 2)[1]
    return Tokens(yaml.safe_load(front))


if __name__ == "__main__":
    T = load()
    print(T.color("ml"), T.px("margin"), T.type("headline-lg"), T.comp("tag-fail"))
