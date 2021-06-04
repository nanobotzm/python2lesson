import requests
import codecs
from bs4 import BeautifulSoup as BS

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

domain = 'https://www.work.ua'
url = 'https://www.work.ua/ru/jobs-kyiv-python/'
resp = requests.get(url, headers=headers)
vacancies = []
errors = []

if resp.status_code == 200:
    soup = BS(resp.content, 'html.parser')
    main_div = soup.find('div', id='pjax-job-list')
    if main_div:
        div_lst = main_div.find_all('div', attrs={'class': 'job-link'})
        for div in div_lst:
            title = div.find('h2')
            href = title.a['href']
            description = div.p.text
            div_company = div.find('div', attrs={'class': 'add-top-xs'})
            company_check = div.span.text
            # company = 'No name'
            # logo = div.find('img')
            # if logo:
            #     company = logo['alt']
            vacancies.append({'title': title.text, 'url': domain + href, 'description': description,
                              'company': company_check})
    else:
        errors.append({'url': url, 'title': "Page do not respond"})
else:
    errors.append({'url': url, 'title': "Div does not exist"})

with codecs.open('work.txt', 'w', 'utf-8') as file:
    file.write(str(vacancies))

# file = codecs.open('work.html', 'w', 'utf-8')
# file.write(str(resp.text))
# file.close()
