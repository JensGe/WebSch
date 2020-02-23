from typing import List

from pydantic import BaseModel, HttpUrl, EmailStr
from uuid import UUID
from datetime import datetime


class CrawlerBase(BaseModel):

    reg_date: datetime = None
    contact: EmailStr
    location: str = None
    # pref_tld: TLD = None
