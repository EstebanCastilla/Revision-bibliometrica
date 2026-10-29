"""Paso 7 - Análisis de brechas y minería de texto dirigida.

1. Matriz cultivo x ruta de transformación y cultivo x método de evaluación
   (ACV, TEA, ACV-S) sobre el corpus de raíces y tubérculos (N3 + N4 + N5).
2. Grado de integración: documentos que combinan >= 2 rutas y >= 2 pilares.
3. Minería de metabolitos candidatos en ñame (N4e) y batata (N4f) para
   sustentar la selección de los metabolitos "por definir".
4. Contexto territorial (N6): instituciones y temas en Colombia.
Clasificación por diccionarios controlados (expresiones regulares) aplicada
a título + resumen + palabras clave.
"""
from __future__ import annotations

import re
import textwrap
import warnings
from collections import Counter

import numpy as np
import pandas as pd

from common import FIGURES, PROCESSED, TABLES, read_jsonl_gz
from viz import INK, SEQ, SERIES, plt, save

CROPS = {
    "Yuca": r"\b(cassava|manioc|manihot)\b",
    "Papa": r"(?<!sweet )(?<!sweet-)\b(potato(es)?|solanum tuberosum)\b",
    "Ñame": r"\b(yams?|dioscorea|ñame)\b",
    "Batata": r"\b(sweet[ -]?potato(es)?|ipomoea batatas|batata)\b",
    "Malanga/Taro": r"\b(taro|cocoyam|colocasia|xanthosoma|malanga)\b",
}
ROUTES = {
    "Almidón": r"\bstarch",
    "Bioetanol": r"bio-?ethanol|ethanol (production|fermentation|yield)|fuel ethanol",
    "Biogás": r"biogas|anaerobic (co-?)?digestion|biomethane|methane (yield|production|potential)",
    "Biofertilizante": r"bio-?fertili[sz]|compost|digestate|organic fertili[sz]|biochar|soil amendment",
    "Metabolitos/bioactivos": r"bioactive|anthocyanin|phenolic|polyphenol|flavonoid|carotenoid|diosgenin|"
                              r"dioscorin|saponin|chlorogenic|sporamin|antioxidant",
    "Bioplásticos/biomateriales": r"bioplastic|biopolymer|biodegradable film|edible film|packaging",
    "Alimento animal": r"animal feed|livestock feed|\bfeed\b|silage",
    "Biorrefinería integrada": r"bio-?refiner|cascad|zero[- ]waste|integrated (process|valori)",
}
METHODS = {
    "ACV": r"life[- ]cycle assessment|life[- ]cycle analysis|\blca\b|carbon footprint|"
           r"environmental impact assessment|global warming potential",
    "TEA": r"techno-?economic|minimum (ethanol |fuel )?selling price|net present value|\bnpv\b|"
           r"internal rate of return|payback period|capital (cost|investment)|aspen plus|superpro|"
           r"process simulation|plant design",
    "Análisis económico agrícola/mercado": r"profitability|economic analysis|cost-benefit|gross margin|"
                                           r"production cost|economic feasibility|market price|value chain",
    "ACV-S": r"social life[- ]cycle|\bs-?lca\b|social lca|social hotspot|social impact assessment",
    "Dimensión socioeconómica (no ACV-S)": r"livelihood|smallholder|stakeholder|working conditions|gender|"
                                           r"food security|household income|rural development|employment",
    "LCSA / multicriterio": r"life[- ]cycle sustainability|\blcsa\b|sustainability assessment|"
                            r"multi-?criteria|sustainability index",
}
METABOLITES = {
    "Ñame": {
        "Diosgenina": r"diosgenin", "Dioscorina (proteína)": r"dioscorin",
        "Alantoína": r"allantoin", "Saponinas esteroidales": r"saponin",
        "Polisacáridos/mucílago": r"mucilage|polysaccharide|non-starch",
        "Compuestos fenólicos": r"phenolic|polyphenol", "Flavonoides": r"flavonoid",
        "Carotenoides": r"carotenoid|carotene", "Almidón resistente": r"resistant starch",
        "Batatasinas/estilbenos": r"batatasin|stilben", "Antocianinas": r"anthocyanin",
    },
    "Batata": {
        "Antocianinas": r"anthocyanin", "Ácido clorogénico/cafeoilquínicos": r"chlorogenic|caffeoylquinic",
        "β-caroteno/carotenoides": r"carotenoid|carotene|β-carotene", "Esporamina (proteína)": r"sporamin",
        "Compuestos fenólicos": r"phenolic|polyphenol", "Flavonoides": r"flavonoid",
        "Pectina": r"pectin", "Fibra dietaria": r"dietary fib", "Almidón resistente": r"resistant starch",
        "Proteína (aislados)": r"protein (isolate|concentrate|recovery)",
        "Polisacáridos": r"polysaccharide",
    },
}
RESIDUE = re.compile(r"\b(peels?|residues?|wastes?|by-?products?|wastewater|pulp|vines?|leaves|skins?)\b", re.I)
EXTRACT = re.compile(r"extract|recover|isolat|purif", re.I)
RECENT = 2021
warnings.filterwarnings("ignore", message="This pattern is interpreted as a regular expression")


