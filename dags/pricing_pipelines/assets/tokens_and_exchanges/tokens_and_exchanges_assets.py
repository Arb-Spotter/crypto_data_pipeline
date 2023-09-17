from dagster import asset
from prisma import Prisma
import logging
logger = logging.getLogger("mainlog")

@asset()
async def tokens_asset():
    async with Prisma() as prisma:
        tokens = await prisma.tokens.find_many()
        return [token.token for token in tokens]

@asset()
async def exchanges_asset():
    async with Prisma() as prisma:
        exchanges = await prisma.exchanges.find_many()
        logger.error(exchanges)
        return [exchange.exchange for exchange in exchanges]
