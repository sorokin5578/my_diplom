import requests
import re
import datetime
import threading
from bs4 import BeautifulSoup as BS
from threading import Thread

"""Get page"""


def get_finviz_page(ticker):
    try:
        return requests.get("https://finviz.com/quote.ashx?t=" + ticker)
    except:
        return []


def return_new_page_ffin():
    page = []
    for i in range(1, 29):
        page.append("https://ffin.ru/market/directory/data/?PAGEN_1=" + str(i))
    return page


"""End Get page"""


def get_link2(r, find_string):
    """Get link for stock, which we find"""
    dict_stock = {}
    try:
        html = BS(r.content, 'html.parser')
        el = html.select("table.directory-list_table")
        ticker = el[0].select("td", text=True)
        count_tic = 2
        for a_tag in el[0].select("a", href=True):
            if len(find_string) == 0:
                break
            if not (re.search(r'([A-Za-z0-9_\&\.\,\'\(\)])',
                              a_tag.text[0])) or "ETF" in a_tag.text:
                continue
            for str_key in find_string:
                tic = ticker[count_tic].text.replace(u'\n', u'').replace(u' ', u'')
                if str_key.lower() == a_tag.text.lower() or str_key.lower() == tic.lower():
                    dict_stock.update({str_key: ["https://ffin.ru" + a_tag.get("href"), a_tag.text, tic]})
                    find_string.remove(str_key)
                    continue
            count_tic += 9
    except:
        return {}
    return dict_stock


def get_info_stock(link):
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
        return []
    return [dict_stock, dict_news]


def get_news_finviz(r):
    """Get news about stock from finviz"""
    dict_news = {}
    try:
        html = BS(r.content, 'html.parser')
        el = html.select("table.fullview-news-outer")
        time_mass = []
        cnt = 0
        for news in el[0].select("tr"):
            news_time = news.next.text
            if re.search(r'[A-Z]', news_time[0]):
                if delta_time_for_finviz_date(news_time):
                    dict_news.update({news.text.replace(u'\xa0\xa0', u' ').replace(u'\xa0',
                                                                                   u' '): news.select_one("a",href=True).get("href")})
                else:
                    break
            else:
                dict_news.update({news.text.replace(u'\xa0\xa0', u' ').replace(u'\xa0',
                                                                               u' '): news.select_one("a",href=True).get("href")})
    except:
        return {}
    return dict_news


"""Get delta_time block"""


def delta_time(then):
    now = datetime.datetime.today().strftime("%d.%m.%Y")
    if int(now[6:10]) - int(then[6:10]) == 0:
        if int(now[3:5]) - int(then[3:5]) == 0:
            if int(now[0:2]) - int(then[0:2]) < 10:
                return True
    return False


def delta_time_for_finviz_date(then):
    now = datetime.datetime.today().strftime("%b-%d-%y %H:%M")
    if int(now[7:9]) - int(then[7:9]) == 0:
        if now[0:3] == then[0:3]:
            if int(now[4:6]) - int(then[4:6]) == 0:
                return True
                # hour_now = int(now[10:12])
                # if then[15:17] == "PM":
                #     hour_then = int(then[10:12]) + 12
                # else:
                #     hour_then = int(then[10:12])
                # if hour_now - hour_then < 12:
                #     return True
    return False


# def delta_time_for_finviz_time(then):
#     now = datetime.datetime.today().strftime("%H:%M")
#     hour_now = int(now[0:2])
#     if then[5:7] == "PM":
#         hour_then = int(then[0:2]) + 12
#     else:
#         hour_then = int(then[0:2])
#     if hour_now - hour_then < 12:
#         return True
#     return False


"""End delta_time block"""


def sout(d, info, l):
    # event = threading.Event()
    l.acquire()
    for key in d:
        print("Company: " + d.get(key)[1])
        print("Ticker: " + d.get(key)[2])
        print("Link: " + d.get(key)[0])
        for j in range(0, 2):
            for item in info[j].items():
                print(item)
        print("------------")
    l.release()


class DownloadThread(Thread):
    """
    Пример скачивание файла используя многопоточность
    """

    def __init__(self, url, name, find_string):
        """Инициализация потока"""
        Thread.__init__(self)
        self.name = name
        self.url = url
        self.find_string = find_string

    def run(self):
        """Запуск потока"""
        d = get_link2(requests.get(self.url), self.find_string)
        if d:
            lock = threading.Lock()
            for key in d:
                info = get_info_stock(d.get(key)[0])
                name = d.get(key)[1]
            sout(d, info, lock)


def main(urls, find_str):
    """
    Запускаем программу
    """
    for item, url in enumerate(urls):
        name = "Поток %s" % (item + 1)
        thread = DownloadThread(url, name, find_str)
        thread.start()


if __name__ == "__main__":
    urls = return_new_page_ffin()
    main(urls, ["NFLX", "Tesla Motors Inc", "Apple Inc.", "TEL"])#"3D Systems Corp"
