"""Genera Review_V02.docx a partir de Review_V01.docx.

- Correcciones menores (ortotipografía, tildes, sintaxis, nomenclatura): se aplican directamente.
- Propuestas de cambio mayor: se insertan resaltadas en amarillo y con comentario,
  pendientes de aprobación del autor.
"""
import re
import sys
from copy import deepcopy

import docx
from docx.enum.text import WD_COLOR_INDEX
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph
from docx.text.run import Run

SRC, DST = sys.argv[1], sys.argv[2]
d = docx.Document(SRC)
P = list(d.paragraphs)  # índices del original
AUTHOR, INI = "Claude (revisión)", "CL"
PENDING = []  # (runs, comentario)


def base_rpr(p, strip=True):
    for r in p._p.findall(qn("w:r")):
        if "".join(t.text or "" for t in r.findall(qn("w:t"))).strip():
            rpr = r.find(qn("w:rPr"))
            rpr = deepcopy(rpr) if rpr is not None else None
            if rpr is not None and strip:
                for tag in ("w:b", "w:bCs", "w:i", "w:iCs", "w:highlight"):
                    for e in rpr.findall(qn(tag)):
                        rpr.remove(e)
            return rpr
    return None


def set_text(p, md, strip=True, comment=None):
    """Reescribe el párrafo. Marcas: **negrita**, *cursiva*, ==propuesta==."""
    rpr = base_rpr(p, strip)
    for child in list(p._p):
        if child.tag != qn("w:pPr"):
            p._p.remove(child)
    bold = ital = hl = False
    hl_runs = []
    for tok in re.split(r"(\*\*|\*|==)", md):
        if tok == "**":
            bold = not bold
        elif tok == "*":
            ital = not ital
        elif tok == "==":
            hl = not hl
        elif tok:
            r = p.add_run(tok)
            if rpr is not None:
                r._r.insert(0, deepcopy(rpr))
            if bold:
                r.bold = True
            if ital:
                r.italic = True
            if hl:
                r.font.highlight_color = WD_COLOR_INDEX.YELLOW
                hl_runs.append(r)
    if comment and hl_runs:
        PENDING.append((hl_runs, comment))
    return p


def insert_after(ref, model, md, strip=True, comment=None):
    new = deepcopy(model._p)
    ref._p.addnext(new)
    para = Paragraph(new, ref._parent)
    return set_text(para, md, strip, comment)


SCI = re.compile(
    r"\b(Dioscorea(?: (?:zingiberensis|alata|rotundata|bulbifera|nipponica|esculenta|opposita|polystachya|cayenensis|batatas))?"
    r"|D\. (?:alata|rotundata|zingiberensis)|Ipomoea batatas|Mangifera indica|Xanthosoma sagittifolium"
    r"|Saccharomyces cerevisiae|Colletotrichum|Pachyrhizus|Manihot esculenta)\b"
)


def italicize(p, rx=SCI):
    for r in list(p.runs):
        if r.italic or not rx.search(r.text):
            continue
        t, pos, segs = r.text, 0, []
        for m in rx.finditer(t):
            segs += [(t[pos:m.start()], False), (m.group(0), True)]
            pos = m.end()
        segs.append((t[pos:], False))
        for s, it in segs:
            if not s:
                continue
            nr = deepcopy(r._r)
            r._r.addprevious(nr)
            run = Run(nr, p)
            run.text = s
            if it:
                run.italic = True
        r._r.getparent().remove(r._r)


def normalize_spaces(p):
    runs = [r for r in p.runs if r.text]
    for r in runs:
        t = re.sub(r"[ \t]{2,}", " ", r.text)
        t = re.sub(r" +([.,;:)])", r"\1", t)
        t = t.replace("( ", "(")
        if t != r.text:
            r.text = t
    for a, b in zip(runs, runs[1:]):
        if a.text.endswith(" ") and b.text.startswith(" "):
            b.text = b.text.lstrip(" ")
    if runs and p._p.find(qn("w:hyperlink")) is None:
        runs[0].text = runs[0].text.lstrip(" ")
        runs[-1].text = runs[-1].text.rstrip(" ")


