"""Diagrama de flujo PRISMA 2020 a partir de results/tables/prisma_flow.csv."""
from __future__ import annotations

import pandas as pd
from matplotlib.patches import FancyBboxPatch

from common import FIGURES, TABLES
from viz import INK, INK2, plt, save


def box(ax, x, y, w, h, text, fc="#f4f8fd", ec="#2a78d6"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.01,rounding_size=0.015",
                                fc=fc, ec=ec, lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=8, color=INK, wrap=True)


def arrow(ax, x1, y1, x2, y2):
    ax.annotate("", (x2, y2), (x1, y1), arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1))


def es(n) -> str:
    return f"{int(n):,}".replace(",", ".")


def main() -> None:
    p = pd.read_csv(TABLES / "prisma_flow.csv").set_index("level")
    ident = pd.read_csv(TABLES / "prisma_identification_by_query.csv")
    t = p.loc["Total"]
    by_src = ident.groupby("source")["records"].sum()
    enrich = int(by_src.get("Scopus -> OpenAlex (DOI)", 0))
    by_src = by_src.drop("Scopus -> OpenAlex (DOI)", errors="ignore")
    src_txt = " · ".join(f"{s}: {es(n)}" for s, n in by_src.items())
    if enrich:
        src_txt += f"\n(+{es(enrich)} DOI de Scopus completados\ncon metadatos de OpenAlex)"
    nq = ident["query"].nunique()
    items = [f"{i}: {es(int(r.included))}" for i, r in p.drop("Total").iterrows()]
    lv = "\n".join("   ".join(items[k:k + 2]) for k in range(0, len(items), 2))

    fig, ax = plt.subplots(figsize=(8, 7))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    L, W, H = 0.05, 0.42, 0.13
    R = 0.55
    rows = [0.82, 0.60, 0.38, 0.04]
    box(ax, L, rows[0], W, H, f"Registros identificados ({nq} consultas, N1-N6)\n{src_txt}\nTotal: {es(int(t.identified))}")
    box(ax, R, rows[0], W, H, f"Duplicados eliminados\n(DOI y título normalizado + año)\nn = {es(int(t.duplicates_removed))}",
        fc="#fdf3ee", ec="#eb6834")
    box(ax, L, rows[1], W, H, f"Registros únicos cribados\nn = {es(int(t.screened))}")
    box(ax, R, rows[1], W, H, f"Excluidos en cribado\n(sin título, retractados,\nfuera de periodo o de tipo)\nn = {es(int(t.excluded_screening))}",
        fc="#fdf3ee", ec="#eb6834")
    box(ax, L, rows[2], W, H, f"Registros evaluados para elegibilidad\n(verificación léxica en título,\nresumen y palabras clave)\nn = {es(int(t.assessed_eligibility))}")
    box(ax, R, rows[2], W, H, f"Excluidos por elegibilidad\n(falsos positivos, fuera de alcance)\nn = {es(int(t.excluded_eligibility))}",
        fc="#fdf3ee", ec="#eb6834")
    box(ax, L, rows[3], W, H + 0.08, f"Estudios incluidos (registros únicos)\nn = {es(int(t.included))}\n\nPor nivel (un registro puede\npertenecer a varios niveles):\n{lv}",
        fc="#e8f6ef", ec="#1baf7a")
    for i in range(3):
        arrow(ax, L + W / 2, rows[i], L + W / 2, rows[i + 1] + H + (0.08 if i == 2 else 0))
        arrow(ax, L + W, rows[i] + H / 2, R, rows[i] + H / 2)
    for y, lab in zip([0.89, 0.67, 0.45, 0.15], ["Identificación", "Cribado", "Elegibilidad", "Inclusión"]):
        ax.text(0.0, y, lab, rotation=90, ha="center", va="center", fontsize=8.5, fontweight="bold", color=INK2)
    ax.set_title("Figura 1. Diagrama de flujo PRISMA 2020 de la búsqueda")
    save(fig, FIGURES / "fig01_prisma.png")


if __name__ == "__main__":
    main()
