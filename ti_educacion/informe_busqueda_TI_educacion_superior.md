# ¿Qué se ha publicado sobre TI en la educación superior? Mapeo bibliométrico exploratorio y propuestas de tema para la Maestría en Gerencia e Innovación en Tecnologías

**Proyecto independiente.** No forma parte de la revisión bibliométrica del ñame y la batata que está en este mismo repositorio: tiene sus propios scripts, datos y resultados dentro de `ti_educacion/`.

| | |
|---|---|
| Aspirante | Funcionario del CTEV (Centro Tecnológico para la Educación Virtual y a Distancia), Universidad de Cartagena. Administra servidores Linux y da soporte a la operación de Moodle |
| Programa | Maestría en Gerencia e Innovación en Tecnologías, Universidad de Cartagena |
| Fecha de la búsqueda | 31 de octubre de 2026 |
| Bases consultadas | OpenAlex (API REST) para todo el análisis; Scopus (Search API de Elsevier) para validar los conteos en revistas indexadas |
| Periodo | 2015-2026 (2026 es un año parcial, con corte al 31 de octubre) |
| Documentos | Artículos y revisiones publicados en **revistas científicas** (se excluyen repositorios, preprints, tesis y actas), sin retractados |

---

## 1. Resumen ejecutivo

1. **El tema está en plena expansión.** En el marco general ("TI/TIC en educación superior") OpenAlex registra **21.484 artículos en revistas** entre 2015 y 2026, de los cuales **11.169 están en Scopus**. La producción de 2025 (3.619) quintuplica la de 2015 (660).
2. **El motor actual es la IA generativa.** Pasó de 35 artículos en 2019 a 5.886 en 2025, y en 2026 ya suma 9.044 sin haber terminado el año (18.950 en total; 8.888 en Scopus). En segundo lugar está la **transformación digital de universidades**, que se multiplicó por 12 entre los quinquenios 2015-2019 y 2020-2024.
3. **Los temas cercanos a la operación de una plataforma son los menos estudiados.** Infraestructura, nube, rendimiento y alta disponibilidad de plataformas e-learning suman apenas **611 artículos** (210 en Scopus). La observabilidad y el monitoreo, unos 78, y en su mayoría no son pertinentes. El gobierno y la gestión de servicios de TI (ITIL, COBIT) en universidades, **714** (200 en Scopus). Todos son nichos con poca competencia académica y alto valor práctico.
4. **Colombia aparece poco.** Sus autores firman entre el 0,2 % y el 2,3 % de los artículos de cada eje. Hay **3 artículos en revistas** que usan datos de un LMS para la analítica del aprendizaje o la predicción de la deserción con autores de Colombia, y **2** sobre gobierno de TI en universidades. Esto deja espacio para aportes originales con datos locales.
5. **Recomendación.** Las brechas más claras que además puedes ejecutar desde el CTEV son dos:
   - **(A)** un asistente de IA generativa *soberano* (LLM de código abierto alojado en la infraestructura de la Universidad e integrado a Moodle), con su modelo de gobernanza;
   - **(B)** un sistema de alerta temprana de la deserción basado en los registros de Moodle (PostgreSQL) y con intervenciones automatizadas (SMTP).

   Ambos temas encajan con una maestría que combina *gerencia* e *innovación* si se abordan con *Design Science Research*. Es decir, no basta con "montar la herramienta": hay que diseñar un artefacto (arquitectura más modelo de gestión), implementarlo en piloto y evaluarlo con indicadores. Los detalles están en la sección 6.

---

## 2. Método

### 2.1 Estrategia de búsqueda

Se definieron **15 ejes temáticos** (E00-E14), que van del marco general a los temas más cercanos a tu trabajo. Cada eje combina dos bloques de conceptos (*tecnología* AND *contexto educativo*) con operadores booleanos y frases exactas en el **título y el resumen** (`title_and_abstract.search` en OpenAlex, que aplica *stemming*). La misma cadena se ejecutó en Scopus como `TITLE-ABS-KEY(...)`. Todas las cadenas exactas están en `results/resumen_ejes.csv` (columna `consulta_openalex`) y en `src/buscar_openalex.py`.

