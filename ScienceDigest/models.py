from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, UniqueConstraint
import datetime


Base = declarative_base()


# User Table
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    picture = Column(String(300))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
           'name': self.name,
           'id': self.id,
           'email': self.email
        }


# category table
class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), unique=True)
    # Add a property decorator to serialize information from this database

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id
        }


class Articles(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    about = Column(String, nullable=False)
    category_name = Column(String, ForeignKey('categories.name'))
    categories = relationship(Categories)
    time = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    picture = Column(String(300))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'about': self.about,
            'category_name': self.category_name,
            'updated_time': self.time
        }


engine = create_engine('postgresql://catalog:catalog@localhost/catalog')

Base.metadata.create_all(engine)
