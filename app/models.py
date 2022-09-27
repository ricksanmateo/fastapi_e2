from email.policy import default
from enum import unique
from fastapi import FastAPI
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean, text
from sqlalchemy.orm import relationship
from .database import Base

class Post(Base):
  __tablename__ = "posts"
  
  id = Column(Integer, primary_key=True, nullable=True)
  title = Column(String, nullable=False)
  content = Column(String, nullable=False)
  published = Column(Boolean, server_default='TRUE', nullable=False)
  created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
  owners_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
  
  owner = relationship("User")
  
class User(Base):
  __tablename__ = 'users'
  
  id = Column(Integer, primary_key=True, nullable=True)
  email = Column(String, nullable=False, unique=True)
  password = Column(String, nullable=False)
  created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
  
  phone_number = Column(String, nullable=False)
  
  
class Votes(Base):
  __tablename__ = 'votes'
  
  user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
  post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)