---
title: "Evaluación de sostenibilidad de biorrefinerías basadas en raíces y tubérculos: revisión bibliométrica jerárquica con énfasis en ñame (*Dioscorea rotundata*) y batata (*Ipomoea batatas*)"
subtitle: "Sustainability assessment of root and tuber biorefineries: a hierarchical bibliometric review focused on yam and sweet potato"
author: "[Nombre del autor] — Maestría en Ingeniería, [Universidad]"
date: "Fecha de corte de la búsqueda: 29 de octubre de 2026"
lang: es
---

# Resumen

Este trabajo presenta una revisión bibliométrica jerárquica que sustenta el diseño de una biorrefinería integrada a partir de ñame (*Dioscorea rotundata*) y batata (*Ipomoea batatas*) en San Jacinto (Bolívar, Colombia), cuya sostenibilidad se evaluará mediante análisis de ciclo de vida (ACV), evaluación tecno-económica (TEA) y análisis de ciclo de vida social (ACV-S). La literatura se recuperó por consumo programático de las API REST de OpenAlex y Scopus con 14 consultas organizadas en seis niveles, de lo general a lo específico: (N1) sostenibilidad de biorrefinerías, (N2) ACV-S y evaluación de sostenibilidad del ciclo de vida (LCSA), (N3) raíces y tubérculos en bioprocesos, (N4) rutas de transformación del ñame y la batata, (N5) sostenibilidad de sistemas de ñame y batata y (N6) contexto colombiano. De 34.616 registros identificados (2000-2026) se incluyeron 19.347 documentos únicos tras la deduplicación y el cribado automatizado reportado según PRISMA 2020. La evaluación de sostenibilidad de biorrefinerías creció a una tasa anual compuesta del 29,2 % y está dominada por el ACV y el TEA; la dimensión social es marginal (159 documentos). En el corpus de raíces y tubérculos, el ñame y la batata concentran la investigación en almidones y compuestos bioactivos, pero apenas registran 7 y 21 estudios de ACV, 20 y 39 de TEA y ninguno de ACV-S; ningún documento integra los tres pilares para ningún tubérculo, y solo 7 trabajos sobre ñame combinan tres o más de las rutas fijas. Colombia ocupa el noveno lugar mundial en N1 y aporta al autor más productivo del campo, pero su investigación en ñame forma un nicho desconectado de los temas de biorrefinería. El análisis de metabolitos prioriza los compuestos fenólicos y flavonoides (incluidas las antocianinas) para ambos cultivos, por su volumen de evidencia, su vigencia y su obtención a partir de residuos. Estos resultados delimitan un vacío de investigación explícito que justifica la evaluación integrada propuesta.

**Palabras clave:** biorrefinería; análisis de ciclo de vida; evaluación tecno-económica; análisis de ciclo de vida social; ñame; batata; bibliometría; OpenAlex.

# 1. Introducción

La transición hacia una bioeconomía exige sustituir progresivamente las materias primas fósiles por biomasa en la producción de energía, materiales y productos químicos. El concepto de biorrefinería, entendido como el procesamiento sostenible de la biomasa en un espectro de productos comercializables y energía (Cherubini, 2010), se ha consolidado como el marco tecnológico de esa transición. Sin embargo, la viabilidad de una biorrefinería no depende solo de su desempeño técnico: debe demostrar simultáneamente rentabilidad, menor carga ambiental que el sistema de referencia y beneficios para los actores de la cadena de valor (Moncada B. et al., 2016).

Para responder a esa exigencia se dispone de tres herramientas complementarias. El análisis de ciclo de vida (ACV), normalizado en ISO 14040 e ISO 14044 (ISO, 2006a, 2006b), cuantifica los impactos ambientales de un producto a lo largo de su ciclo de vida. La evaluación tecno-económica (TEA) integra el diseño conceptual del proceso, los balances de materia y energía y los indicadores de costo y rentabilidad (Cardona y Sánchez, 2007). El análisis de ciclo de vida social (ACV-S) evalúa los impactos sobre trabajadores, comunidades locales y demás partes interesadas, siguiendo las directrices del Programa de las Naciones Unidas para el Medio Ambiente (UNEP, 2020). La combinación de los tres pilares se conoce como evaluación de sostenibilidad del ciclo de vida (LCSA, por sus siglas en inglés; Kloepffer, 2008).

Las raíces y los tubérculos son materias primas atractivas para biorrefinerías en regiones tropicales: tienen un alto contenido de almidón fermentable, se cultivan en sistemas de pequeña escala y generan residuos (cáscaras, descartes por calibre o daño, follaje) con potencial de valorización. El ñame (*Dioscorea* spp.) es un cultivo central de la economía campesina del Caribe colombiano (Reina-Aranza, 2012), donde la asociatividad de los productores es un determinante de su desempeño (Mendoza-Crespo y Ortiz-Velásquez, 2020). La subregión de Montes de María, a la que pertenece San Jacinto (Bolívar), es además un territorio de posconflicto priorizado por los Programas de Desarrollo con Enfoque Territorial (PDET). Allí, la cadena del ñame depende de un mercado de exportación concentrado y es estructuralmente frágil (Granados Conde et al., 2026). En la región también se cultiva batata, aunque con menor desarrollo agroindustrial. Una biorrefinería que transforme ambas especies en almidón nativo, bioetanol, biogás, biofertilizante y metabolitos de alto valor podría diversificar mercados y aprovechar descartes. Su conveniencia, sin embargo, debe demostrarse con una evaluación integral de sostenibilidad **[VERIFICAR Y COMPLETAR: producción y área de ñame y batata en San Jacinto según Agronet-EVA, último año disponible]**.

Antes de diseñar dicha evaluación es necesario delimitar el estado del conocimiento: qué se ha investigado, quién lo ha hecho, con qué métodos y dónde están los vacíos. Los análisis bibliométricos permiten responder estas preguntas de manera cuantitativa y reproducible sobre grandes volúmenes de literatura (Donthu et al., 2021; Aria y Cuccurullo, 2017). Este trabajo presenta una revisión bibliométrica **jerárquica**, que recorre el campo de lo general a lo específico, desde la evaluación de sostenibilidad de biorrefinerías hasta el contexto colombiano, con seis preguntas de investigación:

- **PI1.** ¿Cómo ha evolucionado la producción científica sobre la evaluación de sostenibilidad de biorrefinerías y quiénes son sus actores principales?
- **PI2.** ¿Qué grado de madurez tiene la integración del ACV-S con el ACV y el TEA?
- **PI3.** ¿Qué rutas de valorización se han estudiado para raíces y tubérculos y cómo se posicionan el ñame y la batata?
- **PI4.** ¿Cuál es el estado de las rutas fijas (almidón nativo, bioetanol, biogás y biofertilizante) para ñame y batata y qué metabolitos son candidatos a completar el portafolio?
- **PI5.** ¿Existen evaluaciones de sostenibilidad de sistemas de ñame y batata y qué brechas presentan?
- **PI6.** ¿Cuál es la producción científica asociada a Colombia y a la región Caribe?

# 2. Metodología

## 2.1 Diseño del estudio y trazabilidad

Se realizó un análisis bibliométrico con dos componentes: análisis de desempeño y mapeo científico (Donthu et al., 2021). El proceso de identificación, cribado y elegibilidad se reporta con el diagrama de flujo de PRISMA 2020 (Page et al., 2021). Todo el procedimiento está implementado como un *pipeline* de código abierto en Python, versionado en un repositorio Git. El repositorio contiene las cadenas de búsqueda, los datos crudos descargados, el registro de cada consulta (fecha, número de resultados y versión del código), los registros excluidos con su motivo, los resultados intermedios y una bitácora de decisiones metodológicas. Así, cada cifra de este artículo puede rastrearse hasta su origen y reproducirse.

## 2.2 Fuentes de datos y técnica de obtención

La recolección se automatizó mediante el **consumo programático de API REST documentadas**, en lugar de técnicas de *web scraping* sobre las interfaces web de bases comerciales. Estas técnicas están restringidas por los términos de uso de los proveedores y no son reproducibles, porque dependen de la estructura HTML y de la sesión.

- **OpenAlex** (fuente principal; Priem et al., 2022). Es un índice bibliográfico abierto que integra metadatos de Crossref, PubMed, ORCID, repositorios y editoriales; su cobertura de referencias es comparable a la de Scopus y Web of Science (Culbert et al., 2025) y sus datos tienen licencia CC0. Se consultó el filtro booleano `title_and_abstract.search` (con *stemming*), restringido a artículos y revisiones de 2000 a 2026. La descarga se hizo por paginación con cursor (lotes de 200 registros), con reintentos y espera exponencial y autenticación mediante clave de API. Para cada nivel se recuperaron además las 60 referencias más citadas localmente.
- **Scopus Search API** (fuente de validación y complemento). Se ejecutaron las cadenas equivalentes en sintaxis TITLE-ABS-KEY. Con la clave disponible, sin token institucional, la API entrega una vista restringida (título, revista, año, citas, DOI y tipo), 25 registros por petición y un máximo de 5.000 resultados por consulta. Por ello, las consultas extensas se dividieron por rangos de años, y los DOI recuperados solo por Scopus se buscaron en OpenAlex para obtener metadatos completos.

La cosecha se ejecutó el 29 de octubre de 2026. Sobre esta fecha de corte, 2026 se trata como un año parcial.

## 2.3 Estrategia de búsqueda jerárquica

La estrategia se organizó en seis niveles anidados (Tabla 1). El nivel N4 se descompuso en siete sub-consultas: las cuatro rutas fijas de la biorrefinería, los metabolitos candidatos de cada cultivo y la valorización integral. Las cadenas completas se encuentran en `config/queries.yaml`.

