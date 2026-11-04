"""Agrega a Review_V02 los elementos que faltan para un estándar Q1 (todo resaltado en amarillo):
preguntas de investigación, sección de Discusión, limitaciones adicionales, agenda de investigación
y cierre de conclusiones sobre metabolitos. Todas las cifras provienen de results/tables/ y las citas,
de la lista de referencias del propio manuscrito.
"""
import re
import sys
from copy import deepcopy

import docx
from docx.enum.text import WD_COLOR_INDEX
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

SRC, DST = sys.argv[1], sys.argv[2]
d = docx.Document(SRC)
AUTHOR, INI = "Claude (revisión)", "CL"
PENDING = []


def find(start):
    for p in d.paragraphs:
        if p.text.strip().startswith(start):
            return p
    raise SystemExit(f"no encontrado: {start}")


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


def set_text(p, md, model_rpr):
    for child in list(p._p):
        if child.tag != qn("w:pPr"):
            p._p.remove(child)
    bold = ital = False
    runs = []
    for tok in re.split(r"(\*\*|\*)", md):
        if tok == "**":
            bold = not bold
        elif tok == "*":
            ital = not ital
        elif tok:
            r = p.add_run(tok)
            if model_rpr is not None:
                r._r.insert(0, deepcopy(model_rpr))
            if bold:
                r.bold = True
            if ital:
                r.italic = True
            r.font.highlight_color = WD_COLOR_INDEX.YELLOW
            runs.append(r)
    return runs


def add_after(ref, model, md, strip=True, comment=None):
    new = deepcopy(model._p)
    ref._p.addnext(new)
    para = Paragraph(new, ref._parent)
    runs = set_text(para, md, base_rpr(model, strip))
    if comment:
        PENDING.append((runs, comment))
    return para


def add_block(ref, model, items, comment=None):
    """Inserta varios párrafos seguidos; el comentario se ancla al primero."""
    last = ref
    for k, md in enumerate(items):
        last = add_after(last, model, md, comment=comment if k == 0 else None)
    return last


BODY = find("Para responder a esa exigencia")          # párrafo normal de la introducción
H1 = find("Resultados")                                 # formato de encabezado de sección
H2 = find("Sostenibilidad de biorrefinerías")           # formato de subencabezado (negrita)

# ---------------------------------------------------------------- 1. Preguntas de investigación
cierre = find("Pese a la disponibilidad de estas herramientas")
add_block(cierre, BODY, [
    "Para cumplir este objetivo, la revisión recorre el campo de lo general a lo específico y responde seis "
    "preguntas de investigación (PI):",
    "**PI1.** ¿Cómo ha evolucionado la producción científica sobre la evaluación de sostenibilidad de biorrefinerías "
    "y quiénes son sus actores principales?",
    "**PI2.** ¿Qué grado de madurez tiene la integración del ACV-S con el ACV y el TEA?",
    "**PI3.** ¿Qué rutas de valorización se han estudiado para raíces y tubérculos y cómo se posicionan el ñame y la "
    "batata?",
    "**PI4.** ¿Cuál es el estado de las rutas fijas (almidón nativo, bioetanol, biogás y biofertilizante) para el ñame "
    "y la batata, y qué metabolitos son candidatos a completar el portafolio de productos?",
    "**PI5.** ¿Existen evaluaciones de sostenibilidad de sistemas de ñame y batata y qué brechas presentan?",
    "**PI6.** ¿Cuál es la producción científica asociada a Colombia y a la región Caribe?",
], comment="AGREGADO Q1 (pendiente de aprobación): preguntas de investigación explícitas. Son las mismas del "
           "protocolo registrado en el repositorio (protocolo/protocolo_revision.md, §1); la Discusión las responde "
           "una a una.")

est = find("La estrategia se organizó en seis niveles")
add_after(est, BODY, "Cada nivel responde a una pregunta de investigación: N1 a PI1, N2 a PI2, N3 a PI3, N4 a PI4, "
          "N5 a PI5 y N6 a PI6.",
          comment="AGREGADO Q1: vincula cada nivel de búsqueda con su pregunta de investigación.")

