from bs4 import BeautifulSoup
import requests
import re


def crawl_sub_categories(cat_link, cat_name):
    """ crawls the cat_link to return a list containing
    the links of different subcategories
    """

    html_doc = requests.get(cat_link)
    soup = BeautifulSoup(html_doc.text, 'html.parser')
    subcat = soup.find_all("a", {"href": re.compile(f"/{cat_name}")})[:10]
    subcat = [i for i in subcat if i]


    def is_short(string): return bool(len(string.split("/")) == 3)
    def join_base(path): return cat_link.split(cat_name)[0][:-1]+path

    subcat1 = list()
    for i in subcat:
        url = join_base(i["href"])
        if is_short(i["href"]) and url not in subcat1:
            subcat1.append(url)

    return subcat1


def get_headlines(link):
    html_doc = requests.get(link)
    soup = BeautifulSoup(html_doc.text, "html.parser")
    hey = soup.find_all("h3")
    headlines = []
    for h in hey[1:15]:
        headlines.append(h.text.strip())
    return headlines
