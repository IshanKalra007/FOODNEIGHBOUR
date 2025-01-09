import pytest
import Backend.Functions.ResponseFunc as ResponseFunc
from Backend.Class.Advert import Advert
from Backend.Class.Response import Response
from Backend.Class.User import User
from Main import Session


def test_create_response(): # RF1
    session = Session

    # Add data with existing user ID and advert ID
    user_id = 64
    advert_id = 75
    response_content = 'TEST'

    # Create new response
    ResponseFunc.create_response(user_id=user_id, advert_id=advert_id, response_content=response_content)
    # Finds the added response in db
    retrieve_response = session.query(Response).filter(Response.user_id==user_id).first()

    # Check the added response exists in db
    assert retrieve_response is not None

    assert retrieve_response.user_id == user_id
    assert retrieve_response.advert_id == advert_id
    assert retrieve_response.response_content == response_content

    # Delete response
    session.query(Response).filter(Response.response_content == "TEST").delete()
    session.commit()
    session.close()


def test_query_response(): # RF2
    session = Session()

    # Add data with existing user ID and advert ID
    user_id = 64
    advert_id = 75

    # Create new response
    ResponseFunc.create_response(user_id=user_id, advert_id=advert_id, response_content='TEST01')

    # Calling function using advert_id=75
    result = ResponseFunc.query_response(advert_id=advert_id)

    # Check there is only one result
    assert len(result) == 1

    for user, response in result:
        assert response.advert_id == advert_id
        assert response.user_id == user.user_id
        assert response.bookmarked is False

    # Delete response
    session.query(Response).filter(Response.user_id == user_id).delete()
    session.commit()
    session.close()


def test_query_response_with_nonexistent_id(): # RF3
    session = Session

    # Add data with existing user ID and advert ID
    user_id = 64
    advert_id = 75

    # Create new response
    ResponseFunc.create_response(user_id=user_id, advert_id=advert_id, response_content='TEST01')

    # Calling function using non-existent id/wrong id == 76
    result = ResponseFunc.query_response(advert_id=76)

    # Check there is no result
    assert len(result) == 0

    for user, response in result:
        assert response.advert_id is None
        assert response.user_id == user.user_id
        assert response.bookmarked is False

    # Delete response
    session.query(Response).filter(Response.user_id == user_id).delete()
    session.commit()
    session.close()


def test_bookmark_advert(): # RF4
    session = Session

    # Add data with existing user ID and advert ID
    advert_id = 75
    user_id = 64

    # Calling test function
    ResponseFunc.bookmark_advert(advert_id, user_id)

    # Finds the response in db
    added_response = session.query(Response).filter(Response.user_id == user_id).first()

    assert added_response is not None
    assert added_response.advert_id == advert_id
    assert added_response.user_id == user_id
    assert added_response.bookmarked is True

    # Delete response
    session.query(Response).filter(Response.user_id == 64).delete()
    session.commit()
    session.close()


def test_check_is_bookmarked_existing_bookmark(): # RF5
    session = Session

    # Add data with existing user ID and advert ID
    advert_id = 75
    user_id = 64

    # Calling function to create response with bookmark
    ResponseFunc.bookmark_advert(advert_id, user_id)

    # Calling test function
    check_bookmarked = ResponseFunc.check_is_bookmarked(advert_id, user_id, session)

    assert check_bookmarked == True

    # Delete response
    session.query(Response).filter(Response.user_id == user_id).delete()
    session.commit()
    session.close()

def test_check_is_bookmarked_nonexistent_bookmark(): # RF6
    session = Session

    # Add data with existing user ID and advert ID
    advert_id = 75
    user_id = 64

    # Calling test function
    check_bookmarked = ResponseFunc.check_is_bookmarked(advert_id, user_id, session)

    assert check_bookmarked == False
    session.commit()
    session.close()


def test_remove_bookmark(): #RF7
    session = Session

    # Add data with existing user ID and advert ID
    advert_id = 75
    user_id = 64

    # Add existing advert with bookmark
    bookmarked_advert = Response(user_id=user_id, advert_id=advert_id, response_content='', bookmarked=True)
    session.add(bookmarked_advert)
    session.commit()

    # Call test function
    removed_bookmark = ResponseFunc.remove_bookmark(advert_id, user_id)

    assert removed_bookmark[0] == True
    assert removed_bookmark[1] == 'Bookmark deleted successfully'

    session.close()


def test_remove_nonexistent_bookmark(): #RF8
    session = Session

    # Add data with existing user ID and advert ID
    advert_id = 75
    user_id = 64

    # Call function without creating new advert and bookmark
    removed_bookmark = ResponseFunc.remove_bookmark(advert_id, user_id)

    assert removed_bookmark == 'Bookmark does not exist'
    session.commit()
    session.close()


def test_remove_bookmark_failure(): # RF9
    session = Session

    # Add data with existing user ID and advert ID
    advert_id = 75
    user_id = 64

    # Add existing advert with bookmark
    bookmarked_advert = Response(user_id=user_id, advert_id=advert_id, response_content='', bookmarked=True)
    session.add(bookmarked_advert)
    session.commit()

    # Call function to expect failure
    removed_bookmark = ResponseFunc.remove_bookmark(advert_id, user_id=65) # Set wrong user_id
    assert removed_bookmark == 'Bookmark does not exist' or removed_bookmark == 'Failed to delete bookmark due to database error'

    # Finds the response in db
    added_response = session.query(Response).filter(Response.user_id==user_id).first()
    # Check response still exists in db
    assert added_response is not None

    # Delete response
    session.query(Response).filter(Response.user_id == 64).delete()
    session.commit()

    session.close()