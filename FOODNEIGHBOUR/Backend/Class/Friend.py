from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Friend(Base): # The Friend Class mapped to the Friend table in the database
    __tablename__ = 'Friend'

    user_id = Column(Integer, ForeignKey('User.user_id'), primary_key=True) # Associated columns of the Friend Table
    friend_id = Column(Integer, primary_key=True) # Composite key formed of user_id and friend_id
    friend_status = Column(String)  # status = pending/accepted/denied

    def __init__(self, user_id, friend_id, friend_status='pending'):
        self.user_id = user_id
        self.friend_id = friend_id
        self.friend_status = friend_status

    def accept_friendship(self):
        "accept a friendship request"
        self.friend_status = 'accepted'

    def decline_friendship(self):
        """Decline a friendship request"""
        self.friend_status = 'declined'

        def __repr__(self):
            return f"<Friends(users_ID={self.user_id}, friend_ID={self.friend_id}, status={self.friend_status})>"
