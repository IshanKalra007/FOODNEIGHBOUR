import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Backend.Class.Friend import Friend
from Backend.Class.User import User
import Backend.Functions.FriendshipFunc as FriendFunc
from Main import Session


@pytest.fixture(scope='function')
def setup_database():
    # Setup: create a new session and add sample users
    session = Session()
    user1 = User(user_id=7, user_name="User7", user_email="User7@gmail.com", user_mobile="0700000007",
                 user_postcode="NE7 9PO", user_flag_counter=0, user_type="USER")
    user2 = User(user_id=8, user_name="User8", user_email="User8@gmail.com", user_mobile="0700000008",
                 user_postcode="AT5 9PO", user_flag_counter=0, user_type="USER")
    session.add(user1)
    session.add(user2)
    session.commit()
    yield session
    # Teardown: delete the sample users
    session.query(Friend).filter(Friend.user_id.in_([7, 8]) | Friend.friend_id.in_([7, 8])).delete()
    session.query(User).filter(User.user_id.in_([7, 8])).delete()
    session.commit()
    session.close()


def test_add_friend(setup_database):  # FF1
    session = setup_database
    result, message = FriendFunc.add_friend(7, 8)
    assert result == True
    assert message == 'Friend added successfully'
    # Verify the friendship was added
    friendship = session.query(Friend).filter_by(user_id=7, friend_id=8).first()
    assert friendship is not None


def test_add_friend_invalid_user(setup_database):  # FF2
    result = FriendFunc.add_friend(999, 1)
    assert result == 'Invalid user ID'
    result = FriendFunc.add_friend(7, 1000)
    assert result == 'Invalid friend ID'


def test_add_friend_existing_friendship(setup_database):  # FF3
    session = setup_database
    FriendFunc.add_friend(7, 8)  # Add the friendship first
    result = FriendFunc.add_friend(7, 8)
    assert result == 'Friendship already exists'


def test_check_friendship_exists(setup_database):  # FF4
    session = setup_database
    FriendFunc.add_friend(7, 8)
    assert FriendFunc.check_friendship_exists(7, 8) is not None
    assert FriendFunc.check_friendship_exists(7, 999) is None


def test_list_friends(setup_database):  # FF5
    session = setup_database
    FriendFunc.add_friend(7, 8)
    friends = FriendFunc.list_friends(7)
    assert isinstance(friends, list)
    assert "User8" in friends
    friends = FriendFunc.list_friends(8)
    assert "User7" in friends


def test_delete_friend(setup_database):  # FF6
    session = setup_database
    FriendFunc.add_friend(7, 8)
    result, message = FriendFunc.delete_friend(7, 8)
    assert result == True
    assert message == 'Friendship deleted successfully'
    friendship = session.query(Friend).filter_by(user_id=7, friend_id=8).first()
    assert friendship is None


def test_delete_nonexistent_friend(setup_database):  # FF7
    session = setup_database
    result = FriendFunc.delete_friend(7, 999)
    assert result == 'Friendship does not exist'
    result = FriendFunc.delete_friend(999, 8)
    assert result == 'Friendship does not exist'
