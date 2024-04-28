import random
from datetime import timedelta


def random_time(start, end):
    return timedelta(
        seconds=random.randrange(int(timedelta(hours=start).total_seconds()), int(timedelta(hours=end).total_seconds()))
    )
