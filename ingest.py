import concurrent.futures
import datetime
import random
import string
from datetime import timedelta, datetime

import requests


alphanumeric_characters = string.ascii_lowercase + string.digits


def random_datetime(start_date: datetime, end_date: datetime) -> datetime:
    date_difference = end_date - start_date
    random_days = random.randint(0, date_difference.days-1)
    random_time = random.randint(0, 24 * 60 * 60)
    return start_date + timedelta(days=random_days, seconds=random_time)


def ingest_random_log():
    log = {
        "level": random.choice(["debug", "info", "warn", "error"]),
        "message": random.choice(["Failed to connect", "Happy to fail", "success like never before", "unhappy ending"]),
        "resourceId": ''.join([random.choice(alphanumeric_characters) for _ in range(10)]),
        "timestamp": random_datetime(datetime(2023, 11, 1), datetime(2023, 11, 10)).strftime("%Y-%m-%dT%H:%M:%S"),
        "traceId": ''.join([random.choice(alphanumeric_characters) for _ in range(8)]),
        "spanId": ''.join([random.choice(alphanumeric_characters) for _ in range(7)]),
        "commit": ''.join([random.choice(alphanumeric_characters) for _ in range(6)]),
        "metadata": {
            "parentResourceId": ''.join([random.choice(alphanumeric_characters) for _ in range(10)]),
        }
    }
    requests.post("http://localhost:3000/add", json=log)


def ingest_random_logs(count: int):
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(ingest_random_log) for _ in range(count)]
        concurrent.futures.wait(futures)


ingest_random_logs(10000000)

