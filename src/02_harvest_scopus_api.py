"""Paso 2 (opcional) - Recolección desde la Scopus Search API de Elsevier.

Requiere una clave institucional (https://dev.elsevier.com) y, fuera de la red
de la universidad, un token institucional (insttoken). Ejecuta exactamente las
cadenas TITLE-ABS-KEY definidas en config/queries.yaml (campo `scopus`) y
guarda los resultados con el mismo esquema que OpenAlex para fusionarlos en el
paso 4.

Uso:
    export SCOPUS_API_KEY=xxxxx
    export SCOPUS_INSTTOKEN=yyyy        # opcional
    python src/02_harvest_scopus_api.py
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys
import time

import requests

from common import RAW_SCOPUS_API, iter_queries, load_config, write_jsonl_gz

API = "https://api.elsevier.com/content/search/scopus"


def headers() -> dict:
    h = {"X-ELS-APIKey": os.environ["SCOPUS_API_KEY"], "Accept": "application/json"}
    if os.getenv("SCOPUS_INSTTOKEN"):
        h["X-ELS-Insttoken"] = os.environ["SCOPUS_INSTTOKEN"]
    return h


def flatten(e: dict) -> dict:
    affs = e.get("affiliation") or []
    authors = [
        {"id": a.get("authid"), "name": a.get("authname"), "countries": [], "institutions": []}
        for a in e.get("author") or []
    ]
    kw = e.get("authkeywords") or ""
    return {
        "id": "SCOPUS:" + (e.get("eid") or ""),
        "doi": ("https://doi.org/" + e["prism:doi"]) if e.get("prism:doi") else None,
        "title": e.get("dc:title"),
        "year": int((e.get("prism:coverDate") or "0")[:4]) or None,
        "date": e.get("prism:coverDate"),
        "type": {"ar": "article", "re": "review"}.get(e.get("subtype"), e.get("subtype")),
        "language": None,
        "cited_by": int(e.get("citedby-count") or 0),
        "fwci": None,
        "is_retracted": False,
        "source": e.get("prism:publicationName"),
        "source_issn_l": e.get("prism:issn"),
        "source_type": e.get("prism:aggregationType"),
        "publisher": None,
        "authors": authors,
        "institutions": sorted({a.get("affilname") for a in affs if a.get("affilname")}),
        "countries": sorted({a.get("affiliation-country") for a in affs if a.get("affiliation-country")}),
        "abstract": e.get("dc:description") or "",
        "keywords": [k.strip() for k in kw.split("|") if k.strip()],
        "topics": [],
        "sdgs": [],
        "oa_status": None,
        "referenced_works": [],
    }


def main() -> None:
    if not os.getenv("SCOPUS_API_KEY"):
        print("SCOPUS_API_KEY no definida: se omite la recolección en Scopus.")
        return
    cfg = load_config()
    g = cfg["global"]
    logs = {}
    for q in iter_queries(cfg):
        query = f'{q["scopus"]} AND PUBYEAR > {g["from_year"] - 1} AND PUBYEAR < {g["to_year"] + 1} AND DOCTYPE(ar OR re)'
        cursor, recs, total = "*", [], None
        while cursor:
            r = requests.get(API, headers=headers(), timeout=90, params={
                "query": query, "cursor": cursor, "count": 25, "view": "COMPLETE"})
            if r.status_code != 200:
                print(f"[{q['id']}] HTTP {r.status_code}: {r.text[:300]}", file=sys.stderr)
                break
            res = r.json()["search-results"]
            total = int(res["opensearch:totalResults"])
            entries = [e for e in res.get("entry", []) if "error" not in e]
            if not entries:
                break
            recs.extend(flatten(e) for e in entries)
            nxt = res.get("cursor", {}).get("@next")
            cursor = nxt if nxt and nxt != cursor else None
            time.sleep(0.2)
        n = write_jsonl_gz(RAW_SCOPUS_API / f"{q['id']}.jsonl.gz", recs)
        logs[q["id"]] = {"query": query, "count": total, "retrieved": n,
                         "date": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}
        print(f"[{q['id']}] {n}/{total}")
    (RAW_SCOPUS_API / "search_log.json").write_text(json.dumps(logs, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
