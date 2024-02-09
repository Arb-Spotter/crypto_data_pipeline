import ccxt
import asyncio

from multiprocessing import Pool, cpu_count

import logging

logger = logging.getLogger("mainlog")

volumeField = "baseVolume"


def fetch_ticker(exchange, symbol):

    try:
        ticker = exchange.fetch_ticker(symbol)
        return {
            "exchange": exchange.id,
            volumeField: ticker[volumeField] if volumeField in ticker else -1,
        }
    except Exception as e:
        pass


def get_top_30_ex():

    exchanges_data = []
    exchanges = [getattr(ccxt, exchange_id)() for exchange_id in ccxt.exchanges]

    fetched_tickers = []
    with Pool(processes=cpu_count()) as pool:

        tasks = [(exchange, "ETH/USDT") for exchange in exchanges]
        fetched_tickers += pool.starmap(fetch_ticker, tasks)

    for ticker_data in fetched_tickers:
        if not ticker_data:
            continue
        if ticker_data[volumeField] != -1:
            exchanges_data.append(ticker_data)

    sorted_exchanges = sorted(
        exchanges_data, key=lambda x: x[volumeField] or -1, reverse=True
    )

    top_30_exchanges = sorted_exchanges[:30]

    exchanges = [ex["exchange"] for ex in top_30_exchanges]
    logger.info("Top 30 exchanges: {}".format(exchanges))
    return exchanges


if __name__ == "__main__":
    print("Exchange :", get_top_30_ex())
