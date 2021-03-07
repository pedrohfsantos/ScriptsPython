from requests_html import HTMLSession

session = HTMLSession()

urls = [
    "https://www.site.com.br/exemplo-pagina-1",
    "https://www.site.com.br/exemplo-pagina-2",
]


print("\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
print("Error links:\n")

for url in urls:
    try:
        headers = session.head(url).headers

        if "Location" in headers:
            redirect = headers["Location"]
            if redirect.endswith("/404"):
                print(url)

    except Exception as identifier:
        print(f"\n {identifier} \n")
    
print("\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
