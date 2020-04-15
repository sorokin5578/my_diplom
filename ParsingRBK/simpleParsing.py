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


# <tr>
#             <td class="flag"><span title="США" class="ceFlags USA">&nbsp;</span></td>
#     		                <td class="left bold plusIconTd elp"><a title="Tesla Inc" href="/equities/tesla-motors">Tesla</a><span class="alertBellGrayPlus js-plus-icon genToolTip oneliner" data-tooltip="Создать уведомление" data-name="Tesla Inc" data-id="13994" data-volume="20.714.683"></span></td>
#     		            <td class="align_right pid-13994-last">727,15</td>
#             <td class="align_right pid-13994-high">741,70</td>
#             <td class="pid-13994-low">692,99</td>
#             <td class="bold greenFont pid-13994-pc">+76,46</td>
#             <td class="bold greenFont pid-13994-pcp">+11,75%</td>
#             <td class="pid-13994-turnover">13,65M</td>
#             <td class="pid-13994-time" data-value="1586876599">18:03:19</td>
#             <td class="center"><span class="greenClockIcon">&nbsp;</span></td>
#         </tr>


def get_info_stock(find_string):
    link = []
    r = requests.get("https://www.finam.ru")
    print(r)
    html = BS(r.content, 'html.parser')
    # for el in html.find_all('td', class_="left bold plusIconTd elp"):
    for el in html.find_all('h2'):
        print(el)
        # if find_string.lower() in el.text.lower():
        #     link.append(el.get("href"))
        # print(link)
    return link


# print(get_info_stock(" "))
link_rbk = get_link_rbk(["коронавирус", "кабмин", "нефть"])
print(link_rbk.get("нефть"))

