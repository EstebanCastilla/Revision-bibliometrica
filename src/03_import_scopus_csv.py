"""Paso 3 (opcional) - Importa exportaciones CSV de Scopus.

Si se cuenta con acceso institucional a Scopus, cada cadena `scopus` de
config/queries.yaml puede ejecutarse en scopus.com y exportarse como CSV
("All available information"). Guarde el archivo como
data/raw/scopus_export/<ID>.csv (p. ej. N1.csv, N4b.csv); este script lo
convierte al esquema común para fusionarlo con OpenAlex en el paso 4.
"""
from __future__ import annotations

import re

import pandas as pd

from common import RAW_SCOPUS_CSV, write_jsonl_gz

# País = último elemento de cada afiliación ("Univ..., City, Colombia")
COUNTRY_FIX = {"United States": "US", "USA": "US", "United Kingdom": "GB", "UK": "GB"}


def split(val, sep=";"):
    if not isinstance(val, str) or not val.strip():
        return []
    return [v.strip() for v in val.split(sep) if v.strip()]


def row_to_record(r: pd.Series) -> dict:
    affs = split(r.get("Affiliations"))
    countries = sorted({COUNTRY_FIX.get(a.split(",")[-1].strip(), a.split(",")[-1].strip()) for a in affs})
    names = split(r.get("Authors"))
    ids = split(r.get("Author(s) ID"))
    authors = [{"id": ids[i] if i < len(ids) else None, "name": n, "countries": [], "institutions": []}
               for i, n in enumerate(names)]
    doctype = str(r.get("Document Type", "")).lower()
    return {
        "id": "SCOPUS:" + str(r.get("EID", "")),
        "doi": ("https://doi.org/" + r["DOI"]) if isinstance(r.get("DOI"), str) else None,
        "title": r.get("Title"),
        "year": int(r["Year"]) if pd.notna(r.get("Year")) else None,
        "date": None,
        "type": "review" if "review" in doctype else "article",
        "language": str(r.get("Language of Original Document", "")).lower()[:2] or None,
        "cited_by": int(r["Cited by"]) if pd.notna(r.get("Cited by")) else 0,
        "fwci": None,
        "is_retracted": "retracted" in doctype,
        "source": r.get("Source title"),
        "source_issn_l": r.get("ISSN"),
        "source_type": "journal",
        "publisher": r.get("Publisher"),
        "authors": authors,
        "institutions": affs,
        "countries": [c for c in countries if c],
        "abstract": r.get("Abstract") if isinstance(r.get("Abstract"), str) else "",
        "keywords": split(r.get("Author Keywords")) + split(r.get("Index Keywords")),
        "topics": [],
        "sdgs": [],
        "oa_status": None,
        "referenced_works": [],
    }


def main() -> None:
    files = sorted(RAW_SCOPUS_CSV.glob("*.csv"))
    if not files:
        print("No hay exportaciones CSV de Scopus en", RAW_SCOPUS_CSV, "- se omite.")
        return
    for f in files:
        df = pd.read_csv(f)
        qid = re.sub(r"\W+", "", f.stem)
        n = write_jsonl_gz(RAW_SCOPUS_CSV / f"{qid}.jsonl.gz", (row_to_record(r) for _, r in df.iterrows()))
        print(f"{f.name}: {n} registros importados")


if __name__ == "__main__":
    main()
