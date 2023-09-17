
from dataclasses import dataclass


table_name_for_candle_size = {
    "1m": "one_min_ohlcv_data",
    "1h": "one_hour_ohlcv_data",
    "1d": "one_day_ohlcv_data",
}

gaps_report_table_for_candle_size = {
    "1m": "ohlcv_1min_gaps",
    "1h": "ohlcv_1hour_gaps",
    "1d": "ohlcv_1day_gaps",
}

days_from_for_candle_size = {"1m": 1, "1h": 30, "1d": 365}

millis_in_timeframe = {"1m": 60*1000, "1h": 60*60*1000, "1d": 24*60*60*1000}


@dataclass
class TokenData:
    table_name: str
    exchanges: list
    token: str
    candle_size: str
    days_from: int


import logging

def print_progress_bar(current_value, total_value, length=50, fill="█", msg = ""):
    progress = (current_value / total_value)
    arrow = fill * int(length * progress)
    spaces = " " * (length - len(arrow))
    progress_str = f"[{arrow}{spaces}] {int(progress * 100)}% " + msg
    logging.info(progress_str)
