
class CurrentAdvert: # Class that saves the current advert as an instance
    _instance = None
    current_advert = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CurrentAdvert, cls).__new__(cls)
        return cls._instance