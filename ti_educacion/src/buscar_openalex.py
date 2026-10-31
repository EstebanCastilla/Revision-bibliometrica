"""Búsqueda exploratoria (mapeo bibliométrico) sobre TI en educación superior.

Consulta la API de OpenAlex con filtros title_and_abstract.search (booleanos),
artículos y revisiones 2015-2026. Para cada eje temático guarda:
conteo total, producción anual, conteo con autores de Colombia y de
Latinoamérica, fuentes principales, documentos más citados y revisiones
recientes más citadas.

Uso: OPENALEX_API_KEY=... SCOPUS_API_KEY=... python ti_educacion/src/buscar_openalex.py
Solo se consideran documentos publicados en revistas (primary_location.source.type:journal).
"""
import csv, json, os, time, datetime as dt, pathlib, requests

API = "https://api.openalex.org/works"
OUT = pathlib.Path(__file__).resolve().parents[1] / "results"
KEY = os.environ.get("OPENALEX_API_KEY", "")
HE = ('("higher education" OR "university students" OR "university teachers" OR "university faculty" '
      'OR "higher education institutions" OR "tertiary education" OR "college students" '
      'OR "undergraduate students" OR "public universities" OR "university campus")')
BASE = "publication_year:2015-2026,type:article|review,is_retracted:false,primary_location.source.type:journal"
SCOPUS = "https://api.elsevier.com/content/search/scopus"
SKEY = os.environ.get("SCOPUS_API_KEY", "")
LATAM = "AR|BO|BR|CL|CO|CR|CU|DO|EC|GT|HN|MX|NI|PA|PE|PY|SV|UY|VE"

