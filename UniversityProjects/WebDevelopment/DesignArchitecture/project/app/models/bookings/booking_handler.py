from models.api.api_handler import APIHandler
from models.bookings.booking import Booking


class BookingHandler:
    def __init__(self):
        """
        Constructor
        """
        self.apiHandler = APIHandler("/booking")

    def get_bookings(self):
        """
        Gets all bookings

        :return: All Bookings in API Server
        """
        return self.apiHandler.get()

    def get_booking_id(self, pin: str):
        """
        Gets the Booking ID from a Pin

        :param pin: Booking ID or PIN
        :return: Booking ID
        """
        booking = self.get_booking(pin)
        return booking["id"]

    def get_booking(self, pin: str):
        """
        This method return the booking object which will be used to display the information of booking
        to the user

        :param pin: Booking ID or PIN
        :return: booking object in Dictionary type
        """
        # Assume query is Booking ID.
        try:
            return self.apiHandler.get(extension="/" + pin)

        # Assumption is wrong, query should be PIN
        except ImportError:
            bookings = self.get_bookings()
            for booking in bookings:
                if booking['smsPin'] == pin:
                    return booking

            # Query is invalid
            raise ImportError("Booking not found")

    def make_booking(self, user_id: str, test_site_id: str, start_time: str, is_home: bool):
        """
        This method return a POST request which create a booking to the API server

        :param user_id: the id of the user which make the booking
        :param test_site_id: the id of covid test site
        :param start_time: the start datetime of the test
        :param is_home: True - Make home booking, False - Onsite booking
        :return: booking object in JSON type
        """
        response = self.apiHandler.post(
            data={
                'customerId': user_id,
                'testingSiteId': None if test_site_id == "Home" else test_site_id,
                'startTime': start_time,
                'notes': 'Home' if is_home else "Onsite",
                'additionalInfo': {
                    "history": []
                }
            }
        )

        # return the id and smsPin to be display at the web interface
        return response['id'], response['smsPin']

    def edit_booking(self, pin, test_site, start_time):
        """
        Edit the test site or start time of a booking.

        :param pin: Booking ID or PIN
        :param test_site: New Test Site
        :param start_time: New Start Datetime
        """
        booking = Booking(self.get_booking(pin))
        booking.edit(test_site, start_time)
        history = []
        for memento in booking.history:
            history.append(
                {
                    "testingSite": memento.test_site,
                    "startTime": memento.start_time
                }
            )
        return self.apiHandler.patch(
            extension="/" + booking.id,
            data={
                "customerId": booking.user["id"],
                "testingSiteId": booking.test_site["id"],
                "startTime": booking.start_time,
                "status": booking.status,
                "notes": booking.notes,
                "additionalInfo": {
                    "history": history
                }
            }
        )

    def revert_booking(self, pin):
        """
        Revert the booking to its previous state

        :param pin: Booking ID or PIN
        """
        booking = Booking(self.get_booking(pin))
        booking.revert()
        history = []
        for memento in booking.history:
            history.append(
                {
                    "testingSite": memento.test_site,
                    "startTime": memento.start_time
                }
            )
        return self.apiHandler.patch(
            extension="/" + booking.id,
            data={
                "customerId": booking.user["id"],
                "testingSiteId": booking.test_site["id"],
                "startTime": booking.start_time,
                "status": booking.status,
                "notes": booking.notes,
                "additionalInfo": {
                    "history": history
                }
            }
        )

    def cancel_booking(self, pin):
        """
        Cancel a booking

        :param pin: Booking ID or PIN
        """
        booking = Booking(self.get_booking(pin))
        booking.cancel()
        history = []
        for memento in booking.history:
            history.append(
                {
                    "testingSite": memento.test_site,
                    "startTime": memento.start_time
                }
            )
        return self.apiHandler.patch(
            extension="/" + booking.id,
            data={
                "customerId": booking.user["id"],
                "testingSiteId": booking.test_site["id"],
                "startTime": booking.start_time,
                "status": booking.status,
                "notes": booking.notes,
                "additionalInfo": {
                    "history": history
                }
            }
        )

    def delete_booking(self, pin):
        """
        Deletes a booking from the server

        :param pin: Booking ID or PIN
        """
        id = self.get_booking_id(pin)
        return self.apiHandler.delete(extension="/" + id)
