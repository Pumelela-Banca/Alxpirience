"""
User base file with sql structure
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()


class User(Base):
    """
    creates user storage system with id, email, password
    session_id, reset_tokken, jobs, seeking, description, country
    """
    pass
