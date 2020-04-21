import requests
import re
from timeit import default_timer as timer
from bs4 import BeautifulSoup as BS
from threading import Thread


def return_new_page_ffin():
    page = []
    for i in range(1, 29):
        page.append("https://ffin.ru/market/directory/data/?PAGEN_1=" + str(i))
    return page


def return_req_page_ffin():
    page = []
    for i in range(1, 29):
        page.append(requests.get("https://ffin.ru/market/directory/data/?PAGEN_1=" + str(i)))
    return page


class DownloadThread(Thread):
    """
    Пример скачивание файла используя многопоточность
    """

    def __init__(self, url, name, find_string):
        """Инициализация потока"""
        Thread.__init__(self)
        self.name = name
        self.url = url
        self.find_string=find_string

    def run(self):
        """Запуск потока"""
        d=self.get_link2(requests.get(self.url))
        if d:
            print(d)

    def get_link2(self, r):
        dict_stock = {}
        html = BS(r.content, 'html.parser')
        el = html.select("table.directory-list_table")
        ticker = el[0].select("td", text=True)
        count_tic = 2
        for a_tag in el[0].select("a", href=True):
            if len(self.find_string)==0:
                break
            if not (re.search(r'([A-Za-z0-9_\&\.\,\'\(\)])',
                              a_tag.text[0])) or "ETF" in a_tag.text:
                continue
            for str_key in self.find_string:
                tic = ticker[count_tic].text.replace(u'\n', u'').replace(u' ', u'')
                if str_key.lower() in a_tag.text.lower() or str_key.lower() in tic.lower():
                    dict_stock.update({str_key: ["https://ffin.ru" + a_tag.get("href"), a_tag.text, tic]})
                    self.find_string.remove(str_key)
                    continue
            count_tic += 9
        return dict_stock


def main(urls):
    """
    Запускаем программу
    """
    for item, url in enumerate(urls):
        name = "Поток %s" % (item + 1)
        thread = DownloadThread(url, name, ["NFLX", "Tesla Motors Inc", "Apple Inc."])
        thread.start()


if __name__ == "__main__":
    start_time = timer()
    urls = return_new_page_ffin()
    main(urls)
    print(timer() - start_time)
