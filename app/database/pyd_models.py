from typing import List
from enum import Enum
import random

from pydantic import BaseModel, HttpUrl, EmailStr
from uuid import UUID
from datetime import datetime


class TLD(str, Enum):
    germany = "de"
    commercial = "com"
    france = "fr"
    organisation = "org"
    united_kingdom = "co.uk"


class Crawler(BaseModel):
    uuid: UUID
    contact: EmailStr
    name: str
    reg_date: datetime
    location: str = None
    tld_preference: TLD = None

    class Config:
        orm_mode = True


class CreateCrawler(BaseModel):
    contact: EmailStr
    name: str
    location: str = None
    tld_preference: TLD = None

    class Config:
        orm_mode = True


class UpdateCrawler(BaseModel):
    uuid: UUID
    contact: EmailStr = None
    name: str = None
    location: str = None
    tld_preference: str = None

    class Config:
        orm_mode = True


class DeleteCrawler(BaseModel):
    uuid: UUID

    class Config:
        orm_mode = True


class CrawlRequest(BaseModel):
    crawler_uuid: UUID
    amount: int = 1
    length: int = 10
    tld: TLD = None

    class Config:
        orm_mode = True


class GenerateRequest(BaseModel):
    crawler_amount: int
    fqdn_amount: int = 20
    min_url_amount: int = 50
    max_url_amount: int = 100


    class Config:
        orm_mode = True


class FqdnFrontier(BaseModel):
    fqdn: str
    tld: str
    urls: List[HttpUrl] = []

    fqdn_last_ipv4: str = None
    fqdn_last_ipv6: str = None

    fqdn_pagerank: str = None
    fqdn_crawl_delay: int = None
    fqdn_url_count: int = None

    class Config:
        orm_mode = True


class Url(BaseModel):
    url: HttpUrl
    fqdn: FqdnFrontier

    url_last_visited: bool = None
    url_blacklisted: bool = None
    url_bot_excluded: bool = None

    class Config:
        orm_mode = True