**Tabla 1.** Niveles de la estrategia de búsqueda y registros recuperados por base de datos.

| Nivel | Alcance | Núcleo de la consulta (título y resumen) | OpenAlex | Scopus | Incluidos* |
|---|---|---|---:|---:|---:|
| N1 | Sostenibilidad de biorrefinerías | biorefinery AND (LCA OR techno-economic OR economic feasibility OR sustainability assessment OR social LCA OR LCSA) | 2.539 | 2.785 | 2.978 |
| N2 | ACV-S / LCSA en sistemas de base biológica | (biorefinery OR bioeconomy OR bio-based OR biofuel OR bioenergy) AND (social LCA OR S-LCA OR LCSA) | 131 | 142 | 159 |
| N3 | Raíces y tubérculos en bioprocesos | (cassava OR yam OR sweet potato OR potato OR taro OR cocoyam OR root/tuber crop) AND (biorefinery OR bioethanol OR biogas OR biofertilizer OR valorization OR LCA OR techno-economic) | 4.704 | 2.912 | 5.016 |
| N4a | Ñame y batata: almidón nativo | (yam OR Dioscorea OR sweet potato OR *Ipomoea batatas*) AND starch AND (extraction OR properties OR yield…) | 3.005 | 2.398 | 3.285 |
| N4b | Bioetanol | … AND (bioethanol OR ethanol production/fermentation OR fuel ethanol) | 346 | 232 | 376 |
| N4c | Biogás | … AND (biogas OR anaerobic digestion OR biomethane OR methane yield) | 101 | 61 | 105 |
| N4d | Biofertilizante | … AND (peel OR residue OR waste OR by-product OR vine) AND (biofertilizer OR compost OR digestate OR biochar…) | 174 | 100 | 200 |
| N4e | Metabolitos del ñame | (yam OR Dioscorea) AND (diosgenin OR dioscorin OR allantoin OR saponin OR phenolic OR flavonoid OR polysaccharide…) | 2.903 | 2.244 | 3.014 |
| N4f | Metabolitos de la batata | (sweet potato) AND (anthocyanin OR chlorogenic acid OR β-carotene OR sporamin OR phenolic OR pectin…) | 4.416 | 2.931 | 4.702 |
| N4g | Valorización integral | … AND (biorefinery OR valorization OR circular economy OR zero waste OR cascade) | 492 | 200 | 500 |
| N5 | Sostenibilidad de ñame y batata | (yam OR Dioscorea OR sweet potato) AND (LCA OR techno-economic OR economic feasibility OR social LCA OR carbon footprint OR value chain…) | 799 | 351 | 820 |
| N6 | Colombia: ñame y batata | (yam OR Dioscorea OR sweet potato OR batata) AND (Colombia OR Montes de María) | 186 | 80 | 179 |
| N6c | Colombia: bioprocesos con raíces y residuos | (biorefinery OR bioethanol OR biogas OR biofertilizer OR LCA OR techno-economic) AND (cassava OR yam OR starch OR agro-industrial residues) AND Colombia | 95 | 89 | 108 |
| N6b | Colombia: biorrefinerías evaluadas | N1 restringido a instituciones colombianas | 97 | 103 | 118 |

\*Registros únicos incluidos tras la fusión de ambas bases, la deduplicación y el cribado.

Durante las pruebas de las consultas se tomaron tres decisiones documentadas en la bitácora del repositorio:

1. El término «ñame» se excluyó de las consultas, porque ambas bases lo normalizan a «name» y recuperaban miles de falsos positivos.
2. En Scopus, el comodín `yam*` se reemplazó por `(yam OR yams)`, porque recuperaba documentos sobre la prueba econométrica de Toda-Yamamoto y el proyecto gasífero Yamal.
3. Las expresiones de evaluación económica se separaron en dos categorías: TEA de procesos y análisis económico agrícola o de mercado.

## 2.4 Depuración y elegibilidad

Los registros de ambas bases se fusionaron y se deduplicaron, primero por DOI y luego por título normalizado más año. Se excluyeron:

- los documentos sin título, los retractados y los que estaban fuera de periodo o de tipo documental;
- los registros de Scopus que no pudieron enlazarse con metadatos completos.

Los falsos positivos se controlaron con una verificación léxica automatizada sobre el título, el resumen y las palabras clave. Por ejemplo, se eliminaron los registros de *yam bean* (*Pachyrhizus*), los de N1 sin mención a biorrefinerías y los de N6 sin vínculo explícito con Colombia. Cuando OpenAlex no distribuía el resumen de un registro (como ocurre con parte de los resúmenes de Elsevier), su coincidencia temática se dio por confirmada si Scopus lo había recuperado con la misma consulta TITLE-ABS-KEY. Cada exclusión quedó registrada con su motivo.

## 2.5 Análisis

- **Desempeño:** producción anual, tasa de crecimiento anual compuesta (TCAC) hasta 2025, citas por documento, índice *h* de cada corpus y colaboración internacional, distinguiendo publicaciones de un solo país (SCP) y multinacionales (MCP).
- **Leyes bibliométricas:**
  - ley de Bradford, para identificar el núcleo de revistas que concentra un tercio de la producción (Bradford, 1934);
  - ley de Lotka, ajustada en escala log-log y contrastada con la prueba de Kolmogorov-Smirnov con α = 0,01 (Lotka, 1926; Pao, 1985).
- **Base intelectual:** referencias más citadas localmente en cada nivel.
- **Mapeo científico:**
  - redes de co-ocurrencia de palabras clave normalizadas con un tesauro, ponderadas por la fuerza de asociación (van Eck y Waltman, 2009) y agrupadas con el algoritmo de Louvain (Blondel et al., 2008);
  - mapas temáticos de centralidad y densidad construidos con el índice de equivalencia (Callon et al., 1991; Cobo et al., 2011);
  - evolución temática en tres periodos: 2000-2015, 2016-2020 y 2021-2026.
- **Análisis de brechas:** el corpus de N3 a N5 se clasificó con diccionarios controlados por cultivo (yuca, papa, ñame, batata, malanga/taro), por ruta de transformación y por método de evaluación. Con esa clasificación se construyeron matrices de cobertura y se midió el grado de integración: documentos con dos o más rutas fijas y con dos o tres pilares de sostenibilidad.
- **Priorización de metabolitos:** se calculó un índice normalizado por cultivo con cuatro componentes:
  - volumen de documentos (peso 0,35);
  - proporción publicada desde 2021 (0,25);
  - proporción que obtiene el metabolito de residuos o subproductos (0,25);
  - proporción con procesos de extracción o recuperación (0,15).

Las redes se exportaron en formato GraphML y el corpus en formato CSV compatible con Scopus, para verificarlos en VOSviewer (van Eck y Waltman, 2010) o biblioshiny (Aria y Cuccurullo, 2017). Las referencias citadas en este artículo se generaron y verificaron a partir de su DOI en la API de Crossref.

# 3. Resultados

## 3.1 Flujo PRISMA y cobertura de las bases de datos

Se identificaron 34.616 registros: 19.988 en OpenAlex y 14.628 en Scopus. Además, 2.833 DOI presentes solo en Scopus se completaron con metadatos de OpenAlex. Tras eliminar 13.457 duplicados quedaron 21.159 registros únicos. En el cribado se excluyeron 1.150 registros: 1.082 de Scopus sin metadatos enlazables, 55 de tipo documental no elegible, 10 retractados, 2 sin título y 1 fuera de periodo. En la verificación de elegibilidad se excluyeron 845 falsos positivos o registros fuera de alcance. El corpus final quedó en **19.347 documentos únicos** (Figura 1).

![Figura 1. Diagrama de flujo PRISMA 2020.](../results/figures/fig01_prisma.png)

La comparación de bases justifica el uso combinado. Entre el 91,4 % y el 99,3 % de los DOI recuperados por Scopus existen en el índice de OpenAlex. Sin embargo, la búsqueda en OpenAlex solo recuperó directamente entre el 58,7 % y el 80,0 % de ellos, porque no puede buscar en los resúmenes que no distribuye. A la inversa, OpenAlex aportó registros ausentes en Scopus: por ejemplo, 1.578 en N3 y 1.327 en N4f, en su mayoría revistas regionales y de acceso abierto. La Tabla 2 resume los indicadores de desempeño por nivel.

**Tabla 2.** Indicadores de desempeño por nivel jerárquico.

| Indicador | N1 | N2 | N3 | N4 | N5 | N6 |
|---|---:|---:|---:|---:|---:|---:|
| Documentos | 2.978 | 159 | 5.016 | 10.888 | 820 | 388 |
| Periodo | 2002-2026 | 2011-2026 | 2000-2026 | 2000-2026 | 2000-2026 | 2000-2026 |
| Fuentes | 590 | 71 | 2.035 | 3.384 | 524 | 183 |
| Autores | 10.282 | 589 | 17.679 | 35.374 | 3.095 | 1.039 |
| Revisiones | 300 | 10 | 95 | 241 | 14 | 9 |
| TCAC 2000-2025 (%) | 29,2 | 23,4 | 15,1 | 11,6 | 11,9 | 15,3 |
| Documentos 2021-2026 (%) | 64,5 | 63,5 | 44,3 | 40,6 | 52,1 | 46,6 |
| Citas por documento | 41,1 | 37,0 | 16,3 | 19,6 | 12,4 | 18,3 |
| Índice *h* del corpus | 152 | 44 | 122 | 168 | 47 | 45 |
| Coautores por documento | 5,09 | 4,38 | 4,28 | 4,54 | 4,21 | 4,04 |
| Colaboración internacional (%) | 31,9 | 33,3 | 16,7 | 12,6 | 17,3 | 28,1 |
| Acceso abierto (%) | 55,1 | 64,8 | 60,1 | 54,7 | 70,9 | 65,7 |

