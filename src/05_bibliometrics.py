"""Paso 5 - Análisis de desempeño (performance analysis) por nivel jerárquico.

Indicadores: producción anual y tasa de crecimiento anual compuesta (TCAC),
fuentes y ley de Bradford, autores y ley de Lotka, países y colaboración
internacional (SCP/MCP), documentos y referencias más citados, áreas temáticas
(OpenAlex topics) y Objetivos de Desarrollo Sostenible.
"""
from __future__ import annotations

from collections import Counter

import numpy as np
import pandas as pd

from common import FIGURES, PROCESSED, RAW_OA, TABLES, iter_queries, load_config, read_jsonl_gz
from viz import INK2, SERIES, plt, save

LEVELS = ["N1", "N2", "N3", "N4", "N5", "N6"]
LABELS = {
    "N1": "N1 Sostenibilidad de biorrefinerías",
    "N2": "N2 ACV-S / LCSA",
    "N3": "N3 Raíces y tubérculos",
    "N4": "N4 Ñame y batata (rutas)",
    "N5": "N5 Sostenibilidad ñame/batata",
    "N6": "N6 Colombia / Caribe",
}
LAST_FULL_YEAR = 2025


def load() -> pd.DataFrame:
    return pd.DataFrame(list(read_jsonl_gz(PROCESSED / "corpus.jsonl.gz")))


def subset(df, lvl):
    return df[df["levels"].apply(lambda ls: lvl in ls)]


def cagr(series: pd.Series) -> float:
    s = series[series.index <= LAST_FULL_YEAR]
    s = s[s.index >= s[s > 0].index.min()]
    if len(s) < 2 or s.iloc[0] == 0:
        return float("nan")
    return ((s.iloc[-1] / s.iloc[0]) ** (1 / (s.index[-1] - s.index[0])) - 1) * 100


def h_index(cites) -> int:
    c = sorted(cites, reverse=True)
    return sum(1 for i, x in enumerate(c, 1) if x >= i)


def summary(df: pd.DataFrame, lvl: str) -> dict:
    years = df["year"].value_counts().sort_index()
    full = years.reindex(range(int(df["year"].min()), LAST_FULL_YEAR + 1), fill_value=0)
    n_auth = df["authors"].apply(len)
    authors = {a["id"] or a["name"] for al in df["authors"] for a in al}
    intl = df["countries"].apply(lambda c: len(c) > 1)
    return {
        "Nivel": lvl, "Documentos": len(df),
        "Periodo": f'{int(df["year"].min())}-{int(df["year"].max())}',
        "Fuentes": df["source"].nunique(), "Autores": len(authors),
        "Artículos": int((df["type"] == "article").sum()), "Revisiones": int((df["type"] == "review").sum()),
        "TCAC (%)": round(cagr(full), 1),
        "Docs 2021-2026 (%)": round((df["year"] >= 2021).mean() * 100, 1),
        "Citas/doc": round(df["cited_by"].mean(), 1), "h-index corpus": h_index(df["cited_by"]),
        "Coautores/doc": round(n_auth.mean(), 2), "Docs un autor": int((n_auth == 1).sum()),
        "Colab. internacional (%)": round(intl.mean() * 100, 1),
        "Acceso abierto (%)": round(df["oa_status"].isin(["gold", "green", "hybrid", "bronze", "diamond"]).mean() * 100, 1),
        "Con resumen (%)": round(df["has_abstract"].mean() * 100, 1),
    }


def annual_production(df):
    rows = []
    for lvl in LEVELS:
        s = subset(df, lvl)["year"].value_counts()
        for y, n in s.items():
            rows.append({"level": lvl, "year": int(y), "docs": int(n)})
    ap = pd.DataFrame(rows).pivot_table(index="year", columns="level", values="docs", fill_value=0)
    ap.to_csv(TABLES / "annual_production.csv")

    fig, axes = plt.subplots(1, 2, figsize=(10, 3.6), sharex=True)
    for ax, group in zip(axes, [["N1", "N3", "N4"], ["N2", "N5", "N6"]]):
        for i, lvl in enumerate(group):
            if lvl not in ap:
                continue
            col = SERIES[LEVELS.index(lvl)]
            s = ap[lvl]
            ax.plot(s.index[s.index <= LAST_FULL_YEAR], s[s.index <= LAST_FULL_YEAR], color=col, label=LABELS[lvl])
            if (s.index > LAST_FULL_YEAR).any():  # año parcial en línea punteada
                ax.plot(s.index[s.index >= LAST_FULL_YEAR], s[s.index >= LAST_FULL_YEAR], color=col, ls=":")
        ax.set_ylabel("Documentos por año")
        ax.legend(loc="upper left", fontsize=8)
    axes[0].set_title("a) Niveles generales y de cultivo")
    axes[1].set_title("b) Niveles de integración social y territorial")
    fig.text(0.5, -0.02, f"Línea punteada: {LAST_FULL_YEAR + 1} es un año parcial (corte de la búsqueda).",
             ha="center", color=INK2, fontsize=8)
    save(fig, FIGURES / "fig02_annual_production.png")
    return ap


