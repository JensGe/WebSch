from typing import List
from app.common import enum
from app.common import common_values as c

from pydantic import BaseModel, HttpUrl, EmailStr
from uuid import UUID
from datetime import datetime


class BasisModel(BaseModel):
    class Config:
        orm_mode = True


# Crawler
class Crawler(BasisModel):
    uuid: UUID
    contact: EmailStr
    name: str
    reg_date: datetime
    location: str = None
    tld_preference: enum.TLD = None


class CreateCrawler(BasisModel):
    contact: EmailStr
    name: str
    location: str = None
    tld_preference: enum.TLD = None


class UpdateCrawler(BasisModel):
    uuid: UUID
    contact: EmailStr = None
    name: str = None
    location: str = None
    tld_preference: str = None


class DeleteCrawler(BasisModel):
    uuid: UUID


# Frontier
class FrontierRequest(BasisModel):
    crawler_uuid: UUID
    amount: int = c.frontier_amount
    length: int = c.frontier_length
    tld: enum.TLD = None
    prio_mode: enum.PRIO = None
    part_mode: enum.PART = None


class Url(BasisModel):
    url: HttpUrl
    fqdn: str

    url_last_visited: datetime = None
    url_blacklisted: bool = None
    url_bot_excluded: bool = None


class UrlFrontier(BasisModel):
    fqdn: str
    tld: enum.TLD = None

    fqdn_last_ipv4: str = None
    fqdn_last_ipv6: str = None

    fqdn_pagerank: float = None
    fqdn_crawl_delay: int = None
    fqdn_url_count: int = None

    url_list: List[Url] = []


class URLReference(BasisModel):
    url_out: str
    url_in: str
    date: datetime


class FrontierResponse(BasisModel):
    uuid: str
    response_url: HttpUrl
    withdrawal_date: datetime
    url_frontiers_count: int = c.url_frontier_count
    urls_count: int = c.urls_count
    url_frontiers: List[UrlFrontier] = []




# Developer Tools
class GenerateRequest(BasisModel):
    crawler_amount: int = c.crawler
    fqdn_amount: int = c.fqdn
    min_url_amount: int = c.min_url
    max_url_amount: int = c.max_url
    visited_ratio: float = c.visited_ratio
    connection_amount: int = c.connections


class StatsResponse(BasisModel):
    crawler_amount: int
    frontier_amount: int
    url_amount: int
    url_ref_amount: int


class DeleteDatabase(BasisModel):
    delete_url_refs: bool = False
    delete_crawlers: bool = False
    delete_urls: bool = False
    delete_fqdns: bool = False
