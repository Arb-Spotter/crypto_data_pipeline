

from dagster import job

from dags.pricing_pipelines.operations.market_data_op import fetch_token_exchange_pair_from_db, market_data_op




@job
def market_data_job():
    token_exchange_batches = fetch_token_exchange_pair_from_db()
    token_exchange_batches.map(lambda batch: market_data_op(batch))