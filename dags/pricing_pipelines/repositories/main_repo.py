
from dagster import repository
from dags.pricing_pipelines.jobs.market_data_jobs import market_data_job

from dags.pricing_pipelines.jobs.metadata_jobs import fetch_token_from_binance_job, fetch_top_exchanges_job
from dags.pricing_pipelines.jobs.ohlcv_jobs import fetch_ohlcv_data_1day, fetch_ohlcv_data_1hour, fetch_ohlcv_data_1min


@repository
def main_repository():
    jobs = [fetch_token_from_binance_job, fetch_top_exchanges_job, fetch_ohlcv_data_1day, fetch_ohlcv_data_1min, fetch_ohlcv_data_1hour, market_data_job]
    schedules = []
    monitors = []

    return jobs + schedules + monitors