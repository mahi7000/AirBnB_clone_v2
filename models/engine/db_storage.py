#!/usr/bin/python3
"""DBStorage with mysql"""

import os
import models
import sqlalchemy
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.city import City
from models.state import State
from models.place import Place
from models.review import Review
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

classes = {"Amenity": Amenity, "City": City, "State": State,
           "Place": Place, "Review": Review, "User": User}


class DBStorage:
    """MySQL Database"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize class DBStorage"""
        user = os.getenv('HBNB_MYSQL_USER')
        pwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(user, pwd, host, db),
                                      pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """current database"""
        obj_dict = {}
        for att in classes:
            if cls is None or cls is classes[att] or cls is att:
                objs = self.__session.query(classes[att]).all()
                for obj in objs:
                    key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                    obj_dict[key] = obj
        return obj_dict

    def new(self, obj):
        """add to the database"""
        self.__session.add(obj)

    def save(self):
        """commit to session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from current database"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reload from database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session

    def close(self):
        """remove session"""
        self.__session.remove()
