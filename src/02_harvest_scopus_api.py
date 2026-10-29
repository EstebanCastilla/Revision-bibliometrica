"""Paso 2 - Recolección desde la Scopus Search API de Elsevier y enlace con OpenAlex.

Ejecuta las cadenas TITLE-ABS-KEY de config/queries.yaml (campo `scopus`) con
la clave de API de Elsevier (https://dev.elsevier.com).

Nivel de servicio observado con una clave sin token institucional
(verificado el 2026-10-29): vista STANDARD restringida (título, fuente, fecha,
citas, DOI y tipo; sin resumen, autores ni afiliaciones), 25 registros por
petición, sin paginación por cursor y con un máximo de 5000 resultados por
consulta. Por ello:
  * las consultas con más de 5000 resultados se dividen por rangos de años;
  * los DOI que Scopus recupera y que no están en la cosecha de OpenAlex se
    consultan en OpenAlex por DOI para obtener metadatos completos
    (data/raw/scopus_api/<ID>_openalex.jsonl.gz).
Si se define SCOPUS_INSTTOKEN (token institucional) el script solicita la
vista COMPLETE.

Uso:
    export SCOPUS_API_KEY=xxxxx
    export OPENALEX_API_KEY=yyyy
    python src/02_harvest_scopus_api.py [--only N1 N4b]
"""
from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import json
import os
import sys
import time

import requests

from common import (RAW_OA, RAW_SCOPUS_API, iter_queries, load_config, norm_doi, read_jsonl_gz,
                    run_metadata, write_jsonl_gz)

API = "https://api.elsevier.com/content/search/scopus"
PAGE = 25
MAX_START = 5000

_spec = importlib.util.spec_from_file_location("oa", RAW_OA.parents[2] / "src" / "01_harvest_openalex.py")
oa = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(oa)


def headers() -> dict:
    h = {"X-ELS-APIKey": os.environ["SCOPUS_API_KEY"], "Accept": "application/json"}
    if os.getenv("SCOPUS_INSTTOKEN"):
        h["X-ELS-Insttoken"] = os.environ["SCOPUS_INSTTOKEN"]
    return h


def call(query: str, start: int, retries: int = 5) -> dict:
    params = {"query": query, "start": start, "count": PAGE}
    if os.getenv("SCOPUS_INSTTOKEN"):
        params["view"] = "COMPLETE"
    wait = 2.0
    for _ in range(retries):
        try:
            r = requests.get(API, headers=headers(), params=params, timeout=90)
        except requests.RequestException as exc:
            print(f"   ! red: {exc}", flush=True)
        else:
            if r.status_code == 200:
                return r.json()["search-results"]
            print(f"   ! HTTP {r.status_code}: {r.text[:200]}", flush=True)
            if r.status_code in (400, 401, 403):
                raise SystemExit(f"Scopus rechazó la consulta: {r.text[:300]}")
        time.sleep(wait)
        wait *= 2
    raise RuntimeError("Scopus no respondió")


def flatten(e: dict) -> dict:
    affs = e.get("affiliation") or []
    authors = [{"id": a.get("authid"), "name": a.get("authname"), "countries": [], "institutions": []}
               for a in e.get("author") or []]
    if not authors and e.get("dc:creator"):
        authors = [{"id": None, "name": e["dc:creator"], "countries": [], "institutions": []}]
    kw = e.get("authkeywords") or ""
    year = (e.get("prism:coverDate") or "")[:4]
    return {
        "id": "SCOPUS:" + (e.get("eid") or ""),
        "doi": ("https://doi.org/" + e["prism:doi"]) if e.get("prism:doi") else None,
        "title": e.get("dc:title"),
        "year": int(year) if year.isdigit() else None,
        "date": e.get("prism:coverDate"),
        "type": {"ar": "article", "re": "review"}.get(e.get("subtype"), e.get("subtype")),
        "language": None, "cited_by": int(e.get("citedby-count") or 0), "fwci": None,
        "is_retracted": False, "source": e.get("prism:publicationName"),
        "source_issn_l": e.get("prism:issn"), "source_type": e.get("prism:aggregationType"),
        "publisher": None, "authors": authors,
        "institutions": sorted({a.get("affilname") for a in affs if a.get("affilname")}),
        "countries": [], "abstract": e.get("dc:description") or "",
        "keywords": [k.strip() for k in kw.split("|") if k.strip()],
        "topics": [], "sdgs": [], "oa_status": None, "referenced_works": [],
    }