def source_contribution(df):
    """Aporte de cada base por año: búsqueda OpenAlex vs. registros recuperados solo vía Scopus."""
    rows = []
    for lvl in LEVELS:
        d = subset(df, lvl)
        oa = d["sources"].apply(lambda s: "OpenAlex" in s)
        sc = d["sources"].apply(lambda s: "Scopus API" in s)
        for y, g in d.groupby("year"):
            rows.append({"level": lvl, "year": int(y), "total": len(g),
                         "openalex_search": int(oa[g.index].sum()), "scopus_search": int(sc[g.index].sum()),
                         "both": int((oa & sc)[g.index].sum()), "only_scopus": int((sc & ~oa)[g.index].sum()),
                         "only_openalex": int((oa & ~sc)[g.index].sum())})
    pd.DataFrame(rows).to_csv(TABLES / "annual_production_by_source.csv", index=False)


def top_sources(df, lvl, n=15):
    t = (df.groupby("source").agg(docs=("id", "size"), citas=("cited_by", "sum"),
                                  h=("cited_by", h_index)).sort_values(["docs", "citas"], ascending=False))
    t = t.drop(index=[s for s in t.index if not s], errors="ignore")
    t.head(n).to_csv(TABLES / f"{lvl}_top_sources.csv")
    return t


def bradford(src: pd.DataFrame, lvl: str) -> pd.DataFrame:
    """Divide las fuentes en tres zonas con ~1/3 de los documentos cada una."""
    s = src["docs"].sort_values(ascending=False)
    cum = s.cumsum() / s.sum()
    zone = np.where(cum <= 1 / 3, 1, np.where(cum <= 2 / 3, 2, 3))
    # la fuente que cruza el umbral pertenece a la zona inferior
    zone[0] = 1
    b = pd.DataFrame({"docs": s, "cum_share": cum.round(4), "zone": zone})
    b.to_csv(TABLES / f"{lvl}_bradford.csv")
    z = b.groupby("zone").agg(fuentes=("docs", "size"), documentos=("docs", "sum"))
    z["multiplicador"] = (z["fuentes"] / z["fuentes"].shift(1)).round(2)
    z.to_csv(TABLES / f"{lvl}_bradford_zones.csv")

    fig, ax = plt.subplots(figsize=(6, 3.4))
    x = np.arange(1, len(b) + 1)
    ax.plot(np.log(x), b["docs"].cumsum(), color=SERIES[0])
    core = int((b["zone"] == 1).sum())
    ax.axvspan(0, np.log(core), color=SERIES[0], alpha=0.12, lw=0)
    ax.text(np.log(max(core, 1)) / 2, b["docs"].sum() * 0.08, f"Núcleo\n{core} fuentes", ha="center", fontsize=8)
    ax.set_xlabel("ln(rango de la fuente)")
    ax.set_ylabel("Documentos acumulados")
    ax.set_title(f"Ley de Bradford - {LABELS[lvl]}")
    save(fig, FIGURES / f"{lvl}_bradford.png")
    return z