# ---------------------------------------------------------------- Título y resumen
set_text(P[0], "Evaluación de sostenibilidad de biorrefinerías basadas en raíces y tubérculos: revisión bibliométrica "
         "con énfasis en ñame (*Dioscorea rotundata*) y batata (*Ipomoea batatas*)", strip=False)

set_text(P[4], "Mediante una revisión bibliométrica se encontró que ninguno de los 19.164 documentos analizados evalúa una "
         "biorrefinería de ñame (*Dioscorea rotundata*) o batata (*Ipomoea batatas*) con análisis de ciclo de vida (ACV), "
         "evaluación tecno-económica (TEA) y análisis de ciclo de vida social (ACV-S) de forma simultánea; para la yuca solo "
         "existen evaluaciones de las tres dimensiones en cadenas de un único producto. Se estudió la literatura de 2000 a 2026, "
         "recuperada mediante las API de OpenAlex y Scopus con 14 consultas organizadas en seis niveles, desde la sostenibilidad "
         "de biorrefinerías a escala global hasta el ñame y la batata en Colombia. De 34.616 registros, 19.164 se conservaron "
         "tras la deduplicación y el cribado (PRISMA 2020). La evaluación de biorrefinerías creció a una tasa del 29,2 % anual "
         "y se apoya en el ACV y el TEA; la dimensión social reúne 159 documentos, casi todos europeos y centrados en madera, "
         "biodiésel o bioplásticos. Para el ñame se identificaron 7 estudios de ACV, 20 de TEA y ninguno de ACV-S. Colombia es "
         "el noveno país del campo y aporta su autor más productivo, pero su investigación sobre el ñame no se vincula con la "
         "de biorrefinerías. Estos resultados evidencian un vacío de investigación que justifica la evaluación integrada propuesta.")

set_text(P[5], "Palabras clave: biorrefinería; análisis de ciclo de vida; evaluación tecno-económica; análisis de ciclo de vida "
         "social; ñame; batata; bibliometría; Scopus; OpenAlex.")

# ---------------------------------------------------------------- Introducción
set_text(P[7], "El ñame (*Dioscorea rotundata*) sostiene buena parte de la economía campesina del Caribe colombiano "
         "(Reina-Aranza, 2012). En Montes de María, un territorio de posconflicto incluido en los Programas de Desarrollo con "
         "Enfoque Territorial (PDET), la cadena del ñame depende de un grado de exportación que no tiene sustituto local "
         "(Granados Conde et al., 2026). Por ello, una biorrefinería en este territorio no es solo un problema de balances de "
         "masa, sino también de ingresos, empleo y alimentación; en consecuencia, el pilar social no es un accesorio del diseño.")

set_text(P[8], "El concepto de biorrefinería tiene más de quince años de uso estable (Cherubini, 2010), y en Colombia existe una "
         "escuela reconocida de diseño de biorrefinerías sostenibles (Moncada B. et al., 2016). Sin embargo, no se identificó "
         "un puente entre esa escuela, el ñame y la dimensión social.")

set_text(P[9], "La bioeconomía exige sustituir las fuentes de energía derivadas de materias primas fósiles por biomasa para la "
         "producción de energía, materiales y productos químicos. En este contexto cobra relevancia la biorrefinería, entendida "
         "como el procesamiento sostenible de la biomasa en un espectro de productos comercializables y energía (Cherubini, 2010), "
         "concepto que se ha consolidado como el marco tecnológico de esa transición. No obstante, la viabilidad de una "
         "biorrefinería no depende únicamente de su desempeño técnico: debe demostrar simultáneamente su rentabilidad, una menor "
         "carga ambiental que la del sistema de referencia y beneficios para los actores de la cadena de valor "
         "(Moncada B. et al., 2016).")

