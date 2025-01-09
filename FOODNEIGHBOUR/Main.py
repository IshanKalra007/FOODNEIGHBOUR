from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

# Import all models
from Backend.Class.User import User
from Backend.Class.Advert import Advert
from Backend.Class.Response import Response
from Backend.Class.Friend import Friend
# Set up SQLAlchemy base
Base = declarative_base()

# Create engine
engine = create_engine('mysql://sql8698080:rFpjPWykZa@sql8.freesqldatabase.com/sql8698080')

# Bind the engine to the metadata
Base.metadata.bind = engine

# Import and register models
Base.metadata.reflect(engine)
User.__table__.metadata = Base.metadata
Advert.__table__.metadata = Base.metadata
Response.__table__.metadata = Base.metadata
Friend.__table__.metadata = Base.metadata

# Manage a session
Session = scoped_session(sessionmaker(bind=engine))


def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def run_application():
    # Import FoodShareApp here to avoid circular import
    from Frontend.App import FoodShareApp
    # Run the application
    FoodShareApp().run()


# Only run the application if this script is executed directly
if __name__ == "__main__":
    import certifi
    import ssl
    import geopy.geocoders

    from geopy.geocoders import Nominatim

    ctx = ssl._create_unverified_context(cafile=certifi.where())
    geopy.geocoders.options.default_ssl_context = ctx
    run_application()
