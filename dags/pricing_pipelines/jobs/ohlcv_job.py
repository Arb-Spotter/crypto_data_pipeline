from dagster import job
from dags.pricing_pipelines.assets.tokens_and_exchanges.tokens_and_exchanges_assets import exchanges_asset, tokens_asset
from dags.pricing_pipelines.operations.exchanges_op import fan_out_exchanges, fetch_top_exchanges_op, get_exchanges_from_db, ohlcv_1day_table_name, ohlcv_1hour_table_name, ohlcv_1min_table_name 
from dags.pricing_pipelines.operations.tokens_op import fan_out_tokens

@job
def fetch_ohlcv_data_1min():
    top_ex = exchanges_asset()
    tokens = tokens_asset()
    table_name = ohlcv_1min_table_name()
    tokens_data = get_exchanges_from_db(tokens, table_name)
    tokens_data.map(lambda x: fan_out_exchanges(x, top_ex))
    
@job
def fetch_ohlcv_data_1hour():
    top_ex = exchanges_asset()
    tokens = tokens_asset()
    table_name = ohlcv_1hour_table_name()
    tokens_data = get_exchanges_from_db(tokens, table_name)
    tokens_data.map(lambda x: fan_out_exchanges(x, top_ex))

@job
def fetch_ohlcv_data_1day():
    top_ex = exchanges_asset()
    tokens = tokens_asset()
    table_name = ohlcv_1day_table_name()
    tokens_data = get_exchanges_from_db(tokens, table_name)

    tokens_data.map(lambda x: fan_out_exchanges(x, top_ex))