from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    Float,
    Index,
)

from app.database.database import Base
from app.common import common_values as c


class Crawler(Base):
    __tablename__ = "crawler"

    uuid = Column(String, primary_key=True, index=True)
    contact = Column(String)
    name = Column(String)
    reg_date = Column(DateTime(timezone=True))
    location = Column(String)
    tld_preference = Column(String)


class FqdnFrontier(Base):
    __tablename__ = "fqdn_frontiers"

    fqdn_hash = Column(String)
    fqdn = Column(String, primary_key=True, index=True)
    tld = Column(String, index=True)

    fqdn_last_ipv4 = Column(String)
    fqdn_last_ipv6 = Column(String)

    fqdn_url_count = Column(Integer)
    fqdn_pagerank = Column(Float)
    fqdn_crawl_delay = Column(Integer)


class UrlFrontier(Base):
    __tablename__ = "url_frontiers"

    fqdn = Column(String, ForeignKey(c.fqdn_frontier_pk))
    url = Column(String, primary_key=True, index=True)

    url_discovery_date = Column(DateTime(timezone=True))
    url_last_visited = Column(DateTime(timezone=True))
    url_blacklisted = Column(Boolean)
    url_bot_excluded = Column(Boolean)


class CrawlerReservation(Base):
    __tablename__ = "crawler_reservations"

    crawler_uuid = Column(
        String, ForeignKey("crawler.uuid", ondelete="CASCADE"), primary_key=True
    )
    fqdn = Column(String, ForeignKey(c.fqdn_frontier_pk), primary_key=True)
    latest_return = Column(DateTime(timezone=True))


class FetcherSettings(Base):
    __tablename__ = "fetcher_settings"

    id = Column(Integer, primary_key=True)

    logging_mode = Column(Integer)
    crawling_speed_factor = Column(Float)
    default_crawl_delay = Column(Integer)
    parallel_process = Column(Integer)

    iterations = Column(Integer)
    fqdn_amount = Column(Integer)
    url_amount = Column(Integer)

    long_term_mode = Column(String)
    short_term_mode = Column(String)

    min_links_per_page = Column(Integer)
    max_links_per_page = Column(Integer)
    lpp_distribution_type = Column(String)

    internal_vs_external_threshold = Column(Float)
    new_vs_existing_threshold = Column(Float)


class URLRef(Base):
    __tablename__ = "url_references"

    url_out = Column(
        String, ForeignKey(c.url_frontier_pk), primary_key=True, index=True
    )
    url_in = Column(
        String, ForeignKey(c.url_frontier_pk), primary_key=True, index=True
    )
    parsing_date = Column(DateTime, primary_key=True)
    Index("url_ref_index", url_out, url_in)


