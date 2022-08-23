from models.api.api_handler import APIHandler


class UserHandler:
    """
    User Handler class
    """
    def __init__(self):
        """
        Constructor.
        """
        self.api_handler = APIHandler("/user")

    def authenticate_user(self, username, password):
        """
        Authenticates a user by verifying username and password

        :param username: Username to verify
        :param password: Password to verify
        :return: True if user credentials and JWT valid, False otherwise
        """
        try:
            # Authenticate username and password and try to get JWT
            jwt = self.api_handler.post(
                extension="/login",
                params={'jwt': 'true'},
                data={
                    'userName': username,
                    'password': password
                }
            )["jwt"]

            try:
                # Verify JWT
                self.api_handler.post(
                    extension="/verify-token",
                    data={'jwt': jwt}
                )
            except ImportError:
                # JWT Invalid
                return False
            else:
                # JWT Valid, Login Successful
                return True

        except ImportError:
            # Username or password incorrect, reject login
            return False

    def get_user_id(self, username):
        """
        Get the user ID from a username

        :param username: Username as str
        :return: User ID as str
        """
        user = self.get_user(username)
        return user["id"]

    def get_users(self):
        """
        Get all users from server

        :return: List of all users as dictionary
        """
        return self.api_handler.get(params={'fields': "bookings"})

    def get_user(self, username):
        """
        Gets a user by username

        :param username: Username of wanted user
        :return: User as dictionary object
        :raises KeyError: If user not found
        """
        users = self.get_users()
        for user in users:
            if user["userName"] == username:
                return user
        raise KeyError("User not found")
