from functools import wraps

from Backend.Class.User import User
from Main import Session


def role_required(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            session = Session()

            # filter user role from database
            role = session.query(User).filter(User.user_type).first()
            # If user is not authorised, return Forbidden template
            if role not in roles:
                print("Error!")  # for now, do we need any error pages?
            # Else: return function as normal
            return f(*args, **kwargs)

        return wrapped

    return wrapper
