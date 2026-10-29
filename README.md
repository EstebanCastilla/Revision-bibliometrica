# Revisión bibliométrica: sostenibilidad de una biorrefinería integrada de ñame y batata

Repositorio de la revisión bibliométrica de apoyo a la tesis de maestría en ingeniería

> **"Evaluación de sostenibilidad de una biorrefinería integrada a partir de biomasa de ñame (*Dioscorea rotundata*) y batata (*Ipomoea batatas*) en San Jacinto, Bolívar"**

Objetivo general: evaluar la sostenibilidad de una biorrefinería integrada basada en biomasa de ñame y batata en el norte de Colombia mediante **ACV**, **TEA** y **ACV-S**.
Rutas fijas para ambos tubérculos: almidón nativo, bioetanol, biogás, biofertilizante y un metabolito de valor agregado por cultivo (por definir con esta revisión).

## Resultados principales (corrida del 29-oct-2026)

| | |
|---|---|
| Registros identificados | 34.616 (OpenAlex 19.988 + Scopus 14.628) |
| Documentos únicos incluidos | **19.347** (2000-2026) |
| N1 Sostenibilidad de biorrefinerías | 2.978 docs, TCAC 29,2 %; Colombia 9.º país |
| N2 ACV-S / LCSA | 159 docs (dimensión social marginal) |
| Brecha central | 0 estudios que integren ACV + TEA + ACV-S en tubérculos; ñame: 7 ACV, 20 TEA, 0 ACV-S |
| Metabolitos priorizados | Ñame: fenólicos/flavonoides de cáscara; batata: antocianinas, ác. clorogénico o β-caroteno según variedad |

- Artículo: [`articulo/articulo_final.md`](articulo/articulo_final.md) · [DOCX](articulo/articulo_revision_bibliometrica.docx) · fuente editable [`articulo_revision_bibliometrica.md`](articulo/articulo_revision_bibliometrica.md)
- Protocolo: [`protocolo/protocolo_revision.md`](protocolo/protocolo_revision.md) · Bitácora: [`protocolo/bitacora_decisiones.md`](protocolo/bitacora_decisiones.md)

## Trazabilidad: de dónde sale cada cifra del artículo

| Elemento del artículo | Archivo de origen |
|---|---|
| Tabla 1 (consultas y registros) | `results/tables/search_strategy.csv`, `data/raw/*/search_log.json` |
| Figura 1 (PRISMA) | `results/tables/prisma_flow.csv`, `prisma_exclusion_reasons.csv`, `data/processed/excluded.csv` |
| Cobertura OpenAlex vs. Scopus | `results/tables/coverage_openalex_scopus.csv` |
| Tabla 2 (indicadores por nivel) | `results/tables/summary_by_level.csv` |
| Figura 2 (producción anual) | `results/tables/annual_production.csv`, `annual_production_by_source.csv` |
| Bradford y Lotka | `results/tables/bradford_summary.csv`, `lotka_summary.csv`, `N*_bradford*.csv`, `N*_lotka.csv` |
| Fuentes, autores, países, más citados | `results/tables/N*_top_sources.csv`, `N*_top_authors.csv`, `N*_top_countries.csv`, `N*_most_cited.csv`, `N*_top_local_references.csv` |
| Redes y mapas temáticos | `results/tables/N*_keyword_clusters.csv`, `N*_thematic_map.csv`, `N*_thematic_evolution.csv`, `data/processed/networks/*.graphml` |
| Tablas 3 y 5 (brechas) | `results/tables/gap_crop_route.csv`, `gap_crop_method.csv`, `gap_integration.csv` |
| Tabla 4 (metabolitos) | `results/tables/metabolite_candidates.csv`, `metabolite_key_studies.csv` |
| Contexto colombiano | `results/tables/N6_*.csv` |
| Estudios citados (por qué y dónde) | `config/estudios_clave.csv` → `results/tables/estudios_clave.csv`, `articulo/referencias.bib` |

## Estructura

```
config/queries.yaml        Estrategia de búsqueda jerárquica N1 -> N6 (OpenAlex + Scopus)
config/thesaurus.csv       Tesauro de normalización de palabras clave
protocolo/                 Protocolo de la revisión (preguntas, criterios, PRISMA)
src/01_harvest_openalex.py Recolección vía API REST de OpenAlex
src/02_harvest_scopus_api.py   (opcional) Scopus Search API con clave institucional
src/03_import_scopus_csv.py    (opcional) importación de exportaciones CSV de Scopus
src/04_clean_merge.py      Fusión, deduplicación, cribado y flujo PRISMA
src/05_bibliometrics.py    Análisis de desempeño (Bradford, Lotka, países, autores, citas)
src/06_networks.py         Co-ocurrencia, mapa temático, evolución temática, colaboración
src/07_gap_analysis.py     Brechas cultivo x ruta x método y priorización de metabolitos
src/08_build_article.py    Ensambla el artículo final (Markdown + DOCX)
src/09_references.py       Referencias APA/BibTeX verificadas en Crossref a partir del DOI
config/estudios_clave.csv  Estudios citados: DOI, sección y justificación
data/raw/                  Datos crudos versionados (JSONL comprimido) + registro de búsqueda
data/processed/            Corpus depurado, excluidos, redes GraphML, CSV para VOSviewer
results/tables|figures     Tablas y figuras del artículo
articulo/                  Manuscrito (Markdown + DOCX)
.github/workflows/         Pipeline automatizado (GitHub Actions)
```

## Cómo reproducir

### Opción A - GitHub Actions (recomendada, sin instalar nada)
1. Obtenga una clave gratuita de OpenAlex en <https://openalex.org/settings/api> (desde febrero de 2026 la API exige clave).
2. En GitHub: *Settings -> Secrets and variables -> Actions -> New repository secret* y cree `OPENALEX_API_KEY` y `SCOPUS_API_KEY`
   (opcional `SCOPUS_INSTTOKEN` para la vista completa de Scopus). **Nunca suba las claves como archivos al repositorio.**
3. *Actions -> Pipeline bibliometrico -> Run workflow* con `stage = all`.
   Los datos, tablas y figuras se guardan automáticamente en el repositorio.

### Opción B - local
```bash
pip install -r requirements.txt
export OPENALEX_API_KEY=su_clave
export SCOPUS_API_KEY=su_clave_elsevier
python src/01_harvest_openalex.py
python src/02_harvest_scopus_api.py
bash run_analysis.sh
```

### Complementar con Scopus mediante exportación manual
Ejecute en scopus.com cada cadena `scopus` de `config/queries.yaml`, exporte en CSV (*all available information*) y guarde como `data/raw/scopus_export/N1.csv`, `N4b.csv`, etc. Luego ejecute `bash run_analysis.sh`; los registros se fusionan y deduplican con los de OpenAlex.

### Abrir en VOSviewer o biblioshiny
`data/processed/vosviewer/<nivel>_scopus_format.csv` se puede importar como archivo de Scopus en VOSviewer (*Create map -> based on bibliographic data -> Scopus*) o en biblioshiny (`bibliometrix::biblioshiny()`).
