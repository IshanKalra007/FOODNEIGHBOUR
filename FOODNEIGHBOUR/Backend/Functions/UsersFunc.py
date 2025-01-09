from sqlalchemy import func

from Backend.Class.Advert import Advert
from Backend.Class.CurrentUser import CurrentUser
from Backend.Class.Friend import Friend
from Backend.Class.User import User
from Main import Session
from captcha.image import ImageCaptcha

import re
import random
import hashlib

current_user = None


# VALIDATION/VERIFICATION FUNCTIONS
def verify_username(username):  # checks if the username is actually filled
    if username and username.strip():
        return True
    else:
        return "Invalid Username"


def verify_email_reg(email):  # Checks if email is already in db and that it is correct format
    session = Session()
    try:
        user = session.query(User).filter(
            User.user_email == email).first()
        if user:
            return "Email already registered"

        validation = bool(re.match(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}\b", email))
        if not validation:
            return "Invalid email"
        else:
            return True
    finally:
        session.close()


def verify_phone(phone):  # checks if the phone number is the correct Uk format
    if bool(re.match(r"^(07[\d]{8,12}|447[\d]{7,11})$", phone)):
        return True
    else:
        return "Invalid Phone Number"


def verify_postcode(postcode):  # checks if the postcode is the correct Uk format
    if bool(re.match(r"^[A-Z]{1,2}[0-9]{1,2}[A-Z]? [0-9][A-Z]{2}$", postcode)):
        return True
    else:
        return "Invalid Postcode"


def verify_password(password):  # checks if the password is the correct format
    if bool(re.match(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$", password)):
        return True
    else:
        return "Invalid Password"


def verify_inputs(username, email, phone, postcode, password):  # backend confirmation that inputs are correct
    errors = []

    user_ver = verify_username(username)
    email_ver = verify_email_reg(email)
    phone_ver = verify_phone(phone)
    postcode_ver = verify_postcode(postcode)
    password_ver = verify_password(password)

    if is_true(user_ver) and is_true(email_ver) and is_true(phone_ver) and is_true(postcode_ver) and is_true(
            password_ver):  # if all return true
        return True
    else:
        if not (is_true(user_ver)): errors.append(user_ver)
        if not (is_true(email_ver)): errors.append(email_ver)
        if not (is_true(phone_ver)): errors.append(phone_ver)
        if not (is_true(postcode_ver)): errors.append(postcode_ver)
        if not (is_true(password_ver)): errors.append(password_ver)

    if not verify_username(username):
        errors.append("Invalid username")  # if verification fails add username error to list

    if not verify_email_reg(email):
        errors.append("Invalid or already existing email")  # if verification fails add email error to list

    if not verify_phone(phone):
        errors.append("Invalid phone number")  # if verification fails add phone error to list

    if not verify_postcode(postcode):
        errors.append("Invalid postcode")  # if verification fails add postcode error to list

    if not verify_password(password):  # if verification fails add password error to list
        errors.append("Invalid password or passwords don't match")

    if errors:
        return False, errors  # Return False and the list of errors
    else:
        return True, None  # Return True if all validations pass, with no errors


def validate_email_login(email):  # Validates email input for login page (without checking if its already in db)
    validation = bool(re.match(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}\b", email))
    if not validation:
        return "Invalid email"
    else:
        return True


def validate_datetime_format(datetime_str):  # validates that the date/time is in the correct format
    # Define the regex pattern for datetime format 'YYYY-MM-DD HH:MM:SS'
    pattern = r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01]) \d{2}:\d{2}:\d{2}$"

    # Match the pattern with the input string
    if bool(re.match(pattern, datetime_str)):
        return True
    else:
        return "Follow Format: YYYY-MM-DD HH:MM:SS"


def verify_login_inputs(email, password):  # similarly makes sure that both are login details are valid
    errors = []

    if validate_email_login(email) == "Invalid email":
        # if verification fails add email error to list
        errors.append("Invalid email")

    if verify_password(password) == "Invalid Password":
        # if verification fails add password error to list
        errors.append("Invalid password")

    if errors:
        # Return False and the list of errors
        return False, errors
    else:
        # Return True if all validations pass, with no errors
        return True, None


def verify_current_password(current_password, user_id):
    session = Session()

    # Query the User table to find the user with the given user_id and current password
    user = session.query(User).filter(User.user_id == user_id,
                                      User.user_password == current_password).first()

    if user:
        # Current password matches
        return True
    else:
        return 'Current password does not match'


# UPDATE FUNCTIONS
def update_email(new_email, user_id):  # updates a given users email
    session = Session()
    user = session.query(User).filter(User.user_id == user_id).first()

    if new_email == user.user_email:  # if new email and current are same return false
        return False
    else:
        if verify_email_reg(new_email) == True:  # This must == True for it to work
            # User.update_email(user, new_email)
            user = session.query(User).filter(
                User.user_id == user_id).first()  # finds the current user in db
            user.user_email = new_email  # replaces their current email with the new one

            session.commit()
            session.close()
            return True
        else:
            return False


def update_password(new_password, user_id):  # updates a given users password
    session = Session()

    try:
        user = session.query(User).filter(User.user_id == user_id).first()

        if new_password == user.user_password:
            return False

        if verify_password(new_password) == True:
            user.user_password = new_password
            session.commit()
            return True
        else:
            return False
    finally:
        # Always close the session
        session.close()


def update_phone(new_mobile, user_id):  # updates a given users phone
    # Creates a new session
    session = Session()
    try:
        # Gets the current user
        user = session.query(User).filter(User.user_id == user_id).first()

        # If the new phone number and the current are the same return false
        if new_mobile == user.user_mobile:
            return False

        # Checks if the new phone number is correct format
        if verify_phone(new_mobile) == True:
            # Replaces the current phone number with the new one
            user.user_mobile = new_mobile

            session.commit()
            return True
        else:
            return False
    finally:
        # Always close the session
        session.close()


def update_postcode(new_postcode, user_id):  # updates a given users postcode
    session = Session()

    try:
        user = session.query(User).filter(User.user_id == user_id).first()

        if new_postcode == user.user_postcode:
            return False

        if verify_postcode(new_postcode) == True:
            user.user_postcode = new_postcode
            session.commit()
            return True
        else:
            return False
    finally:
        # Always close the session
        session.close()


# OTHER FUNCTIONS
def set_profile_picture(user_id, choice):  # sets profile picture of user based on choice
    session = Session()
    user = session.query(User).filter(User.user_id == user_id).first()
    user.imagepath = choice
    session.commit()
    session.close()
    return


def give_random_profile_picture():  # sets random profile picture for when a user is first made
    image_path = f'Images/{str(random.randint(1, 9))}.png'
    return image_path


def count_friends(user_id):  # counts the number of friends a user has
    session = Session()
    count = session.query(func.count(Friend.friend_id)).filter(
        Friend.user_id == user_id or Friend.friend_id == user_id).scalar()  # counts number of friends associated with provided user
    session.close()
    return count


def add_user(username, password, email, phone, postcode):  # adds a new user to the database
    session = Session()
    new_user = User(
        user_name=username,
        user_password=password,
        user_email=email,
        user_mobile=phone,
        user_postcode=postcode,
        user_flag_counter=0,
        user_type='USER',
        imagepath=give_random_profile_picture()
    )
    session.add(new_user)
    session.commit()
    session.close()
    return True


def report_user(advert_id):  # reports a user based of a connected advert they posted
    session = Session()
    advert = session.query(Advert).filter_by(advert_id=advert_id).first()  # finds advert with specific id
    user = session.query(User).filter(User.user_id == advert.user_id).first()  # finds the user who created said advert
    user.user_flag_counter += 1  # adds +1 counter to flag counter for that user
    session.commit()
    session.close()


def is_true(true_or_error):
    string = str(true_or_error)  # converts input to string (either boolean or string)
    return string == "True"  # returns true if input is True


def get_user(user_id):  # finds the user based off of user_id and returns said user
    session = Session()
    user = session.query(User).filter(User.user_id == int(user_id)).first()
    session.close()
    return user


def authenticate_user(email, password):  # sets the user session when the user logs in
    global current_user
    session = Session()

    # Query the User table to find a user with the given email and password
    user = session.query(User).filter(User.user_email == email, User.user_password == password).first()

    session.close()

    if user:
        # Authentication successful
        CurrentUser().current_user = user  # sets current user in current user class
        return True
    else:
        return False


# CAPTCHA FUNCTIONS
# NOT TESTING CAPTCHA FUNCTIONS AS WE AREN'T USING IT

def generate_captcha():  # Generate a random CAPTCHA string
    captcha_length = 6
    captcha_characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    captcha = ''.join(random.choices(captcha_characters, k=captcha_length))
    return captcha


# Generate CAPTCHA image
def generate_captcha_image(captcha):
    image = ImageCaptcha()
    data = image.generate(captcha)
    return data


# Hash the CAPTCHA response
def hash_captcha_response(captcha_response):
    hashed_response = hashlib.sha256(captcha_response.encode()).hexdigest()
    return hashed_response


# Verify CAPTCHA response
def verify_captcha(captcha, captcha_response):
    expected_hash = hash_captcha_response(captcha)
    provided_hash = hash_captcha_response(captcha_response)
    if expected_hash == provided_hash:
        return True
    else:
        return False
