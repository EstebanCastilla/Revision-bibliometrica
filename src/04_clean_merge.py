"""Paso 4 - Limpieza, fusión, deduplicación y cribado (flujo PRISMA).

Entradas : data/raw/openalex/*.jsonl.gz, data/raw/scopus_api/*.jsonl.gz,
           data/raw/scopus_export/*.jsonl.gz
Salidas  : data/processed/corpus.jsonl.gz   (registros únicos incluidos)
           data/processed/excluded.csv       (registros excluidos y motivo)
           data/processed/vosviewer/<nivel>.csv (formato Scopus para VOSviewer/biblioshiny)
           results/tables/prisma_*.csv, results/tables/search_strategy.csv
"""
from __future__ import annotations

import json
import re
from collections import defaultdict

import pandas as pd

from common import (PROCESSED, RAW_OA, RAW_SCOPUS_API, RAW_SCOPUS_CSV, TABLES,
                    iter_queries, load_config, norm_doi, norm_title, read_jsonl_gz, write_jsonl_gz)

try:
    import pycountry
except ImportError:  # pragma: no cover
    pycountry = None

# Grupos de análisis: cada consulta se asigna a un nivel jerárquico
LEVEL_OF = lambda qid: "N6" if qid.startswith("N6") else qid[:2]  # noqa: E731
LEVEL_NAMES = {
    "N1": "N1 Sostenibilidad de biorrefinerías",
    "N2": "N2 ACV-S / LCSA en sistemas de base biológica",
    "N3": "N3 Raíces y tubérculos en bioprocesos",
    "N4": "N4 Ñame y batata: rutas de transformación",
    "N5": "N5 Sostenibilidad de ñame y batata",
    "N6": "N6 Contexto Colombia / Caribe",
}

# ---------------------------------------------------------------------------
# Reglas de elegibilidad (verificación en título + resumen + palabras clave)
# ---------------------------------------------------------------------------
RX = {
    "yam": re.compile(r"\b(yams?|dioscorea|ñame|name tubers?)\b", re.I),
    "sweet": re.compile(r"\b(sweet ?potato(es)?|ipomoea batatas|batata)\b", re.I),
    "crops": re.compile(r"\b(cassava|manioc|manihot|yams?|dioscorea|sweet ?potato(es)?|ipomoea batatas|"
                        r"potato(es)?|solanum tuberosum|taro|cocoyam|colocasia|xanthosoma|root crops?|"
                        r"tuber crops?|tubers?)\b", re.I),
    "biorefinery": re.compile(r"bio-?refin", re.I),
    "social": re.compile(r"social life[- ]cycle|s-?lca\b|social lca|life[- ]cycle sustainability|\blcsa\b", re.I),
    "colombia": re.compile(r"colombia|montes de mar[ií]a", re.I),
}
FALSE_POSITIVES = re.compile(r"\byam ?beans?\b|pachyrhizus", re.I)


def text_of(rec: dict) -> str:
    return " ".join([rec.get("title") or "", rec.get("abstract") or "", " ".join(rec.get("keywords") or [])])


def eligible(qid: str, rec: dict) -> tuple[bool, str]:
    t = FALSE_POSITIVES.sub(" ", text_of(rec))
    if qid in ("N1", "N6b") and not RX["biorefinery"].search(t):
        return False, "sin mención a biorrefinería"
    if qid == "N2" and not RX["social"].search(t):
        return False, "sin dimensión social / LCSA"
    if qid == "N3" and not RX["crops"].search(t):
        return False, "sin cultivo de raíz o tubérculo"
    if qid == "N4e" and not RX["yam"].search(t):
        return False, "sin mención a ñame (Dioscorea)"
    if qid == "N4f" and not RX["sweet"].search(t):
        return False, "sin mención a batata"
    if (qid.startswith("N4") or qid == "N5") and not (RX["yam"].search(t) or RX["sweet"].search(t)):
        return False, "falso positivo (p. ej. 'yam bean') o sin ñame/batata"
    if qid == "N6" and not (RX["colombia"].search(t) or "CO" in (rec.get("countries") or [])):
        return False, "sin vínculo con Colombia"
    return True, ""


