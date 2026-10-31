"""Intersecciones temáticas (posibles brechas) relevantes para un proyecto de maestría
aplicado al CTEV - Universidad de Cartagena. Mismo filtro común que buscar_openalex.py."""
import csv, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import buscar_openalex as b

LMS = '("learning management system" OR "learning management systems" OR Moodle)'
GENAI = '("generative artificial intelligence" OR "generative AI" OR ChatGPT OR "large language model" OR "large language models" OR chatbot)'
LA = '("learning analytics" OR "educational data mining" OR "dropout prediction" OR "early warning system" OR "at-risk students")'
UNI = '("higher education" OR university OR universities)'
CASOS = [
 ("B01", "IA generativa integrada en Moodle/LMS", f"{GENAI} AND {LMS}", ""),
 ("B02", "Analítica/deserción con datos de Moodle", f"{LA} AND Moodle", ""),
 ("B03", "Analítica/deserción con datos LMS en Colombia", f"{LA} AND {LMS}", "authorships.countries:CO"),
 ("B04", "Analítica/deserción en educación superior en Colombia", f"{LA} AND {UNI}", "authorships.countries:CO"),
 ("B05", "LLM de código abierto / locales en universidades (soberanía de datos)", f'("open-source large language model" OR "open source LLM" OR "local LLM" OR "self-hosted" OR "on-premise" OR Llama OR Ollama) AND {GENAI} AND {UNI}', ""),
 ("B06", "RAG / asistentes basados en recuperación para cursos", f'("retrieval-augmented generation" OR "retrieval augmented generation") AND ({UNI} OR {LMS} OR course)', ""),
 ("B07", "Ciberseguridad de plataformas LMS/Moodle", f'(cybersecurity OR "information security" OR "security vulnerabilities" OR "web security" OR "penetration testing" OR phishing) AND {LMS}', ""),
 ("B08", "Gobierno/gestión de servicios TI aplicado a e-learning", f'("IT governance" OR COBIT OR ITIL OR "IT service management" OR "service level") AND ({LMS} OR "e-learning" OR "distance education")', ""),
 ("B09", "Rendimiento / escalabilidad de Moodle", '("server performance" OR "system performance" OR "performance evaluation" OR "response time" OR "load testing" OR "stress testing" OR "cloud computing" OR "high availability" OR "web server" OR "database performance") AND Moodle', ""),
 ("B10", "Observabilidad, monitoreo o AIOps de plataformas educativas", f'(observability OR "infrastructure monitoring" OR "system monitoring" OR AIOps OR "anomaly detection" OR "log analysis") AND ({LMS} OR "e-learning platform" OR "e-learning system")', ""),
 ("B11", "TI verde / eficiencia energética de TI en universidades", f'("green IT" OR "green computing" OR "green information technology" OR "energy efficiency" OR "carbon footprint") AND ("data center" OR "data centre" OR "IT infrastructure" OR "information technology" OR "e-learning") AND {UNI}', ""),
 ("B12", "Chatbots de soporte / mesa de ayuda universitaria", f'(chatbot OR "virtual assistant" OR "conversational agent") AND ("help desk" OR helpdesk OR "student support" OR "student services" OR "IT support" OR "technical support") AND {UNI}', ""),
 ("B14", "Transformación digital de universidades en Colombia", '("digital transformation" OR "digital maturity" OR "smart university") AND (university OR universities OR "higher education")', "authorships.countries:CO"),
 ("B15", "IA generativa en educación superior en Colombia", f"{GENAI} AND {UNI}", "authorships.countries:CO"),
 ("B16", "Moodle (cualquier tema) en Colombia", "Moodle", "authorships.countries:CO"),
 ("B17", "Políticas institucionales y gobernanza de la IA en universidades", f'("AI governance" OR "AI policy" OR "AI policies" OR "AI readiness" OR "AI adoption framework" OR "institutional policy") AND {GENAI} AND {UNI}', ""),
]

def main():
    rows = []
    for cid, nombre, q, extra in CASOS:
        n = b.get({"filter": b.flt(q, extra), "per-page": 1, "select": "id"})["meta"]["count"]
        n_rec = b.get({"filter": b.flt(q, extra + ("," if extra else "") + "publication_year:2023-2026"), "per-page": 1, "select": "id"})["meta"]["count"]
        tops = b.top(q, extra, n=5)
        rows.append({"id": cid, "interseccion": nombre, "docs_2015_2026": n, "docs_2023_2026": n_rec,
                     "filtro_extra": extra, "consulta": q,
                     "top5_citados": " || ".join(f'{t["titulo"]} ({t["anio"]}; {t["citas"]} citas; {t["doi"]})' for t in tops)})
        print(cid, n, n_rec, nombre, flush=True)
    with open(b.OUT / "brechas_intersecciones.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

if __name__ == "__main__":
    main()
