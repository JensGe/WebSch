import random
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy.orm import Session

from app.database import db_models, frontier
from app.common import random_data_generator as rand_gen
from app.common import common_values as c
from app.data import data_generator as data_gen


def create_sample_crawler(db: Session, amount: int = 3):

    crawlers = []

    for _ in range(amount):
        crawlers.append(
            db_models.Crawler(
                uuid=str(uuid4()),
                contact="admin@owi-crawler.com",
                reg_date=datetime.now(tz=timezone.utc),
                name=rand_gen.random_academic_name(),
                location="Germany",
                tld_preference=data_gen.random_tld(),
            )
        )

    for crawler in crawlers:
        db.add(crawler)

    db.commit()

    for crawler in crawlers:
        db.refresh(crawler)

    return crawlers


def new_fqdn(fqdn_basis, fqdn_url_amount):
    return db_models.FqdnFrontier(
        fqdn=fqdn_basis,
        tld=fqdn_basis.split(".")[-1],
        fqdn_last_ipv4=rand_gen.get_random_ipv4(),
        fqdn_last_ipv6=rand_gen.random_example_ipv6(),
        fqdn_pagerank=data_gen.random_pagerank(),
        fqdn_crawl_delay=data_gen.random_crawl_delay(),
        fqdn_url_count=fqdn_url_amount,
    )


def new_url(url, fqdn, visited_ratio):
    if random.random() < visited_ratio:
        random_date_time = rand_gen.random_datetime()
    else:
        random_date_time = None

    return db_models.UrlFrontier(
        url=url,
        fqdn=fqdn,
        url_last_visited=random_date_time,
        url_blacklisted=False,
        url_bot_excluded=False,
    )


def new_ref(url_out, url_in):
    return db_models.URLRef(
        url_out=url_out, url_in=url_in, parsing_date=rand_gen.random_datetime(),
    )


def create_sample_frontier(
    db: Session,
    fqdns: int = c.fqdn_amount,
    min_url_amount: int = c.min_url,
    max_url_amount: int = c.max_url,
    visited_ratio: float = c.visited_ratio,
    connection_amount: int = c.connections,
):

    fqdn_bases = [rand_gen.get_random_fqdn() for _ in range(fqdns)]
    fqdn_url_amounts = [
        random.randint(min_url_amount, max_url_amount) for _ in range(fqdns)
    ]

    global_url_list = []
    fqdn_frontier = [new_fqdn(fqdn_bases[i], fqdn_url_amounts[i]) for i in range(fqdns)]

    db.bulk_save_objects(fqdn_frontier)
    db.commit()

    for fqdn in fqdn_bases:
        urls = rand_gen.random_urls(fqdn, fqdn_url_amounts[fqdn_bases.index(fqdn)])

        fqdn_url_list = [
            new_url(urls[i], fqdn, visited_ratio)
            for i in range(fqdn_url_amounts[fqdn_bases.index(fqdn)])
        ]

        db.bulk_save_objects(fqdn_url_list)
        db.commit()

        if connection_amount > 0:
            db_url_ref_list = []

            for url in fqdn_url_list:
                ref_urls = frontier.get_referencing_urls(db, url, connection_amount)
                ref_rows = [new_ref(ref_url.url, url.url) for ref_url in ref_urls]
                db_url_ref_list.extend(ref_rows)

            db.bulk_save_objects(db_url_ref_list)
            db.commit()

        global_url_list.extend(fqdn_url_list)

    return {"frontier": fqdn_frontier, "url_list": global_url_list}
