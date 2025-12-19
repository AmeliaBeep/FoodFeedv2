from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./foodfeed.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}) # connects to DB
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False) # lets you do CRUD
Base = declarative_base() # base for ORM