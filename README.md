# Revisión bibliométrica: sostenibilidad de una biorrefinería integrada de ñame y batata

Repositorio de la revisión bibliométrica de apoyo a la tesis de maestría en ingeniería

> **"Evaluación de sostenibilidad de una biorrefinería integrada a partir de biomasa de ñame (*Dioscorea rotundata*) y batata (*Ipomoea batatas*) en San Jacinto, Bolívar"**

Objetivo general: evaluar la sostenibilidad de una biorrefinería integrada basada en biomasa de ñame y batata en el norte de Colombia mediante **ACV**, **TEA** y **ACV-S**.
Rutas fijas para ambos tubérculos: almidón nativo, bioetanol, biogás, biofertilizante y un metabolito de valor agregado por cultivo (por definir con esta revisión).

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
data/raw/                  Datos crudos versionados (JSONL comprimido) + registro de búsqueda
data/processed/            Corpus depurado, excluidos, redes GraphML, CSV para VOSviewer
results/tables|figures     Tablas y figuras del artículo
articulo/                  Manuscrito (Markdown + DOCX)
.github/workflows/         Pipeline automatizado (GitHub Actions)
```

## Cómo reproducir

### Opción A - GitHub Actions (recomendada, sin instalar nada)
1. Obtenga una clave gratuita de OpenAlex en <https://openalex.org/settings/api> (desde febrero de 2026 la API exige clave).
2. En GitHub: *Settings -> Secrets and variables -> Actions -> New repository secret* y cree `OPENALEX_API_KEY`.
   Opcional: `SCOPUS_API_KEY` y `SCOPUS_INSTTOKEN` si su universidad tiene acceso a la API de Scopus.
3. *Actions -> Pipeline bibliometrico -> Run workflow* con `stage = all`.
   Los datos, tablas y figuras se guardan automáticamente en el repositorio.

### Opción B - local
```bash
pip install -r requirements.txt
export OPENALEX_API_KEY=su_clave
python src/01_harvest_openalex.py
bash run_analysis.sh
```

### Complementar con Scopus mediante exportación manual
Ejecute en scopus.com cada cadena `scopus` de `config/queries.yaml`, exporte en CSV (*all available information*) y guarde como `data/raw/scopus_export/N1.csv`, `N4b.csv`, etc. Luego ejecute `bash run_analysis.sh`; los registros se fusionan y deduplican con los de OpenAlex.

### Abrir en VOSviewer o biblioshiny
`data/processed/vosviewer/<nivel>_scopus_format.csv` se puede importar como archivo de Scopus en VOSviewer (*Create map -> based on bibliographic data -> Scopus*) o en biblioshiny (`bibliometrix::biblioshiny()`).
