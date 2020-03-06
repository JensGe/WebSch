import random
from app.database.schemas import TLD


def get_random_tld():
    return random.choice([e.value for e in TLD])
