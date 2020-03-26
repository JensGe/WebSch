from app.database import db_models, pyd_models
from app.common import enum

from sqlalchemy.sql.expression import func


def get_fqdn_list(db, request):
    fqdn_list = db.query(db_models.FqdnFrontier)

    # Filter
    if request.tld is not None:
        fqdn_list = fqdn_list.filter(db_models.FqdnFrontier.tld == request.tld)

    # Order
    if request.prio_mode == enum.PRIO.random:
        fqdn_list = fqdn_list.order_by(func.random())

    if request.prio_mode == enum.PRIO.batch_page_rank:
        fqdn_list = fqdn_list.order_by(db_models.FqdnFrontier.fqdn_pagerank.desc())

    # Limit
    if request.amount > 0:
        fqdn_list = fqdn_list.limit(request.amount)

    return fqdn_list


def get_db_url_list(db, request, fqdn):
    db_url_list = (
        db.query(db_models.Url)
            .filter(db_models.Url.fqdn == fqdn.fqdn)
            .order_by(db_models.Url.url_last_visited.asc())
    )

    db_url_list = db_url_list[: request.length] if request.length > 0 else db_url_list

    return db_url_list


def create_url_frontier(fqdn, url_list):
    return pyd_models.UrlFrontier(
        fqdn=fqdn.fqdn,
        tld=fqdn.tld,
        url_list=url_list,
        fqdn_last_ipv4=fqdn.fqdn_last_ipv4,
        fqdn_last_ipv6=fqdn.fqdn_last_ipv6,
        fqdn_pagerank=fqdn.fqdn_pagerank,
        fqdn_crawl_delay=fqdn.fqdn_crawl_delay,
        fqdn_url_count=len(url_list),
    )
