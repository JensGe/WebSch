from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.common import credentials as cred

# SQLite
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite.db"
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
# )


# PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://{}:{}@{}".format(
    cred.postgres_user, cred.postgres_pw, cred.postgres_uri
)
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
