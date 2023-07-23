#!/usr/bin/python3
"""The Place class module"""

from os import getenv
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from models.amenity import Amenity
from models.base_model import Base, BaseModel
from models.review import Review

association_table = Table(
    "place_amenity",
    Base.metadata,
    Column(
        "place_id", String(60), ForeignKey("places.id"),
        primary_key=True, nullable=False
    ),
    Column(
        "amenity_id", Integer, ForeignKey("amenities.id"),
        primary_key=True, nullable=False
    )
)


class Place(BaseModel, Base):
    """Represents Place class for MySQL database.

    Inherits from SQLAlchemy Base & links to MySQL table places.

    Attributes:
        __tablename__ (str): name of the MySQL table for storing places.
        city_id (sqlalchemy String): place's city id.
        user_id (sqlalchemy String): place's user id.
        name (sqlalchemy String): name of the place.
        description (sqlalchemy String): description of the place.
        number_rooms (sqlalchemy Integer): number of rooms.
        number_bathrooms (sqlalchemy Integer): number of bathrooms.
        max_guest (sqlalchemy Integer): maximum number of guests.
        price_by_night (sqlalchemy Integer): price per night.
        latitude (sqlalchemy Float): place's latitude.
        longitude (sqlalchemy Float): place's longitude.
        reviews (sqlalchemy relationship): Place-Review relationship.
        amenities (sqlalchemy relationship): Place-Amenity relationship.
        amenity_ids (list): list of linked amenity ids.
    """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0)
    number_bathrooms = Column(Integer, default=0)
    max_guest = Column(Integer, default=0)
    price_by_night = Column(Integer, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    reviews = relationship("Review", backref="place", cascade="delete")
    amenities = relationship(
        "Amenity",
        secondary="place_amenity",
        viewonly=False
    )
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE", None) != "db":
        @property
        def reviews(self):
            """Get a list of all linked Reviews.

            Returns:
                list: List of linked Review objects.
            """
            review_list = [
                review for review in list(storage.all(Review).values())
                if review.place_id == self.id
            ]
            return review_list

        @property
        def amenities(self):
            """Get/set linked Amenities.

            Returns:
                list: List of linked Amenity objects.
            """
            amenity_list = [
                amenity for amenity in list(storage.all(Amenity).values())
                if amenity.id in self.amenity_ids
            ]
            return amenity_list

        @amenities.setter
        def amenities(self, value):
            """Set linked Amenities.

            Args:
                value (Amenity): Amenity object to be linked.
            """
            if type(value) == Amenity:
                self.amenity_ids.append(value.id)
