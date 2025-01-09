from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):  # Associated class that is mapped to the User table in the mysql database
    __tablename__ = 'User'

    user_id = Column(Integer, primary_key=True) # Primary key users_id
    user_name = Column(String(255))
    user_password = Column(String(255))
    user_email = Column(String(255))
    user_mobile = Column(String(255))
    user_postcode = Column(String(255))
    recaptcha = Column(String(255))
    user_flag_counter = Column(Integer)
    user_type = Column(String(255))
    imagepath = Column(String(255))
    location = (0, 0)