def load_raw():
    """Devuelve (registros, conteos de identificación por consulta y fuente)."""
    out, ident = [], []
    sources = [("OpenAlex", RAW_OA), ("Scopus API", RAW_SCOPUS_API), ("Scopus CSV", RAW_SCOPUS_CSV)]
    cfg = load_config()
    for q in iter_queries(cfg):
        for src_name, folder in sources:
            f = folder / f"{q['id']}.jsonl.gz"
            if not f.exists():
                continue
            recs = list(read_jsonl_gz(f))
            ident.append({"query": q["id"], "level": LEVEL_OF(q["id"]), "source": src_name, "records": len(recs)})
            for r in recs:
                r["_query"], r["_source"] = q["id"], src_name
                out.append(r)
    return out, pd.DataFrame(ident)


def merge(records: list[dict]) -> list[dict]:
    """Deduplica por DOI y, en su defecto, por título normalizado + año."""
    by_key: dict[str, dict] = {}
    alias: dict[str, str] = {}
    for r in records:
        doi, tkey = norm_doi(r.get("doi")), norm_title(r.get("title"))
        keys = [k for k in (f"doi:{doi}" if doi else None, f"t:{tkey}|{r.get('year')}" if tkey else None) if k]
        if not keys:
            keys = [f"id:{r['id']}"]
        main = next((alias[k] for k in keys if k in alias), keys[0])
        for k in keys:
            alias.setdefault(k, main)
        if main not in by_key:
            base = {k: v for k, v in r.items() if not k.startswith("_")}
            base.update(queries=set(), sources=set())
            by_key[main] = base
        cur = by_key[main]
        cur["queries"].add(r["_query"])
        cur["sources"].add(r["_source"])
        # completa campos vacíos con la otra fuente
        for k, v in r.items():
            if not k.startswith("_") and v and not cur.get(k):
                cur[k] = v
        cur["cited_by"] = max(cur.get("cited_by") or 0, r.get("cited_by") or 0)
    return list(by_key.values())


def country_name(code: str) -> str:
    if pycountry and len(code) == 2:
        c = pycountry.countries.get(alpha_2=code.upper())
        if c:
            return getattr(c, "common_name", None) or c.name
    return code


def scopus_like(df: pd.DataFrame) -> pd.DataFrame:
    """Exporta en columnas tipo Scopus para abrir en VOSviewer o biblioshiny."""
    rows = []
    for _, r in df.iterrows():
        affs = []
        for a in r["authors"]:
            for inst in a.get("institutions") or ["(sin afiliación)"]:
                cs = a.get("countries") or [""]
                affs.append(f"{inst}, {country_name(cs[0])}".strip(", "))
        rows.append({
            "Authors": "; ".join(a["name"] or "" for a in r["authors"]),
            "Author(s) ID": "; ".join((a["id"] or "").rsplit("/", 1)[-1] for a in r["authors"]),
            "Title": r["title"], "Year": r["year"], "Source title": r["source"],
            "Cited by": r["cited_by"], "DOI": norm_doi(r["doi"]),
            "Affiliations": "; ".join(dict.fromkeys(affs)),
            "Abstract": r["abstract"], "Author Keywords": "; ".join(r["keywords"]),
            "Index Keywords": "; ".join(t["topic"] for t in r["topics"]),
            "Document Type": "Review" if r["type"] == "review" else "Article",
            "Language of Original Document": r["language"], "Source": "OpenAlex", "EID": r["id"],
        })
    return pd.DataFrame(rows)


