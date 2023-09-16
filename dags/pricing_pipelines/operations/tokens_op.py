import asyncio
from dagster import op
from scripts.top_tokens import get_top_token
from prisma import Prisma


async def insert_to_db(data):
    async with Prisma() as prisma:
        await prisma.tokens.create_many(data, skip_duplicates=True)


@op()
def fetch_token_from_binance_op():
    tokens = get_top_token(30)
    obj_list = tokens.map(lambda x: {"token": x})
    asyncio.run(insert_to_db(obj_list))
