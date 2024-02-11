import ccxt
import logging
import redis
from redis_rate_limit import RateLimit, TooManyRequests, TimeUnit

redis_pool = redis.ConnectionPool(host="keydb", port=6379, db=0)

logger = logging.getLogger("mainlog")


def get_top_token(exchange1, exchange2, limit):
    exchange = getattr(ccxt, exchange1)()

    markets = exchange.load_markets()

    token_pairs = [pair for pair, data in markets.items() if data["quote"] == "USDT"]

    sorted_tokens = sorted(
        token_pairs,
        key=lambda pair: markets[pair].get("quoteVolume") or -1,
        reverse=True,
    )
    top_30_tokens_from_binance = [token.split("/")[0] for token in sorted_tokens]

    exchange = getattr(ccxt, exchange2)()

    markets = exchange.load_markets()
    token_pairs = [
        pair for pair, data in markets.items() if data["quote"].startswith("USDT")
    ]

    sorted_tokens = sorted(
        token_pairs,
        key=lambda pair: markets[pair].get("quoteVolume") or -1,
        reverse=True,
    )
    top_30_tokens_from_kraken = [token.split("/")[0] for token in sorted_tokens]

    common_tokens = [
        value
        for value in top_30_tokens_from_binance
        if value in top_30_tokens_from_kraken
    ]

    top_tokens = []

    while common_tokens:
        poped_token = common_tokens.pop(0)
        if poped_token not in top_tokens:
            top_tokens.append(poped_token)

    return top_tokens[:limit]


import requests


def search_cg(query):
    url = "https://api.coingecko.com/api/v3/search"
    params = {"query": query}
    headers = {"accept": "application/json"}
    while True:
        try:
            with RateLimit(
                resource="coin_gecko",
                client="coin_gecko",
                max_requests=5,
                expire=60,
                redis_pool=redis_pool,
                time_unit=TimeUnit.SECOND,
            ):
                response = requests.get(url, params=params, headers=headers)
                if response.status_code == 200:
                    logger.info(f"fetched cg_meta for {query}")
                    return response.json()
                else:
                    raise Exception("Failed to fetch data!", response.status_code)

        except TooManyRequests:
            continue


def get_token_metadata(tokens):
    tokens_metadata = []
    for token in tokens:
        token_data = {"token": token}

        try:
            cg_data = search_cg(token)
            coin = cg_data["coins"][0]
            token_data["name"] = coin["name"]
            token_data["thumb"] = coin["thumb"]
            token_data["large"] = coin["large"]
        except Exception as e:
            logger.error(e)

        tokens_metadata.append(token_data)
    return tokens_metadata


if __name__ == "__main__":
    tokens = get_top_token(30)
    print(f"Total Tokens - {tokens} : {len(tokens)}")
