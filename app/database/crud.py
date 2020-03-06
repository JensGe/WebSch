from sqlalchemy.orm import Session

from . import models, schemas
from uuid import UUID, uuid4
from datetime import datetime

from fastapi import HTTPException


def uuid_exists(db: Session, crawler):
    if (
        db.query(models.Crawler)
        .filter(models.Crawler.uuid == str(crawler.uuid))
        .count()
        == 1
    ):
        return True
    else:
        return False


# Crawler
def create_crawler(db: Session, crawler: schemas.CreateCrawler):
    if (
        db.query(models.Crawler)
        .filter(models.Crawler.contact == crawler.contact)
        .filter(models.Crawler.name == crawler.name)
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
    db_crawler = models.Crawler(
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
    return db.query(models.Crawler).all()


def update_crawler(db: Session, crawler: schemas.UpdateCrawler):
    if uuid_exists(db, crawler):
        print(crawler)

        db_crawler = (
            db.query(models.Crawler)
            .filter(models.Crawler.uuid == str(crawler.uuid))
            .first()
        )

        db_crawler.contact = crawler.contact
        db_crawler.name = crawler.name
        db_crawler.location = crawler.location
        db_crawler.tld_preference = crawler.tld_preference

        db.commit()
        db.refresh(db_crawler)
        return db_crawler
    else:
        raise HTTPException(
            status_code=404,
            detail="Crawler with UUID: {} was not found".format(crawler.uuid),
        )


def delete_crawler(db: Session, crawler: schemas.DeleteCrawler):
    if uuid_exists(db, crawler):
        db.query(models.Crawler).filter(
            models.Crawler.uuid == str(crawler.uuid)
        ).delete()
        db.commit()
        return True
    else:
        raise HTTPException(
            status_code=404,
            detail="Crawler with UUID: {} was not found".format(crawler.uuid),
        )


def delete_all_crawler(db: Session):
    db.query(models.Crawler).delete()
    db.commit()


# Frontier
# def get_fqdn_frontier(db: Session, fqdn: str):
#     return (
#         db.query(models.FqdnFrontier).filter(models.FqdnFrontier.fqdn == fqdn).first()
#     )
#


# def get_urls(db: Session, fqdn: str, skip: int = 0, limit: int = 100):
#     return (
#         db.query(models.UrlFrontier)
#         .filter(models.UrlFrontier.fqdn_uri == fqdn)
#         .offset(skip)
#         .limit(limit)
#         .all()
#     )