![Figura 2. Producción anual por nivel. La línea punteada corresponde a 2026, año parcial.](../results/figures/fig02_annual_production.png)

En todos los niveles, la productividad de los autores se ajusta a la ley de Lotka según la prueba de Kolmogorov-Smirnov (α = 0,01). Los exponentes (β) varían entre 2,72 (N6) y 3,90 (N5), por encima del valor clásico de 2, lo que indica campos con muchos autores ocasionales: entre el 80,2 % (N1) y el 91,6 % (N5) de los autores firma un solo documento. La dispersión de Bradford es mayor en los niveles de cultivo. En N1, 11 revistas concentran un tercio de la producción (958 documentos), mientras que en N4 se requieren 73.

## 3.2 N1: evaluación de sostenibilidad de biorrefinerías

N1 reúne 2.978 documentos con el mayor crecimiento del estudio (TCAC del 29,2 %). El 64,5 % se publicó desde 2021, con una caída transitoria en 2023-2024 que aparece en ambas bases de datos (Figura 2). El núcleo de Bradford lo encabezan *Bioresource Technology* (167 documentos), *Journal of Cleaner Production* (151), *Biofuels, Bioproducts and Biorefining* (123), *Biomass and Bioenergy* (101) y *Renewable and Sustainable Energy Reviews* (80).

Por países, la producción la lideran Estados Unidos (540 documentos), India (366), China (315), Brasil (233) y España (186). **Colombia ocupa el noveno lugar**, con 108 documentos y 3.761 citas; el 27 % de los documentos que lidera es de colaboración multinacional. El autor más productivo del nivel es Carlos Ariel Cardona Álzate (Universidad Nacional de Colombia), con 66 documentos e índice *h* local de 30. Le siguen J. F. Görgens (Sudáfrica, 52), M. T. Moreira (España, 42), A. Bonomi (Brasil, 36) y J. C. Solarte-Toro (Colombia, 28).

Los documentos más citados combinan revisiones y estudios de caso emblemáticos: la biorrefinería de microalgas (Chew et al., 2017), la biorrefinería de madera con baja huella de carbono (Liao et al., 2020), el ACV de biocombustibles y bioenergía (Cherubini et al., 2009), el TEA de pirólisis rápida (Wright et al., 2010) y las biorrefinerías de residuos en países en desarrollo (Nizami et al., 2017). La base intelectual, es decir, las referencias más citadas por el corpus, la forman el informe de diseño y economía de procesos de etanol lignocelulósico del NREL (Humbird et al., 2011), la base de datos ecoinvent (Wernet et al., 2016), el método ReCiPe 2016 (Huijbregts et al., 2017) y la definición de biorrefinería de Cherubini (2010). En conjunto, describen un campo de **ingeniería de procesos con evaluación ambiental**.

![Figura 3. Red de co-ocurrencia de palabras clave en N1.](../results/figures/N1_keyword_network.png)

El mapa temático de N1 identifica tres grupos:

- **Tema motor:** ACV, biocombustibles y economía circular (C1).
- **Tema básico o transversal:** TEA de biomasa lignocelulósica para bioetanol (C2).
- **Nicho:** factibilidad económica de digestión anaerobia y microalgas (C3).

La evolución temática muestra un desplazamiento claro. La presencia del TEA pasó del 30,2 % de los documentos en 2000-2015 al 45,0 % en 2021-2026, y la del ACV del 21,9 % al 33,8 %. La bioeconomía circular, ausente antes de 2016, aparece en el 14,0 % de los documentos recientes. En cambio, el etanol celulósico cayó del 11,4 % al 3,1 % y el rastrojo de maíz del 8,0 % al 3,3 %.

## 3.3 N2: integración de la dimensión social

La integración del ACV-S y del marco LCSA en sistemas de base biológica es reciente (desde 2011) y reducida: 159 documentos, frente a 2.978 en N1. Su crecimiento es alto (TCAC del 23,4 %) y la producción es predominantemente europea: Alemania (26 documentos), España (21) e Italia (19). Las fuentes núcleo son *The International Journal of Life Cycle Assessment* (21), *Journal of Cleaner Production* (16) y *Sustainability* (12).

El documento más citado revisa las evaluaciones ambientales, sociales y económicas de los bioplásticos (Spierling et al., 2018). La base intelectual descansa en la Social Hotspot Database (Benoit-Norris et al., 2012), en índices de ACV-S para productos de madera (Siebert et al., 2018), en el ACV-S de biodiésel (Macombe et al., 2013; Manik et al., 2013) y en revisiones de indicadores y marcos (Sala et al., 2013; Kühnen y Hahn, 2017; Lehmann et al., 2013; Ramos Huarachi et al., 2020; Huertas-Valdivia et al., 2020). La aplicación conjunta de LCSA en biorrefinerías se documenta en casos aislados, como el de las macroalgas (Sadhukhan et al., 2019).

El mapa temático ubica a LCSA con toma de decisiones multicriterio, y a ACV con costeo del ciclo de vida, como temas motores. El ACV-S y la sostenibilidad social funcionan como tema básico. La biorrefinería y la bioeconomía circular aparecen como nicho, y la creación de empleo y la salud y seguridad en bioetanol como tema emergente.

## 3.4 N3: raíces y tubérculos como materia prima

N3 reúne 5.016 documentos (TCAC del 15,1 %), con liderazgo de países productores tropicales y emergentes: China (489), Brasil (382), India (347), Nigeria (339) y Tailandia (309). Colombia ocupa el noveno lugar, con 126 documentos. El mapa temático distingue cuatro grupos:

- **Tema motor:** producción de bioetanol con *Saccharomyces cerevisiae* a partir de residuos agrícolas (C1).
- **Tema básico:** digestión anaerobia y biogás de cáscaras de yuca y papa (C2).
- **Nicho:** biofertilizantes en el cultivo de papa (C3).
- **Tema emergente o en declive:** bioetanol de yuca y batata con ACV y gases de efecto invernadero, donde aparece el ñame (C4).

Los trabajos comparativos sitúan a la yuca y la batata entre las fuentes de carbohidratos más productivas para bioetanol (Ziska et al., 2009; Thatoi et al., 2016).

La Tabla 3 cruza cultivos y rutas sobre el corpus de N3 a N5. La yuca es el cultivo con el perfil de rutas más equilibrado (1.102 documentos de almidón, 1.022 de bioetanol y 479 de biogás). El ñame y la batata, en cambio, concentran su literatura en almidón (1.344 y 2.346 documentos) y en metabolitos o bioactivos (2.246 y 3.665). Las rutas energéticas están poco exploradas: el ñame registra 71 documentos de bioetanol y 43 de biogás; la batata, 254 y 52.

**Tabla 3.** Documentos por cultivo y ruta de transformación (corpus N3-N5; un documento puede pertenecer a varias celdas).

| Cultivo | Almidón | Bioetanol | Biogás | Biofertilizante | Metabolitos | Bioplásticos | Alimento animal | Biorrefinería integrada |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Yuca | 1.102 | 1.022 | 479 | 248 | 219 | 168 | 234 | 83 |
| Papa | 892 | 359 | 333 | 642 | 442 | 149 | 159 | 87 |
| Ñame | 1.344 | 71 | 43 | 112 | 2.246 | 182 | 85 | 32 |
| Batata | 2.346 | 254 | 52 | 258 | 3.665 | 276 | 248 | 38 |
| Malanga/taro | 197 | 38 | 14 | 26 | 92 | 16 | 26 | 7 |

![Figura 4. Matriz cultivo × ruta de transformación.](../results/figures/fig06_gap_crop_route.png)

## 3.5 N4: rutas de transformación del ñame y la batata

N4 es el corpus más grande (10.888 documentos), pero su núcleo de Bradford corresponde a revistas de ciencia de alimentos: *Food Chemistry* (242), *International Journal of Biological Macromolecules* (206), *Starch/Stärke* (132) y *Foods* (125). La producción está dominada por China (2.860 documentos), seguida de Indonesia (991), Nigeria (652), India (620) y Estados Unidos (568). Colombia aparece en el duodécimo lugar (142 documentos), con una tasa de colaboración internacional (30,6 %) superior a la de los líderes.

Las rutas fijas presentan una cobertura muy desigual (Figura 5): almidón nativo, 3.285 documentos; bioetanol, 376; biofertilizante a partir de residuos, 200; biogás, 105. La valorización integral reúne 500.

![Figura 5. Documentos por ruta de transformación del ñame y la batata.](../results/figures/fig05_routes_coverage.png)

