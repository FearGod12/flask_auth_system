#!/usr/bin/env python3
"""
sqlalchemy module for communication with postgres
"""
# export DB_NAME="mydb" DB_USER="myuser" DB_PASSWORD="mypassword"


from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from os import getenv
import psycopg2
from models.user import User
from models.book import Book
from models.basemodel import Base

TABLES = [User, Book]

class Database:

    __session = None
    __engine = None

    def __init__(self):
        try:
            DB_NAME = getenv('DB_NAME')
            DB_USER = getenv('DB_USER')
            DB_PASSWORD = getenv('DB_PASSWORD')

            self.__engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@localhost/{DB_NAME}')
            print(f"Connected to {getenv('DB_NAME')} database")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.__session.close()

    def reload(self):
        """(Re)load data from postres database"""
        Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(factory)

    def new(self, obj):
        """Add `obj` to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Save/commit all changes of the current db session"""
        self.__session.commit()

    def get_all(self, cls, author_id=None):
        """
        query-> SELECT * FROM cls.__tablename__
        [Returns a dictionary (key:obj) object for easy indexing]
        """
        objs_dict = {}
        if author_id == None:
            objs = self.__session.query(cls).all()
            return objs
        objs = self.__session.query(cls).filter(cls.author_id == author_id).all()
        return objs

    def delete(self, obj=None):
        """delete `obj` from database"""
        if obj is not None:
            self.__session.delete(obj)

    def rollback(self):
        '''rolls back the current Sqlalchemy session
        after a failed flush occured
        just for testing purposes'''
        self.__session.rollback()

    def close(self):
        """close the current db session"""
        self.__session.remove()
    
    def get(self, cls, id=None, email=None, attr=None):
        """
        Returns a `obj` of `cls` with a matching `id`,
        or None if not exists.
        """
        if cls not in TABLES:
            return None
        if attr is not None:
            obj = self.__session.query(cls).filter(cls.id == id).first()
            if obj is None:
                return None
            return getattr(obj, attr)
        if id is not None:
            return self.__session.query(cls).filter(cls.id == id).first()
        if email is not None:
            return self.__session.query(cls).filter(cls.email == email).first()
