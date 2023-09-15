
from dagster import repository


@repository
def main_repository():
    jobs = []
    schedules = []
    monitors = []

    return jobs + schedules + monitors