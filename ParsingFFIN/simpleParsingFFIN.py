import requests
from bs4 import BeautifulSoup as BS


def return_new_page(num_page):
    return requests.get("https://ffin.ru/market/directory/data/?PAGEN_1=" + str(num_page))


def get_link_stock(find_string):
    dict_stock = {}
    len_str = len(find_string)
    for i in range(1, 29):
        r = return_new_page(i)
        html = BS(r.content, 'html.parser')
        el = html.select("table.directory-list_table")
        for a_tag in el[0].select("a", href=True):
            if len(find_string) == 0:
                break
            for str_key in find_string:
                if str_key.lower() in a_tag.text.lower():
                    dict_stock.update({str_key: "https://ffin.ru" + a_tag.get("href")})
                    find_string.remove(str_key)
                    continue
        if len(dict_stock) == len_str:
            break

    return dict_stock


def get_info_stock(link):
    r = requests.get(link)
    dict_stock = {}
    grow = "down"
    html = BS(r.content, 'html.parser')
    el = html.select("table.td-last-right")
    grow_index = el[0].select_one("td.lastTradeChange").text.replace(u'\n', u'').replace(u' ', u'')
    if not ("-" in grow_index):
        grow = "up"
    dict_stock.update({"Последняя сделка": el[0].select_one("td.lastTradePrice").text.replace(u'\n', u'')})
    dict_stock.update({"Изменение": {grow: grow_index}})
    dict_stock.update({"Дата торгов": el[0].select_one("td.lastTradeDate").text.replace(u'\n', u'')})
    dict_stock.update({"Потенциал роста": el[0].select_one("td.lastTradePotential").text.replace(u'\n', u'')})
    dict_stock.update({"Рекомендации": el[0].find_all("span", text=True)[0].text})
    print(dict_stock)
    return dict_stock


# print(get_link_stock(["Netflix inc", "3d systems corp"]))
# print()
d = get_link_stock(["3d systems corp"])
print(d)
get_info_stock("https://ffin.ru/market/directory/data/quotes/32270/")
