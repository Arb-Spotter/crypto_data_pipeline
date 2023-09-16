import ccxt

def fetch_top_tokens(exchange_name):

    exchange = getattr(ccxt, exchange_name)()

    markets = exchange.load_markets()

    token_markets = [market for market in markets.values() if market['quote'] != 'USD']

    sorted_tokens = sorted(token_markets, key=lambda market: market['baseVolume'], reverse=True)

    top_30_tokens = sorted_tokens[:30]

    token_symbols = [market['symbol'] for market in top_30_tokens]

    return token_symbols
