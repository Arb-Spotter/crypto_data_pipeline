from dags.pricing_pipelines.schedules.schedules import ohlcv_1day_schedule
from dagster import repository
from dags.pricing_pipelines.jobs.market_data_jobs import market_data_job

from dags.pricing_pipelines.jobs.metadata_jobs import (
    fetch_top_tokens,
)
from dags.pricing_pipelines.jobs.ohlcv_jobs import (
    fetch_ohlcv_data_1day,
    fetch_ohlcv_data_1hour,
    fetch_ohlcv_data_1min,
)


@repository
def main_repository():
    jobs = [
        fetch_top_tokens,
        fetch_ohlcv_data_1day,
        fetch_ohlcv_data_1min,
        fetch_ohlcv_data_1hour,
        market_data_job,
    ]
    schedules = [ohlcv_1day_schedule]
    monitors = []

    return jobs + schedules + monitors
