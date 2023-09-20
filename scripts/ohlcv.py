from datetime import datetime, timedelta, timezone
import math
import time
import ccxt
from prisma import Prisma
import redis

from redis_rate_limit import RateLimit, TooManyRequests, TimeUnit


redis_pool = redis.ConnectionPool(host="keydb", port=6379, db=0)


from dags.pricing_pipelines.utils.common import (
    TokenData,
    gaps_report_table_for_candle_size,
    millis_in_timeframe,
    print_progress_bar,
    days_from_for_candle_size,
)

import logging

logger = logging.getLogger("mainlog")


async def start_ohlcv_handler(tokens_data: TokenData, top_exchanges):
    logger.error("called !!!!")
    fetch_attempts_left = 5 - len(tokens_data.exchanges)
    ex_in_db = tokens_data.exchanges
    token = tokens_data.token
    candle_size = tokens_data.candle_size
    table_name = tokens_data.table_name

    for exchange in ex_in_db:
        try:
            await fetch_ohlcv(token, exchange, candle_size, table_name)
        except Exception as e:
            logger.error(e)
            pass

    while fetch_attempts_left and top_exchanges:
        exchange = top_exchanges.pop(0)
        try:
            await fetch_ohlcv(token, exchange, candle_size, table_name)
        except (NoDataException, InvalidDataException):
            pass
        except Exception as e:
            logger.error(e)
            continue
        fetch_attempts_left -= 1


class NoDataException(Exception):
    pass


class InvalidDataException(Exception):
    pass


def fetch_ohlcv_from_ccxt(token, exchange, from_ts, candle_size):
    exchange_obj = getattr(ccxt, exchange)()

    with RateLimit(
        resource=exchange,
        client="ccxt2",
        max_requests=1,
        expire=exchange_obj.rateLimit,
        redis_pool=redis_pool,
        time_unit=TimeUnit.MILLISECOND,
    ):
        ohlcv_data = exchange_obj.fetch_ohlcv(f"{token}/USDT", candle_size, from_ts)

        if not ohlcv_data:
            raise NoDataException

        if ohlcv_data[-1][0] < from_ts:
            raise InvalidDataException


        return ohlcv_data


def milis_to_datetime(milis):
    return datetime.fromtimestamp(milis / 1000, tz=timezone.utc)


def datetime_to_milis(dt):
    return int(dt.timestamp() * 1000)


async def insert_ohlcv_to_db(ohlcv_data, table_name, token, exchange):
    try:
        async with Prisma() as prisma:
            ohlcv_records = [
                {
                    "token": token,
                    "exchange": exchange,
                    "updatedAt": milis_to_datetime(row[0]),
                    "open": row[1],
                    "high": row[2],
                    "low": row[3],
                    "close": row[4],
                    "volume": row[5],
                }
                for row in ohlcv_data
            ]

            logger.info(f"Inserting {len(ohlcv_records)} records into {table_name}!")
            rows_affected = await getattr(prisma, table_name).create_many(
                ohlcv_records, skip_duplicates=True
            )
            logger.info(f"Rows Affected - {rows_affected}")
    except Exception as e:

        logger.error(f"prisma failed - {e}")

async def get_data_gaps_in_series(token, exchange, candle_size, table_name):
    gaps_table_name = gaps_report_table_for_candle_size[candle_size]

    async with Prisma() as prisma:
        gaps_report = await getattr(prisma, gaps_table_name).find_many(
            where={"token": token, "exchange": exchange}
        )

        gap_series = [datetime_to_milis(gap.date_series) for gap in gaps_report]
        initial_len_gap_series = len(gap_series)

        while gap_series:
            gap_timestamp = gap_series[0]

            try:
                data = fetch_ohlcv_from_ccxt(token, exchange, gap_timestamp, candle_size)
            except TooManyRequests:
                continue
            
            while gap_series and gap_series[0] <= data[-1][0]:
                gap_series.pop(0)

            msg = f"Fetching data for {token}-{exchange}"
            print_progress_bar(len(gap_series), initial_len_gap_series, msg=msg)

            await insert_ohlcv_to_db(data, table_name, token, exchange)


async def exchange_exists_in_db(token, exchange, table_name):
    async with Prisma() as prisma:
        count = await getattr(prisma, table_name).count(
            where={"token": token, "exchange": exchange}
        )

        logger.error(f"count - {count}")

        return count != 0


def subtract_miliseconds_from_current_time(milliseconds_to_subtract):
    current_time = datetime.utcnow()
    delta = timedelta(milliseconds=milliseconds_to_subtract)
    result_time = current_time - delta

    # Set the time to 00:00:00 (midnight)
    result_time = result_time.replace(hour=0, minute=0, second=0, microsecond=0)
    result_time_millis = int(result_time.timestamp() * 1000)
    return result_time_millis


async def get_ohlcv_data_from_beggining(token, exchange, candle_size, table_name):
    milis_to_subtracs = days_from_for_candle_size[candle_size] * 24 * 60 * 60 * 1000
    from_ts = subtract_miliseconds_from_current_time(milis_to_subtracs)
    to_ts = int(time.time() * 1000)
    initial_diff = to_ts - from_ts

    while from_ts < to_ts:
        try:
            data = fetch_ohlcv_from_ccxt(token, exchange, from_ts, candle_size)
        except TooManyRequests:
            continue

        current_diff = initial_diff - (to_ts - from_ts)

        msg = f"Fetching data for {token}-{exchange}"
        print_progress_bar(current_diff, initial_diff, msg=msg)

        await insert_ohlcv_to_db(data, table_name, token, exchange)
        from_ts = data[-1][0] if data[-1][0] > from_ts else to_ts


async def fetch_ohlcv(token, exchange, candle_size, table_name):
    logger.error(f"fetching for - {token}-{exchange}")
    if await exchange_exists_in_db(token, exchange, table_name):
        await get_data_gaps_in_series(token, exchange, candle_size, table_name)
    else:
        await get_ohlcv_data_from_beggining(token, exchange, candle_size, table_name)
