import random
import string
from datetime import datetime

from fastapi import HTTPException


def get_random_sld():
    length = random.randint(4, 12)
    first_char = random.choice(string.ascii_lowercase)
    random_allowed_characters = string.ascii_lowercase + "0123456789"
    sld = first_char + "".join(
        random.choice(random_allowed_characters) for i in range(length - 1)
    )
    return sld


def generate_tld_url_list(tld, length):

    url_list = {
        "length": length,
        "tld": tld,
        "fqdn": "http://www.example.com",
        "ipv4": "127.0.0.1",
        "urls": [],
    }

    if tld is None:
        for i in range(length):
            url = (
                "http://www."
                + get_random_sld()
                + "."
                + random.choice(["de", "co.uk", "fr", "com", "org"])
            )
            url_list["urls"].append(url)
    else:
        for i in range(length):
            url = "http://www." + get_random_sld() + "." + tld
            url_list["urls"].append(url)

    return url_list


def generate_frontier(crawler_uuid, amount, length, tld):
    if crawler_uuid != "12345678-90ab-cdef-0000-000000000000":
        raise HTTPException(
            status_code=404, detail="Crawler UUID not Found, please register at /crawler/"
        )

    frontier = {
        "amount": amount,
        "deliver_url": "http://www.example.com/submit",
        "url_lists": [],
    }

    for i in range(amount):
        frontier["url_lists"].append(generate_tld_url_list(tld, length))
    return frontier


def create_new_crawler(crawler):
    crawler.uuid = "12345678-90ab-cdef-0000-000000000000"
    crawler.reg_date = datetime.now()
    return crawler


def update_crawler(crawler):
    return crawler
