import asyncio
from dagster import op
from scripts.top_exchanges import get_top_30_ex
from scripts.top_tokens import get_top_token
from prisma import Prisma


async def insert_to_db(data):
    async with Prisma() as prisma:
        await prisma.exchanges.create_many(data, skip_duplicates=True)

@op()
def fetch_top_exchanges_op():
    # fetch top exchanges on the basis of max volume traded in last 24 hours!
    top_exchanges = get_top_30_ex()
    obj_list = top_exchanges.map(lambda x: {"exchange": x})
    asyncio.run(insert_to_db(obj_list))
