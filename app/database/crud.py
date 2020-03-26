from sqlalchemy.orm import Session

from . import db_models, pyd_models
from uuid import uuid4
from datetime import datetime

from fastapi import HTTPException
from starlette import status


def uuid_exists(db: Session, uuid):
    if db.query(db_models.Crawler).filter(db_models.Crawler.uuid == uuid).count() == 1:
        return True
    else:
        return False


def reset(db: Session):
    db.query(db_models.Crawler).delete()
    db.query(db_models.Url).delete()
    db.query(db_models.FqdnFrontier).delete()

    return True


# Crawler
def create_crawler(db: Session, crawler: pyd_models.CreateCrawler):
    if (
        db.query(db_models.Crawler)
        .filter(db_models.Crawler.contact == crawler.contact)
        .filter(db_models.Crawler.name == crawler.name)
        .count()
        != 0
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Combination of Crawler Contact ({}) and Crawler Name ({}) already "
            "exists, please choose another name for your crawler".format(
                crawler.contact, crawler.name
            ),
        )
    db_crawler = db_models.Crawler(
        uuid=str(uuid4()),
        contact=crawler.contact,
        name=crawler.name,
        reg_date=datetime.now(),
        location=crawler.location,
        tld_preference=crawler.tld_preference,
    )
    db.add(db_crawler)
    db.commit()
    db.refresh(db_crawler)
    return db_crawler


def get_all_crawler(db: Session):
    return db.query(db_models.Crawler).all()


def update_crawler(db: Session, crawler: pyd_models.UpdateCrawler):
    if uuid_exists(db, str(crawler.uuid)):
        db_crawler = (
            db.query(db_models.Crawler)
            .filter(db_models.Crawler.uuid == str(crawler.uuid))
            .first()
        )

        db_crawler.contact = crawler.contact
        db_crawler.name = crawler.name
        db_crawler.location = crawler.location
        db_crawler.tld_preference = crawler.tld_preference

        db.commit()
        db.refresh(db_crawler)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crawler with UUID: {} was not found".format(crawler.uuid),
        )
    return db_crawler


def patch_crawler(db: Session, crawler: pyd_models.UpdateCrawler):
    if uuid_exists(db, str(crawler.uuid)):
        db_crawler = (
            db.query(db_models.Crawler)
            .filter(db_models.Crawler.uuid == str(crawler.uuid))
            .first()
        )

        if crawler.contact is not None:
            db_crawler.contact = crawler.contact

        if crawler.name is not None:
            db_crawler.name = crawler.name

        if crawler.location is not None:
            db_crawler.location = crawler.location

        if crawler.tld_preference is not None:
            db_crawler.tld_preference = crawler.tld_preference

        db.commit()
        db.refresh(db_crawler)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crawler with UUID: {} was not found".format(crawler.uuid),
        )
    return db_crawler


def delete_crawler(db: Session, crawler: pyd_models.DeleteCrawler):
    if uuid_exists(db, str(crawler.uuid)):
        db.query(db_models.Crawler).filter(
            db_models.Crawler.uuid == str(crawler.uuid)
        ).delete()
        db.commit()

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crawler with UUID: {} was not found".format(crawler.uuid),
        )
    return True


def delete_crawlers(db: Session):
    db.query(db_models.Crawler).delete()
    db.commit()


# Frontier
def get_fqdn_list(db, request):
    if request.tld is None:
        fqdn_list = db.query(db_models.FqdnFrontier).order_by(
            db_models.FqdnFrontier.fqdn_pagerank.desc()
        )
    else:
        fqdn_list = (
            db.query(db_models.FqdnFrontier)
            .filter(db_models.FqdnFrontier.tld == request.tld)
            .order_by(db_models.FqdnFrontier.fqdn_pagerank.desc())
        )

    fqdn_list = fqdn_list[: request.amount] if request.amount > 0 else fqdn_list

    return fqdn_list


def create_new_empty_frontier_response(crawler_uuid):
    return pyd_models.FrontierResponse(
        uuid=str(crawler_uuid), url_frontiers=[]
    )


def get_db_url_list(db, request, fqdn):
    db_url_list = (
        db.query(db_models.Url)
            .filter(db_models.Url.fqdn == fqdn.fqdn)
            .order_by(db_models.Url.url_last_visited.asc())
    )

    db_url_list = (
        db_url_list[: request.length] if request.length > 0 else db_url_list
    )

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


def get_fqdn_frontier(db: Session, request: pyd_models.CrawlRequest):
    if uuid_exists(db, str(request.crawler_uuid)):

        frontier_response = create_new_empty_frontier_response(request.crawler_uuid)

        for fqdn in get_fqdn_list(db, request):
            db_url_list = get_db_url_list(db, request, fqdn)
            url_list = [url for url in db_url_list]

            frontier_response.urls_count += len(url_list)
            frontier_response.url_frontiers.append(create_url_frontier(fqdn, url_list))

        frontier_response.url_frontiers_count = len(frontier_response.url_frontiers)

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crawler with UUID: {} was not found".format(request.crawler_uuid),
        )

    return frontier_response


# def get_urls(db: Session, fqdn: str, skip: int = 0, limit: int = 10):
#     return (
#         db.query(db_models.Url)
#         .filter(db_models.Url.fqdn == fqdn)
#         .offset(skip)
#         .limit(limit)
#         .all()
#     )


def get_db_stats(db: Session):
    response = {
        "crawler_amount": len(db.query(db_models.Crawler).all()),
        "frontier_amount": len(db.query(db_models.FqdnFrontier).all()),
        "url_amount": len(db.query(db_models.Url).all()),
    }
    return response
