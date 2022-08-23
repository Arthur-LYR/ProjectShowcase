from models.bookings.state import CurrentState
from models.bookings.state import PreviousState


class Booking:
    """
    Booking class to allow for efficient editing
    """
    def __init__(self, booking):
        """
        Constructor. Given a booking dict extracted from server, convert to Booking.

        :param booking: Dictionary extracted from server
        """
        # Important Attributes
        self.id = booking["id"]
        self.pin = booking["smsPin"]
        self.user = booking["customer"]
        self.status = booking["status"]
        self.notes = booking["notes"]
        self.current_state = CurrentState(booking["testingSite"], booking["startTime"])
        self.history = []

        # Restore Previous States
        for memento in booking["additionalInfo"]["history"]:
            self.history.append(
                PreviousState(
                    memento["testingSite"],
                    memento["startTime"]
                    )
                )

    @property
    def test_site(self):
        """
        Custom getter for current test_site

        :return: self.test_site
        """
        return self.current_state.test_site

    @property
    def start_time(self):
        """
        Custom getter for current start_time

        :return: self.start_time
        """
        return self.current_state.start_time

    def edit(self, test_site, start_time):
        """
        Edit the venue/time of the booking and update the history

        :param test_site: New Test Site
        :param start_time: New Start Time in ISO 8601
        """
        # Save current state and updated to new state
        prev = self.current_state.save()
        self.current_state = CurrentState(test_site, start_time)

        # Update history. Only store most recent 3 states.
        self.history.append(prev)
        if len(self.history) > 3:
            self.history.pop(0)

    def revert(self):
        """
        Revert a booking to the most recent previous state.
        """
        try:
            self.current_state.restore(self.history.pop())
        except IndexError:
            raise ValueError("Booking cannot be reverted as there are no previous records")

    def cancel(self):
        """
        Cancel a booking.
        """
        self.status = "CANCELLED"