def text(r) -> str:
    return " ".join([r.get("title") or "", r.get("abstract") or "", " ".join(r.get("keywords") or [])]).lower()


def tag(texts: pd.Series, dic: dict) -> pd.DataFrame:
    return pd.DataFrame({k: texts.str.contains(v, regex=True, flags=re.I) for k, v in dic.items()})


def heatmap(m: pd.DataFrame, title, path, fmt="{:.0f}", cbar="Documentos"):
    fig, ax = plt.subplots(figsize=(1.0 * m.shape[1] + 2.5, 0.5 * m.shape[0] + 1.6))
    vals = np.log1p(m.values.astype(float))
    im = ax.imshow(vals, cmap=SEQ, aspect="auto")
    ax.set_xticks(range(m.shape[1]), [textwrap.fill(c, 16) for c in m.columns], fontsize=8)
    ax.set_yticks(range(m.shape[0]), m.index, fontsize=8.5)
    ax.grid(False)
    for (i, j), v in np.ndenumerate(m.values):
        ax.text(j, i, fmt.format(v), ha="center", va="center", fontsize=8,
                color="white" if vals[i, j] > vals.max() * 0.6 else INK)
    cb = fig.colorbar(im, ax=ax, shrink=0.75)
    cb.set_label(f"{cbar} (escala log)")
    ax.set_title(title)
    save(fig, path)


