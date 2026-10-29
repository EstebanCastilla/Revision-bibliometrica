"""Paso 10 - Análisis de sensibilidad del periodo de búsqueda.

Cuenta, para cada consulta de config/queries.yaml, cuántos documentos
(artículos y revisiones) existen antes del año de inicio elegido y en cada
década del periodo, en OpenAlex y en Scopus. Solo hace peticiones de conteo
(no descarga registros), por lo que no modifica el corpus.

Salida: results/tables/period_sensitivity.csv
"""
from __future__ import annotations

import datetime as dt
import importlib.util
import os

import pandas as pd
import requests

from common import ROOT, TABLES, iter_queries, load_config

_spec = importlib.util.spec_from_file_location("oa", ROOT / "src" / "01_harvest_openalex.py")
oa = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(oa)

SCOPUS = "https://api.elsevier.com/content/search/scopus"
RANGES = {"antes de 2000": (1900, 1999), "2000-2009": (2000, 2009),
          "2010-2019": (2010, 2019), "2020-2026": (2020, 2026)}


def oa_count(q: dict, y0: int, y1: int) -> int:
    parts = [f'title_and_abstract.search:{q["openalex"]}', f"publication_year:{y0}-{y1}",
             "type:article|review"]
    if q.get("extra_filter"):
        parts.append(q["extra_filter"])
    return oa.get({"filter": ",".join(parts), "per-page": 1, "select": "id"})["meta"]["count"]


def scopus_count(q: dict, y0: int, y1: int) -> int | None:
    if not os.getenv("SCOPUS_API_KEY"):
        return None
    query = f'{q["scopus"]} AND PUBYEAR > {y0 - 1} AND PUBYEAR < {y1 + 1} AND DOCTYPE(ar OR re)'
    r = requests.get(SCOPUS, timeout=60, params={"query": query, "count": 1},
                     headers={"X-ELS-APIKey": os.environ["SCOPUS_API_KEY"], "Accept": "application/json"})
    r.raise_for_status()
    return int(r.json()["search-results"]["opensearch:totalResults"])


def main() -> None:
    rows = []
    for q in iter_queries(load_config()):
        row = {"query": q["id"]}
        for label, (y0, y1) in RANGES.items():
            row[f"openalex {label}"] = oa_count(q, y0, y1)
            row[f"scopus {label}"] = scopus_count(q, y0, y1)
        tot = sum(row[f"openalex {k}"] for k in RANGES)
        row["openalex % antes de 2000"] = round(row["openalex antes de 2000"] / max(tot, 1) * 100, 2)
        if row["scopus antes de 2000"] is not None:
            tot_s = sum(row[f"scopus {k}"] for k in RANGES)
            row["scopus % antes de 2000"] = round(row["scopus antes de 2000"] / max(tot_s, 1) * 100, 2)
        rows.append(row)
        print(row["query"], row["openalex antes de 2000"], row.get("scopus antes de 2000"))
    df = pd.DataFrame(rows)
    df["fecha_consulta"] = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    df.to_csv(TABLES / "period_sensitivity.csv", index=False)
    print(df.to_string())


if __name__ == "__main__":
    main()
