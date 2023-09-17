import asyncio
from dagster import DynamicOut, DynamicOutput, In, Output, op
from dags.pricing_pipelines.assets.tokens_and_exchanges.tokens_and_exchanges_assets import (
    tokens_asset,
)
from dags.pricing_pipelines.utils.common import TokenData, table_name_for_candle_size, days_from_for_candle_size
from scripts.ohlcv import start_ohlcv_handler
from scripts.top_exchanges import get_top_30_ex
from prisma import Prisma
import logging

logger = logging.getLogger("mainlog")



async def insert_to_db(data):
    async with Prisma() as prisma:
        await prisma.exchanges.create_many(data, skip_duplicates=True)


@op()
def ohlcv_1min_candle_size():
    return Output("1m")


@op()
def ohlcv_1hour_candle_size():
    return Output("1h")


@op()
def ohlcv_1day_candle_size():
    return Output("1d")


@op()
def fetch_top_exchanges_op():
    # fetch top exchanges on the basis of max volume traded in last 24 hours!
    top_exchanges = get_top_30_ex()

    logger.info(top_exchanges)

    obj_list = [{"exchange": x} for x in top_exchanges]
    asyncio.run(insert_to_db(obj_list))


async def get_unique_exchanges(prisma, table_name, token):
    exchanges = await getattr(prisma, table_name).find_many(
        where={"token": token}, distinct=["exchange"]
    )
    return [exchange.exchange for exchange in exchanges]


@op(out=DynamicOut())
async def get_exchanges_from_db(tokens, candle_size):
    table_name = table_name_for_candle_size[candle_size]
    days_from = days_from_for_candle_size[candle_size]

    async with Prisma() as prisma:
        for token in tokens:
            exchanges = await get_unique_exchanges(prisma, table_name, token)
            data = TokenData(table_name, exchanges, token, candle_size, days_from)
            yield DynamicOutput(data, mapping_key=f"{token}_{table_name}")


@op()
async def fetch_ohlcv_data(tokens_data: TokenData, all_top_exchanges):
    top_exchanges_except_in_db = [
        i for i in all_top_exchanges if i not in tokens_data.exchanges
    ]
    await start_ohlcv_handler(tokens_data, top_exchanges_except_in_db)
