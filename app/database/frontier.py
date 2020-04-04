from datetime import datetime, timedelta

from app.database import db_models, pyd_models, crawlers
from app.common import enum, http_exceptions as http_ex, common_values as c

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

    rv = [item for item in fqdn_list]
    return rv


def get_db_url_list(db, request, fqdn):
    db_url_list = (
        db.query(db_models.UrlFrontier)
        .filter(db_models.UrlFrontier.fqdn == fqdn.fqdn)
        .order_by(db_models.UrlFrontier.url_last_visited.asc())
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


def get_referencing_urls(db, url, amount):
    return (
        db.query(db_models.UrlFrontier)
        .filter(db_models.UrlFrontier.url_last_visited < url.url_last_visited)
        .order_by(func.random())
        .limit(amount)
    )


def get_url_list_from_frontier_response(frontier_response):
    url_list = []
    for url_frontier in frontier_response.url_frontiers:
        url_list.extend([str(url.url) for url in url_frontier.url_list])

    return url_list


def get_only_new_list_items(new_list, old_list):

    only_new_list = [item for item in new_list if item not in old_list]

    return only_new_list


def save_crawler_urls(db, frontier_response, latest_return):
    uuid = frontier_response.uuid

    frontier_url_only_list = get_url_list_from_frontier_response(frontier_response)
    # print("** frontier_url_only_list: {}".format(str(frontier_url_only_list)))

    db_crawler_url_list = (
        db.query(db_models.CrawlerUrl)
        .filter(db_models.CrawlerUrl.crawler_uuid == uuid)
        .filter(db_models.CrawlerUrl.latest_return > datetime.now())
        .all()
    )
    db_crawler_url_only_list = [url.url for url in db_crawler_url_list]
    # print("** db_crawler_url_only_list: {}".format(str(db_crawler_url_only_list)))

    new_crawler_url_only_list = get_only_new_list_items(
        frontier_url_only_list, db_crawler_url_only_list
    )

    # print("** new_crawler_url_only_list: {}".format(str(new_crawler_url_only_list)))

    new_crawler_url_list = [
        db_models.CrawlerUrl(
            crawler_uuid=str(uuid),
            url=str(url),
            latest_return=latest_return,
        )
        for url in new_crawler_url_only_list
    ]
    # print("** new_crawler_url_list: {}".format(str(new_crawler_url_list)))

    db.bulk_save_objects(new_crawler_url_list)
    db.commit()
    return True


def get_fqdn_frontier(db, request: pyd_models.FrontierRequest):
    if not crawlers.uuid_exists(db, str(request.crawler_uuid)):
        http_ex.raise_http_404(request.crawler_uuid)

    frontier_response = pyd_models.FrontierResponse(uuid=str(request.crawler_uuid))
    fqdn_list = get_fqdn_list(db, request)

    for fqdn in fqdn_list:
        url_list = list(get_db_url_list(db, request, fqdn))

        frontier_response.urls_count += len(url_list)
        frontier_response.url_frontiers.append(create_url_frontier(fqdn, url_list))

    frontier_response.url_frontiers_count = len(frontier_response.url_frontiers)

    # sync crawler_url_connection persisting
    latest_return = datetime.now() + timedelta(hours=c.hours_to_die)
    save_crawler_urls(db, frontier_response, latest_return)

    frontier_response.latest_return = latest_return
    frontier_response.response_url = c.response_url + str(request.crawler_uuid)

    return frontier_response


def get_db_stats(db):
    response = {
        "crawler_amount": db.query(db_models.Crawler).count(),
        "frontier_amount": db.query(db_models.FqdnFrontier).count(),
        "url_amount": db.query(db_models.UrlFrontier).count(),
        "url_ref_amount": db.query(db_models.URLRef).count(),
    }
    return response
