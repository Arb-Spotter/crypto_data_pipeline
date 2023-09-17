from prisma import Prisma

from dags.pricing_pipelines.operations.exchanges_op import TokenData

exchanges_in_db = []
total_exchanges_to_maintain = 5

import logging
logger = logging.getLogger("mainlog")




async def fetch_ohlcv(tokens_data: TokenData):
    count = 5
    ex_in_db = []

    table_name = table_name_for_candle_size[candle_size]
    async with Prisma() as prisma:
        getattr(prisma, table_name)
        prisma.one_day_ohlcv_data.count()
