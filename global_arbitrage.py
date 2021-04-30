from binance.client import Client
from time import sleep, time

class Arbitrage:
    def __init__(self, client, list_paires):
        self.client = client
        self.list_paires = list_paires
        self.dict_order_book = {}
        self.request_nb = 0


    # def buy_action_by_api_binance(self):

    def buy_by_first_crypto(self, wallet): # if negative diff
        print("BUY", [self.list_paires[0]])
        self.maj_order_book()
        wallet.amount[self.list_paires[0]] = wallet.amount[self.list_paires[2]] / self.get_price_buy(self.list_paires[0] + self.list_paires[2])
        wallet.amount[self.list_paires[2]] = 0
        self.maj_order_book()
        wallet.amount[self.list_paires[1]] = wallet.amount[self.list_paires[0]] * self.get_price_sell(self.list_paires[0] + self.list_paires[1])
        wallet.amount[self.list_paires[0]] = 0
        self.maj_order_book()
        wallet.amount[self.list_paires[2]] = wallet.amount[self.list_paires[1]] * self.get_price_sell(self.list_paires[1] + self.list_paires[2])
        wallet.amount[self.list_paires[1]] = 0


    def buy_by_second_crypto(self, wallet): # if positive diff
        print("BUY", [self.list_paires[1]])
        self.maj_order_book()
        wallet.amount[self.list_paires[1]] = wallet.amount[self.list_paires[2]] / self.get_price_buy(self.list_paires[1] + self.list_paires[2])
        wallet.amount[self.list_paires[2]] = 0
        self.maj_order_book()
        wallet.amount[self.list_paires[0]] = wallet.amount[self.list_paires[1]] / self.get_price_buy(self.list_paires[0] + self.list_paires[1])
        wallet.amount[self.list_paires[1]] = 0
        self.maj_order_book()
        wallet.amount[self.list_paires[2]] = wallet.amount[self.list_paires[0]] * self.get_price_sell(self.list_paires[0] + self.list_paires[2])
        wallet.amount[self.list_paires[0]] = 0


    def new_request_price(self,paire):
        return float(self.get_order_book(paire)['bids'][0][0])

    def get_price_sell(self, paire):
        return float(self.dict_order_book[paire]['bids'][0][0])

    def get_price_buy(self, paire):
        return float(self.dict_order_book[paire]['asks'][0][0])

    def get_volume(self, paire):
        return float(self.dict_order_book[paire]['bids'][0][1])

    def get_order_book(self, paire): #requete api binance
        self.request_nb += 1
        return self.client.get_order_book(symbol=paire)
    
    def reinit_nb_request(self):
        self.request_nb = 0

    def maj_order_book(self):
        self.dict_order_book[self.list_paires[0] + self.list_paires[2]] = self.get_order_book(self.list_paires[0] + self.list_paires[2])
        self.dict_order_book[self.list_paires[1] + self.list_paires[2]] = self.get_order_book(self.list_paires[1] + self.list_paires[2])
        self.dict_order_book[self.list_paires[0] + self.list_paires[1]] = self.get_order_book(self.list_paires[0] + self.list_paires[1])

    def get_diff(self):
        wallet = 100
        tmp1 = wallet / self.get_price_buy(self.list_paires[0] + self.list_paires[2])
        tmp2 = tmp1 * self.get_price_sell(self.list_paires[0] + self.list_paires[1])
        wallet = tmp2 * self.get_price_sell(self.list_paires[1] + self.list_paires[2])
        diff_buy_crypto_1 = (wallet - 100)

        wallet = 100
        tmp2 = wallet / self.get_price_buy(self.list_paires[1] + self.list_paires[2])
        tmp1 = tmp2 / self.get_price_buy(self.list_paires[0] + self.list_paires[1])
        wallet = tmp1 * self.get_price_sell(self.list_paires[0] + self.list_paires[2])
        diff_buy_crypto_2 = (wallet - 100)

        if diff_buy_crypto_1 > diff_buy_crypto_2:
            return (True, diff_buy_crypto_1)
        else:
            return (False, diff_buy_crypto_2)