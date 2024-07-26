#!/usr/bin/python3
""" Database engine new """
import os
import models
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class DBStorage:
    """New engine"""
    __engine = None
    __session = None

    def __init__(self):
        """initialization create engine"""
        user = os.getenv('HBNB_MYSQL_USER')
        password = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST', 'localhost')
        db = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv('HBNB_ENV')

        self.__engine = create_engine(
                f"mysql+mysqldb://{user}:{password}@{host}/{db}",
                pool_pre_ping=True)

        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on current database session"""
        obj_list = []
        if cls:
            if instance(cls, str):
                try:
                    cls = classes[cls]
                except KeyError:
                    pass
            if issubclass(cls, Base):
                obj_list = self.__session.query(cls).all()
        else:
            for subclass in Base.__subclasses__():
                obj_list.extend(self.__session.query(subclass).all())
        new_dict = {}
        for obj in obj_list:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """Add object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not none"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database"""
        Base.metadata.create_all(self.__engine)
        sess = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess)
        self.__session = Session

    def close(self):
        """Close the engine"""
        self.__session.remove()
