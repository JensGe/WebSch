from sqlalchemy.orm import Session

from app.database import db_models, pyd_models, frontier
from uuid import uuid4
from datetime import datetime

from fastapi import HTTPException, status


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
def get_fqdn_frontier(db: Session, request: pyd_models.FrontierRequest):
    if uuid_exists(db, str(request.crawler_uuid)):

        frontier_response = pyd_models.FrontierResponse(uuid=str(request.crawler_uuid))

        for fqdn in frontier.get_fqdn_list(db, request):
            url_list = list(frontier.get_db_url_list(db, request, fqdn))

            frontier_response.urls_count += len(url_list)
            frontier_response.url_frontiers.append(
                frontier.create_url_frontier(fqdn, url_list)
            )

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
        "crawler_amount": db.query(db_models.Crawler).count(),
        "frontier_amount": db.query(db_models.FqdnFrontier).count(),
        "url_amount": db.query(db_models.Url).count(),
    }
    return response
