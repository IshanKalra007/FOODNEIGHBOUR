from sqlalchemy import or_, desc
from Backend.Class.CurrentUser import CurrentUser
from Backend.Class.Response import Response
from Backend.Class.User import User
from Backend.Class.Advert import Advert
from Backend.Functions import ResponseFunc
from Main import Session
from datetime import datetime
from geopy import distance


def HomePageAdvertQuery():  # returns all adverts
    session = Session()
    adverts = session.query(Advert, User).join(User, Advert.user_id == User.user_id).all()
    session.close()
    return adverts


def get_user_name(advert_id):  # Get the user_name in user table based on user_id as FK in advert table
    session = Session()
    result = session.query(User.user_name).join(Advert, User.user_id == Advert.user_id).filter(
        Advert.advert_id == advert_id).first()
    return result[0] if result else None


def HomePageSearch(input):  # returns adverts dependent upon the user's input
    session = Session()
    adverts = session.query(Advert, User).join(User, Advert.user_id == User.user_id).filter(
        or_(
            Advert.advert_name.ilike(f'%{input}%'),
            Advert.advert_type.ilike(f'%{input}%'),
            Advert.advert_location.ilike(f'%{input}%'),
            Advert.advert_time.ilike(f'%{input}%'),
            User.user_name.ilike(f'%{input}%')
        )
    ).all()
    session.close()
    return adverts


# Formats the advert coordinate string to a tuple, calculates distance from given location and stores them as attributes on advert instance for later use
def determine_location(advert, target_location):
    split = [0, 0]
    if advert.advert_coord is not None: split = advert.advert_coord.split("/")
    if len(split) == 2: advert.location_coords = (split[0], split[1])
    advert.distance = distance.distance(target_location, advert.location_coords).miles


# Filters a given list of (advert,user) results according to specified criteria
def sort_and_filter(results, post_type='', sort_mode='', sort_order='', owner_id='', cur_user_id='', max_dist_filter='',
                    min_follow_count_filter='', bookmarked_only=False, cur_user_location=(0, 0)):
    # currently sorts by a given choice

    def determine_locations(results, target_location):
        for advert, user in results:
            determine_location(advert, target_location)

    def none_to_earliest(advert_time):
        return advert_time if advert_time is not None else datetime.min

    def none_to_latest(advert_time):
        return advert_time if advert_time is not None else datetime.max

    if sort_mode == "Distance" or max_dist_filter != '':
        determine_locations(results,
                            cur_user_location)  # Distance info is needed so setup info needed for location based filtering

    sorted_results = results
    if max_dist_filter != '':  # Limit results to within a given distance
        sorted_results = [result for result in sorted_results if result.Advert.distance < int(max_dist_filter)]
    if sort_mode == "Pickup Time":  # Sort by advert pick up time
        sorted_results = sorted(sorted_results, key=lambda x: none_to_earliest(x.Advert.advert_time))
    elif sort_mode == "Most Recent":  # Sort by time posted
        sorted_results = sorted(sorted_results, key=lambda x: none_to_latest(x.Advert.advert_timestamp), reverse=True)
    elif sort_mode == "Distance":  # Sort results by closest to cur_user_location (pre-calculated)
        sorted_results = sorted(sorted_results, key=lambda x: none_to_latest(x.Advert.distance))
    if post_type == "Donations":  # Limit to only donations
        sorted_results = [result for result in sorted_results if result.Advert.advert_type == "DONATION"]
    elif post_type == "Requests":  # Limit to only requests
        sorted_results = [result for result in sorted_results if result.Advert.advert_type == "REQUEST"]
    if owner_id != '':  # Limit to only adverts that a specific user has made
        sorted_results = [result for result in sorted_results if str(result.Advert.user_id) == owner_id]
    if bookmarked_only:  # Limit to only bookmarked posts [NEEDS OPTIMIZATION]
        sorted_results = [result for result in sorted_results if
                          ResponseFunc.check_is_bookmarked(result.Advert.advert_id, cur_user_id)]
    if sort_order == 'Descending':  # Inverse order of otherwise ascending results
        sorted_results.reverse()

    return sorted_results


def add_advert(name, description, location, time, type, user_id, coord):  # adds an advert to database
    session = Session()
    new_advert = Advert(
        user_id=user_id,
        advert_name=name,
        advert_description=description,
        advert_location=location,
        advert_time=time,
        advert_type=type,
        advert_coord=(str(coord[0]) + '/' + str(coord[1]))
    )
    print(new_advert.advert_name)
    session.add(new_advert)
    session.commit()
    try:
        session.commit()
        return True  # only if commit is successful
    except Exception as e:
        session.rollback()
        return False, str(e)
    finally:
        session.close()


def get_user_advertisements():  # returns all advertisements posted by the current user
    session = Session()
    current_user = CurrentUser().current_user

    if current_user is None:
        session.close()
        return []  # or handle this case as needed

    user_advertisements = session.query(Advert).join(User, Advert.user_id == User.user_id).filter_by(
        user_id=current_user.user_id).all()

    session.close()
    return user_advertisements


def get_user_mobile_phone(advert_id):  # Get the user_mobile in user table based on user_id as FK in advert table
    session = Session()
    result = session.query(User.user_mobile).join(Advert, User.user_id == Advert.user_id).filter(
        Advert.advert_id == advert_id).first()
    return result[0] if result else None


def delete_advert(advert_id):  # deletes a specific advert based on its advert_id
    session = Session()
    advert = session.query(Advert).filter_by(advert_id=advert_id).first()
    if advert:
        # Delete all responses linked to advert
        responses = session.query(Response).filter_by(advert_id=advert_id).all()
        for response in responses:
            session.delete(response)
        session.commit()
        # Delete advert
        session.delete(advert)
        session.commit()
        return 'Advert deleted'
    else:
        return 'Advert not found or owned by user or technical issue, contact Customer Support'
