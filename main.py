from binance.client import Client
from time import sleep, time
from cle_api import cle
from colorama import Fore, Back, Style, init
from global_arbitrage import Arbitrage

init()

dict_arbitrages = {"BAKE_BNB_BUSD" : ["BAKE", "BNB", "BUSD"],
                   "CAKE_BNB_BUSD" : ["CAKE", "BNB", "BUSD"]}

class Wallet():
    def __init__(self):
        self.amount = {'BNB' : 0, 'BUSD' : 1000, 'USDT' : 0, 'BAKE' : 0, 'TAX_INCOME' : 0}

def make_arbitrage(arbitrage, wallet):
    print("ACTION ARBITRAGE")
    print("WALLET AVANT = ", wallet.amount)
    tmp = wallet.amount['BUSD']
    tax = (wallet.amount['BUSD'] * (0.0750 / 100)) * 3
    wallet.amount['TAX_INCOME'] += tax / 10
    wallet.amount['BUSD'] -= tax
    print(Fore.RED + "TAX : " + str(tax) + Style.RESET_ALL)
    print("WALLET AFTER TAX =", wallet.amount['BUSD'])
    if arbitrage.get_diff() > 0:
        arbitrage.buy(wallet)
    else:
        arbitrage.sell(wallet)
    print("WALLET APRES =", wallet.amount)
    print(Fore.GREEN + "Benefice = " + str(wallet.amount['BUSD'] - tmp) + Style.RESET_ALL)
    print()
    sleep(5)

if __name__ == "__main__":
    # recuperation info api
    mes_clefs = cle()
    api_keys = (mes_clefs.api_key, mes_clefs.api_secret)
    client = Client(api_keys[0], api_keys[1])
    wallet = Wallet()

    # init class arbitrage
    arbitrage_cake = Arbitrage(client, dict_arbitrages["CAKE_BNB_BUSD"])
    arbitrage_bake = Arbitrage(client, dict_arbitrages["BAKE_BNB_BUSD"])

    while True:
        # start_time = time()
        arbitrage_bake.maj_order_book()

        print(" diff =", arbitrage_bake.get_diff(), "%")

        if abs(arbitrage_bake.get_diff()) > 0.10:
            make_arbitrage(arbitrage_bake, wallet)

        sleep(0.1)

        # end_time = time()
        # total_time = end_time - start_time
        # print("Time: ", total_time)
