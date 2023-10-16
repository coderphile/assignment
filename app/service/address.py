from sqlalchemy.orm import Session
from .. import models, schemas
from math import radians, degrees, asin, sin, cos, atan2, pi
from sqlalchemy import cast, Float
from geopy.distance import great_circle

def get_addresses(db: Session):
    return db.query(models.Address).all()

def create_address(db: Session, address: schemas.AddressCreate):
    # Create a new address in the database
    db_address = models.Address(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

def get_address_by_id(db: Session, address_id: int):
    # Retrieve an address by its ID
    return db.query(models.Address).filter(models.Address.id == address_id).first()

def update_address(db: Session, address_id: int, address: schemas.AddressCreate):
    # Update an address by its ID
    db_address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if db_address:
        for key, value in address.dict().items():
            setattr(db_address, key, value)
        db.commit()
        db.refresh(db_address)
    return db_address

def delete_address(db: Session, address_id: int):
    # Delete an address by its ID
    db_address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if db_address:
        db.delete(db_address)
        db.commit()
    return db_address


def get_addresses_within_distance(db, latitude, longitude, distance):
    
    try:
        # Ensure latitude and longitude are valid numeric values
        latitude = float(latitude)
        longitude = float(longitude)
        center = (latitude, longitude)
        radius = distance  # distance in kilometers

        # Calculate min and max points
        min_point = great_circle(kilometers=radius).destination(center, 225)
        max_point = great_circle(kilometers=radius).destination(center, 45)

        # Extract the latitude and longitude from the points
        min_lat, min_lon = min_point.latitude, min_point.longitude
        max_lat, max_lon = max_point.latitude, max_point.longitude

        # Query the database to retrieve addresses within the bounding box
        results = db.query(models.Address).filter(
            (cast(models.Address.latitude, Float) >= min_lat) &
            (cast(models.Address.latitude, Float) <= max_lat) &
            (cast(models.Address.longitude, Float) >= min_lon) &
            (cast(models.Address.longitude, Float) <= max_lon)
        ).all()
        
        # calculate the actual distance from the center to the retrieved addresses
        addresses_within_distance = []
        for address in results:
            address_coordinates = (address.latitude, address.longitude)
            dist = great_circle(center, address_coordinates).kilometers
            if dist <= distance:
                addresses_within_distance.append(address)

        return addresses_within_distance

    except (ValueError, TypeError) as e:
        # Handle invalid input or conversion errors here
        return f"Invalid input or conversion error: {str(e)}"
