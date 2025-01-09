import os

import pytest
import Backend.Functions.UsersFunc as UsersFunc
from Backend.Class.User import User
from Main import Session


# VERIFICATION/VALIDATION FUNCTION TESTS
def test_verify_username_valid():  # UF1
    assert UsersFunc.verify_username("John") == True  # has present characters


def test_verify_username_invalid():  # UF2
    assert UsersFunc.verify_username("") == "Invalid Username"  # is empty
    assert UsersFunc.verify_username(None) == "Invalid Username"  # is None
    assert UsersFunc.verify_username("   ") == "Invalid Username"  # whitespace - issue found


def test_verify_phone_valid():  # UF3
    assert UsersFunc.verify_phone("0794567435") == True
    assert UsersFunc.verify_phone("447123434289") == True


def test_verify_phone_invalid():  # UF4
    assert UsersFunc.verify_phone("") == "Invalid Phone Number"  # empty
    assert UsersFunc.verify_phone("0123456789") == "Invalid Phone Number"  # wrong format
    assert UsersFunc.verify_phone("07123456789012345") == "Invalid Phone Number"  # too long
    assert UsersFunc.verify_phone("0712abc456") == "Invalid Phone Number"  # invalid characters
    assert UsersFunc.verify_phone("0712-345-6789") == "Invalid Phone Number"  # wrong structure


def test_verify_postcode_valid():  # UF5
    assert UsersFunc.verify_postcode("NE1 5LA") == True
    assert UsersFunc.verify_postcode("NE1B 5LA") == True
    assert UsersFunc.verify_postcode("NE11 5LA") == True


def test_verify_postcode_invalid():  # UF6
    assert UsersFunc.verify_postcode("") == "Invalid Postcode"  # empty
    assert UsersFunc.verify_postcode("24L A22") == "Invalid Postcode"  # incorrect format
    assert UsersFunc.verify_postcode("NE43LA") == "Invalid Postcode"  # incorrect spacing


def test_verify_password_valid():  # UF7
    assert UsersFunc.verify_password("Password1!") == True


def test_verify_password_invalid():  # UF8
    assert UsersFunc.verify_password("") == "Invalid Password"  # too short/empty
    assert UsersFunc.verify_password("password1!") == "Invalid Password"  # no uppercase
    assert UsersFunc.verify_password("PASSWORD1!") == "Invalid Password"  # no lowercase
    assert UsersFunc.verify_password("Password!") == "Invalid Password"  # no number
    assert UsersFunc.verify_password("Password123") == "Invalid Password"  # no special char


def test_validate_datetime_format_valid():  # UF9
    assert UsersFunc.validate_datetime_format("2020-01-23 12:30:00") == True  # correct format


def test_validate_datetime_format_invalid():  # UF10
    assert UsersFunc.validate_datetime_format("2020-01-23") == "Follow Format: YYYY-MM-DD HH:MM:SS"  # just date
    assert UsersFunc.validate_datetime_format("12:30:00") == "Follow Format: YYYY-MM-DD HH:MM:SS"  # just time
    assert UsersFunc.validate_datetime_format(
        "2020-23-01 12:30:00") == "Follow Format: YYYY-MM-DD HH:MM:SS"  # wrong format - issue found


def test_verify_login_inputs():  # UF11
    assert UsersFunc.verify_login_inputs("valid@example.com", "ValidPassword!1") == (True, None)
    assert UsersFunc.verify_login_inputs("email", "password") == (False, ["Invalid email", "Invalid password"])
    assert UsersFunc.verify_login_inputs("", "ValidPassword1!") == (False, ["Invalid email"])
    assert UsersFunc.verify_login_inputs("valid@example.com", "") == (False, ["Invalid password"])


def test_validate_email_login():  # UF12
    assert UsersFunc.validate_email_login("") == "Invalid email"
    assert UsersFunc.validate_email_login("test") == "Invalid email"
    assert UsersFunc.validate_email_login("test@") == "Invalid email"
    assert UsersFunc.validate_email_login("test@gmail") == "Invalid email"
    assert UsersFunc.validate_email_login("test@gmail.com") == True


def test_verify_inputs():  # UF13
    assert UsersFunc.verify_inputs("validuser", "valid@example.com", "07944414625", "NE2 4LA",
                                   "ValidPassword1!") == True
    assert UsersFunc.verify_inputs("", "valid@example.com", "07944414625", "NE2 4LA", "ValidPassword1!") == (
        False, ["Invalid Username"])
    assert UsersFunc.verify_inputs("validuser", "invalid@example", "07944414625", "NE2 4LA", "ValidPassword1!") == (
        False, ["Invalid email"])
    assert UsersFunc.verify_inputs("validuser", "valid@example.com", "invalidphone", "NE2 4LA", "ValidPassword1!") == (
        False, ["Invalid Phone Number"])
    assert UsersFunc.verify_inputs("validuser", "valid@example.com", "07944414625", "invalidpostcode",
                                   "ValidPassword1!") == (
               False, ["Invalid Postcode"])
    assert UsersFunc.verify_inputs("validuser", "valid@example.com", "07944414625", "NE2 4LA", "invalidpassword") == (
        False, ["Invalid Password"])
    assert UsersFunc.verify_inputs("", "invalid@example", "invalidphone", "invalidpostcode", "invalidpassword") == (
        False, ["Invalid Username", "Invalid email", "Invalid Phone Number", "Invalid Postcode", "Invalid Password"])


