---
title: "Evaluación de sostenibilidad de biorrefinerías basadas en raíces y tubérculos: revisión bibliométrica jerárquica con énfasis en ñame (*Dioscorea rotundata*) y batata (*Ipomoea batatas*)"
subtitle: "Sustainability assessment of root and tuber biorefineries: a hierarchical bibliometric review focused on yam and sweet potato"
author: "[Nombre del autor] - Maestría en Ingeniería, [Universidad]"
date: "[Fecha]"
lang: es
---

> **Estado del borrador.** Las secciones 1 (Introducción) y 2 (Metodología) están redactadas. Las secciones 3 a 5 se escriben con las cifras reales del corpus una vez se ejecute el *pipeline* de recolección (`src/01_harvest_openalex.py`). Ningún resultado de este documento proviene de datos simulados. Los marcadores **[VERIFICAR]** señalan datos de contexto que el autor debe confirmar en la fuente oficial antes de enviar el artículo.

# Resumen

*[Se redacta al final, a partir de los resultados. Estructura sugerida (250 palabras): contexto - objetivo - método (OpenAlex/Scopus vía API, N registros, 2000-2026, PRISMA, indicadores de desempeño y mapeo científico) - resultados principales por nivel - brecha identificada - implicaciones para la biorrefinería de San Jacinto.]*

**Palabras clave:** biorrefinería; análisis de ciclo de vida; evaluación tecno-económica; análisis de ciclo de vida social; ñame; batata; bibliometría.

# 1. Introducción

La transición hacia una bioeconomía exige sustituir progresivamente las materias primas fósiles por biomasa en la producción de energía, materiales y productos químicos. El concepto de biorrefinería, entendido como el procesamiento sostenible de biomasa en un espectro de productos comercializables y energía (Cherubini, 2010), se ha consolidado como el marco tecnológico de esa transición. Sin embargo, la viabilidad de una biorrefinería no depende solo de su desempeño técnico: requiere demostrar simultáneamente rentabilidad, menor carga ambiental que el sistema de referencia y beneficios sociales para los actores de la cadena de valor (Moncada et al., 2016).

Para responder a esa exigencia se han desarrollado herramientas complementarias. El análisis de ciclo de vida (ACV), normalizado en ISO 14040 e ISO 14044 (ISO, 2006a, 2006b), cuantifica los impactos ambientales de un producto a lo largo de su ciclo de vida. La evaluación tecno-económica (TEA) integra el diseño conceptual del proceso, los balances de materia y energía y los indicadores de costo y rentabilidad. El análisis de ciclo de vida social (ACV-S) evalúa los impactos sobre trabajadores, comunidades locales y otros actores siguiendo las directrices del PNUMA (UNEP, 2020). La combinación de los tres pilares se conoce como evaluación de sostenibilidad del ciclo de vida (LCSA, por sus siglas en inglés; Kloepffer, 2008). Su aplicación conjunta a biorrefinerías es todavía heterogénea, en particular en lo relativo a la dimensión social.

Las raíces y tubérculos son materias primas atractivas para biorrefinerías en regiones tropicales: tienen un alto contenido de almidón fermentable, se cultivan en sistemas de pequeña escala y generan residuos (cáscaras, descartes por calibre o daño, follaje) con potencial de valorización. La yuca (*Manihot esculenta*) ha concentrado buena parte de la investigación sobre bioetanol y almidones en el trópico (Cardona & Sánchez, 2007). El ñame (*Dioscorea* spp.) y la batata (*Ipomoea batatas*) han recibido menos atención, a pesar de que el ñame es un cultivo central en la economía campesina del Caribe colombiano (Aguilera Díaz, 2012). Ambas especies contienen, además, metabolitos de interés (proteínas de reserva como la dioscorina y la esporamina, compuestos fenólicos, antocianinas, carotenoides y polisacáridos no amiláceos) que podrían elevar el valor agregado de una biorrefinería.