Bloque de contexto común ("educación superior"): `"higher education" OR "university students" OR "university teachers" OR "university faculty" OR "higher education institutions" OR "tertiary education" OR "college students" OR "undergraduate students" OR "public universities" OR "university campus"`, en algunos ejes complementado con `university OR universities`.

### 2.2 Control de calidad de las consultas

- **Precisión verificada por muestreo.** Para cada eje se tomó una muestra aleatoria de 50 registros (semilla fija 2026) y se comprobó que el título o el resumen contuvieran los dos conceptos. Todos los ejes quedaron con **una precisión del 90 % o más** (columna `precision_muestra_%`).
- **Términos ambiguos detectados y corregidos.** `virtualization` se reducía a "virtual" por el *stemming* y recuperaba "aula virtual"; `scalability` se reducía a "scale"; `dropout` se confunde con la técnica *dropout* de las redes neuronales; `LMS` también significa *least mean squares*. Todos se reemplazaron por frases exactas.
- **Solo revistas.** Una primera corrida mostró que Zenodo y DOAJ (repositorios) eran las "fuentes" más frecuentes, así que se restringió a `primary_location.source.type:journal`. Además se reporta cuántos artículos están en **revistas núcleo CWTS** (`is_core`, un indicador de revistas internacionales de calidad) y cuántos en **Scopus**.

### 2.3 Limitaciones

- Es un **mapeo exploratorio** (*scoping*), no una revisión sistemática con cribado manual. Los conteos tienen un margen de ruido de alrededor del 10 %, y las listas de "más citados" de algunos ejes amplios incluyen documentos marginales. Por ejemplo, en E12 (datos e interoperabilidad) aparecen bodegas de datos hospitalarias. Para la tesis hay que hacer el cribado PRISMA (ver la sección 7).
- Los conteos de 2026 son parciales. El "crecimiento quinquenal" compara 2015-2019 con 2020-2024.
- La sección de intersecciones (sección 5) usa consultas más finas. Las de los ejes B08, B10 y B11 tienen menos precisión: el conteo **sobreestima** la literatura realmente pertinente, lo que refuerza la conclusión de que esos temas están poco explorados.
- La página web de la maestría devolvió el error 503 el día de la búsqueda, así que **no se pudieron verificar sus líneas de investigación oficiales**. Antes de elegir el tema, confírmalas con la coordinación.

---

## 3. Panorama general: 15 ejes temáticos

Conteos de artículos y revisiones en revistas, 2015-2026. "Núcleo" = revistas núcleo CWTS. "CO" = al menos un autor con afiliación en Colombia. "LATAM" = al menos un autor latinoamericano.