- **Almidón nativo.** La literatura caracteriza las propiedades fisicoquímicas y funcionales de los almidones de tubérculos tropicales (Moorthy, 2002) y sus aplicaciones en películas biodegradables (Mali et al., 2002) y en empaques inteligentes con antocianinas de batata morada (Choi et al., 2017). Para *D. rotundata* cultivado en Colombia ya existen caracterizaciones de almidones nativos y modificados (Rodríguez‐Manrique et al., 2025). Estos datos son directamente útiles para el inventario del TEA.
- **Bioetanol.** Predominan los estudios de hidrólisis y fermentación de batata (Lareo et al., 2013). Para el ñame la evidencia es escasa y procede, sobre todo, de África occidental y de residuos del procesamiento farmacéutico de *Dioscorea*.
- **Biogás.** Hay estudios de co-digestión de batata con estiércol, con evaluación técnico-económica (Montoro et al., 2019), de digestión de ramas de batata (Zhang et al., 2018) y de pretratamiento de cáscara de ñame (Onu et al., 2022). También se ha tratado por vía anaerobia el efluente de la extracción de diosgenina (Cheng et al., 2009).
- **Biofertilizante.** Es la ruta menos desarrollada como producto de biorrefinería. La literatura se refiere mayoritariamente al efecto de los abonos orgánicos sobre el cultivo (Agbede et al., 2013), no a la transformación de residuos de ñame o batata en un producto fertilizante caracterizado.
- **Valorización integral.** Existen esquemas en cascada para la batata: bioetanol y bebida destilada a partir de residuos (Weber et al., 2020) y extracción secuencial de proteínas y pectinas con uso del residuo sólido en biocompuestos (Vannini et al., 2021). Para el ñame, la obtención combinada de antocianinas y almidón de *D. alata* constituye el antecedente más cercano a una biorrefinería (Ochoa et al., 2023).

El mapa temático de N4 confirma esta orientación:

- **Tema motor:** actividad antioxidante, flavonoides, ñame y diosgenina (C2).
- **Tema básico:** batata, antocianinas y batata de pulpa morada o naranja (C1).
- **Nicho:** almidón de batata y de *D. alata* y sus propiedades funcionales (C3).

Desde 2000, la proporción de documentos sobre actividad antioxidante pasó del 10,3 % al 16,8 %, la de flavonoides del 4,8 % al 9,3 % y la de alimentos funcionales del 2,5 % al 7,1 %. La diosgenina, en cambio, bajó del 7,3 % al 4,1 %.

### Metabolitos candidatos

La minería de metabolitos (Tabla 4, Figura 6) muestra resultados distintos para cada cultivo.

- **Batata.** Los compuestos fenólicos (1.368 documentos; 477 vinculados a residuos), los flavonoides (760) y las antocianinas (1.613 documentos; 601 con procesos de extracción o recuperación) obtienen los índices de priorización más altos. Le siguen los carotenoides (1.347) y el ácido clorogénico, este último con el mayor impacto por documento (34,5 citas) y un 47 % de trabajos basados en hojas, cáscaras u otros residuos.
- **Ñame.** Los flavonoides (índice 0,806), las saponinas esteroidales (0,758), los compuestos fenólicos (0,749) y la diosgenina (0,689) encabezan la priorización. Sin embargo, la evidencia específica en *D. rotundata* es muy distinta según el compuesto: 52 documentos para compuestos fenólicos, 27 para saponinas, 23 para flavonoides y solo 5 para diosgenina. La diosgenina procede sobre todo de especies medicinales como *D. zingiberensis*, *D. bulbifera* y *D. nipponica* (Zhu et al., 2010; Obidiegwu et al., 2020).

**Tabla 4.** Metabolitos con mayor índice de priorización por cultivo.

| Cultivo | Metabolito | Documentos | % desde 2021 | Con residuos o subproductos | Con extracción o recuperación | En *D. rotundata* | Índice |
|---|---|---:|---:|---:|---:|---:|---:|
| Batata | Compuestos fenólicos | 1.368 | 47,7 | 477 | 471 | — | 0,696 |
| Batata | Flavonoides | 760 | 55,3 | 321 | 354 | — | 0,679 |
| Batata | Antocianinas | 1.613 | 44,1 | 306 | 601 | — | 0,637 |
| Batata | β-caroteno/carotenoides | 1.347 | 44,0 | 299 | 190 | — | 0,544 |
| Batata | Ácido clorogénico | 273 | 35,5 | 129 | 122 | — | 0,479 |
| Ñame | Flavonoides | 449 | 55,9 | 80 | 251 | 23 | 0,806 |
| Ñame | Saponinas esteroidales | 756 | 35,6 | 106 | 419 | 27 | 0,758 |
| Ñame | Compuestos fenólicos | 658 | 46,5 | 94 | 295 | 52 | 0,749 |
| Ñame | Diosgenina | 709 | 30,2 | 109 | 321 | 5 | 0,689 |
| Ñame | Polisacáridos/mucílago | 630 | 39,5 | 54 | 257 | 10 | 0,581 |
| Ñame | Dioscorina (proteína) | 125 | 24,0 | 16 | 54 | 3 | 0,320 |

![Figura 6. Metabolitos reportados en batata y ñame y proporción asociada a residuos o subproductos.](../results/figures/fig08_metabolites.png)

## 3.6 N5: evaluaciones de sostenibilidad del ñame y la batata

N5 reúne 820 documentos, con un perfil de impacto bajo (12,4 citas por documento) y liderado por Nigeria (137 documentos), India (62) e Indonesia (57). Su mapa temático muestra que la «sostenibilidad» del ñame y la batata se ha abordado sobre todo desde la economía agrícola. Son temas motores la rentabilidad de pequeños productores, los márgenes brutos y la seguridad alimentaria; el análisis beneficio-costo de sistemas de cultivo es transversal, y la factibilidad económica con valor presente neto es un nicho asociado a Nigeria.

La Tabla 5 cuantifica la brecha metodológica.

**Tabla 5.** Documentos por cultivo y método de evaluación, y grado de integración (corpus N3-N5).

| Cultivo | Documentos | ACV | TEA | Análisis económico agrícola o de mercado | ACV-S | Dimensión socioeconómica sin ACV-S | LCSA/multicriterio | ≥ 2 rutas fijas | ≥ 3 rutas fijas | ACV + TEA | ACV + TEA + ACV-S |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Yuca | 2.828 | 137 | 100 | 228 | 3 | 234 | 25 | 673 | 57 | 24 | 0 |
| Papa | 2.781 | 143 | 72 | 206 | 0 | 148 | 8 | 479 | 31 | 8 | 0 |
| Ñame | 4.378 | 7 | 20 | 254 | 0 | 247 | 4 | 353 | 7 | 0 | 0 |
| Batata | 7.153 | 21 | 39 | 350 | 0 | 355 | 11 | 692 | 15 | 1 | 0 |
| Malanga/taro | 398 | 2 | 6 | 37 | 0 | 54 | 1 | 57 | 1 | 0 | 0 |

![Figura 7. Matriz cultivo × método de evaluación.](../results/figures/fig07_gap_crop_method.png)

Los ACV identificados para la batata se centran en el bioetanol. Uno se realizó en una planta experimental (Costa et al., 2018) y otro comparó tres modos de producción, con la mejor eficiencia energética para el modo de economía circular (Zhang et al., 2017); un tercer trabajo evaluó el consumo energético del proceso (Ferrari et al., 2013). El único estudio que combina TEA y ACV para tubérculos amiláceos encontró que la batata tiene una alta rentabilidad inicial (retorno de la inversión del 41,96 %), pero un potencial de calentamiento global de 2,53 kg CO₂-eq frente a 0,25 kg CO₂-eq de la yuca, en una planta de 158.000 m³/año (Sanni et al., 2022).

Para el ñame, los TEA disponibles se concentran en la extracción de metabolitos de *D. alata* en Colombia. Ochoa et al. (2020) evaluaron la extracción de antocianinas asistida por ultrasonido y Ochoa et al. (2023) la integraron con la recuperación de almidón. Quiñonez-Ensuncho et al. (2026) mostraron que el almidón residual de esa extracción puede hidrolizarse a jarabe de glucosa, con factibilidad económica si se adquiere por menos de 1,20 USD/kg. Para la batata, Mokhtar (2022) simuló cinco escenarios de transformación de una variedad de pulpa naranja en productos de valor agregado con SuperPro Designer.

**No se identificó ningún estudio de ACV-S, ni ninguna evaluación que integre ACV, TEA y ACV-S, para ningún tubérculo.**

## 3.7 N6: contexto colombiano

N6 reúne 388 documentos, con crecimiento reciente (51 documentos en 2026, año parcial). Las instituciones colombianas más productivas son la Universidad Nacional de Colombia (122 documentos), la Universidad de Sucre (28), la Universidad de Cartagena (27), AGROSAVIA (23) y la Universidad de Córdoba. Por cultivo, el ñame (117 documentos) supera a la batata (64) y a la yuca (44). Por ruta, predominan la biorrefinería integrada (141), el biogás (63), el almidón (56) y el bioetanol (54). Por método, el TEA (107) supera al ACV (73), y el ACV-S apenas registra 6 documentos.

La capacidad colombiana en diseño y TEA de biorrefinerías es reconocida internacionalmente. Destacan el TEA de la biorrefinería de caña para el caso colombiano (Moncada et al., 2013), el etanol a partir de caña y maíz (Quintero et al., 2008), el TEA y la evaluación ambiental del etanol a partir de diez residuos agroindustriales (Duque et al., 2015), la revisión de la lignina como plataforma (Poveda-Giraldo et al., 2021) y la biorrefinería de malanga (*Xanthosoma sagittifolium*) orientada a la seguridad alimentaria (Serna-Loaiza et al., 2018). Para el almidón de yuca se comparó la huella de carbono, el uso de agua y el de energía entre Tailandia, Vietnam y Colombia (Tran et al., 2015).

El trabajo más cercano al objeto de esta tesis compara la producción de bioetanol a partir de caña, yuca y ñame en Colombia mediante simulación en Aspen Plus (Villadiego-del Villar et al., 2026). El ñame alcanzó un costo de producción de 1,11 USD/L, frente a 2,28 USD/L de la yuca y 0,68 USD/L de la caña. También mostró el mayor potencial de cogeneración eléctrica (171.330 kWh), pero su valor presente neto fue negativo en el escenario de producto único.