# Regla 5: cierre de la introducción (problema -> objetivo de la revisión)
insert_after(P[10], P[10],
             "Pese a la disponibilidad de estas herramientas, se desconoce en qué medida se han aplicado de forma integrada a "
             "cultivos como el ñame (*D. rotundata*) y la batata (*Ipomoea batatas*). Este vacío tiene consecuencias concretas "
             "en Montes de María: si la cadena del ñame es estructuralmente frágil y de ella depende el ingreso campesino, una "
             "biorrefinería que no demuestre al mismo tiempo su viabilidad técnica, económica, ambiental y social no ofrece una "
             "alternativa real para el territorio. En consecuencia, el objetivo de esta revisión bibliométrica es caracterizar la "
             "producción científica sobre la evaluación de sostenibilidad (ACV, TEA y ACV-S) de biorrefinerías, desde el nivel "
             "global hasta las rutas de transformación del ñame y la batata en Colombia, con el fin de identificar los vacíos que "
             "debe cubrir una evaluación integrada de la biorrefinería propuesta para Montes de María.")

# ---------------------------------------------------------------- Metodología
set_text(P[13], "El análisis bibliométrico se realizó con dos componentes: análisis de desempeño y mapeo científico "
         "(Donthu et al., 2021). El proceso de identificación, ==cribado== y elegibilidad se reporta con el diagrama de flujo "
         "de PRISMA 2020 (Page et al., 2021). El procedimiento se ejecutó mediante un flujo de trabajo (*pipeline*) de código "
         "abierto en lenguaje Python, alojado en un repositorio de GitHub. Este repositorio contiene las cadenas de búsqueda, "
         "los datos crudos descargados, el registro de cada consulta (fecha, número de resultados y versión del código), los "
         "registros excluidos, los resultados intermedios y la bitácora de decisiones metodológicas, lo que garantiza el "
         "respaldo de las cifras y los resultados presentados en el artículo.",
         comment="PROPUESTA (pendiente de aprobación): el original dice «identificación, normalización y elegibilidad». "
                 "En PRISMA 2020 la etapa se denomina «cribado» (screening); «normalización» no es una etapa del diagrama. "
                 "Si no se aprueba, se restituye «normalización».")

set_text(P[15], "La recolección de los documentos se realizó mediante API REST. Como fuente principal se utilizó OpenAlex, una "
         "base bibliográfica abierta que integra metadatos de Crossref, PubMed, ORCID, repositorios y editoriales, cuya "
         "cobertura de referencias es comparable a la de Scopus y Web of Science (Culbert et al., 2025) y cuyos datos se "
         "distribuyen con licencia CC0. Scopus se empleó como fuente de validación y complemento, con la misma metodología de "
         "consumo de API.")

set_text(P[18], "La estrategia se organizó en seis niveles anidados (Tabla 1). El nivel N4 se descompuso en siete subconsultas: "
         "las cuatro rutas fijas de la biorrefinería, los metabolitos candidatos de cada cultivo y la valorización integral.")

set_text(P[20], "Los registros de ambas bases se fusionaron y se deduplicaron, primero por DOI y luego por título normalizado "
         "más año. Se excluyeron los documentos sin título, los retractados y los que estaban fuera del periodo o del tipo "
         "documental definido, así como los registros de Scopus que no pudieron enlazarse con metadatos completos.")

set_text(P[21], "Los falsos positivos se controlaron con una verificación léxica automatizada sobre el título, el resumen y las "
         "palabras clave. Por ejemplo, se eliminaron los registros de *yam bean* (*Pachyrhizus*), los de N1 sin mención a "
         "biorrefinerías y los de N6 sin vínculo explícito con Colombia. Cuando OpenAlex no distribuía el resumen de un registro "
         "(como ocurre con parte de los resúmenes de Elsevier), su coincidencia temática se dio por confirmada si Scopus lo "
         "había recuperado con la misma consulta TITLE-ABS-KEY.")

# Propuesta B: subsección «Análisis»
h_an = insert_after(P[21], P[17], "==Análisis==", strip=False,
                    comment="PROPUESTA B (pendiente de aprobación): nueva subsección de Metodología. Los Resultados usan la "
                            "TCAC, las leyes de Lotka y Bradford, los clústeres C1-C4 y los cuadrantes del mapa temático sin "
                            "que el método esté descrito. Además, cita referencias que hoy están en la lista pero no en el "
                            "texto (Bradford, Lotka, Pao, Blondel, Callon, Cobo, van Eck y Waltman, Aria y Cuccurullo).")