| Eje | Tema | OpenAlex | Núcleo | **Scopus** | Revisiones | 2015-19 → 2020-24 | 2025 | CO (OpenAlex / Scopus) | % LATAM |
|---|---|---:|---:|---:|---:|---|---:|---|---:|
| E00 | TI/TIC en educación superior (marco general) | 21.484 | 5.834 | **11.169** | 362 | 3.902 → 9.999 (+156 %) | 3.619 | 155 / 235 | 6,6 |
| E01 | Transformación digital de universidades | 12.101 | 2.902 | **3.465** | 221 | 301 → 3.718 (+1.135 %) | 3.463 | 61 / 60 | 3,8 |
| E02 | Adopción, uso y evaluación de LMS / Moodle | 9.709 | 3.540 | **4.462** | 147 | 2.151 → 4.882 (+127 %) | 1.285 | 72 / 64 | 7,0 |
| E03 | Analítica del aprendizaje / minería de datos educativos | 3.863 | 2.062 | **2.957** | 151 | 740 → 1.337 (+81 %) | 625 | 25 / 34 | 5,8 |
| E04 | Predicción de la deserción / alerta temprana | 942 | 483 | **695** | 19 | 90 → 330 (+267 %) | 218 | 22 / 16 | **11,1** |
| E05 | IA generativa y chatbots en educación superior | 18.950 | 9.008 | **8.888** | 538 | 51 → 3.969 (+7.682 %) | 5.886 | 86 / 64 | 4,4 |
| E06 | IA integrada en LMS (tutores, asistentes, recomendadores) | 1.746 | 513 | **720** | 102 | 75 → 488 (+551 %) | 470 | 9 / 6 | 4,5 |
| E07 | Gobierno y gestión de servicios de TI (ITIL, COBIT) en universidades | 714 | 142 | **200** | 7 | 196 → 320 (+63 %) | 88 | **2 / 6** | 7,0 |
| E08 | Nube, infraestructura y rendimiento de plataformas e-learning | 611 | 194 | **210** | 13 | 134 → 232 (+73 %) | 105 | **1 / 3** | 2,5 |
| E09 | Ciberseguridad en universidades / e-learning | 4.312 | 1.506 | **1.746** | 47 | 650 → 1.801 (+177 %) | 856 | 14 / 7 | 2,2 |
| E10 | Aceptación tecnológica (TAM/UTAUT) de e-learning | 1.260 | 612 | **989** | 21 | 236 → 727 (+208 %) | 157 | 2 / 4 | 1,6 |
| E11 | Calidad y éxito de sistemas e-learning (DeLone-McLean) | 1.801 | 674 | **981** | 26 | 325 → 967 (+198 %) | 255 | 6 / 6 | 1,7 |
| E12 | Interoperabilidad (LTI, xAPI), BI y gobierno de datos | 3.508 | 2.032 | **1.656** | 71 | 742 → 1.311 (+77 %) | 609 | 20 / 19 | 4,8 |
| E13 | Integridad académica y evaluación en línea | 9.265 | 3.745 | **3.940** | 262 | 1.068 → 3.540 (+232 %) | 1.893 | 28 / 15 | 2,7 |
| E14 | Accesibilidad e inclusión en entornos virtuales | 2.670 | 1.138 | **1.573** | 78 | 490 → 1.201 (+145 %) | 448 | 12 / 21 | 7,6 |

Datos: `results/resumen_ejes.csv`, `results/produccion_anual.csv`, `results/fuentes_principales.csv`.

### 3.1 Producción anual de los ejes más relevantes (artículos en revistas, OpenAlex)

| Año | LMS/Moodle (E02) | Analítica (E03) | Deserción (E04) | IA generativa (E05) | IA en LMS (E06) | Gobierno TI (E07) | Infraestructura (E08) | Ciberseguridad (E09) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2015 | 373 | 86 | 14 | 2 | 11 | 33 | 21 | 95 |
| 2017 | 384 | 138 | 16 | 3 | 16 | 21 | 34 | 124 |
| 2019 | 545 | 222 | 28 | 35 | 21 | 66 | 33 | 173 |
| 2020 | 792 | 231 | 44 | 68 | 42 | 60 | 35 | 232 |
| 2021 | 1.045 | 211 | 39 | 77 | 48 | 59 | 47 | 282 |
| 2022 | 1.028 | 260 | 40 | 116 | 73 | 67 | 40 | 326 |
| 2023 | 970 | 258 | 79 | 960 | 101 | 64 | 49 | 406 |
| 2024 | 1.047 | 377 | 128 | 2.748 | 224 | 70 | 61 | 555 |
| 2025 | 1.285 | 625 | 218 | 5.886 | 470 | 88 | 105 | 856 |
| 2026* | 1.391 | 1.161 | 304 | 9.044 | 713 | 110 | 140 | 1.005 |

\* Año parcial, con corte al 31 de octubre de 2026.

**Lectura.** La COVID-19 (2020-2021) duplicó los estudios sobre LMS. ChatGPT (finales de 2022) cambió la escala de todo el campo. Desde 2024, la **IA dentro del LMS** (E06) y la **analítica del aprendizaje** (E03) vuelven a acelerarse, empujadas por la IA. En cambio, la infraestructura y el gobierno de TI crecen poco: ahí está la oportunidad.

### 3.2 Revistas donde más se publica (OpenAlex, revistas)