def main() -> None:
    df = pd.DataFrame(list(read_jsonl_gz(PROCESSED / "corpus.jsonl.gz")))
    df["text"] = df.apply(text, axis=1).str.replace(r"\byam ?beans?\b|pachyrhizus", " ", regex=True)

    # ---- 1. Matrices de brecha --------------------------------------------
    rt = df[df["levels"].apply(lambda ls: bool({"N3", "N4", "N5"} & set(ls)))].copy()
    crops, routes, methods = tag(rt["text"], CROPS), tag(rt["text"], ROUTES), tag(rt["text"], METHODS)
    cr = pd.DataFrame({c: routes[crops[c]].sum() for c in CROPS}).T
    cm = pd.DataFrame({c: methods[crops[c]].sum() for c in CROPS}).T
    cr.to_csv(TABLES / "gap_crop_route.csv")
    cm.to_csv(TABLES / "gap_crop_method.csv")
    heatmap(cr, "Cultivo x ruta de transformación (corpus N3-N5)", FIGURES / "fig06_gap_crop_route.png")
    heatmap(cm, "Cultivo x método de evaluación de sostenibilidad", FIGURES / "fig07_gap_crop_method.png")

    # ---- 2. Integración ----------------------------------------------------
    fixed = ["Almidón", "Bioetanol", "Biogás", "Biofertilizante", "Metabolitos/bioactivos"]
    pillars = ["ACV", "TEA", "ACV-S"]
    integ = []
    for c in CROPS:
        sel = crops[c]
        nr = routes.loc[sel, fixed].sum(axis=1)
        npil = methods.loc[sel, pillars].sum(axis=1)
        integ.append({"Cultivo": c, "Documentos": int(sel.sum()),
                      ">=2 rutas fijas": int((nr >= 2).sum()), ">=3 rutas fijas": int((nr >= 3).sum()),
                      "ACV+TEA": int((methods.loc[sel, "ACV"] & methods.loc[sel, "TEA"]).sum()),
                      "ACV+TEA+ACV-S": int((npil == 3).sum()),
                      ">=2 rutas y >=1 pilar": int(((nr >= 2) & (npil >= 1)).sum())})
    integ = pd.DataFrame(integ)
    integ.to_csv(TABLES / "gap_integration.csv", index=False)
    both = crops["Ñame"] & crops["Batata"]
    rt.loc[both | ((crops["Ñame"] | crops["Batata"]) & (routes[fixed].sum(axis=1) >= 2)),
           ["title", "year", "source", "cited_by", "doi"]] \
        .sort_values("cited_by", ascending=False).to_csv(TABLES / "gap_closest_studies.csv", index=False)
    # Estudios con evaluación de sostenibilidad para ñame o batata
    ys = (crops["Ñame"] | crops["Batata"]) & methods[pillars].any(axis=1)
    out = rt.loc[ys, ["title", "year", "source", "cited_by", "doi"]].copy()
    for m in pillars:
        out[m] = methods.loc[ys, m]
    out["rutas"] = routes.loc[ys].apply(lambda r: "; ".join(k for k, v in r.items() if v), axis=1)
    out.sort_values("year", ascending=False).to_csv(TABLES / "gap_yam_sweetpotato_assessments.csv", index=False)

    # ---- 3. Metabolitos candidatos ------------------------------------------
    rows = []
    for crop, qid in (("Ñame", "N4e"), ("Batata", "N4f")):
        d = df[df["queries"].apply(lambda qs, q=qid: q in qs)]
        if d.empty:
            continue
        rot = d["text"].str.contains(r"rotundata|white (guinea )?yam", regex=True)
        for name, rx in METABOLITES[crop].items():
            hit = d["text"].str.contains(rx, regex=True)
            if not hit.any():
                continue
            h = d[hit]
            rows.append({
                "Cultivo": crop, "Metabolito": name, "Documentos": int(hit.sum()),
                "% del corpus": round(hit.mean() * 100, 1),
                f"% desde {RECENT}": round((h["year"] >= RECENT).mean() * 100, 1),
                "Citas/doc": round(h["cited_by"].mean(), 1),
                "Con residuos/subproductos": int(h["text"].str.contains(RESIDUE).sum()),
                "Con extracción/recuperación": int(h["text"].str.contains(EXTRACT).sum()),
                "En D. rotundata": int((hit & rot).sum()) if crop == "Ñame" else None,
            })
    met = pd.DataFrame(rows)
    if not met.empty:
        # Índice de priorización: volumen, actualidad y vínculo con residuos (min-max por cultivo)
        def mm(s):
            return (s - s.min()) / (s.max() - s.min()) if s.max() > s.min() else s * 0

        parts = []
        for crop, g in met.groupby("Cultivo"):
            g = g.copy()
            g["Índice de priorización"] = (0.35 * mm(g["Documentos"]) + 0.25 * mm(g[f"% desde {RECENT}"])
                                           + 0.25 * mm(g["Con residuos/subproductos"] / g["Documentos"])
                                           + 0.15 * mm(g["Con extracción/recuperación"] / g["Documentos"])).round(3)
            parts.append(g.sort_values("Índice de priorización", ascending=False))
        met = pd.concat(parts)
        met.to_csv(TABLES / "metabolite_candidates.csv", index=False)
        fig, axes = plt.subplots(1, 2, figsize=(13, 4.6))
        fig.subplots_adjust(wspace=0.6)
        for ax, (crop, g) in zip(axes, met.groupby("Cultivo", sort=False)):
            g = g.sort_values("Documentos")
            y = np.arange(len(g))
            ax.barh(y, g["Documentos"], color=SERIES[0], height=0.7, label="Total")
            ax.barh(y, g["Con residuos/subproductos"], color=SERIES[1], height=0.7,
                    label="Mencionan residuos/subproductos")
            ax.set_yticks(y, g["Metabolito"], fontsize=8)
            ax.grid(axis="y", visible=False)
            ax.set_title(f"Metabolitos en {crop.lower()}")
            ax.set_xlabel("Documentos")
            ax.legend(fontsize=7.5, loc="lower right")
        save(fig, FIGURES / "fig08_metabolites.png")

    # ---- 3b. Estudios clave por ruta y metabolito (insumo para la discusión) --
    keys = []
    for qid, route in (("N4a", "Almidón nativo"), ("N4b", "Bioetanol"), ("N4c", "Biogás"),
                       ("N4d", "Biofertilizante"), ("N4g", "Biorrefinería / valorización")):
        d = df[df["queries"].apply(lambda qs, q=qid: q in qs)]
        for crop, rx in (("Ñame", CROPS["Ñame"]), ("Batata", CROPS["Batata"])):
            sel = d[d["text"].str.contains(rx, regex=True)]
            for _, r in sel.sort_values("cited_by", ascending=False).head(8).iterrows():
                keys.append({"ruta": route, "cultivo": crop, "año": r["year"], "citas": r["cited_by"],
                             "primer_autor": r["authors"][0]["name"] if r["authors"] else "",
                             "título": r["title"], "fuente": r["source"], "doi": r["doi"]})
    pd.DataFrame(keys).to_csv(TABLES / "route_key_studies.csv", index=False)
    mk = []
    for crop, qid in (("Ñame", "N4e"), ("Batata", "N4f")):
        d = df[df["queries"].apply(lambda qs, q=qid: q in qs)]
        for name, rx in METABOLITES[crop].items():
            sel = d[d["text"].str.contains(rx, regex=True)]
            res = sel[sel["text"].str.contains(RESIDUE)]
            for tag_, sub in (("más citados", sel), ("con residuos/subproductos", res)):
                for _, r in sub.sort_values("cited_by", ascending=False).head(4).iterrows():
                    mk.append({"cultivo": crop, "metabolito": name, "criterio": tag_, "año": r["year"],
                               "citas": r["cited_by"], "rotundata": "rotundata" in r["text"],
                               "primer_autor": r["authors"][0]["name"] if r["authors"] else "",
                               "título": r["title"], "fuente": r["source"], "doi": r["doi"]})
    pd.DataFrame(mk).to_csv(TABLES / "metabolite_key_studies.csv", index=False)

    # ---- 4. Contexto territorial -------------------------------------------
    co = df[df["levels"].apply(lambda ls: "N6" in ls)]
    if not co.empty:
        inst = Counter(i for _, r in co.iterrows() for a in r["authors"] if "CO" in (a.get("countries") or [])
                       for i in a.get("institutions") or [])
        pd.Series(inst).sort_values(ascending=False).head(20).rename("docs") \
            .to_csv(TABLES / "N6_colombian_institutions.csv")
        ct = tag(co["text"], CROPS).sum().rename("docs")
        rtc = tag(co["text"], ROUTES).sum().rename("docs")
        mtc = tag(co["text"], METHODS).sum().rename("docs")
        pd.concat({"cultivo": ct, "ruta": rtc, "metodo": mtc}).to_csv(TABLES / "N6_profile.csv")
        co[co["text"].str.contains(r"\b(yams?|dioscorea|ñame|sweet ?potato|batata)\b")][
            ["title", "year", "source", "cited_by", "doi"]].sort_values("year", ascending=False) \
            .to_csv(TABLES / "N6_yam_sweetpotato_colombia.csv", index=False)
    print(cr, cm, integ, met.head(25) if not met.empty else "", sep="\n\n")


if __name__ == "__main__":
    main()
