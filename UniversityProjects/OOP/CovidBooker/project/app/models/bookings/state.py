class CurrentState:
    """
    Originator class to store current booking state
    """
    def __init__(self, test_site, start_time):
        """
        Constructor.

        :param test_site: Test site as dict
        :param start_time: Start time in ISO 8601
        """
        self.test_site = test_site
        self.start_time = start_time

    def save(self):
        """
        Store the state as a PreviousState

        :return: State converted to PreviousState
        """
        return PreviousState(self.test_site, self.start_time)

    def restore(self, state):
        """
        Restore the state.
        """
        self.test_site = state.test_site
        self.start_time = state.start_time


class PreviousState:
    """
    Memento class to store previous states of booking
    """
    def __init__(self, test_site, start_time):
        """
        Constructor.

        :param test_site: Test site as dict
        :param start_time: Start time in ISO 8601
        """
        self.test_site = test_site
        self.start_time = start_time