El mapa temático de N6 revela una desconexión (Figura 8). Los temas de biorrefinería, TEA y ACV forman un grupo motor, y la digestión anaerobia de residuos agroindustriales un grupo básico. En cambio, la investigación colombiana sobre ñame (*D. rotundata*, *D. alata*, Montes de María, diversidad genética, antracnosis por *Colletotrichum*, seguridad alimentaria) forma un **nicho de alta densidad interna y baja centralidad**: es un tema bien desarrollado, pero aislado de los temas de biorrefinería. Los estudios recientes del Caribe abordan la cadena del ñame desde la fragilidad estructural (Granados Conde et al., 2026), la optimización logística con pérdidas superiores al 30 % en Sucre (Vergara Rodríguez et al., 2025) y la transformación agroindustrial a escala rural (Martín et al., 2026; Paternina et al., 2026). En batata, los trabajos colombianos se orientan a la conservación de germoplasma (Rosero et al., 2022) y a la bioprospección de metabolitos de variedades nativas (CHÁVEZ et al., 2026).

![Figura 8. Mapa temático del nivel N6 (Colombia).](../results/figures/N6_thematic_map.png)

# 4. Discusión

## 4.1 Madurez desigual de los tres pilares de sostenibilidad

El embudo bibliométrico confirma que la evaluación de sostenibilidad de biorrefinerías es un campo maduro y en expansión acelerada, con un núcleo de revistas de ingeniería y un corpus metodológico consolidado: diseño de procesos al estilo NREL, ecoinvent y ReCiPe. Ese desarrollo, sin embargo, es asimétrico. El TEA y el ACV dominan y crecen, mientras que la dimensión social apenas reúne 159 documentos en todo el espectro de sistemas de base biológica. Además, el ACV-S está geográficamente concentrado en Europa y aplicado sobre todo a madera, biodiésel y bioplásticos. Los pocos casos tropicales, como la palma de aceite (Manik et al., 2013), muestran que las categorías de impacto social dependen fuertemente del contexto, lo que refuerza la necesidad de datos primarios regionales.

Para la tesis, esto implica que la evaluación social no podrá apoyarse en estudios análogos de tubérculos. Deberá construirse con las directrices de UNEP (2020) y bases de *hotspots* sociales (Benoit-Norris et al., 2012), adaptando sus indicadores a las categorías de trabajadores, comunidad local y agricultores definidas en los objetivos.

## 4.2 Ñame y batata: abundante ciencia de alimentos, escasa ingeniería de biorrefinerías

El volumen de literatura sobre ñame y batata (10.888 documentos en N4) contrasta con su escasa presencia como materia prima de bioprocesos evaluados. La comparación con la yuca es ilustrativa: la yuca tiene 137 ACV, 100 TEA y 24 estudios que combinan ambos, mientras que el ñame tiene 7 ACV, 20 TEA y ninguno combinado. La integración de rutas es igualmente baja: solo 7 documentos sobre ñame y 15 sobre batata combinan tres o más de las rutas fijas.

La evidencia económica disponible sugiere por qué la integración es necesaria. En Colombia, el bioetanol de ñame como producto único tiene costos competitivos frente a la yuca, pero un valor presente neto negativo (Villadiego-del Villar et al., 2026). En la batata, la rentabilidad del bioetanol se acompaña de una carga climática diez veces superior a la de la yuca (Sanni et al., 2022). Ambos resultados apuntan a que la viabilidad depende de distribuir costos e impactos entre varios productos, que es precisamente la lógica de la biorrefinería integrada.

## 4.3 Implicaciones para el diseño conceptual (TEA)

La literatura permite proponer una configuración en cascada coherente con las rutas fijas:

1. Extracción del metabolito de alto valor a partir del tubérculo de descarte o de la cáscara.
2. Recuperación de almidón nativo del residuo de extracción. Ochoa et al. (2023) y Quiñonez-Ensuncho et al. (2026) mostraron que el almidón residual conserva su valor.
3. Hidrólisis y fermentación del almidón no comercializable y de los descartes a bioetanol.
4. Digestión anaerobia de vinazas, cáscaras y ramas para obtener biogás y cogenerar energía (Montoro et al., 2019; Onu et al., 2022; Zhang et al., 2018).
5. Acondicionamiento del digestato como biofertilizante.

La ruta del biofertilizante es la menos documentada como producto: la tesis deberá caracterizar el digestato y el compost (nutrientes, estabilidad, inocuidad), en lugar de asumir su valor comercial. Del mismo modo, como el ñame carece de casi todo ACV, el inventario de ciclo de vida exige datos primarios de San Jacinto (rendimientos, fertilización, transporte y pérdidas poscosecha).

## 4.4 Selección de los metabolitos

La priorización ofrece un criterio cuantitativo para los metabolitos «por definir», que deberá confirmarse con la caracterización del material vegetal local:

- **Batata.** Los compuestos fenólicos y, dentro de ellos, las antocianinas y el ácido clorogénico combinan el mayor volumen de evidencia, una alta proporción de estudios con extracción desde residuos y aplicaciones industriales demostradas, como colorantes, empaques inteligentes y antioxidantes (Teow et al., 2007; Choi et al., 2017; Alam, 2021). La elección entre antocianinas y carotenoides depende de la variedad que se cultive en San Jacinto: las antocianinas son pertinentes para batata de pulpa morada y el β-caroteno para variedades de pulpa naranja, como Agrosavia Aurora. El ácido clorogénico es una alternativa que permite valorizar hojas y ramas, un residuo voluminoso del cultivo (Sun et al., 2014). La fibra y la pectina del residuo de extracción de almidón (Mei et al., 2010) y las proteínas o péptidos recuperables (Zhang et al., 2014) son coproductos secundarios.
- **Ñame.** Aunque la diosgenina y las saponinas esteroidales dominan la literatura del género, su evidencia en *D. rotundata* es mínima (5 documentos) y procede de especies medicinales con contenidos mucho mayores. Por ello, para el ñame de San Jacinto se recomienda priorizar el **extracto fenólico o de flavonoides** a partir de cáscaras, que es el grupo con más evidencia específica en *D. rotundata* (52 documentos) y una tendencia creciente (Adomėnienė y Venskutonis, 2022). Como segunda opción, los **polisacáridos no amiláceos o mucílago** de la cáscara, con propiedades funcionales documentadas (Zhao et al., 2023). La dioscorina (Hou et al., 2001) y la alantoína (Fu et al., 2006) son alternativas de alto valor, pero con evidencia insuficiente para un diseño conceptual sin experimentación previa.

## 4.5 Implicaciones para el ACV-S y el contexto territorial

El análisis de N6 muestra que Colombia cuenta con una escuela consolidada de diseño y evaluación de biorrefinerías (Moncada B. et al., 2016; Poveda-Giraldo et al., 2021) y con grupos regionales que estudian el ñame del Caribe desde la agronomía, la poscosecha y la cadena de suministro. Ambas comunidades, sin embargo, no se han encontrado. Una evaluación integrada en San Jacinto conecta esos dos nichos y aborda problemas sociales documentados en la región: la fragilidad de la cadena exportadora (Granados Conde et al., 2026), las pérdidas logísticas (Vergara Rodríguez et al., 2025) y la importancia de la asociatividad productiva (Mendoza-Crespo y Ortiz-Velásquez, 2020). Estos problemas sugieren subcategorías prioritarias para el ACV-S: ingresos justos y estabilidad de precios para agricultores, empleo local y condiciones de trabajo en la planta, acceso a recursos materiales e infraestructura comunitaria, y seguridad alimentaria.

## 4.6 Limitaciones

1. La búsqueda en título y resumen no recupera los documentos que tratan el tema solo en el texto completo, y parte de los resúmenes no está disponible en OpenAlex. La fusión con Scopus mitigó esta limitación (entre el 91,4 % y el 99,3 % de los DOI de Scopus se enlazaron), pero no la elimina.
2. La API de Scopus se usó en su vista restringida, por lo que los registros de Scopus no enlazables (1.082) no aportan autores ni afiliaciones.
3. La clasificación por diccionarios y las palabras clave de OpenAlex, asignadas automáticamente, introducen ruido. En N5 persisten documentos donde el cultivo se menciona de forma incidental. Esos documentos no se excluyeron manualmente, para preservar la reproducibilidad, y no se usaron en la interpretación cualitativa.
4. La literatura gris (informes de AGROSAVIA, MADR, ICA y tesis) no forma parte del análisis bibliométrico.
5. 2026 es un año parcial, por lo que las tasas de crecimiento se calcularon hasta 2025.

# 5. Conclusiones

1. La evaluación de sostenibilidad de biorrefinerías crece a una tasa anual compuesta del 29,2 % y se estructura alrededor del ACV y el TEA de biomasa lignocelulósica, con un giro reciente hacia la bioeconomía circular. Colombia es un actor relevante del campo: ocupa el noveno lugar mundial y aporta al autor más productivo.
2. La dimensión social es el pilar menos desarrollado (159 documentos sobre ACV-S o LCSA en sistemas de base biológica), con aplicaciones concentradas en Europa y en materias primas no amiláceas.
3. Entre las raíces y los tubérculos, la yuca concentra la investigación sobre rutas energéticas y evaluación de sostenibilidad. El ñame y la batata concentran su literatura en almidón y compuestos bioactivos, con muy pocos ACV (7 y 21) y TEA (20 y 39), y sin ningún ACV-S.
4. No existe en la literatura indexada ninguna evaluación que integre ACV, TEA y ACV-S para biorrefinerías de tubérculos. Solo 7 documentos sobre ñame y 15 sobre batata combinan tres o más de las rutas fijas. Este es el vacío de investigación que aborda la tesis.
5. La evidencia bibliométrica respalda una configuración en cascada (metabolito → almidón → bioetanol → biogás → biofertilizante). Como metabolitos se priorizan los compuestos fenólicos o flavonoides de la cáscara para el ñame y las antocianinas, el ácido clorogénico o el β-caroteno (según la variedad) para la batata. La selección final requiere caracterizar la biomasa de San Jacinto.
6. En Colombia, la investigación en biorrefinerías y la investigación en ñame forman comunidades desconectadas. Integrarlas en un caso territorial de Montes de María aporta novedad científica y pertinencia social.