def main() -> None:
    cfg = load_config()
    g = cfg["global"]
    raw, ident = load_raw()
    if not raw:
        raise SystemExit("No hay datos crudos. Ejecute primero src/01_harvest_openalex.py")
    merged = merge(raw)

    excluded, included = [], []
    for r in merged:
        reason = None
        if not r.get("title"):
            reason = "sin título"
        elif r.get("is_retracted"):
            reason = "artículo retractado"
        elif not r.get("year") or not g["from_year"] <= r["year"] <= g["to_year"]:
            reason = "fuera del periodo"
        elif r.get("type") not in g["types"]:
            reason = "tipo documental no elegible"
        if reason:
            excluded.append({"id": r["id"], "title": r.get("title"), "stage": "cribado", "reason": reason,
                             "queries": ";".join(sorted(r["queries"]))})
            continue
        keep, reasons = set(), []
        for qid in r["queries"]:
            ok, why = eligible(qid, r)
            (keep.add(qid) if ok else reasons.append(f"{qid}: {why}"))
        if not keep:
            excluded.append({"id": r["id"], "title": r.get("title"), "stage": "elegibilidad",
                             "reason": " | ".join(reasons), "queries": ";".join(sorted(r["queries"]))})
            continue
        r["queries"] = sorted(keep)
        r["levels"] = sorted({LEVEL_OF(q) for q in keep})
        r["sources"] = sorted(r["sources"])
        r["has_abstract"] = bool(r.get("abstract"))
        included.append(r)

    PROCESSED.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)
    write_jsonl_gz(PROCESSED / "corpus.jsonl.gz", included)
    exc = pd.DataFrame(excluded)
    exc.to_csv(PROCESSED / "excluded.csv", index=False)

    # ---- Tablas PRISMA por nivel -------------------------------------------
    prisma = []
    raw_df = pd.DataFrame({"query": [r["_query"] for r in raw]})
    raw_df["level"] = raw_df["query"].map(LEVEL_OF)
    for lvl in list(LEVEL_NAMES) + ["Total"]:
        sel = (lambda qs: True) if lvl == "Total" else (lambda qs, l=lvl: any(LEVEL_OF(q) == l for q in qs))
        identified = len(raw_df) if lvl == "Total" else int((raw_df["level"] == lvl).sum())
        unique = sum(1 for r in merged if sel(r["queries"]))
        exc_screen = sum(1 for e in excluded if e["stage"] == "cribado" and sel(e["queries"].split(";")))
        exc_elig = sum(1 for e in excluded if e["stage"] == "elegibilidad" and sel(e["queries"].split(";")))
        incl = sum(1 for r in included if lvl == "Total" or lvl in r["levels"])
        prisma.append({"level": lvl, "name": LEVEL_NAMES.get(lvl, "Corpus total (registros únicos)"),
                       "identified": identified, "duplicates_removed": identified - unique,
                       "screened": unique, "excluded_screening": exc_screen,
                       "assessed_eligibility": unique - exc_screen, "excluded_eligibility": exc_elig,
                       "included": incl})
    pd.DataFrame(prisma).to_csv(TABLES / "prisma_flow.csv", index=False)
    ident.to_csv(TABLES / "prisma_identification_by_query.csv", index=False)
    if not exc.empty:
        (exc.assign(reason=exc["reason"].str.replace(r"N\d\w?: ", "", regex=True).str.split(" | ", regex=False))
            .explode("reason").groupby(["stage", "reason"]).size().rename("n").reset_index()
            .sort_values("n", ascending=False).to_csv(TABLES / "prisma_exclusion_reasons.csv", index=False))

    # ---- Estrategia de búsqueda documentada -------------------------------
    log_path = RAW_OA / "search_log.json"
    logs = json.loads(log_path.read_text()) if log_path.exists() else {}
    strat = []
    for q in iter_queries(cfg):
        lg = logs.get(q["id"], {})
        strat.append({"id": q["id"], "level": LEVEL_OF(q["id"]), "name": q["name"],
                      "openalex_query": q["openalex"], "extra_filter": q.get("extra_filter") or "",
                      "scopus_query": q["scopus"], "openalex_hits": lg.get("count"),
                      "retrieved": lg.get("retrieved"), "date": lg.get("date"),
                      "included": sum(1 for r in included if q["id"] in r["queries"])})
    pd.DataFrame(strat).to_csv(TABLES / "search_strategy.csv", index=False)

    # ---- Exportación para VOSviewer / biblioshiny --------------------------
    df = pd.DataFrame(included)
    vos = PROCESSED / "vosviewer"
    vos.mkdir(exist_ok=True)
    for lvl in LEVEL_NAMES:
        sub = df[df["levels"].apply(lambda ls, l=lvl: l in ls)]
        scopus_like(sub).to_csv(vos / f"{lvl}_scopus_format.csv", index=False)
    print(pd.DataFrame(prisma).to_string(index=False))
    print(f"Corpus incluido: {len(included)} registros únicos -> {PROCESSED / 'corpus.jsonl.gz'}")


if __name__ == "__main__":
    main()
