from binance.client import Client
from time import sleep, time
from cle_api import cle
from arbitrage_bakebnb import BAKE_BNB
from arbitrage_cakebnb import CAKE_BNB



if __name__ == "__main__":
    # recuperation info api
    mes_clefs = cle()
    api_keys = (mes_clefs.api_key, mes_clefs.api_secret)
    client = Client(api_keys[0], api_keys[1])


    # init class arbitrage
    arbitrage_cake = CAKE_BNB(client)
    arbitrage_bake = BAKE_BNB(client)

    while True:
        # start_time = time()

        # arbitrage_cake.get_prices()
        arbitrage_bake.get_prices()


        # arbitrage_cake.print_diff()
        arbitrage_bake.print_diff()
        arbitrage_bake.print_volume()

        sleep(0.1)

        # end_time = time()
        # total_time = end_time - start_time
        # print("Time: ", total_time)
