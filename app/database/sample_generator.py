import random
from datetime import datetime
from uuid import uuid4

from sqlalchemy.orm import Session

from app.database import db_models
from app.common import random_data_generator as rand_gen


def create_sample_crawler(db: Session, amount: int = 3):

    crawlers = []

    for i in range(amount):
        crawlers.append(
            db_models.Crawler(
                uuid=str(uuid4()),
                contact="admin@owi-crawler.com",
                reg_date=datetime.now(),
                name="OWI Crawler {}".format(rand_gen.get_random_german_text().title()),
                location="Germany",
                tld_preference=rand_gen.get_random_tld(),
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
    fqdn_basis = [rand_gen.get_random_fqdn() for _ in range(fqdns)]

    global_url_list = []

    fqdn_frontier = []
    for i in range(fqdns):
        fqdn_frontier.append(
            db_models.FqdnFrontier(
                fqdn=fqdn_basis[i],
                tld=fqdn_basis[i].split(".")[-1],
                fqdn_last_ipv4=rand_gen.get_random_ipv4(),
                fqdn_last_ipv6=rand_gen.get_random_ipv6(),
                fqdn_pagerank=rand_gen.get_random_pagerank(),
                fqdn_crawl_delay=5,
                fqdn_url_count=0,
            )
        )

    for item in fqdn_frontier:
        db.add(item)

    db.commit()

    for fqdn in fqdn_basis:
        for i in range(random.randint(min_url_amount, max_url_amount)):
            global_url_list.append(
                db_models.Url(
                    url=rand_gen.get_random_url(fqdn),
                    fqdn=fqdn,
                    url_last_visited=rand_gen.get_random_datetime(),
                    url_blacklisted=False,
                    url_bot_excluded=False,
                )
            )

    for item in global_url_list:
        db.add(item)

    db.commit()
    return {"frontier": fqdn_frontier, "url_list": global_url_list}
