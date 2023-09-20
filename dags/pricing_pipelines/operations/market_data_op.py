import asyncio
import logging
import ccxt
from dagster import DynamicOut, DynamicOutput, op
from prisma import Prisma
import redis
from redis_rate_limit import RateLimit, TooManyRequests, TimeUnit

redis_pool = redis.ConnectionPool(host="keydb", port=6379, db=0)
logger = logging.getLogger("mainlog")



def get_ticker(token, exchange):
    exchange_obj = getattr(ccxt, exchange)()

    while True:
        try:
            with RateLimit(
                resource=exchange,
                client="ccxt2",
                max_requests=1,
                expire=exchange_obj.rateLimit,
                redis_pool=redis_pool,
                time_unit=TimeUnit.MILLISECOND,
            ):
                return exchange_obj.fetch_ticker(token + "/USDT")

        except TooManyRequests:
            continue


def get_bid_ask_spread(ticker):
    return float(ticker["bid"] or 0) - float(ticker["ask"] or 0)


async def insert_to_db(data):
    async with Prisma() as prisma:
        rows_affecteds = await prisma.market_data.create_many(data)
        logger.error(f"rows_affected - {rows_affecteds}")


@op(out=DynamicOut())
async def fetch_token_exchange_pair_from_db():
    async with Prisma() as prisma:
        data = await prisma.ohlcv_1day_gaps.find_many(distinct=["token", "exchange"])
        data = [[i.token, i.exchange] for i in data]
        chunk_size = 15
        # chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
        for i in range(0, len(data), chunk_size):
            yield DynamicOutput(data[i : i + chunk_size], f"batch_{i}")


@op
async def market_data_op(token_exchange_pairs):
    for i in range(300):
        await asyncio.sleep(5)
        data = []
        for token, exchange in token_exchange_pairs:
            try:
                ticker = get_ticker(token, exchange)
            except Exception as e:
                logger.error(e)
                continue

            b_a_spread = get_bid_ask_spread(ticker)
            volume_24h = ticker["quoteVolume"]
            high_24h = ticker["high"]
            low_24h = ticker["low"]
            close_24h = ticker["close"]
            open_24h = ticker["open"]
            change = ticker["change"]
            percentage_change = ticker["percentage"]

            data.append(
                {
                    "token": token,
                    "open": open_24h,
                    "high": high_24h,
                    "low": low_24h,
                    "close": close_24h,
                    "volume": volume_24h,
                    "exchange": exchange,
                    "percentage_change": percentage_change,
                    "change": change,
                    "b_a_spread": b_a_spread,
                }
            )

        await insert_to_db(data)
        logger.error(f"fetched for iteration-{i}")

# {
#     "symbol": "BTC/USDT",
#     "timestamp": 1695179386654,
#     "datetime": "2023-09-20T03:09:46.654Z",
#     "high": 27479.99,
#     "low": 26753.44,
#     "bid": 27194.06,
#     "bidVolume": 0.01819,
#     "ask": 27194.07,
#     "askVolume": 0.00074,
#     "vwap": 27155.35054224798,
#     "open": 26811.08,
#     "close": 27193.73,
#     "last": 27193.73,
#     "previousClose": None,
#     "change": 382.65,
#     "percentage": 1.43,
#     "average": 27002.405,
#     "baseVolume": 16303.9335,
#     "quoteVolume": 442739029.41,
#     "info": {
#         "symbol": "BTC_USDT",
#         "last_price": "27193.73",
#         "quote_volume_24h": "442739029.41",
#         "base_volume_24h": "16303.93350",
#         "high_24h": "27479.99",
#         "low_24h": "26753.44",
#         "open_24h": "26811.08",
#         "close_24h": "27193.73",
#         "best_ask": "27194.07",
#         "best_ask_size": "0.00074",
#         "best_bid": "27194.06",
#         "best_bid_size": "0.01819",
#         "fluctuation": "+0.0143",
#         "url": "https://www.bitmart.com/trade?symbol=BTC_USDT",
#         "timestamp": "1695179386654",
#     },
# }