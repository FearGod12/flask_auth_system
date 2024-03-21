#!/usr/bin/env python

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.basemodel import Base, BaseModel

class Book(BaseModel, Base):
    __tablename__ = 'books'
    
    id = Column(String, primary_key=True) 
    title = Column(String)
    publication_year = Column(Integer)
    author_id = Column(String, ForeignKey('users.id'))
    author = relationship("User", backref="books")
