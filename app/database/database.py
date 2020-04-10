from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.common import credentials as cred
from app.database import pyd_models, db_models


# PostgreSQL
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

    if request.delete_crawlers:
        db.query(db_models.Crawler).delete()
        db.commit()

    if request.delete_urls:
        db.query(db_models.UrlFrontier).delete()
        db.commit()

    if request.delete_fqdns:
        db.query(db_models.FqdnFrontier).delete()
        db.commit()

    if request.delete_reserved_fqdns:
        db.query(db_models.ReservationList).delete()
        db.commit()

    return True
