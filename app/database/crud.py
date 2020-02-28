from sqlalchemy.orm import Session

from . import models, schemas
from uuid import UUID, uuid4
from datetime import datetime


def get_fqdn_frontier(db: Session, fqdn: str):
    return (
        db.query(models.FqdnFrontier).filter(models.FqdnFrontier.fqdn == fqdn).first()
    )


def create_crawler(db: Session, crawler: schemas.Crawler):
    db_crawler = models.Crawler(
        uuid=str(uuid4()),
        contact=crawler.contact,
        reg_date=str(datetime.now()),
        location=crawler.location,
        tld_preference=crawler.tld_preference,
    )
    db.add(db_crawler)
    db.commit()
    db.refresh(db_crawler)
    return db_crawler


def get_urls(db: Session, fqdn: str, skip: int = 0, limit: int = 100):
    return (
        db.query(models.UrlFrontier)
        .filter(models.UrlFrontier.fqdn_uri == fqdn)
        .offset(skip)
        .limit(limit)
        .all()
    )
