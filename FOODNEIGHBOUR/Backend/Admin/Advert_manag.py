from sqlalchemy.orm import Session
from Backend.Admin.Login import role_required
from Backend.Class.Advert import Advert
from Backend.Functions.AdvertFunc import HomePageSearch, sort_and_filter, get_user_advertisements


@role_required('ADMIN')
def view_adverts():
    session = Session()
    adverts = session.query(Advert).all()
    session.close()
    return adverts


@role_required('ADMIN')
def remove_advert(advert_id):
    session = Session()
    advert = session.query(Advert).filter(Advert.advert_id == advert_id).first()
    if advert:
        session.delete(advert)
        session.commit()
        session.close()
        return True
    else:
        session.close()
        return False


@role_required('ADMIN')
def admin_home_page_search(input):
    return HomePageSearch(input)

@role_required('ADMIN')
def admin_sort_and_filter(choice, results):
    return sort_and_filter(choice, results)


@role_required('ADMIN')
def admin_get_user_advertisements(user_id):
    return get_user_advertisements(user_id)