def test_verify_email_reg():  # UF14
    assert UsersFunc.verify_email_reg("testuser@gmail.com") == "Email already registered"  # fail as it is already in db
    assert UsersFunc.validate_email_login("") == "Invalid email"
    assert UsersFunc.validate_email_login("test") == "Invalid email"
    assert UsersFunc.validate_email_login("test@") == "Invalid email"
    assert UsersFunc.validate_email_login("test@gmail") == "Invalid email"
    assert UsersFunc.validate_email_login("test@gmail.com") == True


def test_verify_current_password():  # UF15
    assert UsersFunc.verify_current_password("Password1!", 64) == True
    assert UsersFunc.verify_current_password("NotCurrentPassword", 64) == "Current password does not match"


# UPDATE FUNCTION TESTS
def test_update_postcode():  # UF16
    assert UsersFunc.update_postcode("NE1 4AL", 64) == True  # updated so should be true
    assert UsersFunc.update_postcode("NE1 4AL", 64) == False  # Is the same so should fail
    assert UsersFunc.update_postcode("TEST_USER", 64) == False  # Not correct format
    assert UsersFunc.update_postcode("NE1 2BL", 64) == True  # different postcode to reset test


def test_update_phone(): # UF17
    assert UsersFunc.update_phone("07944784626", 64) == True
    assert UsersFunc.update_phone("07944784626", 64) == False  # The same as previous should fail
    assert UsersFunc.update_phone("TEST_USER", 64) == False  # wrong format should fail
    assert UsersFunc.update_phone("07944414626", 64) == True


def test_update_password(): # UF18
    assert UsersFunc.update_password("Password!1", 64) == True
    assert UsersFunc.update_password("Password!1", 64) == False  # The same as previous should fail
    assert UsersFunc.update_password("Password", 64) == False  # wrong format should fail
    assert UsersFunc.update_password("Password1!", 64) == True  # reset password for next time this function is ran


def test_update_email(): # UF19
    assert UsersFunc.update_email("testuser1@gmail.com", 64) == True
    assert UsersFunc.update_email("testuser1@gmail.com", 64) == False  # The same as previous should fail
    assert UsersFunc.update_email("test_user", 64) == False  # wrong format should fail
    assert UsersFunc.update_email("testuser@gmail.com", 64) == True  # reset email for next time function is ran


# OTHER FUNCTION TESTS
def test_authenticate_user(): # UF20
    assert UsersFunc.authenticate_user("testuser@gmail.com", "Password1!") == True  # both correct return true
    assert UsersFunc.authenticate_user("testuser@gmail.com", "Wrong Password") == False  # incorrect password
    assert UsersFunc.authenticate_user("Wrong email", "Password1!") == False  # incorrect email


def test_count_friend_valid(): # UF21
    # Test count_friends function
    # created a test user (ID = 64)
    assert UsersFunc.count_friends(64) == 1


def test_set_profile_picture_valid(): # UF22
    session = Session()
    UsersFunc.set_profile_picture(64, "Images/5.png")  # choice as 5, can change this
    session.commit()
    test_user = session.query(User).filter(User.user_id == 64).first()
    session.close()
    assert test_user.imagepath == "Images/5.png"  # change this if choice is changed


def test_give_random_profile_picture(): # UF23
    profile_picture_path = UsersFunc.give_random_profile_picture()
    assert isinstance(profile_picture_path, str)  # Check if the path is a string
    assert profile_picture_path.startswith('Images/')  # Check if the path starts with 'Images/'
    assert profile_picture_path.endswith('.png')  # Check if the path ends with '.png'
    image_number = int(profile_picture_path.split('/')[1].split('.')[0])
    assert 1 <= image_number <= 9  # Check if the image number is between 1 and 9


def test_add_user_valid(): # UF24
    session = Session()
    add_user = UsersFunc.add_user("TEST", "TEST", "TEST", "TEST", "TEST")  # creates a user
    retrieve_user = session.query(User).filter(User.user_email == "TEST").first()  # finds user in the database
    assert add_user == True  # add function should return true
    assert retrieve_user.user_email == "TEST"  # if the user is actually in the database
    session.query(User).filter(User.user_email == "TEST").delete()  # then deletes said user
    session.commit()
    session.close()


def test_report_user_valid(): # UF25
    session = Session()
    before_flag = session.query(User).filter(User.user_id == 64).first()  # finds test user
    current_count = before_flag.user_flag_counter  # saves test user flag counter
    UsersFunc.report_user(75)  # id of test advert associated with test user
    after_flag = session.query(User).filter(User.user_id == 64).first()  # saves their new flag counter
    assert after_flag.user_flag_counter == current_count + 1
    session.close()


def test_get_user(): # UF26
    session = Session()
    user = UsersFunc.get_user(64)
    assert user.user_id == 64
    session.close()


def test_is_true(): # UF27
    assert UsersFunc.is_true(True) == True
    assert UsersFunc.is_true(False) == False
