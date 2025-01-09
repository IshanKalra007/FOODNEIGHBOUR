import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Response(Base): # Associated to the Response table in the database
    __tablename__ = 'Response'

    response_id = Column(Integer, primary_key=True) # Associated columns mapped to those in response table
    user_id = Column(Integer, ForeignKey('User.user_id'))
    advert_id = Column(Integer, ForeignKey('Advert.advert_id')) # forms a many-to-many relationship between adverts and users
    response_content = Column(String(1000))
    response_timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    bookmarked = Column(Boolean, default=False) # responses can be in the form of a bookmark

    def __init__(self, user_id, advert_id, response_content, bookmarked=False):
        self.user_id = user_id
        self.advert_id = advert_id
        self.response_content = response_content
        self.bookmarked = bookmarked

    def __repr__(self):
        return f"<Response(response_id={self.response_id}, user_id={self.user_id}, advert_id={self.advert_id}, " \
               f"timestamp={self.response_timestamp})>"