insert_after(h_an, P[21],
             "==El análisis de desempeño incluyó la producción anual, la tasa de crecimiento anual compuesta (TCAC) hasta 2025, "
             "las citas por documento, el índice *h* y la colaboración internacional. La concentración de las fuentes se evaluó "
             "con la ley de Bradford (Bradford, 1934), y la productividad de los autores, con la ley de Lotka, contrastada con la "
             "prueba de Kolmogorov-Smirnov (α = 0,01; Lotka, 1926; Pao, 1985). El mapeo científico se basó en redes de "
             "co-ocurrencia de palabras clave normalizadas con un tesauro, ponderadas por la fuerza de asociación (van Eck y "
             "Waltman, 2009) y agrupadas con el algoritmo de Louvain (Blondel et al., 2008). Cada grupo temático o clúster "
             "resultante se identifica como C1, C2, C3…, numerados de mayor a menor tamaño dentro de cada nivel. Los clústeres se "
             "ubicaron en mapas de centralidad y densidad (Callon et al., 1991; Cobo et al., 2011) como temas motores, básicos, "
             "de nicho o emergentes. Por último, el corpus de N3 a N5 se clasificó con diccionarios controlados por cultivo, ruta "
             "de transformación y método de evaluación para construir las matrices de brechas, y se calculó un índice de "
             "priorización de metabolitos por cultivo. Las redes pueden verificarse en VOSviewer (van Eck y Waltman, 2010) o en "
             "biblioshiny (Aria y Cuccurullo, 2017).==")

# ---------------------------------------------------------------- Resultados
set_text(P[25], "La comparación de bases justifica el uso combinado. Entre el 91,4 % y el 99,3 % de los DOI recuperados por "
         "Scopus existen en el índice de OpenAlex. Sin embargo, la búsqueda en OpenAlex solo recuperó directamente entre el "
         "58,7 % y el 80,0 % de ellos, porque no puede buscar en los resúmenes que no distribuye. A la inversa, OpenAlex aportó "
         "registros ausentes en Scopus: ==por ejemplo, 1.578 en N3 y 1.327 en N4f, en su mayoría de revistas regionales y de "
         "acceso abierto. La Tabla 2 resume los indicadores de desempeño por nivel.==",
         comment="PROPUESTA C (pendiente de aprobación): el párrafo original termina en «…registros ausentes en Scopus:» "
                 "sin completar. Cifras tomadas de results/tables/coverage_openalex_scopus.csv (columna only_openalex).")

set_text(P[37], "")

set_text(P[40], "En la red de co-ocurrencia de N1 (Figura 3) se identifican tres clústeres: el tema central, formado por el ACV, "
         "los biocombustibles y la economía circular (C1); el tema básico o transversal, centrado en el TEA de biomasa "
         "lignocelulósica para bioetanol (C2), y la factibilidad económica de la digestión anaerobia y las microalgas (C3).")

# Propuesta G: subsección N2 (dimensión social)
h_n2 = insert_after(P[41], P[35], "==Integración de la dimensión social (ACV-S y LCSA)==", strip=False,
                    comment="PROPUESTA G (pendiente de aprobación): la Tabla 2 y el Resumen reportan N2 (159 documentos), "
                            "pero los Resultados no tienen una subsección para este nivel, que es el que sustenta el eje "
                            "social del artículo. Además, recupera citas de 11 referencias que están en la lista y no en el "
                            "texto (Spierling, Benoit-Norris, Siebert, Macombe, Manik, Sala, Kühnen, Lehmann, Ramos Huarachi, "
                            "Huertas-Valdivia, Sadhukhan). Fuente: results/tables/N2_*.csv.")
n2a = insert_after(h_n2, P[41],
                   "==La integración del ACV-S y del marco LCSA en sistemas de base biológica es reciente (desde 2011) y "
                   "reducida: 159 documentos, frente a 2.978 en N1. Su crecimiento es alto (TCAC del 23,4 %) y la producción "
                   "es predominantemente europea: Alemania (26 documentos), España (21) e Italia (19). Las fuentes núcleo son "
                   "*The International Journal of Life Cycle Assessment* (21), *Journal of Cleaner Production* (16) y "
                   "*Sustainability* (12).==")
