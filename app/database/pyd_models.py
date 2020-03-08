from typing import List
from enum import Enum
import random

from pydantic import BaseModel, HttpUrl, EmailStr
from uuid import UUID
from datetime import datetime


# Common
class TLD(str, Enum):
    Germany = "de"
    Commercial = "com"
    France = "fr"
    Organisation = "org"
    Sweden = "se"


# Crawler
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


# Frontier
class CrawlRequest(BaseModel):
    crawler_uuid: UUID
    amount: int = 1
    length: int = 10
    tld: TLD = None

    class Config:
        orm_mode = True


class Url(BaseModel):
    url: HttpUrl
    fqdn: str

    url_last_visited: datetime = None
    url_blacklisted: bool = None
    url_bot_excluded: bool = None

    class Config:
        orm_mode = True


class UrlFrontier(BaseModel):
    fqdn: str
    tld: TLD = None

    fqdn_last_ipv4: str = None
    fqdn_last_ipv6: str = None

    fqdn_pagerank: float = None
    fqdn_crawl_delay: int = None
    fqdn_url_count: int = None

    url_list: List[Url] = []

    class Config:
        orm_mode = True


class FrontierResponse(BaseModel):
    uuid: str
    url_frontiers: List[UrlFrontier]

    class Config:
        orm_mode = True


# Developer Tools
class GenerateRequest(BaseModel):
    crawler_amount: int = 3
    fqdn_amount: int = 20
    min_url_amount: int = 50
    max_url_amount: int = 100

    class Config:
        orm_mode = True


class GenerateResponse(BaseModel):
    crawler: List[Crawler]
    frontier: List[UrlFrontier]
    url_list: List[Url]

    class Config:
        orm_mode = True


