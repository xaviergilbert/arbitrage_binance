from binance.client import Client


class Arbitrage:
    def __init__(self, client, list_paires):
        self.client = client
        self.list_paires = list_paires
        self.dict_order_book = {}
    
    #"BAKE", "BNB", "BUSD"
    def sell(self, wallet):
        print("SELL")
        wallet.amount[self.list_paires[0]] = wallet.amount[self.list_paires[2]] / self.get_price(self.list_paires[0] + self.list_paires[2])
        wallet.amount[self.list_paires[2]] = 0
        wallet.amount[self.list_paires[1]] = wallet.amount[self.list_paires[0]] * self.get_price(self.list_paires[0] + self.list_paires[1])
        wallet.amount[self.list_paires[0]] = 0
        wallet.amount[self.list_paires[2]] = wallet.amount[self.list_paires[1]] * self.get_price(self.list_paires[1] + self.list_paires[2])
        wallet.amount[self.list_paires[1]] = 0


    def buy(self, wallet):   
        print("BUY")
        wallet.amount[self.list_paires[1]] = wallet.amount[self.list_paires[2]] / self.get_price(self.list_paires[1] + self.list_paires[2])
        wallet.amount[self.list_paires[2]] = 0
        wallet.amount[self.list_paires[0]] = wallet.amount[self.list_paires[1]] / self.get_price(self.list_paires[0] + self.list_paires[1])
        wallet.amount[self.list_paires[1]] = 0
        wallet.amount[self.list_paires[2]] = wallet.amount[self.list_paires[0]] * self.get_price(self.list_paires[0] + self.list_paires[2])
        wallet.amount[self.list_paires[0]] = 0


    def new_request_price(self,paire):
        return float(self.get_order_book(paire)['bids'][0][0])

    def get_price(self, paire):
        return float(self.dict_order_book[paire]['bids'][0][0])

    def get_volume(self, paire):
        return float(self.dict_order_book[paire]['bids'][0][1])

    def get_order_book(self, paire): #requete api binance
        return self.client.get_order_book(symbol=paire)

#anciemment get_prices
    def maj_order_book(self):
        self.dict_order_book[self.list_paires[0] + self.list_paires[2]] = self.get_order_book(self.list_paires[0] + self.list_paires[2])
        self.dict_order_book[self.list_paires[1] + self.list_paires[2]] = self.get_order_book(self.list_paires[1] + self.list_paires[2])
        self.dict_order_book[self.list_paires[0] + self.list_paires[1]] = self.get_order_book(self.list_paires[0] + self.list_paires[1])

    def get_diff(self):
        self.prix_one_per_two = self.get_price(self.list_paires[0] + self.list_paires[2]) / self.get_price(self.list_paires[1] + self.list_paires[2])
        self.prix_constate = self.get_price(self.list_paires[0] + self.list_paires[1])
        return (self.prix_one_per_two - self.prix_constate) / self.prix_constate * 100


