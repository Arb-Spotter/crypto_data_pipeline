import asyncio
from dagster import DynamicOut, DynamicOutput, In, Output, op
from dags.pricing_pipelines.assets.tokens_and_exchanges.tokens_and_exchanges_assets import tokens_asset
from scripts.top_exchanges import get_top_30_ex
from scripts.top_tokens import get_top_token
from prisma import Prisma

import logging
logger = logging.getLogger("mainlog")
from dataclasses import dataclass


@dataclass
class TokenData:

    table_name: str
    exchanges: list
    token: str




async def insert_to_db(data):
    async with Prisma() as prisma:
        await prisma.exchanges.create_many(data, skip_duplicates=True)


@op()
def ohlcv_1min_table_name():
    return Output("one_min_ohlcv_data")

@op()
def ohlcv_1hour_table_name():
    return Output("one_hour_ohlcv_data")

@op()
def ohlcv_1day_table_name():
    return Output("one_day_ohlcv_data")


@op()
def fetch_top_exchanges_op():
    # fetch top exchanges on the basis of max volume traded in last 24 hours!
    top_exchanges = get_top_30_ex()

    logger.info(top_exchanges)

    obj_list = [{"exchange": x} for x in top_exchanges]
    asyncio.run(insert_to_db(obj_list))

async def get_unique_exchanges(prisma, table_name, token):
    exchanges = await getattr(prisma, table_name).find_many(
        where={"token": token},
        distinct=["exchange"]
    )
    return [exchange.exchange for exchange in exchanges]

@op(out=DynamicOut())
async def get_exchanges_from_db(tokens, table_name):
    async with Prisma() as prisma:
        for token in tokens: 
            exchanges = await get_unique_exchanges(prisma, table_name, token)
            data = TokenData(table_name, exchanges, token)
            yield DynamicOutput(data, mapping_key=f"{token}_{table_name}")


@op()
async def fan_out_exchanges(unique_exchanges_in_db, fetch_top_exchanges_op):
    logger.error(unique_exchanges_in_db)
    logger.error(fetch_top_exchanges_op)
    