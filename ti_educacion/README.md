# TI en la educación superior: mapeo bibliométrico exploratorio (proyecto independiente)

> Este proyecto **no** está relacionado con la revisión bibliométrica de ñame y batata que está en la raíz de este repositorio. Tiene sus propios scripts, datos y resultados, todos dentro de esta carpeta.

Búsqueda en OpenAlex y Scopus (31-oct-2026) sobre qué se ha publicado en revistas científicas acerca de TI en la educación y su implementación en universidades, como base para elegir el tema de tesis de la Maestría en Gerencia e Innovación en Tecnologías (Universidad de Cartagena), aplicado al CTEV.

**Informe principal:** [`informe_busqueda_TI_educacion_superior.md`](informe_busqueda_TI_educacion_superior.md)

Reproducir (desde la raíz del repositorio):

```bash
export OPENALEX_API_KEY=su_clave SCOPUS_API_KEY=su_clave_elsevier
python3 ti_educacion/src/buscar_openalex.py   # 15 ejes temáticos
python3 ti_educacion/src/brechas.py           # 16 intersecciones (brechas)
python3 ti_educacion/src/referencias.py       # referencias seleccionadas
```

Requiere solo `requests` (y `pandas` si se quieren explorar los CSV).
