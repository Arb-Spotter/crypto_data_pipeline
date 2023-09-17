from datetime import datetime, timezone
import ccxt
from prisma import Prisma

from dags.pricing_pipelines.utils.common import (
    TokenData,
    gaps_report_table_for_candle_size,
    millis_in_timeframe,
    print_progress_bar,
)


exchanges_in_db = []
total_exchanges_to_maintain = 5

import logging

logger = logging.getLogger("mainlog")


async def start_ohlcv_handler(tokens_data: TokenData, top_exchanges):
    logger.error("called !!!!")
    fetch_attempts_left = 5 - len(tokens_data.exchanges)
    ex_in_db = tokens_data.exchanges
    token = tokens_data.token
    candle_size = tokens_data.candle_size
    days_from = tokens_data.days_from
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


class NoDataException(Exception):
    pass


class InvalidDataException(Exception):
    pass


def fetch_ohlcv_from_ccxt(token, exchange, from_ts, candle_size):
    timestamp_ms = int(from_ts.timestamp() * 1000)

    exchange_obj = getattr(ccxt, exchange)()

    ohlcv_data = exchange_obj.fetch_ohlcv(token, candle_size, timestamp_ms)

    if ohlcv_data[-1][0] < timestamp_ms:
        raise InvalidDataException

    if not ohlcv_data:
        raise NoDataException

    return ohlcv_data


def milis_to_datetime(milis):
    return datetime.fromtimestamp(milis / 1000, tz=timezone.utc)


def datetime_to_milis(dt):
    return int(dt.timestamp() * 1000)


async def insert_ohlcv_to_db(ohlcv_data, table_name):
    async with Prisma() as prisma:
        ohlcv_records = [
            {
                "updatedAt": row[0],
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
            data = fetch_ohlcv_from_ccxt(token, exchange, candle_size, table_name, gap_timestamp)

            while gap_series and gap_series[0] <= data[-1][0]:
                gap_series.pop(0)

            await insert_ohlcv_to_db(data, table_name)
            print_progress_bar(len(gap_series), initial_len_gap_series)


async def fetch_ohlcv(token, exchange, candle_size, table_name):
    await get_data_gaps_in_series(token, exchange, candle_size, table_name)
