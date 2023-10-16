from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AddressCreate(BaseModel):
    name: str 
    latitude: str 
    longitude: str 


class Address(BaseModel):
    id: int
    name: str 
    latitude: str 
    longitude: str 

    class Config:
        orm_mode = True


class AddressInDB(Address):
    pass
