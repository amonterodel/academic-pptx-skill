"""Inserta o sustituye una diapositiva en una presentación ya montada, sin tocar las demás.

    python3 insertar_diapositiva.py <entrada.pptx> <salida.pptx> <función> <posición> [--sustituir]

<función> es el nombre de una función slide_* de build_deck.py y <posición> el
número de la diapositiva (1 = primera). Con --sustituir, la diapositiva que
ocupa esa posición se elimina y la nueva ocupa su lugar. Ejemplo, rehacer el
caso de las tres IA (diapositiva 2):

    python3 insertar_diapositiva.py salida/ponencia-ia-tdm-montero.pptx \
        salida/ponencia-ia-tdm-montero.pptx slide_case 2 --sustituir
"""

import sys

from pptx import Presentation

import build_deck


def insert(src, out, func_name, position, replace=False):
    prs = Presentation(src)
    builder = getattr(build_deck, func_name)
    ids = prs.slides._sldIdLst
    if replace:
        old = list(ids)[position - 1]
        ids.remove(old)                     # primero la referencia: drop_rel la cuenta
        prs.part.drop_rel(old.rId)          # la diapositiva y sus notas salen del paquete
        prs.part.rename_slide_parts([i.rId for i in ids])   # evita dos slideN.xml iguales
    slide = prs.slides.add_slide(prs.slide_layouts[0])     # fondo de contenido de la plantilla
    builder(slide)
    new_id = list(ids)[-1]
    ids.remove(new_id)
    ids.insert(position - 1, new_id)
    prs.save(out)
    verb = "sustituye a la" if replace else "como"
    print(f"Escrito {out}: «{func_name}» {verb} diapositiva {position} de {len(prs.slides)}")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--sustituir"]
    insert(args[0], args[1], args[2], int(args[3]), replace="--sustituir" in sys.argv)