def lotka(df: pd.DataFrame, lvl: str) -> dict:
    """Ajuste de la ley de Lotka y prueba de Kolmogorov-Smirnov."""
    prod = Counter(a["id"] or a["name"] for al in df["authors"] for a in al)
    freq = Counter(prod.values())
    x = np.array(sorted(freq))
    y = np.array([freq[i] for i in x], dtype=float)
    obs = y / y.sum()
    mask = x <= max(2, np.percentile(list(prod.values()), 99.5))
    b, logc = np.polyfit(np.log10(x[mask]), np.log10(obs[mask]), 1)
    beta = -b
    nmax = x.max()
    c = 1 / sum(1 / k ** beta for k in range(1, nmax + 1))
    exp = c / x ** beta
    d = float(np.max(np.abs(np.cumsum(obs) - np.cumsum(exp))))
    crit = 1.63 / np.sqrt(y.sum())
    t = pd.DataFrame({"docs_por_autor": x, "autores": y.astype(int), "prop_observada": obs.round(4),
                      "prop_teorica": exp.round(4)})
    t.to_csv(TABLES / f"{lvl}_lotka.csv", index=False)

    fig, ax = plt.subplots(figsize=(5.2, 3.4))
    ax.loglog(x, obs, "o", ms=5, color=SERIES[0], label="Observado")
    ax.loglog(x, exp, color=SERIES[1], label=f"Lotka (β = {beta:.2f})")
    ax.set_xlabel("Documentos por autor (n)")
    ax.set_ylabel("Proporción de autores")
    ax.set_title(f"Ley de Lotka - {LABELS[lvl]}")
    ax.legend()
    save(fig, FIGURES / f"{lvl}_lotka.png")
    return {"Nivel": lvl, "beta": round(beta, 3), "C": round(c, 4), "KS_D": round(d, 4),
            "KS_crit_0.01": round(crit, 4), "Ajusta (D<crit)": d < crit,
            "Autores 1 doc (%)": round(freq[1] / y.sum() * 100, 1)}


def top_authors(df, lvl, n=15):
    rows = {}
    for _, r in df.iterrows():
        for a in r["authors"]:
            k = a["id"] or a["name"]
            e = rows.setdefault(k, {"autor": a["name"], "docs": 0, "citas": [], "paises": Counter()})
            e["docs"] += 1
            e["citas"].append(r["cited_by"])
            e["paises"].update(a.get("countries") or [])
    t = pd.DataFrame([{"autor": e["autor"], "docs": e["docs"], "citas": sum(e["citas"]),
                       "h_local": h_index(e["citas"]),
                       "pais": e["paises"].most_common(1)[0][0] if e["paises"] else ""} for e in rows.values()])
    t = t.sort_values(["docs", "citas"], ascending=False).head(n)
    t.to_csv(TABLES / f"{lvl}_top_authors.csv", index=False)
    return t


def countries(df, lvl, n=20):
    rows = Counter()
    scp, mcp, cites = Counter(), Counter(), Counter()
    for _, r in df.iterrows():
        cs = r["countries"]
        for c in cs:
            rows[c] += 1
            cites[c] += r["cited_by"]
        # país del autor de correspondencia (o primer autor) para SCP/MCP
        lead = next((a for a in r["authors"] if a.get("corresponding") and a.get("countries")), None) or \
            next((a for a in r["authors"] if a.get("countries")), None)
        if lead:
            lc = lead["countries"][0]
            (mcp if len(cs) > 1 else scp)[lc] += 1
    t = pd.DataFrame({"docs": pd.Series(rows), "citas": pd.Series(cites), "SCP": pd.Series(scp),
                      "MCP": pd.Series(mcp)}).fillna(0).astype(int)
    t["MCP_ratio"] = (t["MCP"] / (t["SCP"] + t["MCP"]).replace(0, np.nan)).round(3)
    t["citas/doc"] = (t["citas"] / t["docs"]).round(1)
    t = t.sort_values("docs", ascending=False)
    t.head(n).to_csv(TABLES / f"{lvl}_top_countries.csv")
    return t


def most_cited(df, lvl, n=20):
    t = df.sort_values("cited_by", ascending=False).head(n)
    out = pd.DataFrame({
        "primer_autor": t["authors"].apply(lambda a: a[0]["name"] if a else ""),
        "año": t["year"], "título": t["title"], "fuente": t["source"], "citas": t["cited_by"],
        "tipo": t["type"], "doi": t["doi"],
    })
    out.to_csv(TABLES / f"{lvl}_most_cited.csv", index=False)
    return out


