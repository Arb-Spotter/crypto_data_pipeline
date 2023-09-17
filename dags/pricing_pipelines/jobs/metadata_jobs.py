



from dagster import job
from dags.pricing_pipelines.operations.exchanges_op import fetch_top_exchanges_op

from dags.pricing_pipelines.operations.tokens_op import fetch_token_from_binance_op


@job
def fetch_token_from_binance_job():
    fetch_token_from_binance_op()
    
@job
def fetch_top_exchanges_job():
    fetch_top_exchanges_op()
    