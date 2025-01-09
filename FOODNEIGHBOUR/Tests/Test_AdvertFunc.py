
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Backend.Class.Advert import Advert
from Backend.Class.CurrentUser import CurrentUser
from Backend.Class.User import User
import Backend.Functions.AdvertFunc as AdvertFunc
from Main import Session


def add_sample_data():
    session = Session()
    advert = Advert(advert_name="KATSU CURRY", advert_description="Very yum yum food", advert_location="NE2 1HQ", advert_time="2023-01-01 12:00:00", advert_type="DONATION", user_id=(64),advert_coord = "-0.2/0.5")
    session.add(advert)
    session.commit()
    session.close()
    return advert

def test_HomePageAdvertQuery():
    session = Session()
    added_advert = add_sample_data()
    homepage_ads = AdvertFunc.HomePageAdvertQuery()
    assert isinstance(homepage_ads, list)
    assert len(homepage_ads) > 0
    for ad in homepage_ads:
        assert hasattr(ad.Advert, "advert_name")
        assert hasattr(ad.Advert, "advert_description")
        assert hasattr(ad.Advert, "advert_location")
    session.delete(added_advert)
    session.commit()
    session.close()

def test_HomePageSearch():
    session = Session()
    added_advert = add_sample_data()
    search_results = AdvertFunc.HomePageSearch("KATSU CURRY")
    assert isinstance(search_results, list)
    assert len(search_results) > 0
    for result in search_results:
        assert hasattr(result.Advert, "advert_name")
        assert hasattr(result.Advert, "advert_description")
        assert hasattr(result.Advert, "advert_location")
    session.delete(added_advert)
    session.commit()
    session.close()

def test_sort_and_filter():
    session = Session()
    added_advert = add_sample_data()
    results = AdvertFunc.HomePageAdvertQuery()
    sorted_filtered_results = AdvertFunc.sort_and_filter(results, post_type="DONATION")
    assert isinstance(sorted_filtered_results, list)
    assert len(sorted_filtered_results) > 0
    for result in sorted_filtered_results:
        assert hasattr(result, 'Advert')
    session.delete(added_advert)
    session.commit()
    session.close()


def test_add_advert():
    session = Session()
    result = AdvertFunc.add_advert(
        "FRIED RICE",
        "Tooo good",
        "NE1 7RU",
        "2023-01-02 12:00:00",
        "REQUEST", # Example coordinates
        64,
        (54.9784, -1.6174)
    )
    assert result is True, "Advert was not added successfully."
    added_advert = session.query(Advert).filter_by(advert_name="FRIED RICE", user_id=64).first()
    assert added_advert is not None, "Advert was not found in the database."
    session.delete(added_advert)
    session.commit()
    session.close()



def test_get_user_mobile_phone():
    session = Session()
    added_advert = add_sample_data()
    advert = session.query(Advert).first()
    user_phone = AdvertFunc.get_user_mobile_phone(advert.advert_id)
    assert isinstance(user_phone, str)
    assert user_phone == "07944784626"
    session.delete(added_advert)
    session.commit()
    session.close()



