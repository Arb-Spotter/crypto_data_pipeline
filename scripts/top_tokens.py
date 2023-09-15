import ccxt

def fetch_top_tokens(exchange):
    try:
        markets = exchange.load_markets()

        token_markets = [market for market in markets.values() if market['quote'] != 'USD']

        sorted_tokens = sorted(token_markets, key=lambda market: market['baseVolume'], reverse=True)

        top_30_tokens = sorted_tokens[:30]

        token_symbols = [market['symbol'] for market in top_30_tokens]

        return token_symbols

    except Exception as e:
        print(f"Error fetching top tokens from Kraken: {str(e)}")
        return []

def main():
    try:
        kraken = ccxt.kraken()
        top_tokens = fetch_top_tokens(kraken)

        print("Top 30 tokens on Kraken:")
        for token in top_tokens:
            print(token)

    except Exception as e:
        print(f"Error in main function: {str(e)}")

if __name__ == "__main__":
    main()
