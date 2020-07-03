from sqlalchemy import create_engine, or_, and_
from sqlalchemy.orm import sessionmaker, aliased
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import func

from app.common import credentials as cred
from app.common import enum
from app.database import pyd_models, db_models


SQLALCHEMY_DATABASE_URL = "postgresql://{}:{}@{}/{}".format(
    cred.postgres_user, cred.postgres_pw, cred.postgres_uri, cred.postgres_db
)
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def reset(db, request: pyd_models.DeleteDatabase):
    if request.delete_url_refs:
        db.query(db_models.URLRef).delete()
        db.commit()

    if request.delete_fetcher_hashes:
        db.query(db_models.FetcherHash).delete()
        db.commit()

    if request.delete_fetchers:
        db.query(db_models.Fetcher).delete()
        db.commit()

    if request.delete_urls:
        db.query(db_models.Url).delete()
        db.commit()

    if request.delete_fqdns:
        db.query(db_models.Frontier).delete()
        db.commit()

    if request.delete_reserved_fqdns:
        db.query(db_models.FetcherReservation).delete()
        db.commit()

    return True


def refresh_fqdn_hashes(db):
    frontier = db.query(db_models.Frontier).all()
    fetcher_amount = db.query(db_models.Fetcher).count()

    if fetcher_amount != 0:
        for f in frontier:
            f.fqdn_hash_fetcher_index = hash(f.fqdn) % fetcher_amount

        db.bulk_save_objects(frontier)
        db.commit()

    return True


def fqdn_hash_activated(db):
    return (
        db.query(db_models.FetcherSettings.long_term_part_mode)
        .filter(db_models.FetcherSettings.id == 1)
        .first()[0]
        == enum.LONGPART.fqdn_hash
    )


def consistent_hash_activated(db):
    return (
        db.query(db_models.FetcherSettings.long_term_part_mode)
        .filter(db_models.FetcherSettings.id == 1)
        .first()[0]
        == enum.LONGPART.consistent_hashing
    )


def get_fetcher_hashes(db):
    return [
        dict(uuid=f.fetcher_uuid, hash=f.fetcher_hash)
        for f in db.query(db_models.FetcherHash).all()
    ]


def get_fetcher_hash_ranges(db, uuid):
    """
    ordered by start_hash, ascending
    """
    fh0 = aliased(db_models.FetcherHash)
    fh1 = aliased(db_models.FetcherHash)
    fh2 = aliased(db_models.FetcherHash)

    return (
        db.query(
            fh1.fetcher_uuid,
            fh1.fetcher_hash,
            func.coalesce(func.min(fh2.fetcher_hash), func.min(fh0.fetcher_hash)),
        )
        .join(fh2, fh2.fetcher_hash > fh1.fetcher_hash, isouter=True)
        .filter(fh1.fetcher_uuid == uuid)
        .group_by(fh1.fetcher_uuid, fh1.fetcher_hash)
        .order_by(fh1.fetcher_hash)
    ).all()


def get_hash_range_filter_query(fetcher_hash_range):
    hash_range_filter = [
        and_(
            db_models.Frontier.fqdn_hash >= hash_range[1],
            db_models.Frontier.fqdn_hash < hash_range[2],
        )
        for hash_range in fetcher_hash_range[:-1]
    ]

    if fetcher_hash_range[-1][1] > fetcher_hash_range[-1][2]:
        hash_range_filter.append(
            or_(
                db_models.Frontier.fqdn_hash >= fetcher_hash_range[-1][1],
                db_models.Frontier.fqdn_hash < fetcher_hash_range[-1][2],
            ),
        )

    else:
        hash_range_filter.append(
            and_(
                db_models.Frontier.fqdn_hash >= fetcher_hash_range[-1][1],
                db_models.Frontier.fqdn_hash < fetcher_hash_range[-1][2],
            ),
        )

    return or_(*hash_range_filter)
