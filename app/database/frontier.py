from datetime import datetime, timedelta

from app.database import db_models, pyd_models, crawlers
from app.common import enum, http_exceptions as http_ex, common_values as c

from sqlalchemy.sql.expression import func


def get_fqdn_list(db, request):

    fqdn_block_list = db.query(db_models.CrawlerReservation.fqdn).filter(
        db_models.CrawlerReservation.latest_return > datetime.now()
    )

    fqdn_list = db.query(db_models.FqdnFrontier).filter(
        db_models.FqdnFrontier.fqdn.notin_(fqdn_block_list)
    )

    # Filter
    if request.long_term_mode == enum.LTF.top_level_domain:
        crawler_pref_tld = (
            db.query(db_models.Crawler)
            .filter(db_models.Crawler.uuid == str(request.crawler_uuid))
            .first()
        ).tld_preference

        fqdn_list = fqdn_list.filter(db_models.FqdnFrontier.tld == crawler_pref_tld)

    # Order
    if request.long_term_mode == enum.LTF.random:
        fqdn_list = fqdn_list.order_by(func.random())

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
        .filter(
            db_models.UrlFrontier.url_last_visited
            is not None
            # db_models.UrlFrontier.url_last_visited < url.url_last_visited,
        )
        .order_by(func.random())
        .limit(amount)
    )


def get_url_list_from_frontier_response(frontier_response):
    url_list = []
    for url_frontier in frontier_response.url_frontiers:
        url_list.extend([str(url.url) for url in url_frontier.url_list])

    return url_list


def get_fqdn_list_from_frontier_response(frontier_response):
    return [url_frontier.fqdn for url_frontier in frontier_response.url_frontiers]


def get_only_new_list_items(new_list, old_list):

    only_new_list = [item for item in new_list if item not in old_list]

    return only_new_list


def clean_reservation_list(db):
    db.query(db_models.CrawlerReservation).filter(
        db_models.CrawlerReservation.latest_return < datetime.now()
    ).delete()

    db.commit()
    return True


def save_reservations(db, frontier_response, latest_return):
    uuid = frontier_response.uuid
    fqdn_only_list = get_fqdn_list_from_frontier_response(frontier_response)

    clean_reservation_list(db)

    current_db_reservation_list = (
        db.query(db_models.CrawlerReservation)
        .filter(db_models.CrawlerReservation.crawler_uuid == uuid)
        .filter(db_models.CrawlerReservation.latest_return > datetime.now())
    )
    current_block_list = [fqdn.fqdn for fqdn in current_db_reservation_list]

    fqdn_new_block_list = get_only_new_list_items(
        new_list=fqdn_only_list, old_list=current_block_list
    )

    new_db_block_list = [
        db_models.CrawlerReservation(
            crawler_uuid=str(uuid), fqdn=fqdn, latest_return=latest_return
        )
        for fqdn in fqdn_new_block_list
    ]

    db.bulk_save_objects(new_db_block_list)
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
    save_reservations(db, frontier_response, latest_return)

    frontier_response.latest_return = latest_return
    frontier_response.response_url = c.response_url

    return frontier_response


def get_db_stats(db):
    clean_reservation_list(db)
    response = {
        "crawler_amount": db.query(db_models.Crawler).count(),
        "frontier_amount": db.query(db_models.FqdnFrontier).count(),
        "url_amount": db.query(db_models.UrlFrontier).count(),
        "url_ref_amount": db.query(db_models.URLRef).count(),
        "reserved_fqdn_amount": db.query(db_models.CrawlerReservation)
        .filter(db_models.CrawlerReservation.latest_return > datetime.now())
        .count(),
    }
    return response


def get_random_urls(db, request: pyd_models.GetRandomUrls):
    urls = (
        db.query(db_models.UrlFrontier)
        .filter(db_models.UrlFrontier.fqdn == request.fqdn)
        .order_by(func.random())
        .limit(request.amount)
    )

    url_list = [url for url in urls]

    return pyd_models.RandomUrls(url_list=url_list)