def harvest_range(base: str, y0: int, y1: int, out: list, parts: list) -> None:
    q = f"{base} AND PUBYEAR > {y0 - 1} AND PUBYEAR < {y1 + 1} AND DOCTYPE(ar OR re)"
    first = call(q, 0)
    total = int(first["opensearch:totalResults"])
    if total > MAX_START and y1 > y0:
        mid = (y0 + y1) // 2
        harvest_range(base, y0, mid, out, parts)
        harvest_range(base, mid + 1, y1, out, parts)
        return
    parts.append({"years": f"{y0}-{y1}", "query": q, "count": total})
    res, start = first, 0
    while True:
        out.extend(flatten(e) for e in res.get("entry", []) if "error" not in e)
        start += PAGE
        if start >= min(total, MAX_START):
            break
        res = call(q, start)
        time.sleep(0.12)
    print(f"   {y0}-{y1}: {total} -> acumulado {len(out)}", flush=True)


def enrich_with_openalex(qid: str, recs: list) -> int:
    """Busca en OpenAlex los DOI de Scopus ausentes en la cosecha de OpenAlex."""
    f = RAW_OA / f"{qid}.jsonl.gz"
    have = {norm_doi(r["doi"]) for r in read_jsonl_gz(f)} if f.exists() else set()
    missing = sorted({norm_doi(r["doi"]) for r in recs if r["doi"]} - have - {""})
    found = []
    for i in range(0, len(missing), 50):
        chunk = [d for d in missing[i:i + 50] if "," not in d and "|" not in d]
        if not chunk:
            continue
        data = oa.get({"filter": "doi:" + "|".join(chunk), "per-page": 50, "select": oa.SELECT})
        for w in data.get("results", []):
            rec = oa.flatten(w)
            rec["referenced_works"] = []
            found.append(rec)
        time.sleep(0.1)
    write_jsonl_gz(RAW_SCOPUS_API / f"{qid}_openalex.jsonl.gz", found)
    return len(found)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*")
    args = ap.parse_args()
    if not os.getenv("SCOPUS_API_KEY"):
        print("SCOPUS_API_KEY no definida: se omite la recolección en Scopus.")
        return
    cfg = load_config()
    g = cfg["global"]
    RAW_SCOPUS_API.mkdir(parents=True, exist_ok=True)
    log_path = RAW_SCOPUS_API / "search_log.json"
    logs = json.loads(log_path.read_text()) if log_path.exists() else {}
    for q in iter_queries(cfg):
        if args.only and q["id"] not in args.only:
            continue
        print(f"[{q['id']}] {q['name']}", flush=True)
        recs, parts = [], []
        harvest_range(q["scopus"], g["from_year"], g["to_year"], recs, parts)
        n = write_jsonl_gz(RAW_SCOPUS_API / f"{q['id']}.jsonl.gz", recs)
        enriched = enrich_with_openalex(q["id"], recs) if os.getenv("OPENALEX_API_KEY") else 0
        logs[q["id"]] = {
            "id": q["id"], "query_scopus": q["scopus"], "parts": parts,
            "count": sum(p["count"] for p in parts), "retrieved": n,
            "with_doi": sum(1 for r in recs if r["doi"]), "scopus_only_resolved_in_openalex": enriched,
            "view": "COMPLETE" if os.getenv("SCOPUS_INSTTOKEN") else "STANDARD",
            "date": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), **run_metadata(),
        }
        print(f"[{q['id']}] Scopus: {n} registros; {enriched} DOI adicionales enlazados en OpenAlex", flush=True)
        log_path.write_text(json.dumps(logs, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    try:
        main()
    except SystemExit as exc:
        print(exc, file=sys.stderr)
        raise
