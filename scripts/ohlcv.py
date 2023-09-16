from prisma import Prisma

exchanges_in_db = []
total_exchanges_to_maintain = 5


table_name_for_candle_size = {
    "1m": "one_min_ohlcv_data ", 
    "1h": "one_hour_ohlcv_data ",
    "1d": "one_day_ohlcv_data "
}


async def fetch_ohlcv(token, candle_size):
    count = 5
    ex_in_db = []

    table_name = table_name_for_candle_size[candle_size]
    async with Prisma() as prisma:
        getattr(prisma, table_name)
        prisma.one_day_ohlcv_data.count()

    
    
    