EJES = {
 "E00_TI_general": "TI/TIC en educación superior (marco general)",
 "E01_transformacion_digital": "Transformación digital de universidades",
 "E02_LMS_Moodle": "Adopción, uso y evaluación de LMS / Moodle",
 "E03_learning_analytics": "Analítica del aprendizaje y minería de datos educativos (logs LMS)",
 "E04_desercion_alerta_temprana": "Predicción de deserción / sistemas de alerta temprana",
 "E05_IA_generativa": "IA generativa y chatbots en educación superior",
 "E06_IA_en_LMS": "IA integrada en LMS (tutores, asistentes, recomendadores)",
 "E07_gobierno_TI": "Gobierno y gestión de servicios de TI (ITIL, COBIT, ISO 20000) en universidades",
 "E08_cloud_infraestructura": "Nube, infraestructura, escalabilidad y rendimiento de plataformas e-learning",
 "E09_ciberseguridad": "Ciberseguridad en universidades / plataformas e-learning",
 "E10_aceptacion_TAM_UTAUT": "Aceptación tecnológica (TAM/UTAUT) de e-learning",
 "E11_calidad_elearning": "Calidad y éxito de sistemas e-learning (DeLone-McLean, estándares)",
 "E12_interoperabilidad_datos": "Interoperabilidad (LTI, xAPI), integración y gobierno de datos académicos",
 "E13_integridad_proctoring": "Integridad académica y evaluación en línea (proctoring)",
 "E14_accesibilidad": "Accesibilidad e inclusión en entornos virtuales",
}
Q = {
 "E00_TI_general": f'("information technology" OR "information and communication technology" OR "information and communication technologies" OR "educational technology" OR "digital technologies" OR ICT) AND {HE}',
 "E01_transformacion_digital": f'("digital transformation" OR "digital maturity" OR "digital strategy" OR "smart university" OR "smart campus") AND ({HE} OR university OR universities)',
 "E02_LMS_Moodle": f'("learning management system" OR "learning management systems" OR Moodle OR "virtual learning environment" OR "virtual learning environments" OR "Canvas LMS" OR "Blackboard Learn") AND ({HE} OR university OR universities)',
 "E03_learning_analytics": f'("learning analytics" OR "educational data mining" OR "academic analytics") AND ({HE} OR university OR Moodle OR "learning management system" OR MOOC)',
 "E04_desercion_alerta_temprana": f'("student dropout" OR "dropout prediction" OR "student attrition" OR "at-risk students" OR "student retention" OR "early warning system" OR "early warning systems" OR "academic failure") AND ("machine learning" OR "predictive model" OR "learning analytics" OR "data mining" OR "deep learning") AND ({HE} OR university OR universities)',
 "E05_IA_generativa": f'("generative artificial intelligence" OR "generative AI" OR ChatGPT OR "large language model" OR "large language models" OR chatbot) AND ({HE} OR university OR universities)',
 "E06_IA_en_LMS": '("artificial intelligence" OR "machine learning" OR "large language model" OR chatbot OR "intelligent tutoring" OR "recommender system" OR "virtual assistant") AND ("learning management system" OR "learning management systems" OR Moodle)',
 "E07_gobierno_TI": f'("IT governance" OR "information technology governance" OR COBIT OR ITIL OR "IT service management" OR "ISO 20000" OR "enterprise architecture" OR "IT management") AND ({HE} OR university OR universities)',
 "E08_cloud_infraestructura": '("cloud computing" OR "cloud-based" OR "server virtualization" OR "virtual machine" OR "virtual machines" OR docker OR kubernetes OR "high availability" OR "load balancing" OR "load testing" OR "scalable architecture" OR "performance testing" OR "stress testing" OR "server performance" OR "server infrastructure") AND ("learning management system" OR "learning management systems" OR Moodle OR "e-learning platform" OR "e-learning system" OR "e-learning systems")',
 "E09_ciberseguridad": f'(cybersecurity OR "cyber security" OR "information security" OR phishing OR ransomware OR "security awareness") AND ({HE} OR university OR universities OR "e-learning" OR Moodle OR "learning management system")',
 "E10_aceptacion_TAM_UTAUT": f'("technology acceptance model" OR TAM OR UTAUT OR "unified theory of acceptance") AND ("e-learning" OR "learning management system" OR Moodle OR "online learning" OR "virtual learning environment") AND ({HE} OR university OR universities)',
 "E11_calidad_elearning": '("e-learning success" OR "information systems success" OR DeLone OR "service quality" OR "system quality" OR "quality assurance") AND ("e-learning" OR "learning management system" OR Moodle OR "online learning" OR "distance education")',
 "E12_interoperabilidad_datos": f'(interoperability OR "learning tools interoperability" OR xAPI OR "experience API" OR "data governance" OR "data warehouse" OR "student information system" OR "business intelligence") AND ({HE} OR university OR universities OR "learning management system" OR Moodle)',
 "E13_integridad_proctoring": f'(proctoring OR "online exam" OR "online examination" OR "online assessment" OR "e-assessment" OR "academic integrity" OR "academic dishonesty" OR "contract cheating") AND ({HE} OR university OR universities OR "online learning" OR Moodle)',
 "E14_accesibilidad": '("web accessibility" OR "digital accessibility" OR "universal design for learning" OR "students with disabilities" OR WCAG OR "accessible e-learning") AND ("e-learning" OR "learning management system" OR Moodle OR "online learning" OR "virtual learning" OR "higher education")',
}
# Términos (en minúscula, raíces) para verificar la precisión en una muestra aleatoria
VERIF = {
 "E00_TI_general": (["information technolog","communication technolog","educational technolog","digital technolog","ict"], None),
 "E01_transformacion_digital": (["digital transformation","digital maturity","digital strateg","smart universit","smart campus"], ["universit","higher education","college"]),
 "E02_LMS_Moodle": (["learning management system","moodle","virtual learning environment","canvas","blackboard"], ["universit","higher education","college","undergraduate","tertiary"]),
 "E03_learning_analytics": (["learning analytic","educational data mining","academic analytic"], None),
 "E04_desercion_alerta_temprana": (["dropout","attrition","at-risk","retention","early warning","academic failure"], ["machine learning","predict","analytic","data mining","deep learning"]),
 "E05_IA_generativa": (["generative","chatgpt","large language model","chatbot","llm"], ["universit","higher education","college","undergraduate","tertiary"]),
 "E06_IA_en_LMS": (["artificial intelligence","machine learning","language model","chatbot","tutoring","recommend","assistant"," ai "], ["learning management system","moodle"]),
 "E07_gobierno_TI": (["it governance","technology governance","cobit","itil","service management","iso 20000","enterprise architecture","it management"], ["universit","higher education","college"]),
 "E08_cloud_infraestructura": (["cloud","virtualiz","virtual machine","docker","kubernetes","availability","load balanc","load test","scalab","performance test","infrastructure"], ["learning management system","moodle","e-learning"]),
 "E09_ciberseguridad": (["cybersecurity","cyber security","cyber-security","information security","phishing","ransomware","security awareness"], None),
 "E10_aceptacion_TAM_UTAUT": (["technology acceptance","tam","utaut","unified theory"], ["e-learning","learning management","moodle","online learning","virtual learning"]),
 "E11_calidad_elearning": (["success","delone","service quality","system quality","quality assurance"], ["e-learning","learning management","moodle","online learning","distance education"]),
 "E12_interoperabilidad_datos": (["interoperab","lti","xapi","experience api","data governance","data warehouse","information system","business intelligence"], None),
 "E13_integridad_proctoring": (["proctor","online exam","online assessment","e-assessment","academic integrity","academic dishonesty","cheating"], None),
 "E14_accesibilidad": (["accessib","universal design","disabilit","wcag"], None),
}
S = requests.Session()