- **Marco general, LMS y aceptación:** *Education and Information Technologies* (Springer), *Sustainability* (MDPI), *Frontiers in Education*, *Education Sciences* (MDPI), *International Journal of Emerging Technologies in Learning (iJET)*.
- **Analítica y deserción:** *Journal of Learning Analytics*, *IEEE Access*, *Education and Information Technologies*, *Scientific Reports*.
- **IA generativa:** *Frontiers in Education*, *Education Sciences*, *Frontiers in Psychology*, *Education and Information Technologies*.
- **Ciberseguridad:** *Computers & Security*, *Journal of The Colloquium for Information Systems Security Education*, *Journal of Cybersecurity Education Research and Practice*.
- **Referentes de alto impacto** que conviene leer y considerar como destino de publicación: *International Journal of Educational Technology in Higher Education* (ETHE), *Computers & Education*, *Computers in Human Behavior*, *The Internet and Higher Education*, *IEEE Transactions on Learning Technologies*.
- **Revistas iberoamericanas que aparecen en los resultados:** *IEEE Revista Iberoamericana de Tecnologías del Aprendizaje (RITA)*, *IEEE Latin America Transactions*, *Comunicar*, *DYNA*, *Revista Colombiana de Computación*, *Íkala*.

---

## 4. ¿Qué se ha publicado? Hallazgos por línea temática

Las referencias completas están en [`results/referencias_seleccionadas.md`](results/referencias_seleccionadas.md). Los 30-40 documentos clave por eje (los más citados, las revisiones de 2023-2026, los recientes y los colombianos) están en [`results/documentos_clave.csv`](results/documentos_clave.csv).

### 4.1 Transformación digital de las universidades (E01)

- La revisión de referencia es colombiana: **Castro Benavides et al. (2020, *Sensors*)**, con 725 citas, sobre la transformación digital en instituciones de educación superior.
- Las revisiones recientes se concentran en las **barreras** organizacionales, culturales, de infraestructura y de competencias (Gkrimpizi et al., 2023; Singun, 2025) y en la relación entre la transformación digital y la sostenibilidad o la alfabetización digital (Farias-Gaytan et al., 2023).
- En América Latina, Okoye et al. (2022) analizan el alcance, las barreras y los cuellos de botella de las tecnologías digitales en la educación superior.
- **Para ti:** es el "paraguas gerencial" ideal para enmarcar cualquier proyecto técnico del CTEV como parte de la estrategia de transformación digital de la Universidad.

### 4.2 LMS y Moodle: adopción, éxito y calidad (E02, E10, E11)

- Es una línea madura, dominada por modelos de aceptación (**TAM/UTAUT**) y de éxito de sistemas de información (**DeLone-McLean**): Al-Fraihat et al. (2019), con 1.351 citas; Mohammadi (2015); Abbad (2021). Gamage et al. (2022) revisan las tendencias de uso de Moodle.
- Hay un mapeo sistemático colombiano-cubano sobre **TAM y Moodle** (García-Murillo et al., 2020).
- **Lectura crítica:** es un tema muy saturado. Otro estudio TAM sobre Moodle tendría poco valor de innovación. Sirve como **instrumento de evaluación** dentro de un proyecto mayor, por ejemplo para medir la aceptación de un asistente de IA.

### 4.3 Analítica del aprendizaje y deserción (E03, E04)

- Referentes: Viberg et al. (2018), Ifenthaler y Yau (2020) y Gašević et al. (2015), cuya tesis es que *los modelos predictivos no deben ser de talla única: dependen del diseño de cada curso*.
- **Uso de los registros de Moodle para predecir:** Conijn et al. (2016) compararon 17 cursos y encontraron que la capacidad predictiva varía mucho entre ellos. Otros trabajos predicen el riesgo desde las primeras semanas (VLE *big data* con *deep learning*, Waheed et al., 2019).
- Las revisiones recientes son sobre la predicción de la graduación con *machine learning* (Pelima et al., 2024) y sobre la deserción con *business intelligence* (Córdova Esparza et al., 2025).
- **Colombia:** el modelo de deserción de Heredia Vizcaíno et al. (2015); AnalyTIC, una solución para gestionar el ciclo de vida de la analítica en un LMS (Herrera et al., 2019); el análisis de la brecha digital colombiana con registros de Moodle (Morales Dussan et al., 2021); y la predicción con LSTM (Vives et al., 2024).
- **Contexto nacional:** según SPADIES (MEN), la deserción anual fue del 8,97 % en 2023, y la deserción acumulada en programas universitarios ronda el 25 % a los 10 semestres. Estudios anteriores reportan que los programas a distancia tienen tasas unos 12 puntos mayores que los presenciales. Es un problema institucional prioritario y está directamente ligado a la educación virtual.

