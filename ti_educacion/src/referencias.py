"""Genera referencias (formato APA simplificado) desde OpenAlex para una lista curada de DOI."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import buscar_openalex as b

DOIS = """10.1186/s41239-019-0171-0 10.1186/s40594-021-00323-x 10.3390/s20113291 10.3390/educsci13070746
10.1057/s41599-023-01875-9 10.1007/s10639-022-11214-1 10.1016/j.chb.2018.07.027 10.1007/s11423-020-09788-z
10.1109/tlt.2016.2616312 10.1016/j.iheduc.2015.10.002 10.1109/rita.2019.2950148 10.1108/itse-03-2021-0052
10.1109/tla.2015.7350068 10.1109/access.2024.3361479 10.3390/info16040326 10.1080/14703297.2023.2190148
10.1186/s41239-023-00411-8 10.1186/s41239-023-00408-3 10.1016/j.chbah.2025.100121 10.1016/j.csi.2024.103940
10.1109/te.2024.3467912 10.1016/j.nlp.2024.100101 10.3390/info15100596 10.1080/10494820.2025.2596058
10.3390/su141912726 10.1080/07421222.2020.1790190 10.1016/j.ijinfomgt.2018.11.012 10.15446/dyna.v90n228.108569
10.1109/access.2021.3090366 10.1007/s10639-017-9642-x 10.1016/j.compedu.2018.05.016 10.3390/fi17120575
10.3390/computers14020049 10.1109/access.2021.3129488 10.58346/jisis.2024.i2.007 10.3390/electronics13163257
10.1016/j.chb.2019.08.004 10.1007/s10639-021-10573-5 10.1177/0266666920959367 10.1007/s10639-024-12518-0
10.3390/info16040296 10.1007/s10209-022-00904-9
10.1016/j.chb.2019.106189 10.1016/j.chb.2014.07.044 10.1007/s44217-025-00430-9 10.1109/access.2024.3350169""".split()

# Apellidos compuestos hispanos que la regla automática "último token = apellido" no resuelve
FIX = {"Benavides, L. M. C.": "Castro Benavides, L. M.", "Dussan, S. D. M.": "Morales Dussan, S. D.",
       "Vizcaíno, D. H.": "Heredia Vizcaíno, D.", "Aristizábal, C. R.": "Ramírez Aristizábal, C.",
       "Esparza, D. M. C.": "Córdova Esparza, D. M.", "Vivas, D. E. D.": "Díaz Vivas, D. E.",
       "Rodriǵuez": "Rodríguez", "OKOYE, K. O.": "Okoye, K."}

def apa(w):
    au = [a["author"]["display_name"] for a in w["authorships"]]
    def fmt(n):
        p = n.split(); return f"{p[-1]}, {' '.join(x[0] + '.' for x in p[:-1])}" if len(p) > 1 else n
    a = ", ".join(fmt(x) for x in au[:3]) + (", et al." if len(au) > 3 else "")
    src = ((w.get("primary_location") or {}).get("source") or {}).get("display_name", "")
    for k, v in FIX.items():
        a = a.replace(k, v)
    return f"{a} ({w['publication_year']}). {w['title']}. *{src}*. {w['doi']}"

def main():
    d = b.get({"filter": "doi:" + "|".join(DOIS), "per-page": 100, "select": "doi,title,publication_year,authorships,primary_location"})
    refs = sorted(apa(w) for w in d["results"])
    (b.OUT / "referencias_seleccionadas.md").write_text("# Referencias seleccionadas (metadatos de OpenAlex)\n\nGeneradas automáticamente desde OpenAlex a partir del DOI; antes de citarlas en un documento formal, verifique el formato APA 7 completo (volumen, número, páginas) en la página del DOI.\n\n" + "\n".join(f"- {r}" for r in refs) + "\n", encoding="utf-8")
    print(len(refs), "de", len(DOIS))

if __name__ == "__main__":
    main()
