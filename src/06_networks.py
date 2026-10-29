"""Paso 6 - Mapeo científico (science mapping).

* Red de co-ocurrencia de palabras clave (normalización por fuerza de
  asociación, agrupamiento de Louvain) -> equivalente a VOSviewer.
* Mapa temático de Callon (centralidad vs. densidad) -> equivalente a bibliometrix.
* Evolución temática por periodos.
* Red de colaboración entre países.
Las redes se exportan en GraphML para abrirlas en Gephi o VOSviewer.
"""
from __future__ import annotations

import itertools
from collections import Counter

import networkx as nx
import numpy as np
import pandas as pd

from common import FIGURES, PROCESSED, ROOT, TABLES, read_jsonl_gz
from viz import INK, INK2, OTHER, SERIES, SEQ, plt, save

try:
    import pycountry
except ImportError:  # pragma: no cover
    pycountry = None

SEED = 42
NET = PROCESSED / "networks"
THES = dict(pd.read_csv(ROOT / "config" / "thesaurus.csv").values)
LABELS = {"N1": "N1 Sostenibilidad de biorrefinerías", "N2": "N2 ACV-S / LCSA",
          "N3": "N3 Raíces y tubérculos", "N4": "N4 Ñame y batata (rutas)",
          "N5": "N5 Sostenibilidad ñame/batata", "N6": "N6 Colombia / Caribe"}


def norm_kw(k: str) -> str:
    k = k.strip().lower()
    return THES.get(k, k)


def doc_keywords(df: pd.DataFrame) -> list[set]:
    return [{norm_kw(k) for k in ks if k and len(k) > 2} for ks in df["keywords"]]


def cooccurrence(docs: list[set], top_n: int, min_freq: int = 3) -> nx.Graph:
    freq = Counter(k for d in docs for k in d)
    keep = {k for k, v in freq.most_common(top_n) if v >= min_freq}
    g = nx.Graph()
    for k in keep:
        g.add_node(k, freq=freq[k])
    for d in docs:
        for a, b in itertools.combinations(sorted(d & keep), 2):
            w = g[a][b]["weight"] + 1 if g.has_edge(a, b) else 1
            g.add_edge(a, b, weight=w)
    for a, b, e in g.edges(data=True):  # fuerza de asociación (van Eck & Waltman, 2009)
        e["assoc"] = e["weight"] / (freq[a] * freq[b])
        e["equiv"] = e["weight"] ** 2 / (freq[a] * freq[b])  # índice de equivalencia (Callon)
    g.remove_nodes_from([n for n in list(g) if g.degree(n) == 0])
    return g


def cluster(g: nx.Graph) -> dict:
    comms = nx.community.louvain_communities(g, weight="weight", seed=SEED, resolution=1.0)
    comms = sorted(comms, key=lambda c: -sum(g.nodes[n]["freq"] for n in c))
    part = {}
    for i, c in enumerate(comms):
        for n in c:
            part[n] = i
    nx.set_node_attributes(g, part, "cluster")
    return part


def cluster_label(g, nodes, k=3):
    return " / ".join(sorted(nodes, key=lambda n: -g.nodes[n]["freq"])[:k])


def draw_network(g: nx.Graph, part: dict, title: str, path, n_labels: int = 45):
    pos = nx.spring_layout(g, weight="assoc", seed=SEED, k=1.6 / np.sqrt(len(g)), iterations=300)
    fig, ax = plt.subplots(figsize=(10, 7.5))
    ax.axis("off")
    maxw = max(e["weight"] for *_, e in g.edges(data=True))
    edges = sorted(g.edges(data=True), key=lambda e: e[2]["weight"])
    for a, b, e in edges[-min(len(edges), 600):]:
        ax.plot(*zip(pos[a], pos[b]), color="#c9c8c3", lw=0.3 + 2.2 * e["weight"] / maxw, alpha=0.55, zorder=1)
    freq = np.array([g.nodes[n]["freq"] for n in g])
    sizes = 30 + 900 * freq / freq.max()
    colors = [SERIES[part[n]] if part[n] < len(SERIES) else OTHER for n in g]
    ax.scatter(*zip(*[pos[n] for n in g]), s=sizes, c=colors, edgecolors="white", linewidths=1.2, zorder=2)
    for n in sorted(g, key=lambda n: -g.nodes[n]["freq"])[:n_labels]:
        ax.annotate(n, pos[n], fontsize=7.5, color=INK, ha="center", va="center", zorder=3,
                    xytext=(0, 7 + 10 * g.nodes[n]["freq"] / freq.max()), textcoords="offset points")
    handles = []
    for c in sorted(set(part.values()))[:len(SERIES)]:
        nodes = [n for n in g if part[n] == c]
        handles.append(plt.Line2D([], [], marker="o", ls="", color=SERIES[c], ms=7,
                                  label=f"C{c + 1}: {cluster_label(g, nodes)}"))
    ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(0, -0.01), ncol=2, fontsize=7.5)
    ax.set_title(title)
    save(fig, path)