### 4.4 IA generativa en la educación superior (E05, E06, B01, B05, B06, B17)

- Los temas dominantes son la **integridad académica** (Cotton et al., 2023, con 3.084 citas; Bittle y El-Gayar, 2025), las **percepciones de estudiantes y docentes** (Chan y Hu, 2023) y las **políticas institucionales** (Chan, 2023, marco de política de IA para universidades; McDonald et al., 2025, análisis de políticas y guías institucionales).
- **La IA dentro del LMS crece rápido** (E06: de 101 artículos en 2023 a 470 en 2025). Hay asistentes inteligentes integrados (Sajja et al., 2024), chatbots basados en LLM para cursos (Neumann et al., 2024) y el paso de los chatbots por intenciones a los asistentes con LLM (Alsafari et al., 2024).
- Un hallazgo muy pertinente para el CTEV es **LAMB (Alier et al., 2024)**: un *framework* de código abierto para crear asistentes de IA desplegados e **integrados en LMS** como Moodle, desarrollado por universidades españolas.
- La **gobernanza de la IA generativa** en la educación superior es una línea emergente (revisión de Barus et al., 2025).
- **Ecosistema tecnológico:** desde la versión 4.5, Moodle trae un **subsistema de IA** (*placements*, *actions*, *providers*). En Moodle 5.0 se puede usar **Ollama** como proveedor para correr modelos abiertos (por ejemplo Llama) en servidores propios, con el aviso de que Ollama no trae autenticación y debe protegerse con un *firewall* o un *proxy* inverso. Esto vuelve técnicamente viable una "IA soberana" en Rocky Linux.

### 4.5 Infraestructura, nube y operación de plataformas (E08, B09, B10)

- La literatura es **escasa y de bajo impacto**: 611 artículos en revistas y 210 en Scopus. Predominan los estudios de beneficios y desafíos de la nube para el e-learning (El Mhouti et al., 2017; Al-Samarraie y Saeed, 2018).
- Un trabajo colombiano relevante es el de **Ariza et al. (2021, *IEEE Access*)**: aprovisionar recursos de cómputo para plataformas e-learning en la nube con *deep learning*, es decir, predecir la demanda para dimensionar los servidores.
- Rendimiento y escalabilidad de Moodle: unos 110 artículos. Observabilidad, monitoreo o AIOps de plataformas educativas: unos 78 artículos, en su mayoría **no pertinentes** al revisar los más citados. **Es un vacío real.**

### 4.6 Gobierno y gestión de servicios de TI (E07, B08)

- Son 714 artículos en total y solo 7 revisiones. Destaca Liu, Huang y Lucas (2020, *Journal of Management Information Systems*), que encontraron que la **centralización de las decisiones de TI** en universidades de EE. UU. se asocia con menos brechas de ciberseguridad.
- **Colombia:** el marco de gobierno de *business intelligence* de la Universidad de la Costa (Combita-Niño et al., 2018) y el estudio sobre gobierno y desempeño de proyectos de TI (Vivas-Martín et al., 2023, *DYNA*).
- La aplicación de ITIL o COBIT a **plataformas de educación virtual** se reduce prácticamente a auditorías COBIT en Indonesia. Hay mucho espacio para aportar.

### 4.7 Ciberseguridad (E09, B07)

- Revisiones recientes: Afolalu y Tšoeu (2025) sobre la ciberseguridad en instituciones de educación superior, y Lallie et al. (2025) sobre los ataques al sector universitario.
- Para LMS en particular: la evaluación del riesgo de seguridad de la información en LMS con un sistema experto difuso (Abdymanapov et al., 2021).
- Colombia: un ataque de *phishing* controlado en una comunidad universitaria (Díaz Vivas et al., 2024).

### 4.8 Otros ejes de apoyo

- **Integridad académica y evaluación en línea** (E13): un tema enorme, hoy absorbido por la IA generativa.
- **Accesibilidad** (E14): Baldiris et al. (2022), con autores colombianos, evalúan herramientas de autor según ATAG y WCAG. Es un posible componente de cumplimiento normativo.
- **Interoperabilidad y datos** (E12): LTI, xAPI y BI. Es útil como componente técnico de las propuestas A y B.

