from sqlalchemy.orm import Session

from . import models, schemas
from uuid import UUID, uuid4
from datetime import datetime

from fastapi import HTTPException

# def get_fqdn_frontier(db: Session, fqdn: str):
#     return (
#         db.query(models.FqdnFrontier).filter(models.FqdnFrontier.fqdn == fqdn).first()
#     )
#


def create_crawler(db: Session, crawler: schemas.CreateCrawler):
    # ToDo Check for bereits bestehende Crawler / Email Adressen
    if db.query(models.Crawler).filter(models.Crawler.contact == crawler.contact).filter(models.Crawler.name == crawler.name).count() != 0:
        raise HTTPException(
            status_code=409, detail="Combination of Crawler Contact ({}) and Crawler Name ({}) already exists, please choose another name for your crawler".format(crawler.contact, crawler.name)
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


def get_crawlers(db: Session):
    return db.query(models.Crawler).all()


# def get_urls(db: Session, fqdn: str, skip: int = 0, limit: int = 100):
#     return (
#         db.query(models.UrlFrontier)
#         .filter(models.UrlFrontier.fqdn_uri == fqdn)
#         .offset(skip)
#         .limit(limit)
#         .all()
#     )
