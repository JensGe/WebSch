import random
import string
from datetime import datetime, timedelta

from app.common import enum


def get_random_datetime():
    start = datetime(year=2019, month=1, day=1, hour=0, minute=0, second=0)
    end = datetime(year=2020, month=3, day=3, hour=0, minute=0, second=0)
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)


def get_random_tld():
    return random.choice([e.value for e in enum.TLD])


def get_random_sld():
    first_char = random.choice(string.ascii_lowercase)
    random_allowed_characters = string.ascii_lowercase + "0123456789-"
    last_char = random.choice(random_allowed_characters[:-1])
    sld = (
        first_char
        + "".join(
            random.choice(random_allowed_characters)
            for _ in range(random.randint(4, 12) - 1)
        )
        + last_char
    )
    return sld


def get_random_german_text(length: int = None):
    chars = [
        "e",
        "n",
        "i",
        "s",
        "r",
        "a",
        "t",
        "d",
        "h",
        "u",
        "l",
        "c",
        "g",
        "m",
        "o",
    ]
    distribution = [
        0.1740,
        0.0978,
        0.0755,
        0.0758,
        0.0700,
        0.0651,
        0.0615,
        0.0508,
        0.0476,
        0.0435,
        0.0344,
        0.0306,
        0.0301,
        0.0253,
        0.0251,
    ]

    if length is None:
        length = random.randint(3, 10)

    return "".join(random.choices(population=chars, weights=distribution, k=length))


def get_random_academic_name():
    return (
        str(random.choice([e.value for e in enum.ACADEMICS]))
        + " "
        + int_to_roman(random.randint(0, 1000))
    )


def get_random_fqdn():
    return "www." + get_random_sld() + "." + get_random_tld()


def get_random_ipv4():
    return "{}.{}.{}.{}".format(
        str(random.randint(0, 256)),
        str(random.randint(0, 256)),
        str(random.randint(0, 256)),
        str(random.randint(0, 256)),
    )


def get_random_hex():
    return random.choice(string.digits + "ABCDEF")


def get_random_example_ipv6():
    return "2001:DB8::{}{}{}{}".format(
        get_random_hex(), get_random_hex(), get_random_hex(), get_random_hex()
    )


def get_random_pagerank():
    return random.uniform(0, 0.0003)


def get_random_web_filename():
    file = random.choice(["/index", "/home", "/impressum", "/contact"])
    extension = random.choice([".php", ".html", ".aspx", "", "/"])
    return file + extension


def get_random_url(fqdn):
    return "http://{}/{}{}".format(
        fqdn, get_random_german_text(), get_random_web_filename()
    )


def int_to_roman(num):
    # Source: https://www.w3resource.com/python-exercises/class-exercises/python-class-exercise-1.php
    val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    syb = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    roman_num = ''
    i = 0
    while num > 0:
        for _ in range(num // val[i]):
            roman_num += syb[i]
            num -= val[i]
        i += 1
    return roman_num
