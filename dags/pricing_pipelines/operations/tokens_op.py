import asyncio
from dagster import DynamicOut, DynamicOutput, op
from scripts.top_tokens import get_top_token
from prisma import Prisma

import logging

logger = logging.getLogger("mainlog")

async def insert_to_db(data):
    async with Prisma() as prisma:
        await prisma.tokens.create_many(data, skip_duplicates=True)


@op()
def fetch_token_from_binance_op():
    tokens = get_top_token(30)
    logger.info(tokens)
    
    obj_list = [{"token": x} for x in tokens]
    asyncio.run(insert_to_db(obj_list))


@op(out=DynamicOut())
def fan_out_tokens(tokens):
    for i in tokens:
        yield DynamicOutput(i, mapping_key=i)