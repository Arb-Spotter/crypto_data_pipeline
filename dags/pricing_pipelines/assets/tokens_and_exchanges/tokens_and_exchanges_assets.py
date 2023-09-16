from dagster import asset
from prisma import Prisma

@asset()
async def tokens_asset():
    async with Prisma() as prisma:
        tokens = prisma.tokens.find_many()
        return [token["token"] for token in tokens]

@asset()
async def exchanges_asset():
    async with Prisma() as prisma:
        tokens = prisma.exchanges.find_many()
        return [token["exchange"] for token in tokens]