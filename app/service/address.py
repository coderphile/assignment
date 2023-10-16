from sqlalchemy.orm import Session
from .. import models, schemas
from math import radians, sin, cos, sqrt, atan2, degrees, asin

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

def get_addresses_within_distance(db: Session, latitude: float, longitude: float, distance: float):
    # Define the Earth's radius in kilometers
    earth_radius = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1 = radians(latitude)
    lon1 = radians(longitude)

    # Calculate the maximum and minimum latitude and longitude to define a bounding box
    d = distance / earth_radius
    lat_max = lat1 + degrees(d)
    lat_min = lat1 - degrees(d)

    # Find the maximum and minimum longitude for the bounding box
    delta_lon = asin(sin(d) / cos(lat1))
    lon_max = lon1 + delta_lon
    lon_min = lon1 - delta_lon

    # Query the database to retrieve addresses within the bounding box
    results = db.query(Address).filter(Address.latitude >= lat_min, Address.latitude <= lat_max, Address.longitude >= lon_min, Address.longitude <= lon_max).all()

    # Calculate the actual distance between the specified coordinates and the retrieved addresses
    addresses_within_distance = []
    for address in results:
        # Calculate the distance using the Haversine formula
        lat2 = radians(address.latitude)
        lon2 = radians(address.longitude)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        # Calculate the distance in kilometers
        distance_km = earth_radius * c

        if distance_km <= distance:
            addresses_within_distance.append(address)

    return addresses_within_distance