---

## 5. Brechas: intersecciones temáticas

Conteos de artículos en revistas (OpenAlex). Los cinco documentos más citados de cada intersección están en `results/brechas_intersecciones.csv`.

| Id | Intersección | 2015-2026 | 2023-2026 | Lectura |
|---|---|---:|---:|---|
| B01 | IA generativa integrada en Moodle/LMS | 425 | 405 | Casi todo es de los últimos 3 años: **frente emergente** |
| B05 | LLM de código abierto o locales en universidades (soberanía de datos) | 129 | 129 | **Nicho emergente**, todo de 2023 en adelante |
| B06 | RAG / asistentes basados en recuperación para cursos | 443 | 443 | Emergente, con poca evaluación institucional |
| B17 | Políticas y gobernanza de la IA en universidades | 959 | 958 | En auge; falta ligarlo a la implementación técnica |
| B02 | Analítica o deserción con datos de Moodle | 255 | 140 | Consolidado internacionalmente |
| **B03** | **Analítica o deserción con datos de LMS, autores de Colombia** | **3** | **2** | **Vacío local muy claro** |
| B04 | Analítica o deserción en la educación superior, Colombia | 26 | 18 | Poco desarrollado |
| B16 | Moodle (cualquier tema), Colombia | 180 | 57 | La mayoría son estudios pedagógicos, no de gestión |
| B07 | Ciberseguridad de plataformas LMS/Moodle | 171 | 140 | Poco estudiado |
| B08 | Gobierno o gestión de servicios de TI aplicado al e-learning | 117* | 69* | *Sobreestimado: muy poco pertinente en realidad |
| B09 | Rendimiento y escalabilidad de Moodle | 110 | 62 | Muy poco estudiado |
| B10 | Observabilidad o AIOps de plataformas educativas | 78* | 59* | *Casi nada pertinente: **vacío** |
| B11 | TI verde o eficiencia energética de TI en universidades | 87* | 45* | *Ruidoso; muy poco pertinente |
| B12 | Chatbots de soporte o mesa de ayuda universitaria | 121 | 117 | Emergente |
| B14 | Transformación digital de universidades, Colombia | 57 | 44 | Moderado |
| B15 | IA generativa en la educación superior, Colombia | 82 | 82 | Moderado, casi todo sobre percepciones |

**Conclusión.** Hay mucha literatura sobre *qué opinan* estudiantes y docentes de la IA o del LMS, y muy poca sobre ***cómo una universidad pública latinoamericana diseña, opera, gobierna y evalúa*** esa tecnología en producción. Ese hueco, entre la infraestructura y la gestión, es justamente donde trabajas.

---

## 6. Propuestas de tema de tesis, alineadas con el CTEV

Criterios: (1) hay una brecha en la literatura; (2) se puede ejecutar con tu acceso y tus competencias (Rocky Linux, Moodle, PostgreSQL, SMTP, Windows Server); (3) tiene un componente de *gerencia* (modelo de gestión, gobierno, costos, indicadores) y no solo técnico; (4) aporta valor directo a la Universidad.

Metodología sugerida para todas: **Design Science Research (DSR)** (Hevner et al., 2004; Peffers et al., 2007). Consiste en identificar el problema, definir los objetivos, diseñar el artefacto, demostrarlo en un piloto y evaluarlo. Es el estándar en sistemas de información y encaja con una maestría de gerencia e innovación tecnológica, sea de profundización o de investigación.

### ⭐ Propuesta A (recomendada): IA generativa soberana integrada a Moodle

**Título tentativo:** *Modelo de gestión e implementación de un asistente de inteligencia artificial generativa soberano, integrado al LMS Moodle, para la educación virtual de la Universidad de Cartagena.*