# ---------------------------------------------------------------- 2. Discusión
lim = find("Limitaciones")
fig8 = lim._p.getprevious()
anchor = Paragraph(fig8, lim._parent)

discusion = [
    ("H1", "Discusión"),
    ("H2", "Madurez desigual de los tres pilares de sostenibilidad (PI1 y PI2)"),
    ("P", "La evaluación de sostenibilidad de biorrefinerías es un campo maduro y en expansión acelerada, con un núcleo "
          "de revistas de ingeniería y un corpus metodológico consolidado: diseño de procesos al estilo del NREL "
          "(Humbird et al., 2011), la base de datos ecoinvent (Wernet et al., 2016) y el método ReCiPe (Huijbregts et "
          "al., 2017). Ese desarrollo, sin embargo, es asimétrico. El TEA y el ACV dominan y crecen, mientras que la "
          "dimensión social apenas reúne 159 documentos en todo el espectro de sistemas de base biológica, "
          "concentrados en Europa y aplicados sobre todo a madera, biodiésel y bioplásticos."),
    ("P", "Este resultado coincide con las revisiones previas del ACV-S, que describen un campo en consolidación, con "
          "predominio de marcos e indicadores sobre aplicaciones empíricas y con sus fuentes principales en *The "
          "International Journal of Life Cycle Assessment* y *Journal of Cleaner Production* (Kühnen y Hahn, 2017; "
          "Huertas-Valdivia et al., 2020; Ramos Huarachi et al., 2020). El aporte de esta revisión es mostrar que esa "
          "inmadurez se agudiza a medida que el análisis desciende de los sistemas de base biológica en general a las "
          "raíces y tubérculos, donde el ACV-S es prácticamente inexistente. Los pocos casos tropicales, como el "
          "biodiésel de palma (Manik et al., 2013), muestran además que las categorías de impacto social dependen del "
          "contexto, por lo que la evaluación social de una biorrefinería de tubérculos no podrá apoyarse en estudios "
          "análogos: deberá construirse con las directrices de UNEP (2020) y bases de *hotspots* sociales "
          "(Benoit-Norris et al., 2012), con datos primarios del territorio."),
    ("H2", "Ñame y batata: abundante ciencia de alimentos, escasa ingeniería de biorrefinerías (PI3 y PI5)"),
    ("P", "El volumen de literatura sobre el ñame y la batata (10.888 documentos en N4) contrasta con su escasa "
          "presencia como materia prima de bioprocesos evaluados. La comparación con la yuca es ilustrativa: la yuca "
          "suma 137 ACV, 100 TEA y 24 estudios que combinan ambos, mientras que el ñame registra 7 ACV, 20 TEA y "
          "ninguno combinado. La integración de rutas es igualmente baja: solo 7 documentos sobre ñame y 15 sobre "
          "batata combinan tres o más de las rutas fijas."),
    ("P", "La evidencia económica disponible sugiere por qué la integración es necesaria. En Colombia, el bioetanol de "
          "ñame como producto único tiene costos competitivos frente a la yuca, pero un valor presente neto negativo "
          "(Villadiego-del Villar et al., 2026). En *I. batatas*, la rentabilidad del bioetanol se acompaña de una "
          "carga climática diez veces superior a la de la yuca (Sanni et al., 2022). Ambos resultados indican que la "
          "viabilidad depende de distribuir costos e impactos entre varios productos, que es precisamente la lógica de "
          "la biorrefinería integrada."),
    ("H2", "Implicaciones para el diseño conceptual y la selección de metabolitos (PI4)"),
    ("P", "La literatura permite proponer una configuración en cascada coherente con las rutas fijas: (1) extracción del "
          "metabolito de alto valor a partir del tubérculo de descarte o de la cáscara; (2) recuperación del almidón "
          "nativo del residuo de extracción, cuyo valor se conserva (Ochoa et al., 2023; Quiñonez-Ensuncho et al., "
          "2026); (3) hidrólisis y fermentación del almidón no comercializable y de los descartes a bioetanol; "
          "(4) digestión anaerobia de vinazas, cáscaras y ramas para obtener biogás y cogenerar energía (Montoro et "
          "al., 2019; Zhang et al., 2018; Onu et al., 2022), y (5) acondicionamiento del digestato como biofertilizante. "
          "Esta última ruta es la menos documentada como producto, por lo que el digestato y el compost deberán "
          "caracterizarse (nutrientes, estabilidad e inocuidad) en lugar de asumir su valor comercial."),
    ("P", "En cuanto a los metabolitos, la priorización ofrece un criterio cuantitativo que deberá confirmarse con la "
          "caracterización del material vegetal local. Para la batata, la elección depende de la variedad: las "
          "antocianinas son pertinentes para la batata de pulpa morada y el β-caroteno para la de pulpa naranja "
          "(Teow et al., 2007; Alam, 2021). Como la batata cultivada en la zona de estudio es de pulpa naranja, se prioriza el "
          "β-caroteno (1.347 documentos; 299 vinculados a residuos o subproductos), y el ácido clorogénico queda como "
          "coproducto opcional para valorizar hojas y ramas (Sun et al., 2014); la fibra (Mei et al., 2010) y los "
          "péptidos antioxidantes (Zhang et al., 2014) son coproductos secundarios. Para el ñame, aunque la diosgenina "
          "domina la literatura del género, su evidencia en *D. rotundata* es mínima (5 documentos) y procede de "
          "especies medicinales. Por ello se recomienda priorizar el extracto fenólico o de flavonoides de la cáscara, "
          "el grupo con más evidencia específica en *D. rotundata* (52 documentos; Adomėnienė y Venskutonis, 2022), "
          "y, como segunda opción, los polisacáridos no amiláceos o mucílago (Zhao et al., 2023). La dioscorina "
          "(Hou et al., 2001) y la alantoína (Fu et al., 2006) son alternativas de alto valor, pero con evidencia "
          "insuficiente para un diseño conceptual sin experimentación previa."),
    ("H2", "Implicaciones para el ACV-S y el contexto territorial (PI6)"),
    ("P", "Colombia cuenta con una escuela consolidada de diseño y evaluación de biorrefinerías (Moncada B. et al., "
          "2016; Poveda-Giraldo et al., 2021) y con grupos regionales que estudian el ñame del Caribe desde la "
          "agronomía, la poscosecha y la cadena de suministro; sin embargo, ambas comunidades no se han encontrado. "
          "Una evaluación integrada en Montes de María conectaría esos dos nichos y abordaría problemas sociales "
          "documentados en la región: la fragilidad de la cadena exportadora (Granados Conde et al., 2026), las "
          "pérdidas logísticas (Vergara Rodríguez et al., 2025) y la importancia de la asociatividad productiva "
          "(Mendoza-Crespo y Ortiz-Velásquez, 2020). Estos problemas sugieren subcategorías prioritarias para el "
          "ACV-S: ingresos justos y estabilidad de precios para los agricultores, empleo local y condiciones de "
          "trabajo en la planta, acceso a infraestructura comunitaria y seguridad alimentaria."),
]
last = anchor
for k, (kind, md) in enumerate(discusion):
    model = {"H1": H1, "H2": H2, "P": BODY}[kind]
    last = add_after(last, model, md, strip=(kind == "P"),
                     comment=("AGREGADO Q1 (pendiente de aprobación): sección de Discusión. Interpreta los resultados, "
                              "los contrasta con revisiones previas del ACV-S y responde las PI1-PI6. Las cifras salen "
                              "de results/tables/ (gap_crop_method.csv, gap_integration.csv, metabolite_candidates.csv) "
                              "y todas las citas están en la lista de referencias del manuscrito; con esto quedan "
                              "citadas las referencias de la lista que no aparecían en el texto (Adomėnienė, Alam, "
                              "Fu, Hou, Mei, Mendoza-Crespo, Sun, Teow, Zhang 2014 y Zhao 2023).") if k == 0 else None)

