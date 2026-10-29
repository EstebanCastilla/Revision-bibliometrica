"""Paso 1 - Recolección automatizada de registros desde la API REST de OpenAlex.

Técnica: consumo programático de una API REST documentada (OpenAlex, Priem et al.,
2022) con paginación por cursor, reintentos con espera exponencial y registro
(log) de cada consulta, fecha de ejecución y número de resultados. Es la
alternativa reproducible y legal al "web scraping" de bases de datos
comerciales, cuyos términos de uso prohíben la extracción automatizada del
sitio web.

Uso:
    python src/01_harvest_openalex.py               # todas las consultas
    python src/01_harvest_openalex.py --only N1 N4a  # consultas puntuales
    python src/01_harvest_openalex.py --counts-only  # solo conteos

Variables de entorno opcionales:
    OPENALEX_API_KEY   clave gratuita de OpenAlex (https://openalex.org/settings/api)
    OPENALEX_MAILTO    correo para el "polite pool"
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import time
from collections import Counter

import requests

from common import RAW_OA, iter_queries, load_config, write_jsonl_gz

API = "https://api.openalex.org/works"
SELECT = ",".join([
    "id", "doi", "title", "publication_year", "publication_date", "type", "language",
    "cited_by_count", "fwci", "is_retracted", "authorships", "primary_location",
    "abstract_inverted_index", "keywords", "topics", "primary_topic",
    "referenced_works", "sustainable_development_goals", "open_access",
])
SESSION = requests.Session()
SESSION.headers["User-Agent"] = "revision-bibliometrica/1.0 (tesis de maestria; python-requests)"


def base_params() -> dict:
    params = {}
    if os.getenv("OPENALEX_API_KEY"):
        params["api_key"] = os.environ["OPENALEX_API_KEY"]
    if os.getenv("OPENALEX_MAILTO"):
        params["mailto"] = os.environ["OPENALEX_MAILTO"]
    return params


def get(params: dict, retries: int = 6) -> dict:
    wait = 2.0
    for attempt in range(retries):
        try:
            r = SESSION.get(API, params={**base_params(), **params}, timeout=90)
        except requests.RequestException as exc:  # red inestable
            print(f"   ! error de red: {exc}; reintento en {wait:.0f}s", flush=True)
        else:
            if r.status_code == 200:
                return r.json()
            print(f"   ! HTTP {r.status_code}: {r.text[:300]}; reintento en {wait:.0f}s", flush=True)
            if r.status_code in (400, 401, 403):
                r.raise_for_status()
        time.sleep(wait)
        wait *= 2
    raise RuntimeError("OpenAlex no respondió tras varios reintentos")


def build_filter(q: dict, cfg: dict) -> str:
    g = cfg["global"]
    parts = [
        f'title_and_abstract.search:{q["openalex"]}',
        f'publication_year:{g["from_year"]}-{g["to_year"]}',
        "type:" + "|".join(g["types"]),
    ]
    if q.get("extra_filter"):
        parts.append(q["extra_filter"])
    return ",".join(parts)


def abstract_from_index(inv: dict | None) -> str:
    if not inv:
        return ""
    pos = {}
    for word, idxs in inv.items():
        for i in idxs:
            pos[i] = word
    return " ".join(pos[i] for i in sorted(pos))


def flatten(w: dict) -> dict:
    """Reduce el registro de OpenAlex a los campos necesarios para el análisis."""
    loc = w.get("primary_location") or {}
    src = loc.get("source") or {}
    authors, insts, countries = [], [], []
    for a in w.get("authorships") or []:
        au = a.get("author") or {}
        authors.append({
            "id": au.get("id"),
            "name": au.get("display_name"),
            "position": a.get("author_position"),
            "corresponding": a.get("is_corresponding"),
            "countries": a.get("countries") or [],
            "institutions": [i.get("display_name") for i in a.get("institutions") or []],
        })
        insts.extend(i.get("display_name") for i in a.get("institutions") or [])
        countries.extend(a.get("countries") or [])
    return {
        "id": w.get("id"),
        "doi": w.get("doi"),
        "title": w.get("title"),
        "year": w.get("publication_year"),
        "date": w.get("publication_date"),
        "type": w.get("type"),
        "language": w.get("language"),
        "cited_by": w.get("cited_by_count"),
        "fwci": w.get("fwci"),
        "is_retracted": w.get("is_retracted"),
        "source": src.get("display_name"),
        "source_issn_l": src.get("issn_l"),
        "source_type": src.get("type"),
        "publisher": src.get("host_organization_name"),
        "authors": authors,
        "institutions": sorted({i for i in insts if i}),
        "countries": sorted(set(countries)),
        "abstract": abstract_from_index(w.get("abstract_inverted_index")),
        "keywords": [k.get("display_name") for k in w.get("keywords") or []],
        "topics": [
            {
                "topic": t.get("display_name"),
                "subfield": (t.get("subfield") or {}).get("display_name"),
                "field": (t.get("field") or {}).get("display_name"),
                "domain": (t.get("domain") or {}).get("display_name"),
            }
            for t in w.get("topics") or []
        ],
        "sdgs": [s.get("display_name") for s in w.get("sustainable_development_goals") or []],
        "oa_status": (w.get("open_access") or {}).get("oa_status"),
        "referenced_works": w.get("referenced_works") or [],
    }


def harvest(q: dict, cfg: dict, counts_only: bool) -> dict:
    flt = build_filter(q, cfg)
    first = get({"filter": flt, "per-page": 1, "select": "id"})
    total = first["meta"]["count"]
    print(f"[{q['id']}] {q['name']}: {total} registros", flush=True)
    log = {
        "id": q["id"], "parent": q["parent"], "name": q["name"],
        "query_openalex": q["openalex"], "filter": flt, "query_scopus": q["scopus"],
        "count": total, "retrieved": 0,
        "date": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
    }
    if counts_only:
        return log

    cap = cfg["global"]["max_records"]
    cursor, records = "*", []
    while cursor and len(records) < cap:
        data = get({"filter": flt, "per-page": cfg["global"]["per_page"],
                    "cursor": cursor, "select": SELECT})
        batch = data.get("results", [])
        if not batch:
            break
        records.extend(flatten(w) for w in batch)
        cursor = data["meta"].get("next_cursor")
        print(f"   {len(records)}/{total}", flush=True)
        time.sleep(0.12)
    log["retrieved"] = write_jsonl_gz(RAW_OA / f"{q['id']}.jsonl.gz", records)

    # Referencias más citadas localmente (base intelectual del corpus)
    refs = Counter(r for rec in records for r in rec["referenced_works"])
    top = [wid for wid, _ in refs.most_common(60)]
    resolved = []
    for i in range(0, len(top), 50):
        chunk = top[i:i + 50]
        ids = "|".join(w.rsplit("/", 1)[-1] for w in chunk)
        data = get({"filter": f"openalex:{ids}", "per-page": 50, "select": SELECT})
        resolved.extend(data.get("results", []))
    top_refs = []
    for w in resolved:
        f = flatten(w)
        f["local_citations"] = refs[w["id"]]
        f.pop("referenced_works", None)
        top_refs.append(f)
    top_refs.sort(key=lambda r: -r["local_citations"])
    write_jsonl_gz(RAW_OA / f"{q['id']}_top_refs.jsonl.gz", top_refs)
    return log


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", help="IDs de consulta a ejecutar")
    ap.add_argument("--counts-only", action="store_true")
    args = ap.parse_args()

    cfg = load_config()
    RAW_OA.mkdir(parents=True, exist_ok=True)
    log_path = RAW_OA / "search_log.json"
    logs = json.loads(log_path.read_text()) if log_path.exists() else {}
    for q in iter_queries(cfg):
        if args.only and q["id"] not in args.only:
            continue
        try:
            logs[q["id"]] = harvest(q, cfg, args.counts_only)
        except Exception as exc:
            print(f"[{q['id']}] FALLÓ: {exc}", file=sys.stderr)
            raise
        log_path.write_text(json.dumps(logs, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Listo. Registro de búsqueda en", log_path)


if __name__ == "__main__":
    main()
