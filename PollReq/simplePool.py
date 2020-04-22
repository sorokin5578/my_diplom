import requests
import re
import datetime
from bs4 import BeautifulSoup as BS
from multiprocessing import Pool

"""Get page"""


def get_finviz_page(ticker):
    try:
        return requests.get("https://finviz.com/quote.ashx?t=" + ticker)
    except:
        return []


def return_new_page_ffin(i):
    return "https://ffin.ru/market/directory/data/?PAGEN_1=" + str(i)


"""End Get page"""


def get_link(arr):
    """Get link for stock, which we find"""
    dict_stock = {}
    link, str_key = arr[0], arr[1]
    try:
        r = requests.get(link)
        html = BS(r.content, 'html.parser')
        el = html.select("table.directory-list_table")
        ticker = el[0].select("td", text=True)
        count_tic = 2
        for a_tag in el[0].select("a", href=True):
            if not (re.search(r'([A-Za-z0-9_\&\.\,\'\(\)])',
                              a_tag.text[0])) or "ETF" in a_tag.text:
                continue
            tic = ticker[count_tic].text.replace(u'\n', u'').replace(u' ', u'')
            if str_key.lower() == a_tag.text.lower() or str_key.lower() == tic.lower():
                dict_stock.update({str_key: ["https://ffin.ru" + a_tag.get("href"), a_tag.text, tic]})
                break
            count_tic += 9
    except:
        get_info_stock({}, {})
    for key in dict_stock:
        get_info_stock(dict_stock.get(key)[0], dict_stock)


def get_info_stock(link, dict_res):
    """Get info about stock"""
    dict_news = {}
    dict_stock = {}
    try:
        r = requests.get(link)
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
        # news = html.select("div.widget_cont")
        # for j in range(2, 4):
        #     for n in news[j].select("li", id=True):
        #         name_news = n.text.replace(u'\n', u' ')
        #         if delta_time(name_news[1:11]):
        #             dict_news.update({name_news: "https://ffin.ru" + n.select_one("a", href=True).get("href")})
        dict_news_finviz = get_news_finviz(get_finviz_page(ticker[ticker.find("(") + 1:len(ticker) - 1]))
        dict_news.update(dict_news_finviz)
    except:
        sout({}, {}, {})
    sout(dict_res, dict_stock, dict_news)


def get_news_finviz(r):
    """Get news about stock from finviz"""
    dict_news = {}
    try:
        html = BS(r.content, 'html.parser')
        el = html.select("table.fullview-news-outer")
        for news in el[0].select("tr"):
            news_time = news.next.text
            if re.search(r'[A-Z]', news_time[0]):
                if delta_time_for_finviz_date(news_time):
                    dict_news.update({news.text.replace(u'\xa0\xa0', u' ').replace(u'\xa0',
                                                                                   u' '): news.select_one("a",
                                                                                                          href=True).get(
                        "href")})
                else:
                    break
            else:
                dict_news.update({news.text.replace(u'\xa0\xa0', u' ').replace(u'\xa0',
                                                                               u' '): news.select_one("a",
                                                                                                      href=True).get(
                    "href")})
    except:
        return {}
    return dict_news


"""Get delta_time block"""


# def delta_time(then):
#     now = datetime.datetime.today().strftime("%d.%m.%Y")
#     if int(now[6:10]) - int(then[6:10]) == 0:
#         if int(now[3:5]) - int(then[3:5]) == 0:
#             if int(now[0:2]) - int(then[0:2]) < 10:
#                 return True
#     return False


def delta_time_for_finviz_date(then):
    now = datetime.datetime.today().strftime("%b-%d-%y %H:%M")
    if int(now[7:9]) - int(then[7:9]) == 0:
        if now[0:3] == then[0:3]:
            if int(now[4:6]) - int(then[4:6]) < 1:
                return True
    return False


"""End delta_time block"""


def sout(info, stock, news):
    """Out res"""
    for key in info:
        print("Company: " + info.get(key)[1])
        print("Ticker: " + info.get(key)[2])
        print("Link: " + info.get(key)[0])
    for key in stock.items():
        print(key)
    for key in news.items():
        print(key)
    print("--------")


def main(find_str):
    """
    Запускаем программу
    """
    res = []
    for key_str in find_str:
        for i in range(1, 29):
            res.append([return_new_page_ffin(i), key_str])
    with Pool(30) as p:
        p.map(get_link, res)
        p.close()


if __name__ == "__main__":
    find_string = ["NFLX", "Tesla Motors Inc"]
    # find_string = ["NFLX", "Tesla Motors Inc", "Apple Inc.", "NKE"]
    # find_string = ["NFLX", "MUR", "MYL", "NKE"]
    main(find_string)
