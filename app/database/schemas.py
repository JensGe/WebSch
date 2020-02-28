from typing import List

from pydantic import BaseModel, HttpUrl, EmailStr
from uuid import UUID
from datetime import datetime


class Crawler(BaseModel):
    uuid: UUID
    reg_date: datetime
    contact: EmailStr
    location: str = None
    tld_preference: str = None

    class Config:
        orm_mode = True


class FqdnFrontier(BaseModel):
    fqdn: str
    tld: str
    urls: List[HttpUrl] = []

    fqdn_last_ipv4: str = None
    fqdn_last_ipv6: str = None

    fqdn_pagerank: float = None
    fqdn_crawl_delay: int = None
    fqdn_url_count: int = None

    class Config:
        orm_mode = True


class UrlFrontier(BaseModel):
    url: HttpUrl
    fqdn: FqdnFrontier

    url_last_visited: bool = None
    url_blacklisted: bool = None
    url_bot_excluded: bool = None

    class Config:
        orm_mode = True









