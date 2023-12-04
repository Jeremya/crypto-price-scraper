from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
import requests
import time
import datetime

# Connect to Cassandra
cluster = Cluster(['127.0.0.1'])
session = cluster.connect('btcscraper')

# Function to fetch prices for multiple cryptocurrencies
def fetch_crypto_prices(symbols):
    ids = ','.join(symbols)
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd'
    response = requests.get(url)
    return response.json()

# Function to insert cryptocurrency price into Cassandra
def insert_crypto_price(symbol, price):
    query = SimpleStatement("INSERT INTO crypto_prices (symbol, time, price) VALUES (%s, %s, %s)")
    session.execute(query, (symbol, datetime.datetime.now(), price))

# CoinGecko API symbols for the cryptocurrencies
crypto_symbols = {
    'bitcoin': 'BTC',
    'ethereum': 'ETH',
    'cosmos': 'ATOM',
    'dogecoin': 'DOGE'
}

# Main loop
try:
    while True:
        try:
            prices = fetch_crypto_prices(list(crypto_symbols.keys()))
            for api_symbol, symbol in crypto_symbols.items():
                price = prices.get(api_symbol, {}).get('usd')
                if price:
                    insert_crypto_price(symbol, price)
                    print(f"Inserted {symbol} price: {price}")
                else:
                    print(f"No price data for {symbol}")
        except Exception as e:
            print(f"Error fetching prices: {e}")
        time.sleep(60)  # Fetch price every minute
except KeyboardInterrupt:
    pass
finally:
    cluster.shutdown()
