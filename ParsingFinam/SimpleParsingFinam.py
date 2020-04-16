import requests
from bs4 import BeautifulSoup as BS


def get_link():
    link = 0
    return link


def get_info_stock(find_string):
    r = requests.get("https://www.finam.ru/profile/akcii-usa-bats/the-pennant-group-inc_pntg")
    dict_stock = {}
    html = BS(r.content, 'html.parser')
    el = html.select("#issuer-profile-informer")
    dict_stock.update({"Последняя сделка": el[0].select_one("#issuer-profile-informer-last").text})
    dict_stock.update({"Изменение":
                           {el[0].select_one("#issuer-profile-informer-change").get("class")[0]:
                                el[0].select_one("#issuer-profile-informer-change").text +
                                el[0].select_one("#issuer-profile-informer-pchange").text}})
    dict_stock.update({"Цена открытия": el[0].select_one("#issuer-profile-informer-open").text})
    dict_stock.update({"Пред. закрытие": el[0].select_one("#issuer-profile-informer-close").text})
    return dict_stock


print(get_info_stock(" "))

print(requests.get("https://ffin.ru/market/directory/data/quotes/40796/"))
