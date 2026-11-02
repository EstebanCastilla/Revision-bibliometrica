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
RAW_WOS_API = ROOT / "data" / "raw" / "wos_api"
RAW_WOS_EXPORT = ROOT / "data" / "raw" / "wos_export"
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
                    "wos": " ".join(sub.get("wos", "").split()),
                    "extra_filter": sub.get("extra_filter"),
                }
        else:
            yield {
                "id": level["id"],
                "parent": level["id"],
                "name": level["name"],
                "openalex": " ".join(level["openalex"].split()),
                "scopus": " ".join(level["scopus"].split()),
                "wos": " ".join(level.get("wos", "").split()),
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
    if not isinstance(doi, str) or not doi:
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


COUNTRY_ALIASES = {
    "usa": "US", "united states": "US", "peoples r china": "CN", "china": "CN", "england": "GB",
    "scotland": "GB", "wales": "GB", "north ireland": "GB", "united kingdom": "GB", "uk": "GB",
    "south korea": "KR", "korea": "KR", "russia": "RU", "iran": "IR", "taiwan": "TW", "vietnam": "VN",
    "viet nam": "VN", "turkiye": "TR", "turkey": "TR", "u arab emirates": "AE", "czech republic": "CZ",
    "bolivia": "BO", "venezuela": "VE", "tanzania": "TZ", "cote ivoire": "CI", "dem rep congo": "CD",
}


def country_to_iso2(name: str) -> str | None:
    """Convierte el nombre de país de una afiliación (Scopus/WoS) a código ISO 3166-1 alfa-2."""
    key = strip_accents((name or "").strip().rstrip(".")).lower()
    if not key:
        return None
    if key in COUNTRY_ALIASES:
        return COUNTRY_ALIASES[key]
    try:
        import pycountry
        return pycountry.countries.lookup(key).alpha_2
    except (ImportError, LookupError):
        return None


def elsevier_key() -> str | None:
    """Clave de la API de Elsevier/Scopus: acepta SCOPUS_API_KEY, ELSEVIER_API_KEY o Elsevier_api_key."""
    import os

    for name in ("SCOPUS_API_KEY", "ELSEVIER_API_KEY", "Elsevier_api_key"):
        if os.getenv(name, "").strip():
            return os.environ[name].strip()
    return None
