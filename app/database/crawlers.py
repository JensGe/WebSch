from sqlalchemy.orm import Session

from app.database import db_models, pyd_models
from app.common import http_exceptions as http
from uuid import uuid4
from datetime import datetime, timezone


def uuid_exists(db: Session, uuid):
    if db.query(db_models.Crawler).filter(db_models.Crawler.uuid == uuid).count() == 1:
        return True
    else:
        return False


def create_crawler(db: Session, crawler: pyd_models.CreateCrawler):
    if (
        db.query(db_models.Crawler)
        .filter(db_models.Crawler.contact == crawler.contact)
        .filter(db_models.Crawler.name == crawler.name)
        .count()
        != 0
    ):
        http.raise_http_409(crawler.contact, crawler.name)

    db_crawler = db_models.Crawler(
        uuid=str(uuid4()),
        contact=crawler.contact,
        name=crawler.name,
        reg_date=datetime.now(tz=timezone.utc),
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
    if not uuid_exists(db, str(crawler.uuid)):
        http.raise_http_404(crawler.uuid)

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

    return db_crawler


def patch_crawler(db: Session, crawler: pyd_models.UpdateCrawler):
    if not uuid_exists(db, str(crawler.uuid)):
        http.raise_http_404(crawler.uuid)

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

    return db_crawler


def delete_crawler(db: Session, crawler: pyd_models.DeleteCrawler):
    if not uuid_exists(db, str(crawler.uuid)):
        http.raise_http_404(crawler.uuid)

    db.query(db_models.Crawler).filter(
        db_models.Crawler.uuid == str(crawler.uuid)
    ).delete()
    db.commit()
    return True


def delete_crawlers(db: Session):
    db.query(db_models.Crawler).delete()
    db.commit()