def get(params):
    params = {**params, "api_key": KEY} if KEY else params
    for i in range(6):
        r = S.get(API, params=params, timeout=90)
        if r.status_code == 200:
            return r.json()
        time.sleep(2 ** i)
    raise RuntimeError(f"{r.status_code} {r.text[:300]}")

def flt(q, extra=""):
    f = f"title_and_abstract.search:{q},{BASE}"
    return f + ("," + extra if extra else "")

def group(q, key, extra=""):
    d = get({"filter": flt(q, extra), "group_by": key, "per-page": 200})
    return d["group_by"]

SEL = "id,doi,title,publication_year,cited_by_count,primary_location,authorships,type"

def short(w):
    src = ((w.get("primary_location") or {}).get("source") or {}).get("display_name", "")
    au = [a["author"]["display_name"] for a in w.get("authorships", [])[:3]]
    ctry = sorted({c for a in w.get("authorships", []) for c in a.get("countries", [])})
    return {"titulo": w.get("title"), "anio": w.get("publication_year"), "citas": w.get("cited_by_count"),
            "tipo": w.get("type"), "fuente": src, "autores": "; ".join(au) + ("; et al." if len(w.get("authorships", [])) > 3 else ""),
            "paises": " ".join(ctry), "doi": w.get("doi") or w.get("id")}

def top(q, extra="", sort="cited_by_count:desc", n=10):
    d = get({"filter": flt(q, extra), "sort": sort, "per-page": n, "select": SEL})
    return [short(w) for w in d["results"]]

def scopus_count(q, extra=""):
    """Conteo en Scopus con la cadena equivalente TITLE-ABS-KEY (artículos y revisiones 2015-2026)."""
    if not SKEY:
        return ""
    query = f"TITLE-ABS-KEY({q}) AND PUBYEAR > 2014 AND PUBYEAR < 2027 AND (DOCTYPE(ar) OR DOCTYPE(re)){extra}"
    for i in range(5):
        r = S.get(SCOPUS, params={"query": query, "count": 1}, headers={"X-ELS-APIKey": SKEY, "Accept": "application/json"}, timeout=60)
        if r.status_code == 200:
            return int(r.json()["search-results"]["opensearch:totalResults"])
        time.sleep(2 ** i)
    return f"error {r.status_code}"

def abstract(inv):
    if not inv:
        return ""
    return " ".join(w for _, w in sorted((p, w) for w, ps in inv.items() for p in ps))

