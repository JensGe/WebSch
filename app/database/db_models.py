from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship

from .database import Base


class Crawler(Base):
    __tablename__ = "crawler"

    uuid = Column(String, primary_key=True, index=True)
    contact = Column(String)
    name = Column(String)
    reg_date = Column(DateTime)
    location = Column(String)
    tld_preference = Column(String)


class FqdnFrontier(Base):
    __tablename__ = "fqdn_frontiers"

    fqdn = Column(String, primary_key=True, index=True)
    tld = Column(String, index=True)

    fqdn_last_ipv4 = Column(String)
    fqdn_last_ipv6 = Column(String)

    fqdn_pagerank = Column(Float)
    fqdn_crawl_delay = Column(Integer)
    fqdn_url_count = Column(Integer)


class Url(Base):
    __tablename__ = "url_frontiers"

    url = Column(String, primary_key=True, index=True)

    fqdn = Column(String, ForeignKey('fqdn_frontiers.fqdn'))

    url_last_visited = Column(DateTime)
    url_blacklisted = Column(Boolean)
    url_bot_excluded = Column(Boolean)
