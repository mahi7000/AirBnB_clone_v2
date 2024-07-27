#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
import models


class Amenity(BaseModel, Base):
    """Amentiy"""
    if models.env == "db":
        __tablename__ = "amenities"
        name = Column(String(128), nullable=False)
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """initialize Amenity"""
        super().__init__(*args, **kwargs)
