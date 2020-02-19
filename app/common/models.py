from enum import Enum

from uuid import UUID
from datetime import datetime
from typing import List

from pydantic import BaseModel, HttpUrl, EmailStr


class TLD(str, Enum):
    germany = 'de'
    commercial = 'com'
    france = 'fr'
    organisation = 'org'
    united_kingdom = 'co.uk'


class Crawler(BaseModel):
    uuid: UUID = None
    reg_date: datetime = None
    contact: EmailStr = None
    location: str = None
    pref_tld: TLD = None


class CrawlRequest(BaseModel):
    crawler: Crawler
    amount: int = 1
    length: int = 5


class URLList(BaseModel):
    length: int = 50
    tld: str = None
    fqdn: str = None
    ipv4: str = None
    urls: List[HttpUrl] = []


class Frontier(BaseModel):
    amount: int = 1
    url_lists: List[URLList]




