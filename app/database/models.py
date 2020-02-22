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


