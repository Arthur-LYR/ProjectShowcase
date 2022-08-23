import requests

from models.users.user import User
from models.bookings.booking_handler import BookingHandler


class AdminInterface:

    def __init__(self, user):
        self.user = user

    def update(self):
        filtered_bookings = []
        i = 0
        bookings = BookingHandler().get_bookings()
        for booking in bookings:
            if booking['notes'] == "Onsite" and self.user.test_site["id"] == booking["testingSite"]["id"]:
                filtered_bookings.append((booking, str(i)))
                i += 1

        return filtered_bookings
