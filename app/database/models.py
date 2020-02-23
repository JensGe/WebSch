from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Crawler(Base):
    __tablename__ = "crawler"

    uuid = Column(Integer, primary_key=True, index=True)
    contact = Column(String, unique=True, index=True)
    reg_date = Column(String)
    location = Column(String)
    pref_tld = Column(String)


class Frontier(Base):
    __tablename__ = "frontier"

    url = Column(String, primary_key=True, index=True)
    url_last_visit = Column(String)
    url_blacklisted = Column(Boolean)

    fqdn = Column(String, index=True)
    tld = Column(String, index=True)
    tld_PR = Column(float)
    tld_last_ip4 = Column(String, index=True)

    url_robots_txt = relationship("RobotsCache", back_populates="frontier_url")


class RobotsCache(Base):
    __tableName__ = "robots_cache"

    robots_txt = Column(String, primary_key=True, index=True)

    frontier_url = relationship("Frontier", back_populates="url_robots_txt")
