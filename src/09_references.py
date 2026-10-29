"""Paso 9 - Referencias verificables de los estudios citados en el artículo.

Lee config/estudios_clave.csv (DOI, sección y justificación de cada cita),
consulta los metadatos de cada DOI en la API REST de Crossref y genera:
  * articulo/referencias.bib              (para Zotero, Mendeley o LaTeX)
  * articulo/referencias_apa.md           (lista en formato APA 7)
  * results/tables/estudios_clave.csv     (trazabilidad: DOI, sección, presencia en el corpus)
"""
from __future__ import annotations

import html
import json
import re
import time

import pandas as pd
import requests

from common import PROCESSED, RAW_OA, ROOT, TABLES, norm_doi, read_jsonl_gz

API = "https://api.crossref.org/works/"
CACHE = ROOT / "data" / "raw" / "crossref_cache.json"
ART = ROOT / "articulo"


def fetch(doi: str, cache: dict) -> dict | None:
    if doi in cache:
        return cache[doi]
    for _ in range(3):
        try:
            r = requests.get(API + requests.utils.quote(doi, safe="/:()<>;"), timeout=60,
                             headers={"User-Agent": "revision-bibliometrica/1.0"})
            if r.status_code == 200:
                cache[doi] = r.json()["message"]
                return cache[doi]
            if r.status_code == 404:
                cache[doi] = None
                return None
        except requests.RequestException:
            pass
        time.sleep(2)
    return None


PARTICLES = {"van", "von", "de", "der", "den", "da", "del", "la", "le", "du"}


def fix_particles(a: dict) -> dict:
    """Mueve partículas nobiliarias del nombre al apellido (p. ej. 'Nees Jan van' + 'Eck')."""
    given = (a.get("given") or "").split()
    tail = []
    while given and given[-1].lower() in PARTICLES:
        tail.insert(0, given.pop())
    if tail:
        a = {**a, "given": " ".join(given), "family": " ".join(tail + [a.get("family", "")])}
    return a


def apa_authors(m: dict) -> str:
    names = []
    for a in map(fix_particles, m.get("author") or []):
        if a.get("family"):
            ini = " ".join(f"{p[0]}." for p in re.split(r"[\s-]+", a.get("given", "")) if p)
            names.append(f"{a['family']}, {ini}".strip(", "))
        elif a.get("name"):
            names.append(a["name"])
    if not names:
        return ""
    if len(names) > 20:
        names = names[:19] + ["...", names[-1]]
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + ", & " + names[-1]


def year_of(m: dict):
    for k in ("published-print", "published-online", "issued", "created"):
        dp = (m.get(k) or {}).get("date-parts")
        if dp and dp[0] and dp[0][0]:
            return dp[0][0]
    return "s. f."


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html.unescape(text or ""))).strip()


def apa(m: dict, doi: str) -> str:
    title = clean((m.get("title") or [""])[0])
    cont = clean((m.get("container-title") or [""])[0])
    vol, iss, pg = m.get("volume"), m.get("issue"), m.get("page") or m.get("article-number")
    s = f"{apa_authors(m)} ({year_of(m)}). {title}."
    if cont:
        s += f" *{cont}*"
        if vol:
            s += f", *{vol}*"
        if iss:
            s += f"({iss})"
        if pg:
            s += f", {pg}"
        s += "."
    elif m.get("publisher"):
        s += f" {m['publisher']}."
    return s + f" https://doi.org/{doi}"


def bibkey(m: dict, used: set) -> str:
    fam = ((m.get("author") or [{}])[0].get("family") or "anon")
    key = re.sub(r"[^A-Za-z]", "", fam.encode("ascii", "ignore").decode()) + str(year_of(m))
    k, i = key, 0
    while k in used:
        i += 1
        k = key + "abcdefghij"[i - 1]
    used.add(k)
    return k


def bibtex(m: dict, doi: str, key: str) -> str:
    authors = " and ".join(f"{a.get('family', '')}, {a.get('given', '')}".strip(", ") if a.get("family")
                           else a.get("name", "") for a in m.get("author") or [])
    typ = "article" if m.get("type") == "journal-article" else "misc"
    fields = {"author": authors, "title": clean((m.get("title") or [""])[0]),
              "journal": clean((m.get("container-title") or [""])[0]), "year": year_of(m),
              "volume": m.get("volume"), "number": m.get("issue"), "pages": m.get("page"), "doi": doi}
    body = ",\n".join(f"  {k} = {{{v}}}" for k, v in fields.items() if v)
    return f"@{typ}{{{key},\n{body}\n}}"


def main() -> None:
    sel = pd.read_csv(ROOT / "config" / "estudios_clave.csv")
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    corpus = {norm_doi(r["doi"]): r for r in read_jsonl_gz(PROCESSED / "corpus.jsonl.gz") if r.get("doi")}
    refs = set()
    for f in RAW_OA.glob("*_top_refs.jsonl.gz"):
        refs |= {norm_doi(r["doi"]) for r in read_jsonl_gz(f) if r.get("doi")}
    rows, bib, apa_list, used = [], [], [], set()
    for _, s in sel.iterrows():
        doi = norm_doi(s["doi"])
        m = fetch(doi, cache)
        c = corpus.get(doi)
        if m:
            key = bibkey(m, used)
            m = {**m, "author": [fix_particles(a) for a in m.get("author") or []]}
            first = (m.get("author") or [{}])[0].get("family", "")
            n_aut = len(m.get("author") or [])
            cite = first if n_aut == 1 else (f"{first} y {m['author'][1].get('family', '')}" if n_aut == 2
                                             else f"{first} et al.")
            bib.append(bibtex(m, doi, key))
            apa_list.append(apa(m, doi))
        else:
            key, cite = "", ""
        rows.append({"doi": doi, "seccion": s["seccion"], "justificacion": s["justificacion"],
                     "cita_texto": f"{cite}, {year_of(m)}" if m else "", "bibkey": key,
                     "titulo": (m.get("title") or [""])[0] if m else "",
                     "en_corpus": bool(c), "niveles": ";".join(c["levels"]) if c else "",
                     "citas_openalex": c["cited_by"] if c else None,
                     "en_referencias_top": doi in refs, "verificado_crossref": bool(m)})
        time.sleep(0.05)
    CACHE.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
    pd.DataFrame(rows).to_csv(TABLES / "estudios_clave.csv", index=False)
    (ART / "referencias.bib").write_text("\n\n".join(bib) + "\n", encoding="utf-8")
    apa_list = sorted(set(apa_list), key=lambda s: s.lower())
    (ART / "referencias_apa.md").write_text("# Referencias (APA 7, generadas desde Crossref)\n\n" +
                                            "\n\n".join(apa_list) + "\n", encoding="utf-8")
    bad = [r["doi"] for r in rows if not r["verificado_crossref"]]
    print(f"{len(rows)} referencias; no verificadas en Crossref: {bad}")


if __name__ == "__main__":
    main()
