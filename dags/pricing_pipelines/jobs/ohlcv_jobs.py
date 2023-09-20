from dagster import job
from dags.pricing_pipelines.assets.tokens_and_exchanges.tokens_and_exchanges_assets import (
    exchanges_asset,
    tokens_asset,
)
from dags.pricing_pipelines.operations.exchanges_op import (
    fetch_ohlcv_data,
    fetch_top_exchanges_op,
    get_exchanges_from_db,
    ohlcv_1day_candle_size,
    ohlcv_1hour_candle_size,
    ohlcv_1min_candle_size,
)


@job
def fetch_ohlcv_data_1min():
    top_ex = exchanges_asset()
    tokens = tokens_asset()
    candle_size = ohlcv_1min_candle_size()
    tokens_data = get_exchanges_from_db(tokens, candle_size)
    tokens_data.map(lambda x: fetch_ohlcv_data(x, top_ex))


@job
def fetch_ohlcv_data_1hour():
    top_ex = exchanges_asset()
    tokens = tokens_asset()
    candle_size = ohlcv_1hour_candle_size()
    tokens_data = get_exchanges_from_db(tokens, candle_size)
    tokens_data.map(lambda x: fetch_ohlcv_data(x, top_ex))


@job
def fetch_ohlcv_data_1day():
    top_ex = exchanges_asset()
    tokens = tokens_asset()
    candle_size = ohlcv_1day_candle_size()
    tokens_data = get_exchanges_from_db(tokens, candle_size)
    tokens_data.map(lambda x: fetch_ohlcv_data(x, top_ex))