En Colombia, la producción de ñame se concentra en la región Caribe, y los departamentos de Bolívar, Córdoba y Sucre aportan la mayor parte del volumen nacional **[VERIFICAR: participación departamental y producción de San Jacinto en Agronet - Evaluaciones Agropecuarias Municipales, último año disponible]**. La subregión de Montes de María, donde se ubica San Jacinto (Bolívar), es una zona priorizada por los Programas de Desarrollo con Enfoque Territorial (PDET) tras el conflicto armado. En ella, la volatilidad de los precios del ñame y las pérdidas poscosecha limitan los ingresos de los productores **[VERIFICAR con fuente MADR/ICA]**. Una biorrefinería integrada que transforme ñame y batata en almidón nativo, bioetanol, biogás, biofertilizante y metabolitos de alto valor podría diversificar los mercados y aprovechar los descartes, pero su conveniencia debe demostrarse con una evaluación integral de sostenibilidad.

Antes de diseñar dicha evaluación es necesario delimitar el estado del conocimiento: qué se ha investigado, quién lo ha hecho, con qué métodos y dónde están los vacíos. Los análisis bibliométricos permiten responder estas preguntas de manera cuantitativa y reproducible sobre grandes volúmenes de literatura (Donthu et al., 2021; Aria & Cuccurullo, 2017). Este trabajo presenta una revisión bibliométrica **jerárquica**, que recorre el campo de lo general a lo específico. Parte de la evaluación de sostenibilidad de biorrefinerías (N1), pasa por la integración de la dimensión social (N2), por las raíces y tubérculos como materia prima (N3) y por las rutas de transformación del ñame y la batata (N4). Continúa con la evaluación de sostenibilidad de estos dos cultivos (N5) y termina en el contexto colombiano y caribeño (N6).

Las preguntas de investigación son:

- **PI1.** ¿Cómo ha evolucionado la producción científica sobre la evaluación de sostenibilidad de biorrefinerías y quiénes son sus actores principales?
- **PI2.** ¿Qué grado de madurez tiene la integración del ACV-S con el ACV y el TEA?
- **PI3.** ¿Qué rutas de valorización se han estudiado para raíces y tubérculos y cómo se posicionan el ñame y la batata?
- **PI4.** ¿Cuál es el estado de las rutas fijas (almidón nativo, bioetanol, biogás y biofertilizante) para ñame y batata, y qué metabolitos son candidatos a completar el portafolio de la biorrefinería?
- **PI5.** ¿Existen evaluaciones de sostenibilidad de sistemas de ñame y batata y qué brechas metodológicas presentan?
- **PI6.** ¿Cuál es la producción científica asociada a Colombia y a la región Caribe?

# 2. Metodología

## 2.1 Diseño del estudio

Se realizó un análisis bibliométrico con dos componentes: análisis de desempeño (*performance analysis*) y mapeo científico (*science mapping*) (Donthu et al., 2021). El proceso de identificación, cribado y elegibilidad se reporta siguiendo el diagrama de flujo de PRISMA 2020 (Page et al., 2021). El protocolo completo, el código y los datos están disponibles en el repositorio del proyecto, de modo que cualquier lector puede repetir el análisis con los mismos parámetros.

## 2.2 Fuente de datos y técnica de obtención

La recolección de datos se automatizó mediante el consumo programático de la **API REST de OpenAlex** (Priem et al., 2022). OpenAlex es un índice bibliográfico abierto que integra los metadatos de Crossref, PubMed, ORCID, repositorios institucionales y editoriales. Su cobertura de revistas y referencias es comparable a la de Scopus y Web of Science (Culbert et al., 2025), y sus datos se distribuyen bajo licencia CC0, lo que permite publicar el corpus completo. Se optó por una API documentada en lugar de técnicas de *web scraping* sobre interfaces web de bases comerciales. Esas técnicas están restringidas por los términos de uso de los proveedores y dependen de la estructura HTML de cada sesión, lo que impide su reproducibilidad.

El recolector se implementó en Python 3 (biblioteca `requests`) con las siguientes características:

1. Consultas booleanas sobre título y resumen (filtro `title_and_abstract.search`), con *stemming* automático.
2. Restricción a artículos y revisiones publicados entre 2000 y la fecha de corte (`publication_year:2000-2026`, `type:article|review`).
3. Paginación por cursor con lotes de 200 registros, reintentos con espera exponencial ante errores de red o de límite de tasa, y autenticación mediante clave de API.
4. Registro automático de cada consulta (cadena exacta, número de resultados, fecha y hora UTC) en `data/raw/openalex/search_log.json`.
5. Recuperación adicional de las 60 referencias más citadas localmente en cada corpus, para caracterizar su base intelectual.

El procedimiento se ejecuta como un flujo de trabajo de integración continua en GitHub Actions. Así quedan versionados el código, los datos crudos y los resultados de cada corrida. Para cada consulta se definió también la sintaxis equivalente de Scopus (TITLE-ABS-KEY). El *pipeline* admite registros de la Scopus Search API o de exportaciones CSV de Scopus, que se fusionan y deduplican con los de OpenAlex.

## 2.3 Estrategia de búsqueda jerárquica

La estrategia se organizó en seis niveles anidados, de lo general a lo específico (Tabla 1). El nivel N4 se descompuso en siete sub-consultas, una por cada ruta fija de la biorrefinería (almidón nativo, bioetanol, biogás y biofertilizante), una por cada grupo de metabolitos candidatos (ñame y batata) y una de valorización integral.

**Tabla 1.** Niveles de la estrategia de búsqueda. *[La columna de resultados se completa con `results/tables/search_strategy.csv`.]*

| Nivel | Alcance | Bloques de la consulta (título y resumen) | Registros |
|---|---|---|---|
| N1 | Sostenibilidad de biorrefinerías | biorefinery AND (LCA OR techno-economic OR economic feasibility OR sustainability assessment OR social life cycle OR life cycle sustainability) | - |
| N2 | ACV-S / LCSA en sistemas de base biológica | (biorefinery OR bioeconomy OR bio-based OR biofuel OR bioenergy) AND (social LCA OR S-LCA OR LCSA) | - |
| N3 | Raíces y tubérculos en bioprocesos | (cassava OR yam OR sweet potato OR potato OR taro OR cocoyam OR root/tuber crop) AND (biorefinery OR bioethanol OR biogas OR biofertilizer OR valorization OR LCA OR techno-economic) | - |
| N4a-g | Ñame y batata: rutas | (yam OR Dioscorea OR sweet potato OR Ipomoea batatas) AND [almidón / bioetanol / biogás / biofertilizante a partir de residuos / metabolitos del ñame / metabolitos de la batata / biorrefinería] | - |
| N5 | Sostenibilidad de ñame y batata | (yam OR Dioscorea OR sweet potato) AND (LCA OR techno-economic OR economic feasibility OR social life cycle OR carbon footprint OR value chain) | - |
| N6 | Colombia y Caribe | (yam OR ñame OR sweet potato OR batata OR cassava OR biorefinery OR bioethanol OR biogas) AND (Colombia OR Montes de María OR Bolívar OR Caribbean region); N1 restringido a instituciones colombianas | - |

## 2.4 Criterios de elegibilidad y depuración

Se fusionaron los registros de todas las consultas y se eliminaron los duplicados, primero por DOI y luego por título normalizado (minúsculas, sin acentos ni signos) más año de publicación. Se excluyeron los documentos sin título, los retractados y los que estaban fuera del periodo. Para controlar falsos positivos se aplicó una verificación léxica automatizada sobre el título, el resumen y las palabras clave. Por ejemplo, se eliminaron los registros de *yam bean* (*Pachyrhizus erosus*), los registros de N1 sin mención explícita a biorrefinerías y los registros de N6 sin vínculo con Colombia. Cada exclusión quedó registrada con su motivo (`data/processed/excluded.csv`).

## 2.5 Análisis

Los indicadores se calcularon en Python con `pandas`, `networkx` y `matplotlib`:

- **Desempeño:** producción anual, tasa de crecimiento anual compuesta (TCAC, calculada hasta el último año completo), citas por documento e índice h de cada corpus. Para los países se distinguieron las publicaciones de un solo país (SCP) y las multinacionales (MCP).
- **Leyes bibliométricas:** la ley de Bradford, para identificar el núcleo de revistas que concentra un tercio de la producción (Bradford, 1934), y la ley de Lotka, ajustada por mínimos cuadrados en escala log-log y contrastada con la prueba de Kolmogorov-Smirnov (Lotka, 1926; Pao, 1985).
- **Base intelectual:** las referencias más citadas por los documentos de cada nivel.
- **Mapeo científico:** redes de co-ocurrencia de palabras clave normalizadas mediante un tesauro. Las aristas se ponderaron por la fuerza de asociación (van Eck & Waltman, 2009) y los nodos se agruparon con el algoritmo de Louvain (Blondel et al., 2008). Con el índice de equivalencia se construyeron mapas temáticos de centralidad y densidad (Callon et al., 1991; Cobo et al., 2011) y se analizó la evolución temática en tres periodos (2000-2015, 2016-2020 y 2021-2026).
- **Análisis de brechas:** los documentos de N3 a N5 se clasificaron mediante diccionarios controlados por cultivo (yuca, papa, ñame, batata y malanga/taro), por ruta de transformación y por método de evaluación (ACV, TEA, ACV-S y LCSA). A partir de esa clasificación se construyeron matrices de cobertura y se midió el grado de integración (documentos que combinan dos o más rutas o dos o más pilares).
- **Priorización de metabolitos:** se calculó un índice compuesto, normalizado por cultivo, que pondera el volumen de documentos (0,35), la proporción de publicaciones desde 2021 (0,25), la proporción de estudios que obtienen el metabolito de residuos o subproductos (0,25) y la de estudios de extracción o recuperación (0,15). Así se privilegian los metabolitos compatibles con un esquema de biorrefinería en cascada.

Las redes se exportaron en formato GraphML y el corpus en formato CSV compatible con Scopus, para verificar los mapas en VOSviewer (van Eck & Waltman, 2010) o en biblioshiny (Aria & Cuccurullo, 2017).

# 3. Resultados

*[Pendiente de la ejecución del pipeline. Estructura prevista:]*

## 3.1 Flujo PRISMA y descripción general del corpus
*Figura 1 (diagrama PRISMA a partir de `prisma_flow.csv`) y Tabla 2 (`summary_by_level.csv`).*

## 3.2 N1 - Evaluación de sostenibilidad de biorrefinerías
*Producción anual (Fig. 2), Bradford, Lotka, países y colaboración, documentos más citados, red de palabras clave y mapa temático.*

## 3.3 N2 - Integración de la dimensión social
## 3.4 N3 - Raíces y tubérculos como materia prima
## 3.5 N4 - Rutas de transformación del ñame y la batata
*Cobertura por ruta (Fig. 5), metabolitos candidatos (Fig. 8).*

## 3.6 N5 - Evaluaciones de sostenibilidad de ñame y batata
*Matrices de brecha (Figs. 6 y 7).*

## 3.7 N6 - Contexto colombiano y caribeño

# 4. Discusión
*Implicaciones para el diseño conceptual (TEA), el inventario regional (ACV) y la selección de categorías de impacto social (ACV-S) de la biorrefinería de San Jacinto.*

# 5. Conclusiones

# Disponibilidad de datos y código
El código, los datos crudos, el corpus depurado y los resultados están disponibles en el repositorio GitHub del proyecto bajo licencia abierta.

# Referencias

Aguilera Díaz, M. (2012). *El cultivo de ñame en el Caribe colombiano* (Documentos de Trabajo sobre Economía Regional No. 168). Banco de la República.

Aria, M., & Cuccurullo, C. (2017). bibliometrix: An R-tool for comprehensive science mapping analysis. *Journal of Informetrics, 11*(4), 959-975. https://doi.org/10.1016/j.joi.2017.08.007

Blondel, V. D., Guillaume, J.-L., Lambiotte, R., & Lefebvre, E. (2008). Fast unfolding of communities in large networks. *Journal of Statistical Mechanics: Theory and Experiment, 2008*(10), P10008. https://doi.org/10.1088/1742-5468/2008/10/P10008

