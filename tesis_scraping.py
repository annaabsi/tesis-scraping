import pandas as pd
from requests_html import HTMLSession
session = HTMLSession()

topics = [
    "acoso+escolar",
    "violencia+de+genero",
    "bullying",
    "tratamiento+periodistico",
    "bienestar+psicologico",
    "aborto",
    "habilidades+sociales",
    "actitudes+sexistas",
    "actitudes+maternas",
    "marketing+digital",
    "gestion+de+ventas",
    "estrategias+de+marketing",
    "fidelizacion"
]

for university in ["ucv", "uss", "autonoma"]:
    for year in [2019, 2020, 2021]:
        for topic in topics:
            pdf_links = []
            for page in range(10):
                r = session.get(f'https://repositorio.{university}.edu.pe/discover?rpp=10&etal=0&query=%22{topic}%22&scope=/&group_by=none&page={page}&sort_by=score&order=desc&filtertype_0=dateIssued&filter_relational_operator_0=contains&filter_0={year}')
                links = r.html.find('.img-thumbnail')
                for link in links:
                    img = link.xpath('//img')[0]
                    img_src = img.attrs['src'].split('.jpg')[0]
                    pdf_src = f'https://repositorio.{university}.edu.pe' + img_src
                    pdf_links.append(pdf_src)
                df = pd.DataFrame(pdf_links)
                df.to_csv(f'resultados/{university}_{year}_{topic}_pdf_links.csv', header=False)