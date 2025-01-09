class CurrentUser:  # saves a user as a current user and creates a session
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.user = None
        return cls._instance

    @property
    def current_user(self):
        return self.user

    @current_user.setter
    def current_user(self, user):
        self.user = user