Bradford, S. C. (1934). Sources of information on specific subjects. *Engineering, 137*, 85-86.

Callon, M., Courtial, J. P., & Laville, F. (1991). Co-word analysis as a tool for describing the network of interactions between basic and technological research: The case of polymer chemistry. *Scientometrics, 22*(1), 155-205. https://doi.org/10.1007/BF02019280

Cardona, C. A., & Sánchez, Ó. J. (2007). Fuel ethanol production: Process design trends and integration opportunities. *Bioresource Technology, 98*(12), 2415-2457. https://doi.org/10.1016/j.biortech.2007.01.002

Cherubini, F. (2010). The biorefinery concept: Using biomass instead of oil for producing energy and chemicals. *Energy Conversion and Management, 51*(7), 1412-1421. https://doi.org/10.1016/j.enconman.2010.01.015

Cobo, M. J., López-Herrera, A. G., Herrera-Viedma, E., & Herrera, F. (2011). An approach for detecting, quantifying, and visualizing the evolution of a research field: A practical application to the Fuzzy Sets Theory field. *Journal of Informetrics, 5*(1), 146-166. https://doi.org/10.1016/j.joi.2010.10.002

Culbert, J. H., Hobert, A., Jahn, N., Haupka, N., Schmidt, M., Donner, P., & Mayr, P. (2025). Reference coverage analysis of OpenAlex compared to Web of Science and Scopus. *Scientometrics, 130*. **[VERIFICAR páginas y DOI]**

Donthu, N., Kumar, S., Mukherjee, D., Pandey, N., & Lim, W. M. (2021). How to conduct a bibliometric analysis: An overview and guidelines. *Journal of Business Research, 133*, 285-296. https://doi.org/10.1016/j.jbusres.2021.04.070

ISO. (2006a). *ISO 14040:2006 Environmental management - Life cycle assessment - Principles and framework*. International Organization for Standardization.

ISO. (2006b). *ISO 14044:2006 Environmental management - Life cycle assessment - Requirements and guidelines*. International Organization for Standardization.

Kloepffer, W. (2008). Life cycle sustainability assessment of products. *The International Journal of Life Cycle Assessment, 13*(2), 89-95. https://doi.org/10.1065/lca2008.02.376

Lotka, A. J. (1926). The frequency distribution of scientific productivity. *Journal of the Washington Academy of Sciences, 16*(12), 317-323.

Moncada B., J., Aristizábal M., V., & Cardona A., C. A. (2016). Design strategies for sustainable biorefineries. *Biochemical Engineering Journal, 116*, 122-134. https://doi.org/10.1016/j.bej.2016.06.009

Page, M. J., McKenzie, J. E., Bossuyt, P. M., Boutron, I., Hoffmann, T. C., Mulrow, C. D., et al. (2021). The PRISMA 2020 statement: An updated guideline for reporting systematic reviews. *BMJ, 372*, n71. https://doi.org/10.1136/bmj.n71

Pao, M. L. (1985). Lotka's law: A testing procedure. *Information Processing & Management, 21*(4), 305-320. https://doi.org/10.1016/0306-4573(85)90055-X

Priem, J., Piwowar, H., & Orr, R. (2022). OpenAlex: A fully-open index of scholarly works, authors, venues, institutions, and concepts. *arXiv*. https://doi.org/10.48550/arXiv.2205.01833

UNEP. (2020). *Guidelines for social life cycle assessment of products and organizations 2020* (C. Benoît Norris, M. Traverso, S. Neugebauer, E. Ekener, T. Schaubroeck, S. Russo Garrido, et al., Eds.). United Nations Environment Programme.

van Eck, N. J., & Waltman, L. (2009). How to normalize cooccurrence data? An analysis of some well-known similarity measures. *Journal of the American Society for Information Science and Technology, 60*(8), 1635-1651. https://doi.org/10.1002/asi.21075

van Eck, N. J., & Waltman, L. (2010). Software survey: VOSviewer, a computer program for bibliometric mapping. *Scientometrics, 84*(2), 523-538. https://doi.org/10.1007/s11192-009-0146-3
