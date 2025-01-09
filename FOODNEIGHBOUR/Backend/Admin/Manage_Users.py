# Extract_Customer_Info
# Block_Customer_Account
# Edit_Customer_Account

from Main import Session
from Backend.Class.User import User
from Backend.Admin.Login import role_required
from Backend.Functions.UsersFunc import verify_inputs
from Backend.Class.Friend import Friend


# Remove a user from the database
@role_required('ADMIN')
def remove_user(client_email):
    session = Session()

    try:
        # Query the User table to find a user with the given email
        user = session.query(User).filter(User.user_email == client_email).first()
        user_id = user.user_id

        # Check the user exists in the database and its user_type is user the admin
        if user and user.user_type == 'USER':

            session.query(Friend).filter((Friend.user_id == user_id) | (Friend.friend_id == user_id)).delete()

            # Commit the changes for deleting friends
            session.commit()
            # Delete the user from the db
            session.delete(user)
            session.commit()
            return True
        else:
            return False
    finally:
        session.close()


# Change a user's role to admin
@role_required('ADMIN')
def change_user_role(client_email):
    session = Session()

    try:
        # Query the User table to find a user with the given email
        user = session.query(User).filter(User.user_email == client_email).first()

        # Checks the user exists in the database and its user_type is user the admin
        if user and user.user_type == 'USER':
            # Change the type of the user to admin
            user.user_type = 'ADMIN'
            session.commit()
            session.close()
            return True
        else:
            return False
    finally:
        session.close()


# Adding a new admin
@role_required('ADMIN')
def new_admin(username, email, phone, postcode, password):
    session = Session()

    # Verify the format of the inputs
    if verify_inputs(username, email, phone, postcode, password):
        # Create a new admin
        new_admin = User(
            user_name=username,
            user_password=password,
            user_email=email,
            user_mobile=phone,
            user_postcode=postcode,
            user_flag_counter=0,
            user_type='ADMIN'
        )
        # Add the new admin to the db
        session.add(new_admin)
        session.commit()
        session.close()
        return True
    else:
        return False

