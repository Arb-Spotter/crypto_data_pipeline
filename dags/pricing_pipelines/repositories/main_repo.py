
from dagster import repository

from dags.pricing_pipelines.jobs.metadata_jobs import fetch_token_from_binance_job, fetch_top_exchanges_job


@repository
def main_repository():
    jobs = [fetch_token_from_binance_job, fetch_top_exchanges_job]
    schedules = []
    monitors = []

    return jobs + schedules + monitors