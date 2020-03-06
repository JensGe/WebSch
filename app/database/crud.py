from sqlalchemy.orm import Session

from . import db_models, pyd_models
from uuid import uuid4
from datetime import datetime

from fastapi import HTTPException


def uuid_exists(db: Session, uuid):
    if db.query(db_models.Crawler).filter(db_models.Crawler.uuid == uuid).count() == 1:
        return True
    else:
        return False


def reset(db: Session):
    db.query(db_models.Crawler).delete()
    db.query(db_models.FqdnFrontier).delete()
    db.query(db_models.Url).delete()
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
            status_code=409,
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
            status_code=404,
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
            status_code=404,
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
            status_code=404,
            detail="Crawler with UUID: {} was not found".format(crawler.uuid),
        )
    return True


def delete_crawlers(db: Session):
    db.query(db_models.Crawler).delete()
    db.commit()


# Frontier
def get_fqdn_frontier(db: Session, request: pyd_models.CrawlRequest):
    if uuid_exists(db, str(request.crawler_uuid)):
        fqdn_list = (
            db.query(db_models.FqdnFrontier)
            .filter(db_models.FqdnFrontier.tld == request.tld)
            .order_by(db_models.FqdnFrontier.fqdn_pagerank.desc())
            .limit(request.amount)
        )

        frontier_response = pyd_models.FrontierResponse(
            uuid=str(request.crawler_uuid),
            url_frontiers=[]
        )

        for i in range(request.amount):
            url_frontier = pyd_models.UrlFrontier(fqdn=fqdn_list[i].fqdn, url_list=[])
            url_list = (
                db.query(db_models.Url)
                .filter(db_models.Url.fqdn == fqdn_list[i].fqdn)
                .order_by(db_models.Url.url_last_visited.asc())
                .limit(request.length)
            )

            for j in range(request.length):
                url_frontier.url_list.append(url_list[j].url)

            frontier_response.url_frontiers.append(url_frontier)

    else:
        raise HTTPException(
            status_code=404,
            detail="Crawler with UUID: {} was not found".format(request.crawler_uuid),
        )

    return frontier_response


def get_urls(db: Session, fqdn: str, skip: int = 0, limit: int = 10):
    return (
        db.query(db_models.Url)
        .filter(db_models.Url.fqdn == fqdn)
        .offset(skip)
        .limit(limit)
        .all()
    )