# ---------------------------------------------------------------- 3. Limitaciones adicionales
lim_last = find("A este factor se suma")
add_after(lim_last, BODY,
          "Por otra parte, 2026 es un año parcial, por lo que las tasas de crecimiento se calcularon hasta 2025, y el "
          "corte en el año 2000 excluye entre el 1,6 % y el 10,5 % de la literatura de cultivo, sin afectar a los "
          "niveles de sostenibilidad (N1 y N2), aunque subrepresenta la literatura histórica sobre la diosgenina. "
          "Tampoco se incluyó Web of Science Core Collection, porque la aprobación del acceso a su API era "
          "incompatible con el cronograma del estudio. El riesgo de omisión es bajo: OpenAlex tiene una cobertura de "
          "referencias comparable a la de Scopus y Web of Science (Culbert et al., 2025), y las cadenas de búsqueda "
          "en sintaxis de Web of Science quedan disponibles en el repositorio para una actualización futura.",
          comment="AGREGADO Q1 (pendiente de aprobación): limitaciones que un revisor Q1 pedirá explícitamente "
                  "(año parcial, corte temporal y ausencia de Web of Science). Fuente: "
                  "results/tables/period_sensitivity.csv y protocolo/bitacora_decisiones.md.")

# ---------------------------------------------------------------- 4. Agenda de investigación
lim_extra = Paragraph(lim_last._p.getnext(), lim_last._parent)
agenda = [
    ("H2", "Agenda de investigación"),
    ("P", "A partir de los vacíos identificados, se proponen cinco líneas de investigación, formuladas como preguntas "
          "abiertas:"),
    ("P", "**Evaluación integrada.** ¿Cómo cambia la sostenibilidad de una biorrefinería de tubérculos cuando el ACV, el "
          "TEA y el ACV-S se aplican sobre el mismo sistema multiproducto y con el mismo criterio de asignación de "
          "cargas entre coproductos?"),
    ("P", "**Inventarios primarios.** ¿Cuáles son los rendimientos, insumos y pérdidas poscosecha del ñame y la batata "
          "en sistemas campesinos tropicales, y cuánto difieren de los datos genéricos de las bases de inventario?"),
    ("P", "**ACV-S en territorios rurales.** ¿Qué subcategorías e indicadores sociales capturan mejor los efectos de una "
          "biorrefinería sobre los ingresos, el empleo y la seguridad alimentaria de comunidades campesinas en "
          "territorios de posconflicto?"),
    ("P", "**Biofertilizante como producto.** ¿Cumplen el digestato y el compost obtenidos de residuos de ñame y batata "
          "los requisitos de calidad e inocuidad para comercializarse, y cuál es su valor económico y ambiental real?"),
    ("P", "**Metabolitos en las especies cultivadas.** ¿Qué contenido y qué rendimiento de extracción de compuestos "
          "fenólicos tienen las cáscaras de *D. rotundata*, y de β-caroteno los residuos de batata de pulpa naranja, "
          "a escalas compatibles con una planta rural?"),
]
last = lim_extra
for k, (kind, md) in enumerate(agenda):
    model = {"H2": H2, "P": BODY}[kind]
    last = add_after(last, model, md, strip=(kind == "P"),
                     comment=("AGREGADO Q1 (pendiente de aprobación): agenda de investigación. Cada pregunta se "
                              "deriva de un vacío cuantificado en los Resultados (Tablas 3, 4 y 5; mapa temático de "
                              "N6).") if k == 0 else None)

# ---------------------------------------------------------------- 5. Conclusiones: rutas y metabolitos (PI4)
concl = find("La evaluación de la sostenibilidad de biorrefinerías crece")
add_after(concl, BODY,
          "En cuanto al diseño (PI4), la evidencia bibliométrica respalda una configuración en cascada (metabolito, "
          "almidón, bioetanol, biogás y biofertilizante), con los compuestos fenólicos o flavonoides de la cáscara como "
          "metabolito prioritario del ñame y el β-caroteno para la batata de pulpa naranja. La selección final del "
          "metabolito del ñame requiere caracterizar la biomasa local.",
          comment="AGREGADO Q1 (pendiente de aprobación): las conclusiones no respondían la PI4 (rutas y metabolitos).")

for runs, text in PENDING:
    d.add_comment(runs, text=text, author=AUTHOR, initials=INI)
d.save(DST)
print("ok", len(PENDING), "comentarios")
