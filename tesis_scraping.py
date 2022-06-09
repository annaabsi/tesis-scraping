import pandas as pd
from requests_html import HTMLSession
session = HTMLSession()

# scrapear tesis de 3 carreras de 3 universidades
carreras = {
    # 'ucv_psicología': 'https://repositorio.ucv.edu.pe/handle/20.500.12692/42194',
    # 'ucv_ciencias de la comunicación': 'https://repositorio.ucv.edu.pe/handle/20.500.12692/42449',
    # 'ucv_contabilidad': 'https://repositorio.ucv.edu.pe/handle/20.500.12692/42301',
    'uss_psicología': 'https://repositorio.uss.edu.pe/handle/20.500.12802/785',
    #'uss_ciencias de la comunicación': 'https://repositorio.uss.edu.pe/handle/20.500.12802/786',
    'uss_contabilidad': 'https://repositorio.uss.edu.pe/handle/20.500.12802/663',
    'autonoma_psicología': 'https://repositorio.autonoma.edu.pe/handle/20.500.13067/59',
    'autonoma_contabilidad': 'https://repositorio.autonoma.edu.pe/handle/20.500.13067/61',
    # no disponible
    #'autonoma_ciencias de la comunicación': '',
}

d = []
for carrera, url_carrera in carreras.items():
    university = carrera.split('_')[0]
    career = carrera.split('_')[1]
    for page in range(20):
        try:
            r = session.get(f'{url_carrera}/discover?rpp=10&etal=0&group_by=none&page={page}&filtertype_0=dateIssued&filter_relational_operator_0=equals&filter_0=%5B2020+TO+2021%5D')
            containers = r.html.find('.ds-artifact-item')
            for container in containers:
                # PDF
                img = container.xpath('//img')[0]
                img_src = img.attrs['src'].split('.jpg')[0]
                pdf_src = f'https://repositorio.{university}.edu.pe' + img_src
                # TITULO
                title = container.xpath('//a')[1].text
                # RESUMEN
                abstract = container.find('.abstract')[0].text
                # AUTOR
                autor = container.find('.author')[0].text
                # AÑO
                year = container.find('.date')[0].text.split('-')[0]
                d.append(
                    {
                        'UNIVERSIDAD': university,
                        'CARRERA': career,
                        'TITULO': title,
                        'RESUMEN': abstract,
                        'AUTOR(ES)': autor,
                        'AÑO': year,
                        'PDF': pdf_src
                    }
                )
        except:
            continue
df = pd.DataFrame(d)
df.to_csv('base_datos_tesis.csv')