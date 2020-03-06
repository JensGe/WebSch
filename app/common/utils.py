import random
from app.database.pyd_models import TLD


def get_random_tld():
    return random.choice([e.value for e in TLD])
