import asyncio
from dagster import DynamicOut, DynamicOutput, Output, op
import redis
from scripts.top_tokens import get_token_metadata, get_top_token
from prisma import Prisma

import logging

logger = logging.getLogger("mainlog")



async def insert_to_db(data):
    async with Prisma() as prisma:
        tokens_in_db = {i.token for i in await prisma.tokens.find_many()}
        tokens = {i["token"] for i in data}

        tokens_to_delete = tokens_in_db - tokens

        token_upsert_objects = []

        for i in data:
            if i["token"] in tokens_to_delete:
                pass

            token_upsert_objects.append(
                {
                    "where": {"token": i["token"]},
                    "data": {
                        "create": i,
                        "update": {
                            key: value for key, value in i.items() if key != "token"
                        },
                    },
                }
            )

        await prisma.tokens.delete_many({"token": {"in": list(tokens_to_delete)}})

        for i in token_upsert_objects:
            await prisma.tokens.upsert(**i)


@op()
def fetch_tokens_from_top2_op(exchanges):
    exchange1, exchange2, *_ = exchanges
    tokens = get_top_token(exchange1, exchange2, 30)
    logger.info(tokens)
    return Output(tokens)


@op
def fetch_symbol_meta_from_cg_op(tokens):
    metadata = get_token_metadata(tokens)
    logger.info(f"Metadata : {metadata}")
    return Output(metadata)


@op
def insert_tokens_to_db_op(metadata):
    asyncio.run(insert_to_db(metadata))


@op(out=DynamicOut())
def fan_out_tokens(tokens):
    for i in tokens:
        yield DynamicOutput(i, mapping_key=i)
