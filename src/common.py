"""Utilidades compartidas por el pipeline bibliométrico."""
from __future__ import annotations

import gzip
import json
import re
import unicodedata
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "queries.yaml"
RAW_OA = ROOT / "data" / "raw" / "openalex"
RAW_SCOPUS_API = ROOT / "data" / "raw" / "scopus_api"
RAW_SCOPUS_CSV = ROOT / "data" / "raw" / "scopus_export"
PROCESSED = ROOT / "data" / "processed"
TABLES = ROOT / "results" / "tables"
FIGURES = ROOT / "results" / "figures"


def load_config() -> dict:
    with open(CONFIG, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def iter_queries(cfg: dict):
    """Devuelve cada consulta ejecutable (niveles y subniveles) como dict plano."""
    for level in cfg["levels"]:
        if "sublevels" in level:
            for sub in level["sublevels"]:
                yield {
                    "id": sub["id"],
                    "parent": level["id"],
                    "name": f'{level["name"]} - {sub["route"]}',
                    "openalex": " ".join(sub["openalex"].split()),
                    "scopus": " ".join(sub["scopus"].split()),
                    "extra_filter": sub.get("extra_filter"),
                }
        else:
            yield {
                "id": level["id"],
                "parent": level["id"],
                "name": level["name"],
                "openalex": " ".join(level["openalex"].split()),
                "scopus": " ".join(level["scopus"].split()),
                "extra_filter": level.get("extra_filter"),
            }


def write_jsonl_gz(path: Path, records) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with gzip.open(path, "wt", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            n += 1
    return n


def read_jsonl_gz(path: Path):
    with gzip.open(path, "rt", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                yield json.loads(line)


def strip_accents(text: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c))


def norm_title(title: str | None) -> str:
    """Clave de deduplicación: título en minúsculas, sin acentos ni signos."""
    if not title:
        return ""
    t = strip_accents(title.lower())
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"[^a-z0-9 ]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def norm_doi(doi: str | None) -> str:
    if not doi:
        return ""
    return re.sub(r"^https?://(dx\.)?doi\.org/", "", doi.strip().lower())


def run_metadata() -> dict:
    """Metadatos de trazabilidad: commit del código, entorno y versión de Python."""
    import os
    import platform
    import subprocess

    try:
        commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True,
                                text=True, check=True).stdout.strip()
        dirty = bool(subprocess.run(["git", "status", "--porcelain", "src", "config"], cwd=ROOT,
                                    capture_output=True, text=True).stdout.strip())
    except (OSError, subprocess.CalledProcessError):
        commit, dirty = None, None
    return {
        "code_commit": commit, "code_modified_since_commit": dirty,
        "environment": "GitHub Actions" if os.getenv("GITHUB_ACTIONS") else platform.node() or "local",
        "python": platform.python_version(),
    }
