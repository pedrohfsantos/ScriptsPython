import os
import re
from requests_html import HTMLSession
from tqdm.auto import tqdm
from unidecode import unidecode


log = []

def url(file, mpitemporario=True):
    host =  os.getcwd().split('\\')[-1]
    if mpitemporario:
        return f"https://www.mpitemporario.com.br/projetos/{host}/{file}"
    else:
        host = host.replace('www.', '')
        return f"http://www.{host}/{file}"


def AjustaDescription(file, r):
    h1 = r.html.find('h1')[0].text.lower()
    all_paragraph = r.html.find('article p')
    description_ok = False

    for p in all_paragraph:
        p = re.sub(r'\n|\r|\nr| ]', ' ', p.text)
        i = unidecode(p.lower()).find(unidecode(h1))
        if i >= 0:
            if len(p[i:]) >= 125:
                new_description = p[i:]
                description_ok = True
                break

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

        with open(f"{file}", "rt", encoding="utf-8") as file_open:
            data = file_open.read()

        data = re.sub(r"\$desc\s*=\s*[\"\'].*?[\"\']\s*;", new_description, data)

        with open(f"{file}", "wt", encoding="utf-8") as file_open:
            file_open.write(data)

    else:
        new_description = f"{h1} - "

        for p in all_paragraph:
            p = re.sub(r'\n|\r|\nr| ]', ' ', p.text)
            desc = f"{h1} - {p}"
            if len(p) >= 125:
                new_description = desc
                break

        while len(new_description) > 145:
            new_description = new_description.split(" ")
            del new_description[-1]
            new_description = " ".join(new_description)

        new_description = new_description.capitalize()
        new_description += "... Saiba mais.".encode("latin1").decode("unicode_escape")
        new_description = f"$desc           = \"{new_description}\";"

        with open(f"{file}", "rt", encoding="utf-8") as file_open:
            data = file_open.read()

        data = re.sub(r"\$desc\s*=\s*[\"\'].*?[\"\']\s*;", new_description, data)

        with open(f"{file}", "wt", encoding="utf-8") as file_open:
            file_open.write(data)


files = [x for x in os.listdir() if '.php' in x]

for file in files:
    with open(file, 'rt', encoding="utf-8") as file_open:
        data = file_open.read()
        if not re.findall('\$desc\s*=\s*[\"\'](.*?)[\"\'\;]', data):
            files.remove(file)


session = HTMLSession()
for file in tqdm(files):
    r = session.get(url(file))
    AjustaDescription(file, r)