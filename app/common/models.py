from enum import Enum

from uuid import UUID
from datetime import datetime
from typing import List

from pydantic import BaseModel, HttpUrl, EmailStr


class TLD(str, Enum):
    germany = "de"
    commercial = "com"
    france = "fr"
    organisation = "org"
    united_kingdom = "co.uk"


class Crawler(BaseModel):
    uuid: UUID
    reg_date: datetime = None
    contact: EmailStr
    location: str = None
    pref_tld: TLD = None


class CrawlRequest(BaseModel):
    crawler_uuid: UUID
    amount: int = 1
    length: int = 5
    tld: TLD = None


class URLList(BaseModel):
    length: int = 50
    tld: str = None
    fqdn: str = None
    ipv4: str = None
    urls: List[HttpUrl] = []


class Frontier(BaseModel):
    amount: int = 1
    response_url: HttpUrl = "http://www.example.com/submit"
    url_lists: List[URLList]
