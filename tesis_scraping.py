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

for year in [2019, 2020, 2021]:
    for topic in topics:
        for page in range(200):
            # repositorio UCV
            pdf_links = []
            r = session.get(f'https://repositorio.ucv.edu.pe/discover?rpp=10&etal=0&query=%22{topic}%22&scope=/&group_by=none&page={page}&sort_by=score&order=desc&filtertype_0=dateIssued&filter_relational_operator_0=contains&filter_0={year}')
            links = r.html.find('.img-thumbnail')
            for link in links:
                img = link.xpath('//img')[0]
                img_src = img.attrs['src'].split('.jpg')[0]
                pdf_src = 'https://repositorio.ucv.edu.pe' + img_src
                pdf_links.append(pdf_src)
            df = pd.DataFrame(pdf_links)
            df.to_csv(f'UCV_{year}_{topic}_pdf_links.csv', header=False)