def thematic_map(g: nx.Graph, part: dict, lvl: str) -> pd.DataFrame:
    """Centralidad de Callon (vínculos externos) y densidad (vínculos internos)."""
    rows = []
    for c in sorted(set(part.values())):
        nodes = {n for n in g if part[n] == c}
        if len(nodes) < 2:
            continue
        internal = sum(e["equiv"] for a, b, e in g.edges(data=True) if a in nodes and b in nodes)
        external = sum(e["equiv"] for a, b, e in g.edges(data=True) if (a in nodes) != (b in nodes))
        rows.append({"cluster": f"C{c + 1}", "etiqueta": cluster_label(g, nodes),
                     "n_palabras": len(nodes), "frecuencia": sum(g.nodes[n]["freq"] for n in nodes),
                     "centralidad": external * 10, "densidad": internal / len(nodes) * 100,
                     "palabras": "; ".join(sorted(nodes, key=lambda n: -g.nodes[n]["freq"]))})
    tm = pd.DataFrame(rows)
    if tm.empty:
        return tm
    cx, cy = tm["centralidad"].median(), tm["densidad"].median()
    tm["cuadrante"] = np.select(
        [(tm.centralidad >= cx) & (tm.densidad >= cy), (tm.centralidad < cx) & (tm.densidad >= cy),
         (tm.centralidad < cx) & (tm.densidad < cy)],
        ["Temas motores", "Temas nicho", "Temas emergentes o en declive"], "Temas básicos/transversales")
    tm.to_csv(TABLES / f"{lvl}_thematic_map.csv", index=False)

    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    ax.axvline(cx, color=INK2, lw=0.8, ls="--")
    ax.axhline(cy, color=INK2, lw=0.8, ls="--")
    smax = tm["frecuencia"].max()
    for i, r in tm.iterrows():
        ci = int(r["cluster"][1:]) - 1
        ax.scatter(r["centralidad"], r["densidad"], s=200 + 1800 * r["frecuencia"] / smax,
                   color=SERIES[ci] if ci < len(SERIES) else OTHER, alpha=0.85, edgecolors="white", lw=2)
        ax.annotate(r["etiqueta"].replace(" / ", "\n"), (r["centralidad"], r["densidad"]), fontsize=7,
                    ha="center", va="center", color=INK)
    kw = dict(transform=ax.transAxes, fontsize=8, color=INK2, style="italic")
    ax.text(0.99, 0.98, "Temas motores", ha="right", va="top", **kw)
    ax.text(0.01, 0.98, "Temas nicho", ha="left", va="top", **kw)
    ax.text(0.01, 0.02, "Emergentes / en declive", ha="left", va="bottom", **kw)
    ax.text(0.99, 0.02, "Temas básicos", ha="right", va="bottom", **kw)
    ax.set_xlabel("Centralidad (grado de relevancia)")
    ax.set_ylabel("Densidad (grado de desarrollo)")
    ax.set_title(f"Mapa temático - {LABELS[lvl]}")
    save(fig, FIGURES / f"{lvl}_thematic_map.png")
    return tm


def thematic_evolution(df, lvl, periods, top=25):
    docs = doc_keywords(df)
    freq = Counter(k for d in docs for k in d)
    kws = [k for k, _ in freq.most_common(top)]
    mat = {}
    for lo, hi in periods:
        mask = (df["year"] >= lo) & (df["year"] <= hi)
        sub = [d for d, m in zip(docs, mask) if m]
        n = max(len(sub), 1)
        mat[f"{lo}-{hi}\n(n={len(sub)})"] = [sum(k in d for d in sub) / n * 100 for k in kws]
    m = pd.DataFrame(mat, index=kws)
    m.to_csv(TABLES / f"{lvl}_thematic_evolution.csv")
    fig, ax = plt.subplots(figsize=(6.2, 0.26 * top + 1.2))
    im = ax.imshow(m.values, cmap=SEQ, aspect="auto")
    ax.set_xticks(range(m.shape[1]), m.columns, fontsize=8)
    ax.set_yticks(range(m.shape[0]), m.index, fontsize=7.5)
    ax.grid(False)
    for (i, j), v in np.ndenumerate(m.values):
        ax.text(j, i, f"{v:.0f}", ha="center", va="center", fontsize=6.5,
                color="white" if v > m.values.max() * 0.55 else INK)
    fig.colorbar(im, ax=ax, label="% de documentos del periodo", shrink=0.6)
    ax.set_title(f"Evolución temática - {LABELS[lvl]}")
    save(fig, FIGURES / f"{lvl}_thematic_evolution.png")


