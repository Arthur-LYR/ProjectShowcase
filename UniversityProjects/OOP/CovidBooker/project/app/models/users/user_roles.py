class UserRoles:
    """
    Class to store the roles of a user.
    """
    def __init__(self, is_customer, is_receptionist, is_healthcare_worker):
        """
        Constructor

        :param is_customer: True is User is customer, False otherwise
        :param is_receptionist: True is User is receptionist, False otherwise
        :param is_healthcare_worker: True is User is healthcare worker, False otherwise
        """
        self.is_customer = is_customer
        self.is_receptionist = is_receptionist
        self.is_healthcare_worker = is_healthcare_worker
