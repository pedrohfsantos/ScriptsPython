from requests_html import HTMLSession
from tqdm.auto import tqdm
import re
from unidecode import unidecode


def AjustaDescription(file ,r):
    h1 = r.html.find('h1')[0].text.lower()
    all_paragraph = r.html.find('article p')
    for p in all_paragraph:
        i = unidecode(p.text.lower()).find(unidecode(h1))
        if i >= 0:
            if len(p.text[i:]) >= 125:
                new_description = p.text[i:]
                description_ok = True
                break

        else:
            description_ok = False
    
    if description_ok:
        if new_description[-1] == '.' and len(new_description) >= 140 and len(new_description) <= 160 :
            new_description = new_description.capitalize()

        else:
            while len(new_description) > 145:
                new_description = new_description.split(" ")
                del new_description[-1]
                new_description = " ".join(new_description)

            new_description = new_description.capitalize()
            new_description += "... Saiba mais.".encode("latin1").decode("unicode_escape")
        
        new_description = f"$desc           = \"{new_description}\";"
        mpi = open(f"{file}.php", "rt", -1, "utf-8")
        data = mpi.read()
        data = re.sub(r"\$desc\s*=\s*[\"\']\w*\s*.+[\"\'\;]", new_description, data)
        mpi = open(f"{file}.php", "wt", -1, "utf-8")
        mpi.write(data)
        mpi.close()

    else:
        not_adjusted.append(f"=> {file}")

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
    AjustaDescription(file_url(page), r)

if len(not_adjusted) > 0:
    print(f"\n Error :( \n")
    for link in not_adjusted:
        print(link)