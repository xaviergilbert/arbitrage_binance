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
        wallet.amount[self.list_paires[0]] = wallet.amount[self.list_paires[2]] / self.get_price(self.list_paires[0] + self.list_paires[2])
        wallet.amount[self.list_paires[2]] = 0
        self.maj_order_book()
        wallet.amount[self.list_paires[1]] = wallet.amount[self.list_paires[0]] * self.get_price(self.list_paires[0] + self.list_paires[1])
        wallet.amount[self.list_paires[0]] = 0
        self.maj_order_book()
        wallet.amount[self.list_paires[2]] = wallet.amount[self.list_paires[1]] * self.get_price(self.list_paires[1] + self.list_paires[2])
        wallet.amount[self.list_paires[1]] = 0


    def buy_by_second_crypto(self, wallet): # if positive diff
        print("BUY", [self.list_paires[1]])
        self.maj_order_book()
        wallet.amount[self.list_paires[1]] = wallet.amount[self.list_paires[2]] / self.get_price(self.list_paires[1] + self.list_paires[2])
        wallet.amount[self.list_paires[2]] = 0
        self.maj_order_book()
        wallet.amount[self.list_paires[0]] = wallet.amount[self.list_paires[1]] / self.get_price(self.list_paires[0] + self.list_paires[1])
        wallet.amount[self.list_paires[1]] = 0
        self.maj_order_book()
        wallet.amount[self.list_paires[2]] = wallet.amount[self.list_paires[0]] * self.get_price(self.list_paires[0] + self.list_paires[2])
        wallet.amount[self.list_paires[0]] = 0


    def new_request_price(self,paire):
        return float(self.get_order_book(paire)['bids'][0][0])

    def get_price(self, paire):
        return float(self.dict_order_book[paire]['bids'][0][0])

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
        self.prix_one_per_two = self.get_price(self.list_paires[0] + self.list_paires[2]) / self.get_price(self.list_paires[1] + self.list_paires[2])
        self.prix_constate = self.get_price(self.list_paires[0] + self.list_paires[1])
        return (self.prix_one_per_two - self.prix_constate) / self.prix_constate * 100


        # tmp1 = (self.prix_one_per_two - self.prix_constate) / self.prix_constate * 100


        # tmp2 =

        # return (tmp1, tmp2)