n2b = insert_after(n2a, P[41],
                   "==El documento más citado revisa las evaluaciones ambientales, sociales y económicas de los bioplásticos "
                   "(Spierling et al., 2018). La base intelectual descansa en la Social Hotspot Database (Benoit-Norris et al., "
                   "2012), en índices de ACV-S para productos de madera (Siebert et al., 2018), en el ACV-S de biodiésel "
                   "(Macombe et al., 2013; Manik et al., 2013) y en revisiones de indicadores y marcos (Sala et al., 2013; "
                   "Lehmann et al., 2013; Kühnen y Hahn, 2017; Ramos Huarachi et al., 2020; Huertas-Valdivia et al., 2020). La "
                   "aplicación conjunta de LCSA en biorrefinerías se documenta en casos aislados, como el de las macroalgas "
                   "(Sadhukhan et al., 2019).==")
insert_after(n2b, P[41],
             "==El mapa temático ubica como temas motores el LCSA con toma de decisiones multicriterio y el ACV con costeo del "
             "ciclo de vida. El ACV-S y la sostenibilidad social funcionan como tema básico; la biorrefinería y la bioeconomía "
             "circular aparecen como nicho, y la creación de empleo y la salud y seguridad en la producción de bioetanol, como "
             "tema emergente.==")

set_text(P[42], "Raíces y tubérculos como materia prima", strip=False)

set_text(P[43], "En este nivel, la literatura se agrupa principalmente en la producción de bioetanol con *Saccharomyces "
         "cerevisiae* a partir de residuos agrícolas (C1), seguida de la digestión anaerobia y el biogás de cáscaras de yuca y "
         "papa (C2) y, por último, de los biofertilizantes en el cultivo de papa (C3). Como tema emergente o en declive figura "
         "el bioetanol de yuca y batata (*Ipomoea batatas*) con ACV y gases de efecto invernadero, clúster en el que aparece "
         "el ñame (C4). Los trabajos comparativos sitúan a la yuca y la batata entre las fuentes de carbohidratos más "
         "productivas para bioetanol (Ziska et al., 2009; Thatoi et al., 2016).")

set_text(P[48], "La Tabla 3 cruza cultivos y rutas en el corpus de N3 a N5. La yuca es el cultivo con el perfil de rutas más "
         "equilibrado (1.102 documentos de almidón, 1.022 de bioetanol y 479 de biogás). El ñame y la batata, en cambio, "
         "concentran su literatura en el almidón (1.344 y 2.346 documentos) y en los metabolitos o bioactivos (2.246 y 3.665). "
         "Las rutas energéticas están poco exploradas: el ñame registra 71 documentos de bioetanol y 43 de biogás; "
         "*I. batatas*, 254 y 52.")

set_text(P[51], "Productos de valor agregado del ñame y la batata", strip=False)

set_text(P[55], "**Almidón nativo.** La literatura caracteriza las propiedades fisicoquímicas y funcionales de los almidones de "
         "tubérculos tropicales (Moorthy, 2002) y sus aplicaciones en películas biodegradables (Mali et al., 2002) y en "
         "empaques inteligentes con antocianinas de batata morada (Choi et al., 2017). Para *D. rotundata* cultivada en "
         "Colombia ya existen caracterizaciones de almidones nativos y modificados (Rodríguez‐Manrique et al., 2025). Estos "
         "datos son directamente útiles para el inventario del TEA.")
set_text(P[56], "**Bioetanol.** Predominan los estudios de hidrólisis y fermentación de batata (Lareo et al., 2013). Para el "
         "ñame, la evidencia es escasa y procede, sobre todo, de África occidental y de residuos del procesamiento farmacéutico "
         "de *Dioscorea*.")
set_text(P[57], "**Biogás.** Hay estudios de codigestión de batata con estiércol, con evaluación técnico-económica (Montoro et "
         "al., 2019), de digestión de ramas de batata (Zhang et al., 2018) y de pretratamiento de cáscara de ñame (Onu et al., "
         "2022). También se ha tratado por vía anaerobia el efluente de la extracción de diosgenina (Cheng et al., 2009).")

