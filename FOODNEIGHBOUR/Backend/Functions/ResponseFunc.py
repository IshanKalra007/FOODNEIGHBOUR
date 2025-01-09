from sqlalchemy.exc import IntegrityError
from Backend.Class import Advert
from Backend.Class import Response
from Backend.Class.Response import Response
from Backend.Class.User import User
from Main import Session
import Backend.Functions.AdvertFunc as AdvertFunc


def create_response(user_id, advert_id, response_content):  # function that creates a response on a specific advert
    session = Session()
    new_response = Response(user_id=user_id, advert_id=advert_id, response_content=response_content)
    session.add(new_response)
    session.commit()
    session.close()


def delete_response(session, response_id):  # deletes a response made
    response = session.query(Response).filter_by(
        response_id=response_id).first()
    if response:
        session.delete(response)
        session.commit()
        return 'Response deleted'
    else:
        return 'Response not found or owned by user or technical issue, contact Customer Support'


def respond_to_advert(session, user_id, advert_id, response_content):
    advert = session.query(Advert).filter_by(advert_id=advert_id).first()
    if advert.user_id == user_id:
        return respond_to_advert(session, user_id, advert_id, response_content)

    # Function to respond to your own advert
    return create_response(user_id, advert_id, response_content)


def query_response(advert_id):  # queries all responses of a specific advert
    session = Session()

    # finds all responses to associated advert as well as the information and the users who have responded
    responses = session.query(User, Response).join(Response, Response.user_id == User.user_id).filter(
        Response.advert_id == advert_id and Response.bookmarked == False).all()

    session.close()
    return responses


def bookmark_advert(advert_id, user_id):  # creates a response but in the form of a bookmark (bookmarked=True)
    session = Session()
    print("Bookmarked post")
    new_response = Response(user_id=user_id, advert_id=advert_id, response_content='', bookmarked=True)
    session.add(new_response)
    session.commit()
    session.close()


def check_is_bookmarked(advert_id, user_id, session=None): # check if a specific advert is bookmarked by a specific user
    close_session = False
    if session is None: session = Session(); close_session = True

    is_bookmarked = False
    bookmarked_response = session.query(Response).filter(
        (Response.user_id == user_id) & (Response.advert_id == advert_id) & (Response.bookmarked == True)).first()
    if bookmarked_response:
        is_bookmarked = True

    if close_session: session.close()
    return is_bookmarked


def remove_bookmark(advert_id, user_id): # deletes a bookmarked response
    session = Session()
    print("DELETED bookmark")
    bookmark = session.query(Response).filter(
        (Response.user_id == user_id) & (Response.advert_id == advert_id) & (Response.bookmarked == True)).first()
    if not bookmark:
        session.close()
        return 'Bookmark does not exist'
    try:
        session.delete(bookmark)
        session.commit()
        session.close()
        return True, 'Bookmark deleted successfully'
    except IntegrityError as e:
        session.rollback()
        session.close()
        return 'Failed to delete bookmark due to database error'
