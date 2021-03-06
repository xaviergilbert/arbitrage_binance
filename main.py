from binance.client import Client
from time import sleep, time
from cle_api import cle
from colorama import Fore, Back, Style, init
from global_arbitrage import Arbitrage
from wallet import Wallet

init()

def ping(client):
    start_time = time()
    client.ping()
    end_time = time()
    total_time = end_time - start_time
    print(Fore.CYAN + "Temps de reponse de l'api binance : " + str(int(total_time * 1000)) + "ms" + Style.RESET_ALL)

dict_arbitrages = {"BAKE_BNB_BUSD" : ["BAKE", "BNB", "BUSD"],
                   "CAKE_BNB_BUSD" : ["CAKE", "BNB", "BUSD"],
                #    "DOGE_BTC_BUSD" : ["DOGE", "BTC", "BUSD"],
                #    "DOGE_BTC_USDT" : ["DOGE", "BTC", "USDT"],
                   "SOL_BNB_USDT" : ["SOL", "BNB", "USDT"],
                   "SOL_BNB_BUSD" : ["SOL", "BNB", "BUSD"],
                   "YFII_BNB_BUSD" : ["YFII", "BNB", "BUSD"],
                   "PROM_BNB_BUSD" : ["PROM", "BNB", "BUSD"],
                   "BURGER_BNB_BUSD" : ["BURGER", "BNB", "BUSD"],
                   "BURGER_BNB_USDT" : ["BURGER", "BNB", "USDT"],
                   "SLP_ETH_USDT" : ["SLP", "ETH", "USDT"],
                   "TRX_XRP_USDT" : ["TRX", "XRP", "USDT"],
                   "BTT_TRX_USDT" : ["BTT", "TRX", "USDT"],
                   }

def calcul_nb_request(list_arbitrages):
    request_nb = 0
    for arbitrage in list_arbitrages:
        request_nb += arbitrage.request_nb
        arbitrage.reinit_nb_request()
    return request_nb

def make_arbitrage(arbitrage, wallet):
    print(Fore.YELLOW + "\nACTION ARBITRAGE : " + str(arbitrage.list_paires) + Style.RESET_ALL)
    print("WALLET AVANT = ", round(wallet.amount[arbitrage.list_paires[2]], 2))
    tmp = wallet.amount[arbitrage.list_paires[2]]
    tax = (wallet.amount[arbitrage.list_paires[2]] * (0.0750 / 100)) * 3
    print("ESTIMATION WALLET AFTER ARBITRAGE =", round(wallet.amount[arbitrage.list_paires[2]] * (1 + abs(arbitrage.get_diff()[1] / 100 )) - tax, 2))
    wallet.amount['TAX_INCOME'] += tax / 10
    wallet.amount[arbitrage.list_paires[2]] -= tax
    print(Fore.RED + "TAX : " + str(tax) + Style.RESET_ALL)
    print("WALLET AFTER TAX =", round(wallet.amount[arbitrage.list_paires[2]], 2))
    if arbitrage.get_diff()[0]:
        arbitrage.buy_by_first_crypto(wallet)
    else:
        arbitrage.buy_by_second_crypto(wallet)
    print("FULL WALLET APRES =", wallet.amount)
    print(Fore.GREEN + "Benefice = " + str(round(wallet.amount[arbitrage.list_paires[2]] - tmp, 2)) + Style.RESET_ALL)
    print()
    sleep(5)

if __name__ == "__main__":

    # recuperation info api
    mes_clefs = cle()
    api_keys = (mes_clefs.api_key, mes_clefs.api_secret)
    client = Client(api_keys[0], api_keys[1])
    wallet = Wallet()

    ping(client)

    list_arbitrages = []
    for elem in dict_arbitrages:
        list_arbitrages.append(Arbitrage(client, dict_arbitrages[elem]))

    while True:
        start_time = time()
        for arbitrage in list_arbitrages:
            arbitrage.maj_order_book()
            if arbitrage.get_diff()[1] > 0:
                print(Fore.GREEN, end="")
            print(" diff =", (" " if arbitrage.get_diff()[1] > 0 else "") + str(round(arbitrage.get_diff()[1], 4)) + "%", "de :", arbitrage.list_paires)
            print(Style.RESET_ALL, end="")
            if arbitrage.get_diff()[1] > 0.3:
                print(arbitrage.get_diff()[0])
                make_arbitrage(arbitrage, wallet)
        print(wallet.amount)
        end_time = time()
        total_time = end_time - start_time
        nb_request = calcul_nb_request(list_arbitrages)

        if nb_request / total_time > 5:
            sleep(1)

        print(Fore.MAGENTA + "Time: " + str(round(total_time, 2)) + " nombres de requetes par seconde " + str(round(nb_request / total_time, 3)) + str(Style.RESET_ALL))
        print()