set_text(P[60], "En la red de co-ocurrencia de este nivel destacan tres clústeres: la batata, las antocianinas y las variedades "
         "de pulpa morada o naranja (C1); la actividad antioxidante, los flavonoides, el ñame y la diosgenina (C2), y el "
         "almidón de batata y de *D. alata* con sus propiedades funcionales (C3).")
set_text(P[62], "La priorización de metabolitos arroja resultados distintos para cada cultivo (Tabla 4; Figura 6).")
set_text(P[63], "**Batata (*I. batatas*).** Los compuestos fenólicos (1.368 documentos; 477 vinculados a residuos), los "
         "flavonoides (760) y las antocianinas (1.613 documentos; 601 con procesos de extracción o recuperación) obtienen los "
         "índices de priorización más altos. Les siguen los carotenoides (1.347) y el ácido clorogénico, este último con el "
         "mayor impacto por documento (34,5 citas) y un 47 % de trabajos basados en hojas, cáscaras u otros residuos.")
set_text(P[64], "**Ñame (*Dioscorea* spp.).** Los flavonoides (índice 0,806), las saponinas esteroidales (0,758), los "
         "compuestos fenólicos (0,749) y la diosgenina (0,689) encabezan la priorización. Sin embargo, la evidencia específica "
         "en *D. rotundata* es muy distinta según el compuesto: 52 documentos para compuestos fenólicos, 27 para saponinas, 23 "
         "para flavonoides y solo 5 para diosgenina. La diosgenina procede sobre todo de especies medicinales como "
         "*D. zingiberensis*, *D. bulbifera* y *D. nipponica* (Zhu et al., 2010; Obidiegwu et al., 2020).")
set_text(P[65], "**Tabla 4.** Metabolitos con mayor índice de priorización por cultivo.")

set_text(P[68], "Evaluaciones de sostenibilidad del ñame y la batata", strip=False)
set_text(P[69], "==N5 reúne 820 documentos, con un perfil de impacto bajo (12,4 citas por documento), liderado por Nigeria "
         "(137 documentos), India (62) e Indonesia (57). Su mapa temático muestra que la sostenibilidad del ñame y la batata "
         "se ha abordado sobre todo desde ==la economía agrícola. Son temas motores la rentabilidad de pequeños productores, "
         "los márgenes brutos y la seguridad alimentaria; el análisis beneficio-costo de sistemas de cultivo es transversal, y "
         "la factibilidad económica con valor presente neto es un nicho asociado a Nigeria.",
         comment="PROPUESTA D (pendiente de aprobación): el párrafo original empieza en minúscula («la economía agrícola…»), "
                 "señal de que se perdió el inicio. Cifras tomadas de results/tables/summary_by_level.csv y "
                 "N5_top_countries.csv.")

set_text(P[79], "El trabajo más cercano a la biorrefinería propuesta compara la producción de bioetanol a partir de caña, yuca "
         "y ñame en Colombia mediante simulación en Aspen Plus (Villadiego-del Villar et al., 2026). El ñame alcanzó un costo de "
         "producción de 1,11 USD/L, frente a 2,28 USD/L de la yuca y 0,68 USD/L de la caña. También mostró el mayor potencial "
         "de cogeneración eléctrica (171.330 kWh), pero su valor presente neto fue negativo en el escenario de producto único.")
set_text(P[80], "El mapa temático revela una desconexión (Figura 8). Los temas de biorrefinería, TEA y ACV forman un grupo "
         "motor, y la digestión anaerobia de residuos agroindustriales, un grupo básico. En cambio, la investigación colombiana "
         "sobre el ñame (*D. rotundata*, *D. alata*, Montes de María, diversidad genética, antracnosis por *Colletotrichum*, "
         "seguridad alimentaria) forma un nicho de alta densidad interna y baja centralidad: es un tema bien desarrollado, pero "
         "aislado de los temas de biorrefinería.")
set_text(P[81], "Los estudios recientes del Caribe abordan la cadena del ñame desde la fragilidad estructural (Granados Conde et "
         "al., 2026), la optimización logística con pérdidas superiores al 30 % en Sucre (Vergara Rodríguez et al., 2025) y la "
         "transformación agroindustrial a escala rural (Martín et al., 2026; Paternina et al., 2026). En la batata "
         "(*I. batatas*), los trabajos colombianos se orientan a la conservación de germoplasma (Rosero et al., 2022) y a la "
         "bioprospección de metabolitos de variedades nativas (Chávez et al., 2026).")

