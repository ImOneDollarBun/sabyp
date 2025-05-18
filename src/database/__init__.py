from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import Database

engine = create_engine(Database.url)
SessionLocal = sessionmaker(engine)

Base = declarative_base()
