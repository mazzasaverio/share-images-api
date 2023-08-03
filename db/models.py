from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

class DbUser(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String, unique=True, index=True)
    items = relationship('DbPost', back_populates='user')

    
class DbPost(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, index=True)
    image_url_type = Column(String, index=True)
    caption = Column(String, index=True)
    timestamp = Column(DateTime)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('DbUser', back_populates='items')
