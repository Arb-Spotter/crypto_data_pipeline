


from dagster import op
from scripts.top_tokens_binance import get_top_token



@op()
def get_tokens():
    tokens = get_top_token()

    prisma



