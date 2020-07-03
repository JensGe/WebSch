from sqlalchemy.orm import Session

from app.database import db_models, pyd_models, database
from app.data import data_generator as data_gen
from app.common import http_exceptions as http
from app.common import common_values as c
from uuid import uuid4
from datetime import datetime, timezone


def uuid_exists(db: Session, uuid):
    if db.query(db_models.Fetcher).filter(db_models.Fetcher.uuid == uuid).count() == 1:
        return True
    else:
        return False


def create_fetcher(db: Session, fetcher: pyd_models.CreateFetcher):
    if (
        db.query(db_models.Fetcher)
        .filter(db_models.Fetcher.contact == fetcher.contact)
        .filter(db_models.Fetcher.name == fetcher.name)
        .count()
        != 0
    ):
        http.raise_http_409(fetcher.contact, fetcher.name)

    new_uuid = str(uuid4())

    db_fetcher = db_models.Fetcher(
        uuid=new_uuid,
        contact=fetcher.contact,
        name=fetcher.name,
        reg_date=datetime.now(tz=timezone.utc),
        location=fetcher.location,
        tld_preference=fetcher.tld_preference,
    )
    db.add(db_fetcher)
    db.commit()
    db.refresh(db_fetcher)

    db_fetcher_hashes = [
        db_models.FetcherHash(
            fetcher_uuid=new_uuid,
            fetcher_hash=data_gen.generate_hash(new_uuid, seed=i),
        )
        for i in range(c.ch_hash_amount)
    ]

    db.bulk_save_objects(db_fetcher_hashes)
    db.commit()

    return db_fetcher


def get_all_fetcher(db: Session):
    return db.query(db_models.Fetcher).all()


def update_fetcher(db: Session, fetcher: pyd_models.UpdateFetcher):
    if not uuid_exists(db, str(fetcher.uuid)):
        http.raise_http_404(fetcher.uuid)

    db_fetcher = (
        db.query(db_models.Fetcher)
        .filter(db_models.Fetcher.uuid == str(fetcher.uuid))
        .first()
    )

    db_fetcher.contact = fetcher.contact
    db_fetcher.name = fetcher.name
    db_fetcher.location = fetcher.location
    db_fetcher.tld_preference = fetcher.tld_preference

    db.commit()
    db.refresh(db_fetcher)

    return db_fetcher


def patch_fetcher(db: Session, fetcher: pyd_models.UpdateFetcher):
    if not uuid_exists(db, str(fetcher.uuid)):
        http.raise_http_404(fetcher.uuid)

    db_fetcher = (
        db.query(db_models.Fetcher)
        .filter(db_models.Fetcher.uuid == str(fetcher.uuid))
        .first()
    )

    if fetcher.contact is not None:
        db_fetcher.contact = fetcher.contact

    if fetcher.name is not None:
        db_fetcher.name = fetcher.name

    if fetcher.location is not None:
        db_fetcher.location = fetcher.location

    if fetcher.tld_preference is not None:
        db_fetcher.tld_preference = fetcher.tld_preference

    db.commit()
    db.refresh(db_fetcher)

    return db_fetcher


def delete_fetcher(db: Session, fetcher: pyd_models.DeleteFetcher):
    if not uuid_exists(db, str(fetcher.uuid)):
        http.raise_http_404(fetcher.uuid)

    db.query(db_models.FetcherReservation).filter(
        db_models.FetcherReservation.fetcher_uuid == str(fetcher.uuid)
    ).delete()
    db.query(db_models.FetcherHash).filter(
        db_models.FetcherHash.fetcher_uuid == str(fetcher.uuid)
    ).delete()
    db.query(db_models.Fetcher).filter(
        db_models.Fetcher.uuid == str(fetcher.uuid)
    ).delete()
    db.commit()
    return True


def delete_fetchers(db: Session):
    db.query(db_models.FetcherReservation).delete()
    db.query(db_models.FetcherHash).delete()
    db.query(db_models.Fetcher).delete()
    db.commit()
