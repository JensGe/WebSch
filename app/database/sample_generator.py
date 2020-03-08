import random
import string
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from app.database import pyd_models, db_models, crud
from uuid import uuid4


def get_random_datetime():
    start = datetime(year=2019, month=1, day=1, hour=0, minute=0, second=0)
    end = datetime(year=2020, month=3, day=3, hour=0, minute=0, second=0)
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)


def get_random_tld():
    return random.choice([e.value for e in pyd_models.TLD])


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
        "b",
        "w",
        "f",
        "k",
        "z",
        "p",
        "v",
        "j",
        "y",
        "x",
        "q",
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
        0.0189,
        0.0189,
        0.0166,
        0.0121,
        0.0113,
        0.0079,
        0.0067,
        0.0027,
        0.0004,
        0.0003,
        0.0002,
    ]

    if length is None:
        length = random.randint(3, 10)

    return "".join(random.choices(population=chars, weights=distribution, k=length))


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


def get_random_ipv6():
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


def create_sample_crawler(db: Session, amount: int = 3):

    crawlers = []

    for i in range(amount):
        crawlers.append(
            db_models.Crawler(
                uuid=str(uuid4()),
                contact="admin@owi-crawler.com",
                reg_date=datetime.now(),
                name="OWI Crawler {}".format(get_random_german_text().title()),
                location="Germany",
                tld_preference=get_random_tld(),
            )
        )

    for crawler in crawlers:
        db.add(crawler)

    db.commit()

    for crawler in crawlers:
        db.refresh(crawler)

    return crawlers


def create_sample_frontier(
    db: Session, fqdns: int = 20, min_url_amount: int = 50, max_url_amount: int = 100
):
    fqdn_basis = [get_random_fqdn() for _ in range(fqdns)]

    fqdn_frontier = []
    for i in range(fqdns):
        fqdn_frontier.append(
            db_models.FqdnFrontier(
                fqdn=fqdn_basis[i],
                tld=fqdn_basis[i].split(".")[-1],
                fqdn_last_ipv4=get_random_ipv4(),
                fqdn_last_ipv6=get_random_ipv6(),
                fqdn_pagerank=get_random_pagerank(),
                fqdn_crawl_delay=5,
                fqdn_url_count=0,
            )
        )

    global_url_list = []

    for item in fqdn_frontier:
        db.add(item)

        for i in range(random.randrange(min_url_amount, max_url_amount)):
            global_url_list.append(
                db_models.Url(
                    url=get_random_url(item.fqdn),
                    fqdn=item.fqdn,
                    url_last_visited=get_random_datetime(),
                    url_blacklisted=False,
                    url_bot_excluded=False,
                )
            )

    for item in global_url_list:
        db.add(item)

    db.commit()

    return {"frontier": fqdn_frontier, "url_list": global_url_list}
