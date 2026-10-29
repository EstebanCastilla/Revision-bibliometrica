#!/usr/bin/env bash
# Ejecuta las etapas de procesamiento y análisis sobre los datos ya recolectados.
set -euo pipefail
cd "$(dirname "$0")"
python src/03_import_scopus_csv.py
python src/04_clean_merge.py
python src/05_bibliometrics.py
python src/06_networks.py
python src/07_gap_analysis.py
