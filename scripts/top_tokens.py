import ccxt


def get_top_token(limit):
    exchange = ccxt.binance()

    markets = exchange.load_markets()

    token_pairs = [pair for pair, data in markets.items() if data['quote'] == 'USDT']

    sorted_tokens = sorted(token_pairs, key=lambda pair: markets[pair].get('quoteVolume') or -1, reverse=True)
    top_30_tokens_from_binance = [token.split("/")[0] for token in sorted_tokens]
    
    exchange = ccxt.kraken()

    markets = exchange.load_markets()
    token_pairs = [pair for pair, data in markets.items() if data['quote'].startswith('USDT')]

    sorted_tokens = sorted(token_pairs, key=lambda pair: markets[pair].get('quoteVolume') or -1, reverse=True)
    top_30_tokens_from_kraken = [token.split("/")[0] for token in sorted_tokens]

    common_tokens = [value for value in top_30_tokens_from_binance if value in top_30_tokens_from_kraken]

    top_tokens = []

    while common_tokens:
        poped_token = common_tokens.pop(0)
        if poped_token not in top_tokens:
            top_tokens.append(poped_token)

    print(f"Total of {len(top_tokens)} \nTokens - {top_tokens}")

