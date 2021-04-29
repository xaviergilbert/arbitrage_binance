from binance.client import Client

class CAKE_BNB:
    def __init__(self, client):
        self.client = client

    def get_prices(self):
        depth_cake = self.client.get_order_book(symbol='CAKEUSDT')
        depth_bnb = self.client.get_order_book(symbol='BNBUSDT')
        depth_cakebnb = self.client.get_order_book(symbol='CAKEBNB')

        prix_cake = depth_cake['bids']
        prix_bnb = depth_bnb['bids']
        prix_cakebnb = depth_cakebnb['bids']

        self.prix_cake_per_bnb = float(prix_cake[0][0]) / float(prix_bnb[0][0])
        self.prix_constate = float(prix_cakebnb[0][0])
        self.diff = abs((self.prix_cake_per_bnb - self.prix_constate) / self.prix_constate * 100)

    def print_diff(self):
        print("diff cake: ", self.diff, "%")

        
