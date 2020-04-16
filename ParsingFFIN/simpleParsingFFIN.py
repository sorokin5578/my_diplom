import requests
from bs4 import BeautifulSoup as BS


def read_all_page(max_page):
    page = []
    for x in range(1, max_page + 1):
        page.append(requests.get("https://ffin.ru/market/directory/data/?PAGEN_1=" + str(x)))
    return page


def return_new_page(num_page):
    return requests.get("https://ffin.ru/market/directory/data/?PAGEN_1=" + str(num_page))


def get_link_stock(find_string):
    dict_stock = {}
    i = 1
    # page = read_all_page(28)
    for i in range(1, 29):
        for r in return_new_page(i):
            html = BS(r.content, 'html.parser')
            el = html.select("table.directory-list_table")
            for str_key in find_string:
                for a_tag in el[0].select("a", href=True):
                    if str_key.lower() in a_tag.text.lower():
                        dict_stock.update({str_key: "https://ffin.ru" + a_tag.get("href")})
                        continue;
            print("прочитано " + str(i))
            i += 1
            if len(dict_stock) == len(find_string):
                break
        if len(dict_stock) == len(find_string):
            break

    return dict_stock


def get_info_stock(link):
    dict_stock = {}
    print("nen")
    r = requests.get(link.get("3d systems corp"))
    dict_stock = {}
    html = BS(r.content, 'html.parser')
    el = html.select("table.td-last-right")
    print(el)
    # dict_stock.update({"Последняя сделка": el[0].select_one("#issuer-profile-informer-last").text})
    # dict_stock.update({"Изменение":
    #                        {el[0].select_one("#issuer-profile-informer-change").get("class")[0]:
    #                             el[0].select_one("#issuer-profile-informer-change").text +
    #                             el[0].select_one("#issuer-profile-informer-pchange").text}})
    # dict_stock.update({"Цена открытия": el[0].select_one("#issuer-profile-informer-open").text})
    # dict_stock.update({"Пред. закрытие": el[0].select_one("#issuer-profile-informer-close").text})
    return dict_stock


# print(get_link_stock(["Netflix inc", "3d systems corp"]))
# print()
d = get_link_stock(["3d systems corp","Netflix inc"])
print(d)
# get_info_stock(d)
