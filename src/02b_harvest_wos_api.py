"""Paso 2b - Recolección desde Web of Science (Clarivate) mediante la WoS Starter API.

Ejecuta las cadenas `wos` de config/queries.yaml (etiqueta TS = título,
resumen, palabras clave de autor y Keywords Plus) sobre la Web of Science Core
Collection (db=WOS), restringidas a 2000-2026 y a artículos y revisiones.

Planes de la WoS Starter API (https://developer.clarivate.com/apis/wos-starter,
consultado el 2026-11-02):
  * Free Trial: cualquier persona; 50 peticiones/día; no devuelve citas.
  * Free Institutional Member: miembros de instituciones suscritas a WoS;
    5.000 peticiones/día; devuelve citas.
Cada petición devuelve hasta 50 registros. El script guarda el avance página a
página y, si se agota la cuota diaria (HTTP 429), se detiene sin perder datos:
al volver a ejecutarlo continúa donde quedó.

La Starter API no entrega resúmenes ni afiliaciones; como en Scopus, los DOI
que no están en la cosecha de OpenAlex se completan con metadatos de OpenAlex
(data/raw/wos_api/<ID>_openalex.jsonl.gz).

Uso:
    export WOS_API_KEY=xxxxx            # clave de developer.clarivate.com
    export OPENALEX_API_KEY=yyyy
    python src/02b_harvest_wos_api.py --counts-only   # 14 peticiones: solo conteos
    python src/02b_harvest_wos_api.py                 # cosecha completa (reanudable)
    python src/02b_harvest_wos_api.py --only N1 N4b
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

from common import ROOT, RAW_WOS_API, iter_queries, load_config, read_jsonl_gz, run_metadata, write_jsonl_gz

API = "https://api.clarivate.com/apis/wos-starter/v1/documents"
PAGE = 50
MAX_RESULTS = 10_000  # por seguridad: consultas mayores se dividen por años

_spec = importlib.util.spec_from_file_location("sc", ROOT / "src" / "02_harvest_scopus_api.py")
sc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sc)


class QuotaExceeded(Exception):
    pass


def call(q: str, page: int, limit: int = PAGE, retries: int = 5) -> dict:
    wait = 2.0
    for _ in range(retries):
        try:
            r = requests.get(API, timeout=90, headers={"X-ApiKey": os.environ["WOS_API_KEY"]},
                             params={"q": q, "db": "WOS", "limit": limit, "page": page})
        except requests.RequestException as exc:
            print(f"   ! red: {exc}", flush=True)
        else:
            if r.status_code == 200:
                time.sleep(1.05)  # límite de 1 petición por segundo del plan gratuito
                return r.json()
            if r.status_code == 429 and "day" in r.text.lower():
                raise QuotaExceeded(r.text[:200])
            print(f"   ! HTTP {r.status_code}: {r.text[:200]}", flush=True)
            if r.status_code in (400, 401, 403):
                raise SystemExit(f"WoS rechazó la consulta: {r.text[:300]}")
        time.sleep(wait)
        wait *= 2
    raise RuntimeError("WoS no respondió")


def full_query(base: str, y0: int, y1: int) -> str:
    return f"{base} AND PY=({y0}-{y1}) AND DT=(Article OR Review)"


def flatten(h: dict) -> dict:
    src = h.get("source") or {}
    ids = h.get("identifiers") or {}
    types = [t.lower() for t in (h.get("types") or []) + (h.get("sourceTypes") or [])]
    cites = [c.get("count") for c in h.get("citations") or [] if c.get("db", "").upper() == "WOS"]
    year = src.get("publishYear")
    return {
        "id": h.get("uid"),
        "doi": ("https://doi.org/" + ids["doi"]) if ids.get("doi") else None,
        "title": h.get("title"),
        "year": int(year) if str(year or "").isdigit() else None,
        "date": None,
        "type": "review" if any("review" in t for t in types) else "article",
        "language": None,
        "cited_by": int(cites[0]) if cites and cites[0] is not None else 0,
        "fwci": None, "is_retracted": False,
        "source": src.get("sourceTitle"),
        "source_issn_l": ids.get("issn") or ids.get("eissn"),
        "source_type": "journal", "publisher": None,
        "authors": [{"id": a.get("researcherId"), "name": a.get("displayName") or a.get("wosStandard"),
                     "countries": [], "institutions": []}
                    for a in (h.get("names") or {}).get("authors") or []],
        "institutions": [], "countries": [], "abstract": "",
        "keywords": (h.get("keywords") or {}).get("authorKeywords") or [],
        "topics": [], "sdgs": [], "oa_status": None, "referenced_works": [],
    }


def year_parts(base: str, y0: int, y1: int, parts: list) -> None:
    """Divide el periodo en rangos de años con menos de MAX_RESULTS resultados."""
    total = call(full_query(base, y0, y1), 1, limit=1)["metadata"]["total"]
    if total > MAX_RESULTS and y1 > y0:
        mid = (y0 + y1) // 2
        year_parts(base, y0, mid, parts)
        year_parts(base, mid + 1, y1, parts)
    else:
        parts.append({"years": f"{y0}-{y1}", "query": full_query(base, y0, y1), "count": total})


def harvest(q: dict, cfg: dict, state: dict) -> dict:
    """Cosecha reanudable: `state` guarda los rangos, la siguiente página y los registros."""
    g = cfg["global"]
    if not state.get("parts"):
        state["parts"] = []
        year_parts(q["wos"], g["from_year"], g["to_year"], state["parts"])
        for p in state["parts"]:
            p["next_page"] = 1
    partial = RAW_WOS_API / f"{q['id']}.partial.jsonl.gz"
    recs = list(read_jsonl_gz(partial)) if partial.exists() else []
    try:
        for p in state["parts"]:
            n_pages = -(-min(p["count"], MAX_RESULTS) // PAGE)
            while p["next_page"] <= n_pages:
                data = call(p["query"], p["next_page"])
                recs.extend(flatten(h) for h in data.get("hits") or [])
                p["next_page"] += 1
            print(f"   {p['years']}: {p['count']} -> acumulado {len(recs)}", flush=True)
    finally:
        write_jsonl_gz(partial, recs)
    partial.rename(RAW_WOS_API / f"{q['id']}.jsonl.gz")
    state["complete"] = True
    state["retrieved"] = len(recs)
    return state


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--counts-only", action="store_true")
    ap.add_argument("--force", action="store_true", help="repite consultas ya completas")
    args = ap.parse_args()
    if not os.getenv("WOS_API_KEY"):
        print("WOS_API_KEY no definida: se omite Web of Science.")
        return
    cfg = load_config()
    g = cfg["global"]
    RAW_WOS_API.mkdir(parents=True, exist_ok=True)
    log_path = RAW_WOS_API / "search_log.json"
    logs = json.loads(log_path.read_text()) if log_path.exists() else {}
    try:
        for q in iter_queries(cfg):
            if args.only and q["id"] not in args.only:
                continue
            st = logs.get(q["id"], {})
            if args.counts_only:
                total = call(full_query(q["wos"], g["from_year"], g["to_year"]), 1, limit=1)["metadata"]["total"]
                st.update(id=q["id"], query_wos=q["wos"], count=total)
                print(f"[{q['id']}] WoS: {total} registros", flush=True)
            else:
                if st.get("complete") and not args.force:
                    print(f"[{q['id']}] ya completa ({st.get('retrieved')} registros); se omite")
                    continue
                if args.force:
                    st = {}
                print(f"[{q['id']}] {q['name']}", flush=True)
                st.update(id=q["id"], query_wos=q["wos"])
                logs[q["id"]] = st
                harvest(q, cfg, st)
                st["count"] = sum(p["count"] for p in st["parts"])
                recs = list(read_jsonl_gz(RAW_WOS_API / f"{q['id']}.jsonl.gz"))
                st["with_doi"] = sum(1 for r in recs if r["doi"])
                st["only_wos_resolved_in_openalex"] = (
                    sc.enrich_with_openalex(q["id"], recs, RAW_WOS_API) if os.getenv("OPENALEX_API_KEY") else 0)
                print(f"[{q['id']}] WoS: {st['retrieved']} registros; "
                      f"{st['only_wos_resolved_in_openalex']} DOI adicionales enlazados en OpenAlex", flush=True)
            st.update(date=dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                      database="Web of Science Core Collection (WoS Starter API)",
                      plan=os.getenv("WOS_API_PLAN", "no declarado"), **run_metadata())
            logs[q["id"]] = st
            log_path.write_text(json.dumps(logs, indent=2, ensure_ascii=False), encoding="utf-8")
    except QuotaExceeded as exc:
        log_path.write_text(json.dumps(logs, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Cuota diaria de WoS agotada ({exc}). Avance guardado; vuelva a ejecutar mañana.",
              file=sys.stderr)


if __name__ == "__main__":
    main()
