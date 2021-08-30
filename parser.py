from requests import get
from bs4 import BeautifulSoup
from random import randint
from logger import Logger
import time
import bs4
import socks
import socket

logger = Logger()


def check_ip():
    ip = get('http://checkip.dyndns.org').content
    soup = BeautifulSoup(ip, 'html.parser')
    return soup.find('body').text


def sleep(minutes: int):
    logger.warning(f"{check_ip()}. Sleep")
    time.sleep(minutes)
    logger.warning(f"{check_ip()}. Wake up")


def search_ip(minutes: int):
    for s in range(minutes):
        logger.print(f"{s + 1}", end=' ')
        time.sleep(1)
    logger.print("...")


def is_stop(text: str):
    if text.count("https://www.google.com/recaptcha/api.js") != 0:
        return True
    else:
        return False


def do_request(url: str) -> BeautifulSoup:
    response = get(url=url)
    soup = BeautifulSoup(response.text, "lxml")

    search = False
    counter = 1
    while is_stop(response.text):
        logger.warning(f"[BLOCKED] [{check_ip()}] Searching IP...")

        search_ip(15)

        if counter % 5 == 0:
            sleep(randint(35, 60))

        response = get(url=url)
        soup = BeautifulSoup(response.text, "lxml")

        search = True
        counter += 1

    if search:
        logger.warning(f"[UNBLOCKED] {check_ip()}")

    return soup


def get_mail_phone(page="Магазин2.html"):

    soup = do_request("https://www.moscowmap.ru" + page)

    result = []
    for child in soup.recursiveChildGenerator():
        if isinstance(child, bs4.element.Tag):
            if child.has_attr('class') and child['class'].count('t-prop-and-val') != 0:
                for c in child.children:
                    if isinstance(c, bs4.element.Tag):
                        if c.text.count('Адрес') != 0 or c.text.count('Телефон') != 0 or c.text.count('e-mail') != 0:
                            result.append(c.text)
    return result


def get_data(url="Магазины.html"):
    soup = do_request(url)

    result = []
    for child in soup.recursiveChildGenerator():
        if isinstance(child, bs4.element.Tag):
            if child.has_attr('class') and child['class'].count('t-content-wrapper') != 0:
                for t in child.children:
                    if isinstance(t, bs4.element.Tag) and\
                            t.has_attr('class') and t['class'].count('t-orgs-list') != 0:
                        for c in t.children:
                            result.append(("|".join(get_mail_phone(page=c.a['href'])), c.text))
                            
                            print(f"[{check_ip()}]", "|".join(result[len(result) - 1]))

                            f = open("tabak.txt", "a")
                            f.write("|".join(result[len(result) - 1]) + "\n")
                            f.close()

    return result


if __name__ == "__main__":
    socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
    socket.socket = socks.socksocket

    logger.print(f"{check_ip()}", color='red')
    for i in range(1, 141):
        print(f"----------------------------\n\t\t\tPAGE: {i}")
        if i != 1:
            get_data(url=f"https://www.moscowmap.ru/spravochnik/tabachnye-magaziny/page{i}/")
        else:
            get_data(url=f"https://www.moscowmap.ru/spravochnik/tabachnye-magaziny/")
        sleep(10)
