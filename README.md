# crypto-price-scraper
Retrieve crypto prices and store it in Cassandra using [Coingecko API](https://www.coingecko.com/en/api).


```shell
docker pull cassandra:2.1.22
docker run --name cassandra -p 9042:9042 -d cassandra:2.1.22
docker exec -it cassandra cqlsh
```


```sql
CREATE KEYSPACE btcscraper WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1 };

CREATE TABLE btcscraper.crypto_prices (
    symbol text,
    time timestamp,
    price float,
    PRIMARY KEY (symbol, time)
);
```

```shell
pip install -r requirements.txt
python main.py
```
