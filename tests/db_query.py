from app.database import db_models

from sqlalchemy.sql.expression import func


def get_min_hash(db):
    return db.query(func.min(db_models.FetcherHash.fetcher_hash)).scalar()


def get_max_hash(db):
    return db.query(func.max(db_models.FetcherHash.fetcher_hash)).scalar()


def get_fetcher_uuid_with_min_hash(db):
    return (
        db.query(db_models.FetcherHash.fetcher_uuid)
        .filter(db_models.FetcherHash.fetcher_hash == get_min_hash(db))
        .scalar()
    )


def get_fetcher_uuid_with_max_hash(db):
    return (
        db.query(db_models.FetcherHash.fetcher_uuid)
        .filter(db_models.FetcherHash.fetcher_hash == get_max_hash(db))
        .scalar()
    )
