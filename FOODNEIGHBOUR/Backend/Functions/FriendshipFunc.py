from Backend.Class.Friend import Friend
from Backend.Class.User import User
from Main import session_scope
from sqlalchemy.exc import IntegrityError
from Main import Session


def add_friend(user_id, friend_id):  # adds a friend based on the current users id and the friends id
    session = Session()
    if not session.query(User).filter(User.user_id == user_id).scalar():
        session.close()
        return 'Invalid user ID'
    if not session.query(User).filter(User.user_id == friend_id).scalar():
        session.close()
        return 'Invalid friend ID'
    # check if friend already exists
    if check_friendship_exists(user_id, friend_id, session):
        session.close()
        return 'Friendship already exists'
    # Add new friend
    new_friendship = Friend(user_id=user_id, friend_id=friend_id)
    session.add(new_friendship)
    try:
        session.commit()
        session.close()
        return True, 'Friend added successfully'
    except IntegrityError as e:
        session.rollback()
        session.close()
        return 'Failed to add friendship due to database error'


def check_friendship_exists(user_id, friend_id, session=None): # checks to see if a friendship connection exists between two users
    close = False
    if session is None:
        session = Session()
        close = True
    exists = (session.query(Friend).filter(Friend.user_id == user_id, Friend.friend_id == friend_id).scalar() or
              session.query(Friend).filter(Friend.user_id == friend_id, Friend.user_id == user_id).scalar())
    if close: session.close()
    return exists


def list_friends(user_id): # lists all friends of a specific user
    session = Session()
    friendships = session.query(Friend).filter((Friend.user_id == user_id) | (Friend.friend_id == user_id)).all()
    friend_ids = [f.friend_id if f.user_id == user_id else f.user_id for f in friendships]
    friends = session.query(User).filter(User.user_id.in_(friend_ids)).all()
    session.close()
    return [f.user_name for f in friends]


# Using database query verification rather than regex because regex checks string format
# while database query checks the existence of data in the DB.
# Will use regex for form filling

def delete_friend(user_id, friend_id): # deletes a friendship connection between two users
    session = Session()
    friendship = session.query(Friend).filter(((Friend.user_id == user_id) & (Friend.friend_id == friend_id)) |
                                              ((Friend.user_id == friend_id) & (Friend.friend_id == user_id))).first()
    if not friendship:
        session.close()
        return 'Friendship does not exist'
    try:
        session.delete(friendship)
        session.commit()
        session.close()
        return True, 'Friendship deleted successfully'
    except IntegrityError as e:
        session.rollback()
        session.close()
        return 'Failed to delete friendship due to database error'