def country_name(code):
    if pycountry:
        c = pycountry.countries.get(alpha_2=code)
        if c:
            return getattr(c, "common_name", None) or c.name
    return code


def country_network(df, lvl, top=30):
    freq = Counter(c for cs in df["countries"] for c in cs)
    keep = {c for c, _ in freq.most_common(top)}
    g = nx.Graph()
    for c in keep:
        g.add_node(c, freq=freq[c], name=country_name(c))
    for cs in df["countries"]:
        for a, b in itertools.combinations(sorted(set(cs) & keep), 2):
            g.add_edge(a, b, weight=g[a][b]["weight"] + 1 if g.has_edge(a, b) else 1)
    nx.write_graphml(g, NET / f"{lvl}_countries.graphml")
    pd.DataFrame([{"pais_a": country_name(a), "pais_b": country_name(b), "docs": e["weight"]}
                  for a, b, e in g.edges(data=True)]).sort_values("docs", ascending=False).head(30) \
        .to_csv(TABLES / f"{lvl}_country_links.csv", index=False)
    if g.number_of_edges() == 0:
        return
    pos = nx.kamada_kawai_layout(g, weight=None)
    fig, ax = plt.subplots(figsize=(8, 6.5))
    ax.axis("off")
    maxw = max(e["weight"] for *_, e in g.edges(data=True))
    for a, b, e in g.edges(data=True):
        ax.plot(*zip(pos[a], pos[b]), color="#c9c8c3", lw=0.3 + 3 * e["weight"] / maxw, alpha=0.6, zorder=1)
    f = np.array([g.nodes[n]["freq"] for n in g])
    ax.scatter(*zip(*[pos[n] for n in g]), s=40 + 1200 * f / f.max(),
               c=[SERIES[2] if n == "CO" else SERIES[0] for n in g], edgecolors="white", lw=1.2, zorder=2)
    for n in g:
        ax.annotate(g.nodes[n]["name"], pos[n], fontsize=7.5, ha="center", va="center", zorder=3,
                    xytext=(0, 9 + 12 * g.nodes[n]["freq"] / f.max()), textcoords="offset points")
    ax.set_title(f"Colaboración entre países - {LABELS[lvl]} (Colombia resaltada)")
    save(fig, FIGURES / f"{lvl}_country_network.png")


def main() -> None:
    df = pd.DataFrame(list(read_jsonl_gz(PROCESSED / "corpus.jsonl.gz")))
    NET.mkdir(parents=True, exist_ok=True)
    settings = {"N1": 80, "N2": 60, "N3": 80, "N4": 80, "N5": 60, "N6": 50}
    for lvl, top in settings.items():
        d = df[df["levels"].apply(lambda ls, l=lvl: l in ls)]
        if len(d) < 30:
            continue
        g = cooccurrence(doc_keywords(d), top_n=top, min_freq=2 if len(d) < 300 else 3)
        if g.number_of_nodes() < 5:
            continue
        part = cluster(g)
        nx.write_graphml(g, NET / f"{lvl}_keywords.graphml")
        pd.DataFrame([{"palabra": n, "frecuencia": g.nodes[n]["freq"], "cluster": f"C{part[n] + 1}",
                       "grado": g.degree(n), "fuerza": g.degree(n, weight="weight")} for n in g]) \
            .sort_values(["cluster", "frecuencia"], ascending=[True, False]) \
            .to_csv(TABLES / f"{lvl}_keyword_clusters.csv", index=False)
        draw_network(g, part, f"Co-ocurrencia de palabras clave - {LABELS[lvl]}", FIGURES / f"{lvl}_keyword_network.png")
        thematic_map(g, part, lvl)
        country_network(d, lvl)
    for lvl in ("N1", "N3", "N4"):
        d = df[df["levels"].apply(lambda ls, l=lvl: l in ls)]
        if len(d) >= 100:
            thematic_evolution(d, lvl, [(2000, 2015), (2016, 2020), (2021, 2026)])


if __name__ == "__main__":
    main()