**Trabajo futuro:** actualizar periódicamente la búsqueda ejecutando de nuevo el *pipeline*, incorporar las exportaciones completas de Scopus o Web of Science si se dispone de acceso institucional, y complementar el análisis bibliométrico con una revisión sistemática cualitativa de los estudios clave identificados (`results/tables/estudios_clave.csv`).

# Disponibilidad de datos y código

El código, las cadenas de búsqueda, los datos crudos (OpenAlex y Scopus), el corpus depurado, los registros excluidos con su motivo, las redes (GraphML), las tablas, las figuras y la bitácora de decisiones metodológicas están disponibles en el repositorio GitHub del proyecto (`EstebanCastilla/Revision-bibliometrica`). Para reproducir el análisis: `python src/01_harvest_openalex.py`, `python src/02_harvest_scopus_api.py` y `bash run_analysis.sh`.

# Referencias

Adomėnienė, A., & Venskutonis, P. R. (2022). Dioscorea spp.: Comprehensive Review of Antioxidant Properties and Their Relation to Phytochemicals and Health Benefits. *Molecules*, *27*(8), 2530. https://doi.org/10.3390/molecules27082530

Agbede, T., Adekiya, A., & Ogeh, J. (2013). Effects of organic fertilizers on yam productivity and some soil properties of a nutrient-depleted tropical Alfisol. *Archives of Agronomy and Soil Science*, *59*(6), 803-822. https://doi.org/10.1080/03650340.2012.683423

Alam, M. K. (2021). A comprehensive review of sweet potato (Ipomoea batatas [L.] Lam): Revisiting the associated health benefits. *Trends in Food Science & Technology*, *115*, 512-529. https://doi.org/10.1016/j.tifs.2021.07.001

Aria, M., & Cuccurullo, C. (2017). bibliometrix : An R-tool for comprehensive science mapping analysis. *Journal of Informetrics*, *11*(4), 959-975. https://doi.org/10.1016/j.joi.2017.08.007

Benoit-Norris, C., Cavan, D. A., & Norris, G. (2012). Identifying Social Impacts in Product Supply Chains:Overview and Application of the Social Hotspot Database. *Sustainability*, *4*(9), 1946-1965. https://doi.org/10.3390/su4091946

Blondel, V. D., Guillaume, J. L., Lambiotte, R., & Lefebvre, E. (2008). Fast unfolding of communities in large networks. *Journal of Statistical Mechanics: Theory and Experiment*, *2008*(10), P10008. https://doi.org/10.1088/1742-5468/2008/10/p10008

Bradford, S. C. (1934). Sources of information on specific subjects. *Engineering, 137*, 85-86.

Callon, M., Courtial, J. P., & Laville, F. (1991). Co-word analysis as a tool for describing the network of interactions between basic and technological research: The case of polymer chemsitry. *Scientometrics*, *22*(1), 155-205. https://doi.org/10.1007/bf02019280

Cardona, C. A., & Sánchez, Ó. J. (2007). Fuel ethanol production: Process design trends and integration opportunities. *Bioresource Technology*, *98*(12), 2415-2457. https://doi.org/10.1016/j.biortech.2007.01.002

Cheng, P., Zhao, H., Zhao, B., & Ni, J. (2009). Pilot treatment of wastewater from Dioscorea zingiberensis C.H. Wright production by anaerobic digestion combined with a biological aerated filter. *Bioresource Technology*, *100*(12), 2918-2925. https://doi.org/10.1016/j.biortech.2009.01.054

Cherubini, F. (2010). The biorefinery concept: Using biomass instead of oil for producing energy and chemicals. *Energy Conversion and Management*, *51*(7), 1412-1421. https://doi.org/10.1016/j.enconman.2010.01.015

Cherubini, F., Bird, N. D., Cowie, A., Jungmeier, G., Schlamadinger, B., & Woess-Gallasch, S. (2009). Energy- and greenhouse gas-based LCA of biofuel and bioenergy systems: Key issues, ranges and recommendations. *Resources, Conservation and Recycling*, *53*(8), 434-447. https://doi.org/10.1016/j.resconrec.2009.03.013

Chew, K. W., Yap, J. Y., Show, P. L., Suan, N. H., Juan, J. C., Ling, T. C., Lee, D. J., & Chang, J. S. (2017). Microalgae biorefinery: High value products perspectives. *Bioresource Technology*, *229*, 53-62. https://doi.org/10.1016/j.biortech.2017.01.006

Choi, I., Lee, J. Y., Lacroix, M., & Han, J. (2017). Intelligent pH indicator film composed of agar/potato starch and anthocyanin extracts from purple sweet potato. *Food Chemistry*, *218*, 122-128. https://doi.org/10.1016/j.foodchem.2016.09.050

CHÁVEZ, J. A. S., MARTÍNEZ, Ó. M. M., & ARISTIZÁBAL, L. S. R. (2026). Growth kinetics, secondary metabolite profiles and antioxidant activity in cell cultures for bioprospecting of a native sweet potato variety from La Guajira, Colombia. *Anais da Academia Brasileira de Ciências*, *98*(2), e20250795. https://doi.org/10.1590/0001-3765202620250795

Cobo, M., López-Herrera, A., Herrera-Viedma, E., & Herrera, F. (2011). An approach for detecting, quantifying, and visualizing the evolution of a research field: A practical application to the Fuzzy Sets Theory field. *Journal of Informetrics*, *5*(1), 146-166. https://doi.org/10.1016/j.joi.2010.10.002

Costa, D., Jesus, J., Virgínio e Silva, J., & Silveira, M. (2018). Life Cycle Assessment of Bioethanol Production from Sweet Potato (Ipomoea batatas L.) in an Experimental Plant. *BioEnergy Research*, *11*(3), 715-725. https://doi.org/10.1007/s12155-018-9932-1

Culbert, J. H., Hobert, A., Jahn, N., Haupka, N., Schmidt, M., Donner, P., & Mayr, P. (2025). Reference coverage analysis of OpenAlex compared to Web of Science and Scopus. *Scientometrics*, *130*(4), 2475-2492. https://doi.org/10.1007/s11192-025-05293-3

Donthu, N., Kumar, S., Mukherjee, D., Pandey, N., & Lim, W. M. (2021). How to conduct a bibliometric analysis: An overview and guidelines. *Journal of Business Research*, *133*, 285-296. https://doi.org/10.1016/j.jbusres.2021.04.070

Duque, S. H., Cardona, C. A., & Moncada, J. (2015). Techno-Economic and Environmental Analysis of Ethanol Production from 10 Agroindustrial Residues in Colombia. *Energy & Fuels*, *29*(2), 775-783. https://doi.org/10.1021/ef5019274

Ferrari, M. D., Guigou, M., & Lareo, C. (2013). Energy consumption evaluation of fuel bioethanol production from sweet potato. *Bioresource Technology*, *136*, 377-384. https://doi.org/10.1016/j.biortech.2013.03.045

Fu, Y. C., Ferng, L. H. A., & Huang, P. Y. (2006). Quantitative analysis of allantoin and allantoic acid in yam tuber, mucilage, skin and bulbil of the Dioscorea species. *Food Chemistry*, *94*(4), 541-549. https://doi.org/10.1016/j.foodchem.2004.12.006

Granados Conde, C., Gelvez Ordóñez, V., León-Méndez, G., Torrenegra Alarcón, M. E., & Herrera-García, U. (2026). Network Fragility and Sustainability of a Territorial Yam Supply Chain for Food Security in the Colombian Caribbean. *Sustainability*, *18*(20), 10416. https://doi.org/10.3390/su182010416

Hou, W. C., Lee, M. H., Chen, H. J., Liang, W. L., Han, C. H., Liu, Y. W., & Lin, Y. H. (2001). Antioxidant Activities of Dioscorin, the Storage Protein of Yam (Dioscorea batatas Decne) Tuber. *Journal of Agricultural and Food Chemistry*, *49*(10), 4956-4960. https://doi.org/10.1021/jf010606m

Huertas-Valdivia, I., Ferrari, A. M., Settembre-Blundo, D., & García-Muiña, F. E. (2020). Social Life-Cycle Assessment: A Review by Bibliometric Analysis. *Sustainability*, *12*(15), 6211. https://doi.org/10.3390/su12156211

Huijbregts, M. A. J., Steinmann, Z. J. N., Elshout, P. M. F., Stam, G., Verones, F., Vieira, M., Zijp, M., Hollander, A., & van Zelm, R. (2017). ReCiPe2016: a harmonised life cycle impact assessment method at midpoint and endpoint level. *The International Journal of Life Cycle Assessment*, *22*(2), 138-147. https://doi.org/10.1007/s11367-016-1246-y