set_text(P[85], "==Limitaciones==", strip=False,
         comment="PROPUESTA E (pendiente de aprobación): el título original es «Vacíos de investigación», pero los dos "
                 "párrafos describen limitaciones del estudio (alcance de la búsqueda, vista restringida de Scopus, ruido de "
                 "la clasificación, literatura gris). Los vacíos de investigación ya se exponen en Resultados y Conclusiones.")
set_text(P[86], "En primer lugar, la búsqueda restringida a títulos y resúmenes no recupera los documentos que abordan el tema "
         "exclusivamente en el texto completo; además, una fracción de los resúmenes no está disponible en OpenAlex. Aunque esta "
         "restricción se mitigó mediante la fusión con Scopus, que permitió enlazar entre el 91,4 % y el 99,3 % de sus DOI, el "
         "sesgo no se elimina por completo.")
set_text(P[87], "A este factor se suma que el uso de la API de Scopus en su vista restringida impidió que 1.082 registros no "
         "enlazables aportaran información clave sobre autores y afiliaciones. Asimismo, la clasificación automatizada mediante "
         "diccionarios y palabras clave de OpenAlex introdujo un margen de ruido que, con el fin de preservar la "
         "reproducibilidad del estudio, no se depuró manualmente; no obstante, dichos registros se descartaron en la "
         "interpretación cualitativa posterior. Finalmente, el alcance del análisis bibliométrico se limitó a la literatura "
         "indexada, lo que implicó excluir la literatura gris, es decir, los informes institucionales de entidades como "
         "AGROSAVIA, el MADR y el ICA, así como las tesis de grado.")

# ---------------------------------------------------------------- Conclusiones
set_text(P[89], "La evaluación de la sostenibilidad de biorrefinerías crece a una tasa anual compuesta del 29,2 %, sustentada "
         "en el ACV y el TEA de biomasa lignocelulósica con enfoque de bioeconomía circular; en este campo global, Colombia "
         "ocupa el noveno lugar y aporta el autor más productivo. Sin embargo, la dimensión social sigue siendo el pilar menos "
         "desarrollado (solo 159 documentos sobre ACV-S o LCSA) y se concentra en Europa. Esta brecha se profundiza en las "
         "raíces y tubérculos: mientras la yuca concentra las rutas energéticas, la literatura sobre el ñame y la batata "
         "(*Ipomoea batatas*) se limita al almidón y a los compuestos bioactivos, con escasos estudios de ACV y TEA y una "
         "ausencia total de ACV-S. De hecho, en la literatura indexada no existe ninguna evaluación que integre "
         "simultáneamente ACV, TEA y ACV-S para biorrefinerías de tubérculos. En el contexto nacional, la investigación en "
         "biorrefinerías y el estudio del ñame han operado históricamente como comunidades desconectadas. Integrar ambos "
         "componentes en un caso territorial aplicado a los Montes de María no solo articula estos campos académicos, sino "
         "que otorga al proyecto una alta novedad científica y una profunda pertinencia social.")

# ---------------------------------------------------------------- Referencias (correcciones puntuales)
for p in P[92:]:
    for r in p.runs:
        t = r.text
        t = t.replace("CHÁVEZ, J. A. S., MARTÍNEZ, Ó. M. M., & ARISTIZÁBAL, L. S. R.",
                      "Chávez, J. A. S., Martínez, Ó. M. M., & Aristizábal, L. S. R.")
        t = t.replace("Chains:Overview", "Chains: Overview")
        if t != r.text:
            r.text = t

# ---------------------------------------------------------------- Pasadas globales
allp = list(d.paragraphs)
for t in d.tables:
    for row in t.rows:
        for c in row.cells:
            allp += c.paragraphs
for p in allp:
    italicize(p)
    normalize_spaces(p)

for runs, text in PENDING:
    d.add_comment(runs, text=text, author=AUTHOR, initials=INI)

d.save(DST)
print("ok", DST, "propuestas:", len(PENDING))
