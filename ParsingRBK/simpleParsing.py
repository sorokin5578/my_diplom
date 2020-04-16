import requests
from bs4 import BeautifulSoup as BS


def read_all_page(max_page):
    page = []
    for x in range(1, max_page + 1):
        page.append(requests.get("https://www.rbc.ua/rus/news/" + str(x)))
    return page


def get_link_rbk(find_string):
    dict_key = {}
    dict_res = {}
    for key_str in find_string:
        dict_key.clear()
        for r in read_all_page(2):
            html = BS(r.content, 'html.parser')
            for el in html.find_all('a', class_="news-feed-tag__item news-feed-tag__item--image-disable"):
                if key_str.lower() in el.text.lower():
                    dict_key.update({el.get("href"): el.text})
        dict_res.update({key_str: dict_key.copy()})

    return dict_res


# print(get_info_stock(" "))
link_rbk = get_link_rbk(["коронавирус", "кабмин", "нефть"])
print(link_rbk.get("коронавирус"))