Humbird, D., Davis, R., Tao, L., Kinchin, C., Hsu, D., Aden, A., Schoen, P., Lukas, J., Olthof, B., Worley, M., Sexton, D., & Dudgeon, D. (2011). Process Design and Economics for Biochemical Conversion of Lignocellulosic Biomass to Ethanol: Dilute-Acid Pretreatment and Enzymatic Hydrolysis of Corn Stover. Office of Scientific and Technical Information (OSTI). https://doi.org/10.2172/1013269

ISO. (2006a). *ISO 14040:2006. Environmental management - Life cycle assessment - Principles and framework*. International Organization for Standardization.

ISO. (2006b). *ISO 14044:2006. Environmental management - Life cycle assessment - Requirements and guidelines*. International Organization for Standardization.

Kloepffer, W. (2008). Life cycle sustainability assessment of products. *The International Journal of Life Cycle Assessment*, *13*(2), 89-95. https://doi.org/10.1065/lca2008.02.376

Kühnen, M., & Hahn, R. (2017). Indicators in Social Life Cycle Assessment: A Review of Frameworks, Theories, and Empirical Experience. *Journal of Industrial Ecology*, *21*(6), 1547-1565. https://doi.org/10.1111/jiec.12663

Lareo, C., Ferrari, M. D., Guigou, M., Fajardo, L., Larnaudie, V., Ramírez, M. B., & Martínez-Garreiro, J. (2013). Evaluation of sweet potato for fuel bioethanol production: hydrolysis and fermentation. *SpringerPlus*, *2*(1), 493. https://doi.org/10.1186/2193-1801-2-493

Lehmann, A., Zschieschang, E., Traverso, M., Finkbeiner, M., & Schebek, L. (2013). Social aspects for sustainability assessment of technologies—challenges for social life cycle assessment (SLCA). *The International Journal of Life Cycle Assessment*, *18*(8), 1581-1592. https://doi.org/10.1007/s11367-013-0594-0

Liao, Y., Koelewijn, S. F., Van den Bossche, G., Van Aelst, J., Van den Bosch, S., Renders, T., Navare, K., Nicolaï, T., Van Aelst, K., Maesen, M., Matsushima, H., Thevelein, J. M., Van Acker, K., Lagrain, B., Verboekend, D., & Sels, B. F. (2020). A sustainable wood biorefinery for low–carbon footprint chemicals production. *Science*, *367*(6484), 1385-1390. https://doi.org/10.1126/science.aau1567

Lotka, A. J. (1926). The frequency distribution of scientific productivity. *Journal of the Washington Academy of Sciences, 16*(12), 317-323.

Macombe, C., Leskinen, P., Feschet, P., & Antikainen, R. (2013). Social life cycle assessment of biodiesel production at three levels: a literature review and development needs. *Journal of Cleaner Production*, *52*, 205-216. https://doi.org/10.1016/j.jclepro.2013.03.026

Mali, S., Grossmann, M. V. E., Garcia, M. A., Martino, M. N., & Zaritzky, N. E. (2002). Microstructural characterization of yam starch films. *Carbohydrate Polymers*, *50*(4), 379-386. https://doi.org/10.1016/s0144-8617(02)00058-9

Manik, Y., Leahy, J., & Halog, A. (2013). Social life cycle assessment of palm oil biodiesel: a case study in Jambi Province of Indonesia. *The International Journal of Life Cycle Assessment*, *18*(7), 1386-1392. https://doi.org/10.1007/s11367-013-0581-5

Martín, M. A. B., Martínez, Y. T., & Quicazán, M. M. C. (2026). Application of lactic fermentation of yam (Dioscorea spp.) and mango (Mangifera indica) from Montes de María. *Applied Food Research*, *6*(1), 101663. https://doi.org/10.1016/j.afres.2026.101663

Mei, X., Mu, T. H., & Han, J. J. (2010). Composition and Physicochemical Properties of Dietary Fiber Extracted from Residues of 10 Varieties of Sweet Potato by a Sieving Method. *Journal of Agricultural and Food Chemistry*, *58*(12), 7305-7310. https://doi.org/10.1021/jf101021s

Mendoza-Crespo, H., & Ortiz-Velásquez, M. (2020). Importancia y determinantes de la asociación productiva agrícola: el cultivo de ñame en el caribe colombiano. *Sociedad y Economía*(41). https://doi.org/10.25100/sye.v0i41.8932

Mokhtar, M. N. (2022). Techno‐economic evaluation of a process for the transformation of VitAto sweet potato into value‐added products. *Journal of Food Process Engineering*, *45*(8), e14043. https://doi.org/10.1111/jfpe.14043

Moncada B., J., Aristizábal M., V., & Cardona A., C. A. (2016). Design strategies for sustainable biorefineries. *Biochemical Engineering Journal*, *116*, 122-134. https://doi.org/10.1016/j.bej.2016.06.009

Moncada, J., El-Halwagi, M. M., & Cardona, C. A. (2013). Techno-economic analysis for a sugarcane biorefinery: Colombian case. *Bioresource Technology*, *135*, 533-543. https://doi.org/10.1016/j.biortech.2012.08.137

Montoro, S., Lucas, J., Santos, D., & Costa, M. (2019). Anaerobic co-digestion of sweet potato and dairy cattle manure: A technical and economic evaluation for energy and biofertilizer production. *Journal of Cleaner Production*, *226*, 1082-1091. https://doi.org/10.1016/j.jclepro.2019.04.148

Moorthy, S. N. (2002). Physicochemical and Functional Properties of Tropical Tuber Starches: A Review. *Starch - Stärke*, *54*(12), 559-592. https://doi.org/10.1002/1521-379x(200212)54:12<559::aid-star2222559>3.0.co;2-f

Nizami, A., Rehan, M., Waqas, M., Naqvi, M., Ouda, O., Shahzad, K., Miandad, R., Khan, M., Syamsiro, M., Ismail, I., & Pant, D. (2017). Waste biorefineries: Enabling circular economies in developing countries. *Bioresource Technology*, *241*, 1101-1117. https://doi.org/10.1016/j.biortech.2017.05.097

Obidiegwu, J. E., Lyons, J. B., & Chilaka, C. A. (2020). The Dioscorea Genus (Yam)—An Appraisal of Nutritional and Therapeutic Potentials. *Foods*, *9*(9), 1304. https://doi.org/10.3390/foods9091304

Ochoa, S., Durango-Zuleta, M. M., & Felipe Osorio-Tobón, J. (2020). Techno-economic evaluation of the extraction of anthocyanins from purple yam (Dioscorea alata) using ultrasound-assisted extraction and conventional extraction processes. *Food and Bioproducts Processing*, *122*, 111-123. https://doi.org/10.1016/j.fbp.2020.04.007

Ochoa, S., Durango-Zuleta, M. M., & Osorio-Tobón, J. F. (2023). Integrated process for obtaining anthocyanins rich-extract by ultrasound-assisted extraction and starch recovery from purple yam (Dioscorea alata): a techno-economic evaluation. *Biomass Conversion and Biorefinery*, *13*(12), 10605-10614. https://doi.org/10.1007/s13399-021-01935-7

Onu, C. E., Nweke, C. N., & Nwabanne, J. T. (2022). Modeling of thermo-chemical pretreatment of yam peel substrate for biogas energy production: RSM, ANN, and ANFIS comparative approach. *Applied Surface Science Advances*, *11*, 100299. https://doi.org/10.1016/j.apsadv.2022.100299

Page, M. J., McKenzie, J. E., Bossuyt, P. M., Boutron, I., Hoffmann, T. C., Mulrow, C. D., Shamseer, L., Tetzlaff, J. M., Akl, E. A., Brennan, S. E., Chou, R., Glanville, J., Grimshaw, J. M., Hróbjartsson, A., Lalu, M. M., Li, T., Loder, E. W., Mayo-Wilson, E., McDonald, S., ..., & Moher, D. (2021). The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. *BMJ*, n71. https://doi.org/10.1136/bmj.n71

Pao, M. L. (1985). Lotka's law: A testing procedure. *Information Processing & Management*, *21*(4), 305-320. https://doi.org/10.1016/0306-4573(85)90055-x

Paternina, K., Alfieri, F., Julio-Gonzalez, L. C., López-Padilla, A., Montero, P., Moreno, F. J., & Hernandez-Hernandez, O. (2026). Agro-Industrial Potential of Yam (Dioscorea spp.): From Biological and Chemical Characterization to Industrial Applications and Valorization. *Foods*, *15*(18), 3178. https://doi.org/10.3390/foods15183178

Poveda-Giraldo, J. A., Solarte-Toro, J. C., & Cardona Alzate, C. A. (2021). The potential use of lignin as a platform product in biorefineries: A review. *Renewable and Sustainable Energy Reviews*, *138*, 110688. https://doi.org/10.1016/j.rser.2020.110688

Priem, J., Piwowar, H., & Orr, R. (2022). *OpenAlex: A fully-open index of scholarly works, authors, venues, institutions, and concepts* [Preprint]. arXiv. https://doi.org/10.48550/arXiv.2205.01833

Quintero, J., Montoya, M., Sánchez, O., Giraldo, O., & Cardona, C. (2008). Fuel ethanol production from sugarcane and corn: Comparative analysis for a Colombian case. *Energy*, *33*(3), 385-399. https://doi.org/10.1016/j.energy.2007.10.001

Quiñonez-Ensuncho, J., Ochoa, S., Osorio-Echeverri, V. M., & Osorio-Tobón, J. F. (2026). Enzymatic hydrolysis of starch from the anthocyanin extraction residue (AER-starch) with ultrasound pretreatment: A techno-economic assessment. *PLOS One*, *21*(3), e0343968. https://doi.org/10.1371/journal.pone.0343968

