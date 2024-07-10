#!/usr/bin/python3
""" Database engine new """
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base_model import Base


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        user = os.environ.get('HBNB_MYSQL_USER')
        password = os.environ.get('HBNB_MYSQL_PWD')
        host = os.environ.get('HBNB_MYSQL_HOST', 'localhost')
        database = os.environ.get('HBNB_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{user}:{password}@{host}/{database}',
                pool_pre_ping=True)

        if os.environ.get('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

        Base.metadata.create_all(self.engine)
        self.__session = sessionmaker(bind=self.__engine)
        self.__session = Session()

        def all(self, cls=None):
            if cls is None:
                for cls 
