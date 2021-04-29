from binance.client import Client

class BAKE_BNB:
    def __init__(self, client):
        self.client = client

    def get_prices(self):
        depth_bake = self.client.get_order_book(symbol='BAKEBUSD')
        depth_bnb = self.client.get_order_book(symbol='BNBBUSD')
        depth_bakebnb = self.client.get_order_book(symbol='BAKEBNB')

        self.prix_bake = depth_bake['bids'][0][0]
        self.montant_bake = depth_bake['bids'][0][1]
        self.prix_bnb = depth_bnb['bids']
        self.montant_bnb = depth_bnb['bids'][0][1]
        self.prix_bakebnb = depth_bakebnb['bids']
        self.montant_bakebnb = depth_bakebnb['bids'][0][1]

        self.prix_bake_per_bnb = float(self.prix_bake[0][0]) / float(self.prix_bnb[0][0])
        self.prix_constate = float(self.prix_bakebnb[0][0])
        self.diff = abs((self.prix_bake_per_bnb - self.prix_constate) / self.prix_constate * 100)

    def print_diff(self):
        print("diff bake: ", self.diff, "%")

    def print_volume(self):
        print("volume bake/busd : ", self.montant_bake)
        print("volume bake/bnb : ", self.montant_bakebnb)
        print("volume bnb/busd : ", self.montant_bnb)