from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, database, models
from ..service import address as adr
from typing import List
from fastapi import Depends, HTTPException, Query

router = APIRouter()

@router.get("/", response_model=List[schemas.Address])
def get_addresses(db: Session = Depends(database.get_db)):
    db_addresses = adr.get_addresses(db)
    if not db_addresses:
        raise HTTPException(status_code=404, detail="No address found!")
    return db_addresses

@router.post("/", response_model=schemas.Address)
def create_address(address: schemas.AddressCreate, db: Session = Depends(database.get_db)):
    db_address = adr.create_address(db, address)
    return db_address


@router.get("/{address_id}", response_model=schemas.Address)
def read_address(address_id: int, db: Session = Depends(database.get_db)):
    db_address = adr.get_address_by_id(db, address_id)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address

@router.put("/{address_id}", response_model=schemas.Address)
def update_address(address_id: int, address: schemas.AddressCreate, db: Session = Depends(database.get_db)):
    db_address = adr.update_address(db, address_id, address)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address

@router.delete("/{address_id}", response_model=schemas.Address)
def delete_address(address_id: int, db: Session = Depends(database.get_db)):
    db_address = adr.delete_address(db, address_id)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address


@router.get("/within_distance")
def get_addresses_within_distance(
    latitude: float = Query(..., description="Latitude of the location"),
    longitude: float = Query(..., description="Longitude of the location"),
    distance: float = Query(..., description="Distance in kilometers"),
    db: Session = Depends(database.get_db)
):
    addresses = adr.get_addresses_within_distance(db, latitude, longitude, distance)
    return addresses

