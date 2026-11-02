"""Paso 3b - Importa exportaciones de la plataforma web de Web of Science.

Alternativa a la API cuando se tiene acceso institucional a webofscience.com:
ejecute en *Advanced Search* la cadena `wos` de cada consulta
(config/queries.yaml) con el periodo 2000-2026 y los tipos Article y Review, y
exporte los resultados como **Plain text file** o **Tab delimited file** con
*Full Record* (máximo 1.000 registros por exportación). Guarde los archivos en
data/raw/wos_export/ con el ID de la consulta como prefijo, por ejemplo:

    N1_0001-1000.txt, N1_1001-2000.txt, N4b.txt, ...

Las exportaciones de WoS sí incluyen resumen, palabras clave y direcciones,
por lo que estos registros no requieren enlace con OpenAlex.
"""
from __future__ import annotations

import csv
import io
import re
from collections import defaultdict

from common import RAW_WOS_EXPORT, country_to_iso2, iter_queries, load_config, write_jsonl_gz

MULTI = {"AU", "AF", "C1", "CR"}  # campos con un valor por línea


def read_text(path) -> str:
    raw = path.read_bytes()
    for enc in ("utf-8-sig", "utf-16"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("latin-1")


def parse_plain(text: str) -> list[dict]:
    recs, cur, tag = [], {}, None
    for line in text.splitlines():
        if line.startswith("ER"):
            recs.append(cur)
            cur, tag = {}, None
            continue
        if line[:2].strip() and (len(line) == 2 or line[2] == " "):
            tag, val = line[:2], line[3:]
            if tag in ("FN", "VR", "EF"):
                continue
            cur.setdefault(tag, []).append(val)
        elif tag and line.startswith("   "):
            if tag in MULTI:
                cur[tag].append(line[3:])
            else:
                cur[tag][-1] += " " + line[3:]
    return [{k: ("; ".join(v) if k in MULTI else " ".join(v)) for k, v in r.items()} for r in recs]


def parse_tab(text: str) -> list[dict]:
    return list(csv.DictReader(io.StringIO(text), delimiter="\t", quoting=csv.QUOTE_NONE))


def countries_from_c1(c1: str) -> list[str]:
    out = set()
    for addr in re.split(r";\s*(?=\[)|;\s*", c1 or ""):
        addr = re.sub(r"^\[[^\]]*\]\s*", "", addr).strip().rstrip(".")
        if not addr:
            continue
        last = addr.split(",")[-1].strip()
        if re.search(r"\bUSA$", last):
            last = "USA"
        iso = country_to_iso2(last)
        if iso:
            out.add(iso)
    return sorted(out)


def to_record(r: dict) -> dict:
    dt_ = (r.get("DT") or "").lower()
    py = (r.get("PY") or "").strip()
    split = lambda v: [x.strip() for x in (v or "").split(";") if x.strip()]  # noqa: E731
    countries = countries_from_c1(r.get("C1", ""))
    return {
        "id": r.get("UT"),
        "doi": ("https://doi.org/" + r["DI"].strip()) if (r.get("DI") or "").strip() else None,
        "title": (r.get("TI") or "").strip() or None,
        "year": int(py) if py.isdigit() else None,
        "date": None,
        "type": "review" if "review" in dt_ else "article",
        "language": (r.get("LA") or "").strip().lower()[:2] or None,
        "cited_by": int(r["TC"]) if (r.get("TC") or "").strip().isdigit() else 0,
        "fwci": None, "is_retracted": "retracted" in dt_,
        "source": (r.get("SO") or "").strip().title() or None,
        "source_issn_l": r.get("SN") or r.get("EI"),
        "source_type": "journal", "publisher": r.get("PU"),
        "authors": [{"id": None, "name": a, "countries": [], "institutions": []}
                    for a in split(r.get("AF") or r.get("AU"))],
        "institutions": split(r.get("C3")),
        "countries": countries,
        "abstract": (r.get("AB") or "").strip(),
        "keywords": split(r.get("DE")) + split(r.get("ID")),
        "topics": [{"topic": t, "subfield": None, "field": None, "domain": None} for t in split(r.get("WC"))],
        "sdgs": [], "oa_status": None, "referenced_works": [],
    }


def main() -> None:
    files = sorted(RAW_WOS_EXPORT.glob("*.txt"))
    if not files:
        print("No hay exportaciones de Web of Science en", RAW_WOS_EXPORT, "- se omite.")
        return
    ids = sorted((q["id"] for q in iter_queries(load_config())), key=len, reverse=True)
    groups = defaultdict(list)
    for f in files:
        qid = next((i for i in ids if re.match(rf"{i}(?![a-z0-9])", f.stem, re.I)), None)
        if not qid:
            print(f"! {f.name}: el nombre no empieza por un ID de consulta; se omite")
            continue
        text = read_text(f)
        rows = parse_plain(text) if text.lstrip().startswith("FN ") else parse_tab(text)
        groups[qid].extend(to_record(r) for r in rows if r.get("TI") or r.get("UT"))
    for qid, recs in groups.items():
        uniq = {r["id"] or r["title"]: r for r in recs}
        n = write_jsonl_gz(RAW_WOS_EXPORT / f"{qid}.jsonl.gz", uniq.values())
        print(f"{qid}: {n} registros importados de Web of Science")


if __name__ == "__main__":
    main()
