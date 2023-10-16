from sqlalchemy import Column, Integer, String
from .database import Base

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    latitude = Column(String(255))
    longitude = Column(String(255))