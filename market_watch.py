import time
import requests
import winsound
from sys import exit
from datetime import datetime
from crypto import Crypto


def get_cryptos(api_url):
    cryptos = {}
    current_rank = 1

    # Using API URL instead of regular ULR in order to retrieve dynamic content
    r = requests.get(api_url)

    for item in r.json()["data"]["cryptoCurrencyList"]:
        symbol = item["symbol"]
        name_str = item["name"]
        price_str = item["quotes"][2]["price"]
        mcap_str = item["quotes"][2]["marketCap"]
        supply_str = item["circulatingSupply"]

        new_crypto = Crypto(current_rank, name_str, price_str, mcap_str, supply_str)
        cryptos[symbol] = new_crypto
        current_rank += 1

    return cryptos


def print_top_10(cryptos):
    print("\nTop 10 cryptocurrencies by market cap on", now.strftime("%b-%d-%Y %H:%M:%S: "))
    print("---------------------------------------------")
    top_10 = list(cryptos.items())[:10]
    for i in range(0, 10):
        print(str(i + 1) + ".", top_10[i][0], "|", top_10[i][1].price, "USD")


def search_crypto(cryptos, symbol):
    if symbol in cryptos:
        return True
    print("Invalid input")


def print_crypto_data(cryptos, symbol):
    if search_crypto(cryptos, symbol):
        print("\nSymbol:", symbol, "USD | Name:", cryptos[symbol].name)
        print("Price:", cryptos[symbol].price, "| Market Cap:", cryptos[symbol].mcap, "USD | Supply:", cryptos[symbol].supply, symbol)
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
    global now, url, anti_url
    now = datetime.now()
    url = "https://coinmarketcap.com/"
    api_url = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit=100&sortBy=market_cap&sortType=desc&convert=USD,BTC,ETH&cryptoType=all&tagType=all&audited=false&aux=ath,atl,high24h,low24h,num_market_pairs,cmc_rank,date_added,max_supply,circulating_supply,total_supply,volume_7d,volume_30d"

    while True:
        print("(s)tart the market watch \t (i)nfo about a specific coin \n(a)uto mode \t e(x)it the program")
        action = input(">").lower()

        if action == "s" or action == "a":
            print("Fetch data in what interval? (time in minutes)")
            interval = input(">")

            while True:
                cryptos = get_cryptos(api_url)
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
