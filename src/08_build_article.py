"""Paso 8 - Genera la versión DOCX del artículo a partir del Markdown.

Requiere pandoc (https://pandoc.org). Las rutas de figuras del Markdown son
relativas a la carpeta articulo/.
"""
from __future__ import annotations

import shutil
import subprocess

from common import ROOT

ART = ROOT / "articulo"


def main() -> None:
    if not shutil.which("pandoc"):
        print("pandoc no está instalado: se omite la generación del DOCX.")
        return
    src = ART / "articulo_revision_bibliometrica.md"
    out = ART / "articulo_revision_bibliometrica.docx"
    cmd = ["pandoc", src.name, "-o", out.name, "--resource-path=.:..", "--toc=false"]
    ref = ART / "plantilla_referencia.docx"
    if ref.exists():
        cmd.append(f"--reference-doc={ref.name}")
    subprocess.run(cmd, check=True, cwd=ART)
    print("Artículo generado:", out)


if __name__ == "__main__":
    main()
