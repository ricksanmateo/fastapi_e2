from sqlite3 import SQLITE_ALTER_TABLE
from unicodedata import name
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

hostname = settings.database_hostname
port = settings.database_port
password = settings.database_password
name = settings.database_name
username = settings.database_username

# SQLALCHEMY_DATABASE_URL = 'postgres://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{username}:{password}@{hostname}:{port}/{name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
  db = SessionLocal()
  
  try:
    yield db
  finally:
    db.close()