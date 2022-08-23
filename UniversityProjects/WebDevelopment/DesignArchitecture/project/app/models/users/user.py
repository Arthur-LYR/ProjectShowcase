from models.users.user_roles import UserRoles


class User(object):
    """
    User Singleton Class. Python Singleton implementation obtained from
    https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
    """
    INSTANCE = None

    def __new__(cls, user):
        """
        Override __new__ magic method to apply Singleton

        :param username: Username of user
        """
        if not isinstance(cls.INSTANCE, cls):
            cls.INSTANCE = object.__new__(cls)
        return cls.INSTANCE

    def __init__(self, user):
        """
        Constructor

        :param user: User as dict object
        """
        self.user_id = user["id"]
        self.username = user["userName"]
        self.user_roles = UserRoles(user["isCustomer"], user["isReceptionist"], user["isHealthcareWorker"])
        self.test_site = user['additionalInfo']['testSite']

    @classmethod
    def create_instance(cls, user):
        """
        Creates an instance of User

        :param user: User as dict object
        """
        cls.INSTANCE = User(user)

    @classmethod
    def get_instance(cls):
        """
        Gets instance of User

        :return: Instance if exists, else None
        """
        if not isinstance(cls.INSTANCE, cls):
            return None
        return cls.INSTANCE

    @property
    def is_customer(self):
        """
        Custom getter for current is_customer

        :return: self.is_customer
        """
        return self.user_roles.is_customer

    @property
    def is_receptionist(self):
        """
        Custom getter for current is_receptionist

        :return: self.is_receptionist
        """
        return self.user_roles.is_receptionist

    @property
    def is_healthcare_worker(self):
        """
        Custom getter for current is_healthcare_worker

        :return: self.is_healthcare_worker
        """
        return self.user_roles.is_healthcare_worker

