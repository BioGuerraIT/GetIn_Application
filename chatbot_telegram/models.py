from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    chat_id = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)
    school = Column(String)
    email = Column(String)
    bio = Column(String)
    preferences = Column(String)

def initialize_database(engine):
    Base.metadata.create_all(engine)