Ramos Huarachi, D. A., Piekarski, C. M., Puglieri, F. N., & de Francisco, A. C. (2020). Past and future of Social Life Cycle Assessment: Historical evolution and research trends. *Journal of Cleaner Production*, *264*, 121506. https://doi.org/10.1016/j.jclepro.2020.121506

Reina-Aranza, Y. C. (2012). El cultivo de ñame en el Caribe colombiano. Banco de la República. https://doi.org/10.32468/dtseru.168

Rodríguez‐Manrique, J. A., Salcedo‐Mendoza, J., Chávez‐Salazar, A., Cortés‐Rodríguez, M., & Castellanos‐Galeano, F. J. (2025). Isolation, Modification, and Characterization of Starches from Hawthorn yam (Dioscorea rotundata) Grown in Colombia: Bromatological Composition and Structural Analysis. *Starch - Stärke*, *77*(3), 2400052. https://doi.org/10.1002/star.202400052

Rosero, A., Rodríguez, E., Aguilera‐Arango, G., Rosero, M., Granda, L., Pastrana, I., Martínez, R., Perez, J., Espitia, L., Gomez, E., Rodríguez, T., & Sieber, S. (2022). Assessment of the Current State of In Situ Conservation and Use of Sweet Potato (Ipomoea batatas L.) in Colombia. *Culture, Agriculture, Food and Environment*, *44*(1), 76-89. https://doi.org/10.1111/cuag.12293

Sadhukhan, J., Gadkari, S., Martinez-Hernandez, E., Ng, K. S., Shemfe, M., Torres-Garcia, E., & Lynch, J. (2019). Novel macroalgae (seaweed) biorefinery systems for integrated chemical, protein, salt, nutrient and mineral extractions and environmental protection by green synthesis and life cycle sustainability assessments. *Green Chemistry*, *21*(10), 2635-2655. https://doi.org/10.1039/c9gc00607a

Sala, S., Farioli, F., & Zamagni, A. (2013). Life cycle sustainability assessment in the context of sustainability science progress (part 2). *The International Journal of Life Cycle Assessment*, *18*(9), 1686-1697. https://doi.org/10.1007/s11367-012-0509-5

Sanni, A., Olawale, A. S., Sani, Y. M., & Kheawhom, S. (2022). Sustainability analysis of bioethanol production from grain and tuber starchy feedstocks. *Scientific Reports*, *12*(1), 20971. https://doi.org/10.1038/s41598-022-24854-7

Serna-Loaiza, S., Carmona-Garcia, E., & Cardona, C. A. (2018). Potential raw materials for biorefineries to ensure food security: The Cocoyam case. *Industrial Crops and Products*, *126*, 92-102. https://doi.org/10.1016/j.indcrop.2018.10.005

Siebert, A., Bezama, A., O’Keeffe, S., & Thrän, D. (2018). Social life cycle assessment indices and indicators to monitor the social implications of wood-based products. *Journal of Cleaner Production*, *172*, 4074-4084. https://doi.org/10.1016/j.jclepro.2017.02.146

Spierling, S., Knüpffer, E., Behnsen, H., Mudersbach, M., Krieg, H., Springer, S., Albrecht, S., Herrmann, C., & Endres, H. J. (2018). Bio-based plastics - A review of environmental, social and economic impact assessments. *Journal of Cleaner Production*, *185*, 476-491. https://doi.org/10.1016/j.jclepro.2018.03.014

Sun, H., Mu, T., Xi, L., Zhang, M., & Chen, J. (2014). Sweet potato (Ipomoea batatas L.) leaves as nutritional and functional foods. *Food Chemistry*, *156*, 380-389. https://doi.org/10.1016/j.foodchem.2014.01.079

Teow, C. C., Truong, V. D., McFeeters, R. F., Thompson, R. L., Pecota, K. V., & Yencho, G. C. (2007). Antioxidant activities, phenolic and β-carotene contents of sweet potato genotypes with varying flesh colours. *Food Chemistry*, *103*(3), 829-838. https://doi.org/10.1016/j.foodchem.2006.09.033

Thatoi, H., Dash, P. K., Mohapatra, S., & Swain, M. R. (2016). Bioethanol production from tuber crops using fermentation technology: a review. *International Journal of Sustainable Energy*, *35*(5), 443-468. https://doi.org/10.1080/14786451.2014.918616

Tran, T., Da, G., Moreno-Santander, M. A., Vélez-Hernández, G. A., Giraldo-Toro, A., Piyachomkwan, K., Sriroth, K., & Dufour, D. (2015). A comparison of energy use, water use and carbon footprint of cassava starch production in Thailand, Vietnam and Colombia. *Resources, Conservation and Recycling*, *100*, 31-40. https://doi.org/10.1016/j.resconrec.2015.04.007

UNEP. (2020). *Guidelines for social life cycle assessment of products and organizations 2020* (C. Benoît Norris, M. Traverso, S. Neugebauer, E. Ekener, T. Schaubroeck, S. Russo Garrido, M. Berger, S. Valdivia, A. Lehmann, M. Finkbeiner y G. Arcese, Eds.). United Nations Environment Programme.

van Eck, N. J., & Waltman, L. (2009). How to normalize cooccurrence data? An analysis of some well‐known similarity measures. *Journal of the American Society for Information Science and Technology*, *60*(8), 1635-1651. https://doi.org/10.1002/asi.21075

van Eck, N. J., & Waltman, L. (2010). Software survey: VOSviewer, a computer program for bibliometric mapping. *Scientometrics*, *84*(2), 523-538. https://doi.org/10.1007/s11192-009-0146-3

Vannini, M., Marchese, P., Sisti, L., Saccani, A., Mu, T., Sun, H., & Celli, A. (2021). Integrated Efforts for the Valorization of Sweet Potato By-Products within a Circular Economy Concept: Biocomposites for Packaging Applications Close the Loop. *Polymers*, *13*(7), 1048. https://doi.org/10.3390/polym13071048

Vergara Rodríguez, C. J., Mendoza-Ortega, G. P., Mármol Barriosnuevo, M., & Díaz Sierra, M. (2025). Multi-objective optimization for the sustainable planning of yam cultivation and distribution in the Colombian Caribbean. *Frontiers in Sustainability*, *6*, 1653365. https://doi.org/10.3389/frsus.2025.1653365

Villadiego-del Villar, A. E., Padilla-Barcasnegra, D. P., & Rojas-Pérez, L. C. (2026). Comparative bioethanol production from sugarcane, cassava, and yam: A biorefinery and economic analysis in Colombia. *Biomass Conversion and Biorefinery*, *16*(3), 122. https://doi.org/10.1007/s13399-025-07012-7

Weber, C. T., Trierweiler, L. F., & Trierweiler, J. O. (2020). Food waste biorefinery advocating circular economy: Bioethanol and distilled beverage from sweet potato. *Journal of Cleaner Production*, *268*, 121788. https://doi.org/10.1016/j.jclepro.2020.121788

Wernet, G., Bauer, C., Steubing, B., Reinhard, J., Moreno-Ruiz, E., & Weidema, B. (2016). The ecoinvent database version 3 (part I): overview and methodology. *The International Journal of Life Cycle Assessment*, *21*(9), 1218-1230. https://doi.org/10.1007/s11367-016-1087-8

Wright, M. M., Daugaard, D. E., Satrio, J. A., & Brown, R. C. (2010). Techno-economic analysis of biomass fast pyrolysis to transportation fuels. *Fuel*, *89*, S2-S10. https://doi.org/10.1016/j.fuel.2010.07.029

Zhang, E., Li, J., Zhang, K., Wang, F., Yang, H., Zhi, S., & Liu, G. (2018). Anaerobic digestion performance of sweet potato vine and animal manure under wet, semi-dry, and dry conditions. *AMB Express*, *8*(1), 45. https://doi.org/10.1186/s13568-018-0572-9

Zhang, J., Jia, C., Wu, Y., Xia, X., Xi, B., Wang, L., & Zhai, Y. (2017). Life cycle energy efficiency and environmental impact assessment of bioethanol production from sweet potato based on different production modes. *PLOS ONE*, *12*(7), e0180685. https://doi.org/10.1371/journal.pone.0180685

Zhang, M., Mu, T. H., & Sun, M. J. (2014). Purification and identification of antioxidant peptides from sweet potato protein hydrolysates by Alcalase. *Journal of Functional Foods*, *7*, 191-200. https://doi.org/10.1016/j.jff.2014.02.012

Zhao, Z., Wang, L., Ruan, Y., Wen, C., Ge, M., Qian, Y., & Ma, B. (2023). Physicochemical properties and biological activities of polysaccharides from the peel of Dioscorea opposita Thunb. extracted by four different methods. *Food Science and Human Wellness*, *12*(1), 130-139. https://doi.org/10.1016/j.fshw.2022.07.031

Zhu, Y., Huang, W., & Ni, J. (2010). A promising clean process for production of diosgenin from Dioscorea zingiberensis C. H. Wright. *Journal of Cleaner Production*, *18*(3), 242-247. https://doi.org/10.1016/j.jclepro.2009.10.012

Ziska, L. H., Runion, G. B., Tomecek, M., Prior, S. A., Torbet, H. A., & Sicher, R. (2009). An evaluation of cassava, sweet potato and field corn as potential carbohydrate sources for bioethanol production in Alabama and Maryland. *Biomass and Bioenergy*, *33*(11), 1503-1508. https://doi.org/10.1016/j.biombioe.2009.07.014
