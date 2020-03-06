import random
import string
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from app.database import pyd_models, db_models, crud

from fastapi import HTTPException


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
    sld = first_char + "".join(
        random.choice(random_allowed_characters)
        for i in range(random.randint(4, 12) - 1)
    )
    return sld


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
    return random.choice(string.digits + "abcdef")


def get_random_ipv6():
    return "2001:DB8::{}".format(get_random_hex() * 4)


def get_random_pagerank():
    return str(random.uniform(0, 0.0003))


def get_random_web_filename():
    file = random.choice(["/index", "/home", "/impressum", "/contact"])
    extension = random.choice([".php", ".html", ".aspx", "", "/"])
    return file + extension


def get_random_url(fqdn):
    return "{}/{}{}".format(fqdn, get_random_sld(), get_random_web_filename())


#
# def generate_tld_url_list(tld, length):
#     url_list = {
#         "length": length,
#         "tld": tld,
#         "fqdn": "http://www.example.com",
#         "ipv4": "127.0.0.1",
#         "urls": [],
#     }
#
#     if tld is None:
#         for i in range(length):
#             url = (
#                 "http://www."
#                 + get_random_sld()
#                 + "."
#                 + random.choice([e.value for e in pyd_models.TLD])
#             )
#             url_list["urls"].append(url)
#     else:
#         for i in range(length):
#             url = "http://www." + get_random_sld() + "." + tld
#             url_list["urls"].append(url)
#
#     return url_list
#
#
# def generate_frontier(crawler_uuid, amount, length, tld):
#     if str(crawler_uuid) != "12345678-90ab-cdef-0000-000000000000":
#         raise HTTPException(
#             status_code=404,
#             detail="Crawler UUID {} not Found, please register at /crawler/".format(
#                 crawler_uuid
#             ),
#         )
#
#     frontier = {
#         "amount": amount,
#         "deliver_url": "http://www.example.com/submit",
#         "url_lists": [],
#     }
#
#     for i in range(amount):
#         frontier["url_lists"].append(generate_tld_url_list(tld, length))
#     return frontier


def create_sample_crawler(db: Session):
    crawler_1 = db_models.Crawler(
        uuid="12345678-90ab-cdef-0000-000000000001",
        contact="admin@german-crawler.de",
        reg_date=datetime.now(),
        name="German Crawler Eins",
        location="Germany",
        tld_preference="de",
    )

    crawler_2 = db_models.Crawler(
        uuid="12345678-90ab-cdef-0000-000000000002",
        contact="admin@german-crawler.de",
        reg_date=datetime.now(),
        name="German Crawler Zwei",
        location="Germany",
        tld_preference="de",
    )

    crawler_3 = db_models.Crawler(
        uuid="12345678-90ab-cdef-0000-000000000003",
        contact="admin@us-crawler.com",
        reg_date=datetime.now(),
        name="US Crawler One",
        location="USA",
        tld_preference="com",
    )

    db.add(crawler_1)
    db.add(crawler_2)
    db.add(crawler_3)

    db.commit()

    db.refresh(crawler_1)
    db.refresh(crawler_2)
    db.refresh(crawler_3)

    return [crawler_1, crawler_2, crawler_3]


def create_sample_frontier(
    db: Session, fqdns: int = 20, url_range: (int, int) = (50, 100)
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

        for i in range(random.randrange(*url_range)):
            global_url_list.append(
                db_models.Url(
                    url=get_random_url(item.fqdn),
                    fqdn_uri=item.fqdn,
                    url_last_visited=get_random_datetime(),
                    url_blacklisted=False,
                    url_bot_excluded=False,
                )
            )

    for item in global_url_list:
        db.add(item)

    db.commit()

    return {"frontier": fqdn_frontier,
            "url_list": global_url_list}
