from dagster import job
from dags.pricing_pipelines.operations.exchanges_op import fetch_top_exchanges_op

from dags.pricing_pipelines.operations.tokens_op import (
    fetch_symbol_meta_from_cg_op,
    fetch_tokens_from_top2_op,
    insert_tokens_to_db_op,
)


@job
def fetch_top_tokens():
    exchanges = fetch_top_exchanges_op()
    tokens = fetch_tokens_from_top2_op(exchanges)
    metadata = fetch_symbol_meta_from_cg_op(tokens)
    insert_tokens_to_db_op(metadata)


@job
def fetch_top_exchanges_job():
    fetch_top_exchanges_op()
