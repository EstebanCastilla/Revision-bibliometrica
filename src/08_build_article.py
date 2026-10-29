"""Paso 8 - Ensambla el artículo final (Markdown + DOCX).

Inserta en el marcador <!-- REFERENCIAS --> la lista APA generada desde
Crossref (articulo/referencias_apa.md) más las referencias sin DOI
(config/referencias_sin_doi.md), y convierte el resultado a DOCX con pandoc.
Las rutas de figuras del Markdown son relativas a la carpeta articulo/.
"""
from __future__ import annotations

import shutil
import subprocess

from common import ROOT

ART = ROOT / "articulo"


def main() -> None:
    text = (ART / "articulo_revision_bibliometrica.md").read_text(encoding="utf-8")
    refs = [r.strip() for r in (ART / "referencias_apa.md").read_text(encoding="utf-8").split("\n\n")[1:]]
    refs += [r.strip() for r in (ROOT / "config" / "referencias_sin_doi.md").read_text(encoding="utf-8").split("\n\n")]
    refs = sorted({r for r in refs if r}, key=lambda r: r.lower())
    src = ART / "articulo_final.md"
    src.write_text(text.replace("<!-- REFERENCIAS -->", "\n\n".join(refs)), encoding="utf-8")
    out = ART / "articulo_revision_bibliometrica.docx"
    if not shutil.which("pandoc"):
        print("pandoc no está instalado: se omite la generación del DOCX.")
        return
    cmd = ["pandoc", src.name, "-o", out.name, "--resource-path=.:.."]
    ref = ART / "plantilla_referencia.docx"
    if ref.exists():
        cmd.append(f"--reference-doc={ref.name}")
    subprocess.run(cmd, check=True, cwd=ART)
    print("Artículo generado:", out)


if __name__ == "__main__":
    main()
