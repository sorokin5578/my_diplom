import requests
import re
import datetime
from timeit import default_timer as timer
from bs4 import BeautifulSoup as BS


def return_new_page_ffin(num_page):
    return requests.get("https://ffin.ru/market/directory/data/?PAGEN_1=" + str(num_page))


def get_finviz_page(ticker):
    return requests.get("https://finviz.com/quote.ashx?t=" + ticker)


def get_news_finviz(r):
    dict_news = {}
    html = BS(r.content, 'html.parser')
    el = html.select("table.fullview-news-outer")
    time_mass = []
    cnt = 0
    for news in el[0].select("tr"):
        news_time = news.next.text
        if re.search(r'[A-Z]', news_time[0]):
            if delta_time_for_finviz(news_time):
                dict_news.update({news.text.replace(u'\xa0\xa0', u' ').replace(u'\xa0', u' '): news.select_one("a",
                                                                                                               href=True).get(
                    "href")})
            else:
                break
        else:
            dict_news.update({news.text.replace(u'\xa0\xa0', u' ').replace(u'\xa0', u' '): news.select_one("a",
                                                                                                           href=True).get(
                "href")})
    return dict_news


def delta_time(then):
    now = datetime.datetime.today().strftime("%d.%m.%Y")
    if int(now[6:10]) - int(then[6:10]) == 0:
        if int(now[3:5]) - int(then[3:5]) == 0:
            if int(now[0:2]) - int(then[0:2]) < 10:
                return True
    return False


def delta_time_for_finviz(then):
    now = datetime.datetime.today().strftime("%b-%d-%y %I:%M%p")
    if int(now[7:9]) - int(then[7:9]) == 0:
        if now[0:3] == then[0:3]:
            if int(now[4:6]) - int(then[4:6]) < 2:
                # if int(now[10:12])-int(then[10:12])<2:
                #     return True
                return True
    return False


def get_link_stock(find_string):
    dict_stock = {}
    len_str = len(find_string)
    for i in range(1, 29):
        r = return_new_page_ffin(i)
        html = BS(r.content, 'html.parser')
        el = html.select("table.directory-list_table")
        ticker = el[0].select("td", text=True)
        count_tic = 2
        for a_tag in el[0].select("a", href=True):
            if not (re.search(r'([A-Za-z0-9_\&\.\,\'\(\)])',
                              a_tag.text[0])) or "ETF" in a_tag.text:  # a_tag.text[0] or a_tag.text
                continue
            if len(find_string) == 0:
                break
            for str_key in find_string:
                tic = ticker[count_tic].text.replace(u'\n', u'').replace(u' ', u'')
                if str_key.lower() in a_tag.text.lower() or str_key.lower() in tic.lower():
                    dict_stock.update({str_key: ["https://ffin.ru" + a_tag.get("href"), a_tag.text, tic]})
                    find_string.remove(str_key)
                    continue
            count_tic += 9
        if len(dict_stock) == len_str:
            break
    return dict_stock


def get_info_stock(link):
    r = requests.get(link)
    dict_news = {}
    dict_stock = {}
    html = BS(r.content, 'html.parser')
    el = html.select("table.td-last-right")
    ticker = html.select_one("h1", class_="quotes-company_title").text.replace(u'\n', u'').replace(u' ', u'')
    grow_index = el[0].select_one("td.lastTradeChange").text.replace(u'\n', u'').replace(u' ', u'')
    grow = "down"
    if not ("-" in grow_index):
        grow = "up"
    dict_stock.update({"Последняя сделка": el[0].select_one("td.lastTradePrice").text.replace(u'\n', u'')})
    dict_stock.update({"Изменение": [grow, grow_index]})
    dict_stock.update({"Дата торгов": el[0].select_one("td.lastTradeDate").text.replace(u'\n', u'')})
    dict_stock.update({"Потенциал роста": el[0].select_one("td.lastTradePotential").text.replace(u'\n', u'')})
    dict_stock.update({"Рекомендации": el[0].find_all("span", text=True)[0].text})
    news = html.select("div.widget_cont")
    for j in range(2, 4):
        for n in news[j].select("li", id=True):
            name_news = n.text.replace(u'\n', u' ')
            if delta_time(name_news[1:11]):
                dict_news.update({name_news: "https://ffin.ru" + n.select_one("a", href=True).get("href")})
    dict_news_finviz = get_news_finviz(get_finviz_page(ticker[ticker.find("(") + 1:len(ticker) - 1]))
    dict_news.update(dict_news_finviz)
    return [dict_stock, dict_news]


# print(get_link_stock(["Netflix inc", "3d systems corp"]))

# d = get_link_stock(["ZION"])
# print(d)
# d = get_link_stock(["Alliance Data Systems", "3d systems corp", "Netflix inc", "Tesla Motors Inc","Zoetis Inc"])
# print(d.get("Alliance Data Systems"))
# print(d.get("3d systems corp"))
# print(d.get("Netflix inc"))
# print(d.get("Tesla Motors Inc"))
# print(d.get("Zoetis Inc"))

# start_time = timer()
# d = get_link_stock(["NFLX", "Tesla Motors Inc", "Apple Inc."])
# print(d)
# print(timer() - start_time)

# for key in d:
#     print("Company: " + d.get(key)[1])
#     print("Ticker: " + d.get(key)[2])
#     print("Link: " + d.get(key)[0])
#     info = get_info_stock(d.get(key)[0])
#     for j in range(0, 2):
#         for item in info[j].items():
#             print(item)
#     print("------------")

now = datetime.datetime.today().strftime("%d.%m.%Y %I:%M%p")
now.strftime("%y%m%d %H:%M")
print(now)
# str="Apr-22-20 05:24AM".strftime("%y%m%d %H:%M")
# # # print(str)

