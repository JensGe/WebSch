import random
import string
from app.common.models import TLD


def get_random_sld():
    length = random.randint(4, 12)
    first_char = random.choice(string.ascii_lowercase)
    random_allowed_characters = string.ascii_lowercase + "0123456789-"
    sld = first_char + "".join(
        random.choice(random_allowed_characters) for i in range(length - 1)
    )
    return sld


def generate_tld_url_list(location, length):
    url_list = []

    if location is None:
        for i in range(length):
            url = (
                "http://www."
                + get_random_sld()
                + "."
                + random.choice(["de", "co.uk", "fr", "com", "org"])
            )
            url_list.append({"url": url})
    else:
        for i in range(length):
            url = "http://www." + get_random_sld() + "." + location
            url_list.append({"url": url})

    return url_list


def generate_frontier(location, amount, length):
    url_collection = []
    for i in range(amount):
        url_collection.append(generate_tld_url_list(location, length))
    return url_collection


def create_new_crawler(crawler):
    return True
