# Protocolo de la revisión bibliométrica

**Proyecto de tesis:** *Evaluación de sostenibilidad de una biorrefinería integrada a partir de biomasa de ñame (*Dioscorea rotundata*) y batata (*Ipomoea batatas*) en San Jacinto, Bolívar.*

**Tipo de estudio:** revisión bibliométrica con análisis de desempeño y mapeo científico (Donthu et al., 2021), reportada según la lógica de flujo de PRISMA 2020 (Page et al., 2021).

---

## 1. Preguntas de investigación

| Código | Pregunta | Objetivo de tesis que sustenta |
|---|---|---|
| PI1 | ¿Cómo ha evolucionado la producción científica sobre la evaluación de sostenibilidad (ACV, TEA, ACV-S) de biorrefinerías y quiénes son sus actores principales (autores, fuentes, países)? | General |
| PI2 | ¿Qué grado de madurez tiene la integración de la dimensión social (ACV-S / LCSA) con el ACV y el TEA? | ACV-S |
| PI3 | ¿Qué rutas de valorización se han estudiado para raíces y tubérculos y cómo se posicionan el ñame y la batata frente a la yuca y la papa? | TEA, ACV |
| PI4 | ¿Cuál es el estado del conocimiento de las rutas fijas (almidón nativo, bioetanol, biogás, biofertilizante) para ñame y batata, y qué metabolitos de valor agregado son candidatos? | TEA (diseño conceptual) |
| PI5 | ¿Existen evaluaciones de sostenibilidad de sistemas de ñame y batata y qué brechas metodológicas presentan? | ACV, TEA, ACV-S |
| PI6 | ¿Cuál es la producción científica asociada a Colombia y a la región Caribe (Montes de María) en estos temas? | Contexto territorial |

## 2. Estrategia jerárquica (embudo de lo general a lo específico)

```
N1  Sostenibilidad de biorrefinerías (ACV / TEA / ACV-S)          <- marco general
 └─ N2  Integración social: ACV-S y LCSA en sistemas de base biológica
     └─ N3  Raíces y tubérculos como materia prima de bioprocesos
         └─ N4  Ñame y batata: rutas de transformación
             ├─ N4a Almidón nativo         ├─ N4e Metabolitos del ñame
             ├─ N4b Bioetanol              ├─ N4f Metabolitos de la batata
             ├─ N4c Biogás                 └─ N4g Biorrefinería / valorización integral
             └─ N4d Biofertilizante
             └─ N5  Sostenibilidad (ACV/TEA/ACV-S) de ñame y batata
                 └─ N6  Contexto Colombia / Caribe / Montes de María   <- más específico
```

Las cadenas completas (sintaxis OpenAlex y Scopus) están en [`config/queries.yaml`](../config/queries.yaml) y se documentan con su número de resultados y fecha de ejecución en `results/tables/search_strategy.csv`.

## 3. Fuentes de información y técnica de obtención de datos

| Fuente | Acceso | Técnica | Justificación |
|---|---|---|---|
| **OpenAlex** (Priem et al., 2022) | API REST pública (clave gratuita) | Recolección programática con Python (`requests`): consultas booleanas en título+resumen, paginación por cursor, reintentos con espera exponencial y registro de cada consulta | Índice abierto de >250 millones de trabajos que integra Crossref, PubMed, ORCID, repositorios y cubre la gran mayoría de las revistas indexadas en Scopus y Web of Science; los datos son CC0, lo que permite publicar el corpus y hace la búsqueda 100 % reproducible |
| **Scopus** (Elsevier) | Scopus Search API con clave institucional *o* exportación CSV desde scopus.com | `src/02_harvest_scopus_api.py` (API) o `src/03_import_scopus_csv.py` (CSV) | Base de referencia en ingeniería; se usa para validar la cobertura y complementar el corpus si la universidad provee acceso |

**¿Por qué API y no *web scraping*?** El *scraping* de la interfaz web de Scopus, Web of Science o Google Scholar está prohibido por sus términos de uso y produce resultados no reproducibles (dependen del HTML, de la sesión y de bloqueos). El consumo de **APIs REST documentadas** es la forma técnicamente sustentable de automatizar la obtención de datos: cada petición es una URL auditable, el resultado es JSON estructurado, y el procedimiento se puede repetir con el mismo código. Todo el proceso se ejecuta además como un flujo de trabajo de **GitHub Actions** (`.github/workflows/pipeline.yml`), lo que deja registro público de la fecha, el código y los datos de cada corrida.

## 4. Criterios de elegibilidad

**Inclusión**
- Documentos de tipo artículo o revisión (`type: article | review`).
- Publicados entre 2000 y la fecha de corte (2026 se trata como año parcial).
- Términos de búsqueda presentes en el título o el resumen.
- Cualquier idioma (se reporta la distribución por idioma).

**Exclusión (aplicada automáticamente y registrada en `data/processed/excluded.csv`)**
- Sin título, retractados o fuera del periodo.
- Falsos positivos léxicos: *yam bean* (*Pachyrhizus*), menciones sin el cultivo objetivo, sin mención a biorrefinería (N1), sin dimensión social (N2), sin vínculo con Colombia (N6).
- Duplicados: por DOI y, en su ausencia, por título normalizado + año.

## 5. Análisis

| Tipo | Indicador / técnica | Script |
|---|---|---|
| Desempeño | Producción anual, tasa de crecimiento anual compuesta (TCAC), citas/documento, índice h | `05_bibliometrics.py` |
| Desempeño | Ley de Bradford (zonas núcleo de revistas), ley de Lotka (productividad de autores, prueba K-S) | `05_bibliometrics.py` |
| Desempeño | Países: producción, citas, colaboración SCP/MCP | `05_bibliometrics.py` |
| Base intelectual | Referencias más citadas localmente | `01_harvest_openalex.py`, `05_bibliometrics.py` |
| Mapeo científico | Co-ocurrencia de palabras clave (fuerza de asociación; agrupamiento de Louvain) | `06_networks.py` |
| Mapeo científico | Mapa temático de Callon (centralidad-densidad) y evolución temática por periodos | `06_networks.py` |
| Mapeo científico | Red de colaboración entre países | `06_networks.py` |
| Brechas | Matrices cultivo x ruta y cultivo x método (ACV/TEA/ACV-S); grado de integración | `07_gap_analysis.py` |
| Priorización | Minería de metabolitos candidatos de ñame y batata (índice de priorización) | `07_gap_analysis.py` |

Las redes se exportan en GraphML y el corpus en formato CSV tipo Scopus (`data/processed/vosviewer/`) para replicar los mapas en **VOSviewer** o **biblioshiny (bibliometrix)**.

## 6. Limitaciones previstas
- La búsqueda en título y resumen no recupera documentos que solo mencionan el tema en el texto completo.
- Las palabras clave de OpenAlex se asignan automáticamente; se normalizan con un tesauro (`config/thesaurus.csv`).
- La literatura gris (tesis, informes técnicos de AGROSAVIA, ICA, MADR) no se incluye en el análisis bibliométrico y se trata en la discusión.