- **Brecha:** B01 (425 artículos, el 95 % desde 2023), B05 (129) y B17 (959) existen por separado, pero casi nadie integra **infraestructura propia + LMS + gobernanza + evaluación** en una universidad pública latinoamericana. La producción colombiana sobre IA generativa (82 artículos) trata sobre todo de percepciones.
- **Innovación:** un LLM de código abierto (Llama, Qwen, Mistral u otros) servido en la infraestructura de la Universidad con Ollama o vLLM, conectado al **subsistema de IA de Moodle** (*provider*) o con un enfoque tipo LAMB, más **RAG** sobre los contenidos de los cursos. La soberanía de datos importa por la Ley 1581 de 2012 de protección de datos personales: los datos de estudiantes no salen a terceros.
- **Componente gerencial:** un análisis de costo total de propiedad (TCO) que compare una GPU on-premise con APIs comerciales; una política de uso aceptable; un modelo de gobernanza (roles, riesgos, privacidad, integridad académica); indicadores de servicio.
- **Evaluación:** UTAUT o TAM con docentes y estudiantes del piloto, ya que esa línea es madura y aporta instrumentos validados; métricas técnicas (latencia, concurrencia, consumo de recursos); calidad de las respuestas.
- **Riesgos:** requiere GPU o un servidor con buena RAM, o empezar con modelos pequeños cuantizados en CPU. Necesita aval institucional y de ética.

### Propuesta B: alerta temprana de la deserción con datos de Moodle

**Título tentativo:** *Sistema de alerta temprana de la deserción estudiantil basado en analítica del aprendizaje sobre los registros de Moodle, con intervenciones automatizadas, para los programas virtuales y a distancia de la Universidad de Cartagena.*

- **Brecha:** solo **3 artículos colombianos** en revistas sobre analítica o deserción con datos de LMS (B03), frente a 255 a nivel internacional con datos de Moodle (B02). El problema es nacional (SPADIES) y más grave en la educación a distancia.
- **Ejecución:** extraer los eventos de `mdl_logstore_standard_log`, las calificaciones y las finalizaciones desde PostgreSQL, anonimizados; construir indicadores semanales; entrenar modelos (regresión logística, *random forest*, *gradient boosting*) para predecir el riesgo desde las semanas 2-4; montar un tablero para tutores; enviar mensajes y *nudges* automáticos por SMTP o mensajería de Moodle.
- **Componente gerencial:** un protocolo de intervención (quién actúa, cuándo y cómo), la ética y la privacidad de la analítica, y un análisis costo-beneficio de la retención (ingresos por matrícula conservados).
- **Evaluación:** el desempeño predictivo (AUC, *recall* de estudiantes en riesgo) y, si es posible, un piloto con grupo de comparación sobre la permanencia.
- **Ventaja:** **ya tienes los datos y el acceso**. Es el tema con menor riesgo de ejecución.

### Propuesta C: gestión de servicios de TI y observabilidad de la plataforma

**Título tentativo:** *Modelo de gestión de servicios de TI basado en ITIL 4 y observabilidad para garantizar la disponibilidad y la calidad del servicio de la plataforma de educación virtual.*

- **Brecha:** E07 (714 artículos, 2 colombianos en OpenAlex) y B10 (casi nada pertinente). Es un vacío real entre la gestión de servicios y la operación de un LMS.
- **Ejecución:** definir el catálogo de servicios del CTEV, los SLA y SLO (disponibilidad, tiempo de respuesta en periodos de evaluación) y la gestión de incidentes y de capacidad; implementar la observabilidad (Prometheus, Grafana, Loki u otras) en Rocky Linux, PostgreSQL y Moodle; opcionalmente, detectar anomalías o predecir la demanda (en la línea de Ariza et al., 2021).
- **Componente gerencial:** muy fuerte (ITIL 4, COBIT 2019, indicadores, mejora continua). Es la propuesta más "de gerencia", aunque menos llamativa en innovación que A.

### Propuesta D (complementaria): ciberseguridad de la plataforma de educación virtual

*Evaluación de la madurez en ciberseguridad (NIST CSF 2.0, ISO/IEC 27001) de la plataforma Moodle y su ecosistema (SMTP, autenticación, PostgreSQL), y plan de tratamiento de riesgos.* Hay poca literatura específica (B07: 171) y gran relevancia práctica. Puede ser un capítulo de A o de C.

### Recomendación