def precision(eid, q, n=50):
    """Proporción de una muestra aleatoria (semilla fija) que contiene ambos conceptos en título/resumen."""
    d = get({"filter": flt(q), "sample": n, "seed": 2026, "per-page": n, "select": "title,abstract_inverted_index"})
    a, b = VERIF[eid]; ok = 0
    for w in d["results"]:
        t = " " + ((w.get("title") or "") + " " + abstract(w.get("abstract_inverted_index"))).lower() + " "
        ok += any(x in t for x in a) and (b is None or any(x in t for x in b))
    return round(100 * ok / max(len(d["results"]), 1))

def main():
    resumen, anual, fuentes, citados = [], [], [], []
    for eid, q in Q.items():
        total = get({"filter": flt(q), "per-page": 1, "select": "id"})["meta"]["count"]
        years = {int(g["key"]): g["count"] for g in group(q, "publication_year")}
        co = get({"filter": flt(q, "authorships.countries:CO"), "per-page": 1, "select": "id"})["meta"]["count"]
        la = get({"filter": flt(q, f"authorships.countries:{LATAM}"), "per-page": 1, "select": "id"})["meta"]["count"]
        core = get({"filter": flt(q, "primary_location.source.is_core:true"), "per-page": 1, "select": "id"})["meta"]["count"]
        rev = get({"filter": flt(q, "type:review"), "per-page": 1, "select": "id"})["meta"]["count"]
        p1 = sum(years.get(y, 0) for y in range(2015, 2020)); p2 = sum(years.get(y, 0) for y in range(2020, 2025))
        resumen.append({"eje": eid, "nombre": EJES[eid], "total_2015_2026": total, "revisiones": rev,
                        "2015_2019": p1, "2020_2024": p2, "crec_quinquenal_%": round(100 * (p2 - p1) / p1, 1) if p1 else "",
                        "2025": years.get(2025, 0), "2026_parcial": years.get(2026, 0),
                        "precision_muestra_%": precision(eid, q), "revistas_core_cwts": core, "scopus": scopus_count(q), "scopus_colombia": scopus_count(q, " AND AFFILCOUNTRY(Colombia)"), "colombia": co, "latam": la, "pct_latam": round(100 * la / total, 1) if total else "",
                        "consulta_openalex": q})
        for y in range(2015, 2027):
            anual.append({"eje": eid, "anio": y, "docs": years.get(y, 0)})
        for g in group(q, "primary_location.source.id")[:10]:
            fuentes.append({"eje": eid, "fuente": g["key_display_name"], "docs": g["count"]})
        for cat, extra, sort in [("mas_citados", "", "cited_by_count:desc"),
                                 ("revisiones_2023_2026", "type:review,publication_year:2023-2026", "cited_by_count:desc"),
                                 ("recientes_2025_2026_citados", "publication_year:2025-2026", "cited_by_count:desc"),
                                 ("colombia_mas_citados", "authorships.countries:CO", "cited_by_count:desc")]:
            for r in top(q, extra, sort, 8 if cat != "mas_citados" else 10):
                citados.append({"eje": eid, "categoria": cat, **r})
        print(eid, total, "CO", co, "LATAM", la, flush=True)
    def w(name, rows):
        with open(OUT / name, "w", newline="", encoding="utf-8") as f:
            wr = csv.DictWriter(f, fieldnames=list(rows[0].keys())); wr.writeheader(); wr.writerows(rows)
    w("resumen_ejes.csv", resumen); w("produccion_anual.csv", anual)
    w("fuentes_principales.csv", fuentes); w("documentos_clave.csv", citados)
    json.dump({"fecha_consulta": dt.date.today().isoformat(), "base": "OpenAlex (+ conteos Scopus Search API)", "filtro_comun": BASE,
               "scopus": "TITLE-ABS-KEY(<consulta>) AND PUBYEAR > 2014 AND PUBYEAR < 2027 AND (DOCTYPE(ar) OR DOCTYPE(re))",
               "campo": "title_and_abstract.search"}, open(OUT / "registro_busqueda.json", "w"), indent=2)

if __name__ == "__main__":
    main()
