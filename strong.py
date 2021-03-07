from requests_html import HTMLSession
from unidecode import unidecode
from tqdm.auto import tqdm
import re

def adjust_strong(file ,r):
    try:
        h1 = r.html.find('h1')[0].text.lower()
        all_paragraph = r.html.find('article p')
        adjusted_page = False

        for p in all_paragraph:
            strong = True if p.find('strong') else False
            h1InP = True if unidecode(h1) in unidecode(p.text.lower()) else False

            if strong != h1InP:
                i = unidecode(p.text.lower()).find(unidecode(h1))
                f = i + len(h1)            
                mpi = open(f"{file}.php", "rt", -1, "utf-8")
                data = mpi.read()
                data = re.sub(r'(<\s*(p|li).*?>\s*.*?)(?:(?:<\s*strong\s*>)?' + p.text[i:f] + r'(?:<\s*\/strong\s*>)?)', r'\1<strong>'+h1+'</strong>', data, flags=re.IGNORECASE)
                mpi = open(f"{file}.php", "wt", -1, "utf-8")
                mpi.write(data)
                mpi.close()

                adjusted_page = True

            if adjusted_page:
                break
                
    except:
        not_adjusted.append(file)

def file_url(url):
    url = url.split('//')
    url = url[1].split('/')
    return url[-1]


urls = [
    "https://www.site.com.br/exemplo-pagina-1",
    "https://www.site.com.br/exemplo-pagina-2",
]

not_adjusted = []

session = HTMLSession()

for page in tqdm(urls):
    r = session.get(page)
    adjust_strong(file_url(page), r)

if len(not_adjusted) > 0:
    print(f"\n Error :( \n")
    for link in not_adjusted:
        print(link)