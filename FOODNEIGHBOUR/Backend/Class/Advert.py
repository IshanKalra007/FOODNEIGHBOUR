from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Advert(Base):
    __tablename__ = 'Advert'  # This is mapped to the Advert Table in the MySQL database

    advert_id = Column(Integer, primary_key=True)  # associated columns in the advert table
    user_id = Column(Integer, ForeignKey('User.user_id'))
    advert_name = Column(String)
    advert_description = Column(String)
    advert_location = Column(String)
    advert_time = Column(DateTime)
    advert_timestamp = Column(DateTime(timezone=True), server_default=func.now())
    advert_type = Column(String)
    advert_coord = Column(String)
    distance = -1

    def __init__(self, user_id, advert_name, advert_description, advert_location, advert_time, advert_type,
                 advert_coord):
        self.advert_name = advert_name
        self.advert_description = advert_description
        self.advert_location = advert_location
        self.advert_time = advert_time
        self.advert_type = advert_type
        self.user_id = user_id
        self.advert_coord = advert_coord
        self.location_coords = (0, 0)
        self.distance = -1

    def delete_advertisement(self, session):
        """ Delete the advertisement from the app"""
        session.delete(self)
        session.commit()

    def add_advertisement(self, session):
        """Add a new advertisement to the database"""
        session.add(self)
        session.commit()

    def __repr__(self):
        return f"<Advert(advert_ID={self.advert_id}, users_ID={self.user_id})>"
