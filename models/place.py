#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
import models


if models.env == 'db':
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60), ForeignKey(
                                 'places.id', onupdate='CASCADE',
                                 ondelete='CASCADE'), primary_key=True),
                          Column('amenity_id', String(60), ForeignKey(
                                 'amenities.id', onupdate='CASCADE',
                                 ondelete='CASCADE'), primary_key=True))


class Place(BaseModel, Base):
    """ A place to stay """
    if models.env == 'db':
        __tablename__ = "places"
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship("Review", backref="place")
        amenities = relationship("Amenity", secondary="place_amenity",
                                 backref="place_amenities", viewonly=False)
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """return list of review"""
            from models.review import Review
            review_list = []
            rev = models.storage.all(Review)
            for review in rev.values():
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list

        @property
        def amenities(self):
            """return list of amenities"""
            from models.amenity import Amenity
            amen_list = []
            amen = models.storage.all(Amenity)
            for amenity in amen.values():
                if amenity.place_id == self.id:
                    amen_list.append(amenity)
            return amen_list

    def __init__(self, *args, **kwargs):
        """initialize places"""
        super().__init__(*args, **kwargs)