def local_refs(lvl_queries, lvl, n=20):
    frames = []
    for qid in lvl_queries:
        f = RAW_OA / f"{qid}_top_refs.jsonl.gz"
        if f.exists():
            frames.append(pd.DataFrame(list(read_jsonl_gz(f))))
    if not frames:
        return None
    t = (pd.concat(frames).groupby("id").agg(
        titulo=("title", "first"), año=("year", "first"), fuente=("source", "first"),
        primer_autor=("authors", lambda a: a.iloc[0][0]["name"] if len(a.iloc[0]) else ""),
        citas_locales=("local_citations", "sum"), citas_globales=("cited_by", "first"), doi=("doi", "first"))
         .sort_values("citas_locales", ascending=False).head(n))
    t.to_csv(TABLES / f"{lvl}_top_local_references.csv")
    return t


def topics(df, lvl, n=15):
    sub = Counter(t["subfield"] for ts in df["topics"] for t in ts[:1] if t.get("subfield"))
    top = Counter(t["topic"] for ts in df["topics"] for t in ts[:1] if t.get("topic"))
    sdg = Counter(s for ss in df["sdgs"] for s in ss)
    pd.Series(sub).sort_values(ascending=False).head(n).rename("docs").to_csv(TABLES / f"{lvl}_subfields.csv")
    pd.Series(top).sort_values(ascending=False).head(n).rename("docs").to_csv(TABLES / f"{lvl}_topics.csv")
    pd.Series(sdg).sort_values(ascending=False).rename("docs").to_csv(TABLES / f"{lvl}_sdgs.csv")


def hbar(ax, s: pd.Series, title, color=SERIES[0]):
    s = s[::-1]
    ax.barh(range(len(s)), s.values, color=color, height=0.7)
    ax.set_yticks(range(len(s)), [str(i)[:48] for i in s.index], fontsize=7.5)
    ax.set_title(title)
    ax.grid(axis="y", visible=False)
    for i, v in enumerate(s.values):
        ax.text(v, i, f" {v:,}", va="center", fontsize=7, color=INK2)


def main() -> None:
    df = load()
    df = df[df["year"].notna()]
    cfg = load_config()
    q_by_level = {}
    for q in iter_queries(cfg):
        q_by_level.setdefault("N6" if q["id"].startswith("N6") else q["id"][:2], []).append(q["id"])

    TABLES.mkdir(parents=True, exist_ok=True)
    summ, lot, brad = [], [], []
    for lvl in LEVELS:
        d = subset(df, lvl)
        if d.empty:
            continue
        summ.append(summary(d, lvl))
        src = top_sources(d, lvl)
        top_authors(d, lvl)
        ctry = countries(d, lvl)
        most_cited(d, lvl)
        local_refs(q_by_level.get(lvl, []), lvl)
        topics(d, lvl)
        if len(d) >= 100:
            z = bradford(src, lvl)
            brad.append(z.assign(Nivel=lvl).reset_index())
            lot.append(lotka(d, lvl))

        fig, axes = plt.subplots(1, 2, figsize=(10, 3.8))
        hbar(axes[0], src["docs"].head(12), "Fuentes más productivas (documentos)")
        hbar(axes[1], ctry["docs"].head(12), "Países más productivos (documentos)", SERIES[2])
        fig.suptitle(LABELS[lvl], x=0.01, ha="left", fontweight="bold")
        save(fig, FIGURES / f"{lvl}_sources_countries.png")

    s = pd.DataFrame(summ).set_index("Nivel").T
    s.to_csv(TABLES / "summary_by_level.csv")
    pd.DataFrame(lot).to_csv(TABLES / "lotka_summary.csv", index=False)
    if brad:
        pd.concat(brad).to_csv(TABLES / "bradford_summary.csv", index=False)
    annual_production(df)
    source_contribution(df)

    # Cobertura por sub-consulta (rutas N4a-N4g)
    routes = {q["id"]: q["name"].split(" - ")[-1] for q in iter_queries(cfg) if q["id"].startswith("N4")}
    rc = [{"id": k, "ruta": v, "docs": int(df["queries"].apply(lambda qs, k=k: k in qs).sum())} for k, v in routes.items()]
    rc = pd.DataFrame(rc)
    rc.to_csv(TABLES / "N4_routes_coverage.csv", index=False)
    fig, ax = plt.subplots(figsize=(6, 3))
    hbar(ax, rc.set_index("ruta")["docs"], "Documentos por ruta de transformación (ñame y batata)", SERIES[0])
    ax.grid(axis="x", visible=True)
    save(fig, FIGURES / "fig05_routes_coverage.png")
    print(s.to_string())


if __name__ == "__main__":
    main()
