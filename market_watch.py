import time
import requests
import winsound
from sys import exit
from datetime import datetime
from bs4 import BeautifulSoup
from crypto import Crypto


def get_cryptos(url):
    count = 0
    cryptos = {}
    page_html = requests.get(url)

    soup = BeautifulSoup(page_html.text, "html.parser")
    tbody = soup.tbody
    trs = tbody.contents

    for tr in trs[:10]:
        name_html, price_html = tr.contents[2:4]
        mcap_hmtl = tr.contents[6]
        supply_html = tr.contents[8]

        # Getting the strings inside of the respective tags
        symbol = name_html.find_all("p", class_="q7nmo0-0 krbrab coin-item-symbol")[0].string
        name_str = name_html.p.string
        price_str = price_html.a.string
        mcap_str = mcap_hmtl.p.find_all("span")[1].string
        supply_str = supply_html.p.string

        new_crypto = Crypto(count, name_str, price_str, mcap_str, supply_str)
        cryptos[symbol] = new_crypto
        count += 1

    for tr in trs[10:]:
        # The rest of the table has slightly differently structured rows
        name_html, price_html = tr.contents[2:4]

        symbol = name_html.find_all("span")[2].string
        name_str = name_html.find_all("span")[1].string
        price_str = price_html.span.text

        new_crypto = Crypto(count, name_str, price_str)
        cryptos[symbol] = new_crypto
        count += 1

    return cryptos


def print_top_10(cryptos):
    print("\nTop 10 cryptocurrencies by market cap on", now.strftime("%b-%d-%Y %H:%M:%S: "))
    print("---------------------------------------------")
    top_10 = list(cryptos.items())[:10]
    for i in range(0, 10):
        print(str(i + 1) + ".", top_10[i][0], top_10[i][1].price)


def search_crypto(cryptos, symbol):
    if symbol in cryptos:
        return True
    print("Invalid input")


def print_crypto_data(cryptos, symbol):
    if search_crypto(cryptos, symbol):
        print("\nSymbol:", symbol, "| Name:", cryptos[symbol].name)
        print("Price:", cryptos[symbol].price, "| Market Cap:", cryptos[symbol].mcap, "| Supply:", cryptos[symbol].supply)
        print(cryptos[symbol].name, "is currently the #" + str(cryptos[symbol].placement), "cryptocurrency in the world.\n")


def menu_loop(cryptos):
    while True:
        print("\n(c)ontinue market watch \t(i)nfo about a specific coin \t e(x)it the program")
        action = input(">").lower()
        if action == "i":
            print("Enter the corresponding symbol to see specific info")
            symbol = input(">")
            print_crypto_data(cryptos, symbol)
        elif action == "x":
            exit(0)
        elif action == "c":
            return
        else:
            print("Invalid input")
            continue


def market_watch():
    global now, url
    now = datetime.now()
    url = "https://coinmarketcap.com/"

    while True:
        print("(s)tart the market watch \t (i)nfo about a specific coin \n(a)uto mode \t e(x)it the program")
        action = input(">").lower()

        if action == "s" or action == "a":
            print("Fetch data in what interval? (time in minutes)")
            interval = input(">")

            while True:
                cryptos = get_cryptos(url)
                print_top_10(cryptos)

                if action == "s":
                    menu_loop(cryptos)

                print(f"Waiting {interval} minute(s)")
                time.sleep(float(interval) * 60)
                frequency = 1000
                duration = 1000
                winsound.Beep(frequency, duration)

        elif action == "i":
            cryptos = get_cryptos(url)
            print("Enter the corresponding symbol to see specific info")
            symbol = input(">")
            print_crypto_data(cryptos, symbol)

        elif action == "x":
            exit(0)
        else:
            print("Invalid input.")
            continue
