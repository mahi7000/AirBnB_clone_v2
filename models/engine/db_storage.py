#!/usr/bin/python3
""" Database engine new """
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine('mysql+mysqldb://')
        self.__session = sessionmaker(bind=self.__engine)
