from requests_html import HTMLSession
from unidecode import unidecode
from tqdm.auto import tqdm
import re

def replace_regex(file ,r):
    try:
        mpi = open(f"{file}.php", "rt", -1, "utf-8")
        data = mpi.read()

        data = re.sub(r'<\?=\$caminho\?>', r'<?=$caminhoProdutos?>', data, flags=re.IGNORECASE)
        # data = re.sub(r'<\? include\("inc/coluna-lateral.php"\);\?>', r'<? include("inc/coluna-lateral-produtos.php");?>', data, flags=re.IGNORECASE)
        # data = re.sub(r'</article>', r'</article> \n    <? include("inc/coluna-lateral-produtos.php");?>', data, flags=re.IGNORECASE)
        # data = re.sub(r'([^\.])<\/p>[\n\r ]*?<p>', r'\1 ', data, flags=re.IGNORECASE)
        
        # {start}([\n\r ]|.*)*?{end}
        
        
        mpi = open(f"{file}.php", "wt", -1, "utf-8")
        mpi.write(data)
        mpi.close()
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
    replace_regex(file_url(page), r)

if len(not_adjusted) > 0:
    print(f"\n Error :( \n")
    for link in not_adjusted:
        print(link)