| | A. IA soberana | B. Alerta temprana | C. ITSM y observabilidad |
|---|---|---|---|
| Novedad | Muy alta | Alta en Colombia | Media-alta |
| Brecha en la literatura | Emergente (2023+) | Vacío local claro | Vacío claro |
| Componente gerencial | Alto | Medio-alto | Muy alto |
| Riesgo de ejecución | Medio (hardware, aval) | Bajo | Bajo |
| Impacto institucional | Alto (visibilidad) | Muy alto (retención) | Alto (continuidad) |
| Potencial de publicación | Muy alto | Alto | Medio |

**Sugerencia:** **A como tema principal**, porque es el más innovador y el más publicable. **B es la alternativa segura.** Si buscas algo integrador, se pueden combinar en un "asistente de IA que también alerta a los tutores sobre estudiantes en riesgo", pero conviene acotar el alcance con tu director o directora de tesis.

---

## 7. Próximos pasos

1. **Confirmar las líneas de investigación y la modalidad** (profundización o investigación) de la maestría con la coordinación, ya que la página oficial no estaba disponible.
2. **Conversar con la dirección del CTEV** sobre la viabilidad: datos, aval y, en el caso de A, hardware.
3. **Convertir este mapeo en una revisión sistemática** del tema elegido: cribado PRISMA 2020 de título y resumen sobre la consulta del eje o la intersección correspondiente; exportar a Scopus o Web of Science con la misma cadena `TITLE-ABS-KEY`; analizar en VOSviewer o Bibliometrix. Para la propuesta A, el corpus inicial serían B01 + B05 + B06 + B17 (unos 1.900 artículos antes de deduplicar). Para la B, E04 + B02 (unos 1.200).
4. **Leer primero:** Castro Benavides et al. (2020); Zawacki-Richter et al. (2019); Chan (2023); Alier et al. (2024, LAMB); McDonald et al. (2025); Conijn et al. (2016); Ifenthaler y Yau (2020); Liu, Huang y Lucas (2020).
5. **Ética y datos:** cualquier uso de registros de estudiantes requiere anonimización, aval del comité de ética y ajuste a la Ley 1581 de 2012.

---

## 8. Archivos y reproducibilidad

```
ti_educacion/
├── informe_busqueda_TI_educacion_superior.md   (este informe)
├── src/buscar_openalex.py      15 ejes: conteos, precisión, Scopus, Colombia/LATAM, fuentes, documentos clave
├── src/brechas.py              16 intersecciones temáticas (brechas)
├── src/referencias.py          Referencias desde OpenAlex para la lista curada de DOI
└── results/
    ├── resumen_ejes.csv            Tabla de la sección 3, con las cadenas de búsqueda
    ├── produccion_anual.csv        Producción anual por eje
    ├── fuentes_principales.csv     Top 10 revistas por eje
    ├── documentos_clave.csv        Más citados, revisiones 2023-26, recientes y colombianos por eje
    ├── brechas_intersecciones.csv  Tabla de la sección 5 y top 5 citados
    ├── referencias_seleccionadas.md
    └── registro_busqueda.json      Fecha y filtros comunes
```

Para reproducirlo (desde la raíz del repositorio):

```bash
export OPENALEX_API_KEY=su_clave SCOPUS_API_KEY=su_clave_elsevier
python3 ti_educacion/src/buscar_openalex.py
python3 ti_educacion/src/brechas.py
python3 ti_educacion/src/referencias.py
```

Fuentes web de contexto consultadas: documentación del subsistema de IA de Moodle (<https://docs.moodle.org/500/en/AI_subsystem>; <https://docs.moodle.org/500/en/User:Eloy_Lafuente_(stronk7)/Using_OpenAI_API-compatible_providers>) y cifras de SPADIES reportadas por Bancolombia (<https://www.bancolombia.com/empresas/capital-inteligente/actualidad-economica-sectorial/impacto-desercion-universitaria-colombia>) y el MEN (<https://www.mineducacion.gov.co/sistemasdeinformacion/1735/article-212299.html>).

Referencias metodológicas citadas fuera del corpus: Hevner, A. R., March, S. T., Park, J., & Ram, S. (2004). Design science in information systems research. *MIS Quarterly, 28*(1), 75-105. Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S. (2007). A design science research methodology for information systems research. *Journal of Management Information Systems, 24*(3), 45-77. https://doi.org/10.2753/MIS0742-1222240302
