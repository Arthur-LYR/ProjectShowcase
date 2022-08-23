from django import forms
from django.core.exceptions import ValidationError
from django.http import request
from django.utils.translation import gettext_lazy as _
from models.users.user_handler import UserHandler
from models.testsites.testsite_handler import TestSiteHandler
from models.bookings.booking_handler import BookingHandler
from models.tests.test_handler import TestHandler
import datetime


"""
System Handlers
"""
USER_HANDLER = UserHandler()
TEST_SITE_HANDLER = TestSiteHandler()
BOOKING_HANDLER = BookingHandler()
TEST_HANDLER = TestHandler()


"""
Dropdown options
"""
FACILITY_TYPES = TEST_SITE_HANDLER.facility_types
HOME_TEST_SITES = TEST_SITE_HANDLER.get_test_site_list(is_home=True)
TEST_SITES = TEST_SITE_HANDLER.get_test_site_list(is_home=False)
TEST_TYPES = TEST_HANDLER.test_types
RESULTS = TEST_HANDLER.results


"""
Validator Functions
"""
def validate_pin(value):
    """
    This is a validators function to validate the sms pin input by the user at the booking forms

    :param value: sms Pin entered by the user
    :return: ValidationError: if user entered an invalid pin number
    """
    try:
        BOOKING_HANDLER.get_booking(value)
    except ImportError:
        raise ValidationError("The pin entered is invalid")


def validate_user(value):
    """
    This is a validators function to validate the username input by the user at the booking forms

    :param value: username input by the user
    :return: ValidationError: if user enetred an invalid username
    """
    try:
        USER_HANDLER.get_user_id(value)
    except KeyError:
        raise ValidationError("User not found.")


"""
Web Forms
"""
class LoginForm(forms.Form):
    """
    Form for login subsystem
    """
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class SearchTestSiteForm(forms.Form):
    """
    Form for test site search subsystem
    """
    suburb = forms.CharField()
    facility_type = forms.CharField(widget=forms.Select(choices=FACILITY_TYPES))


class HomeBookForm(forms.Form):
    """
    Form for home test booking subsystem
    """
    testing_site = forms.CharField(widget=forms.Select(choices=HOME_TEST_SITES))
    start_date = forms.DateField()
    start_time = forms.TimeField()

    def clean(self):
        # Get user inputs
        cleaned_data = super(HomeBookForm, self).clean()
        start_date = cleaned_data.get('start_date')
        start_time = cleaned_data.get('start_time')

        # Check if date is past date
        try:
            if start_date < datetime.date.today():
                raise ValidationError("The date entered has passed ")
        except TypeError:
            raise ValidationError("Invalid format date input")

        # Check if time is past time or is after hours
        try:
            if start_date == datetime.date.today() and start_time < datetime.datetime.now().time():
                raise ValidationError("The time entered has passed ")
            elif not datetime.time(8, 0, 0) <= start_time <= datetime.time(19, 0, 0):
                raise ValidationError("Time is after hours")
        except TypeError:
            raise ValidationError("Invalid format of time input")


class CheckBookingForm(forms.Form):
    """
    Form for check booking subsystem
    """
    pin = forms.CharField(validators=[validate_pin])


class EditBookingForm(forms.Form):
    """
    Form for edit booking subsystem
    """
    pin = forms.CharField()
    testing_site = forms.CharField(widget=forms.Select(choices=TEST_SITES))
    start_date = forms.DateField()
    start_time = forms.TimeField()


    def clean(self):
        # Get user inputs
        cleaned_data = super(EditBookingForm, self).clean()
        pin = cleaned_data.get('pin')
        start_date = cleaned_data.get('start_date')
        start_time = cleaned_data.get('start_time')

        # Validate PIN
        try:
            booking = BOOKING_HANDLER.get_booking(pin)
        except ImportError:
            raise ValidationError("The pin entered is invalid")
        else:
            # Check if booking is home booking
            if booking["notes"] == "Home":
                raise ValidationError("This booking is a Home Booking")

        # Check if booking has already lapsed
        booking_time = datetime.datetime.strptime(booking["startTime"], "%Y-%m-%dT%H:%M:%S.%fZ")
        if booking_time < datetime.datetime.now():
            raise ValidationError("Booking has lapsed and cannot be modified")

        # Check if booking cancelled
        if booking["status"] == "CANCELLED":
            raise ValidationError("Booking has been cancelled and cannot be modified")

        # Get Testing site open and close time from user input
        testing_site = TEST_SITE_HANDLER.get_test_site(cleaned_data.get('testing_site'))
        try:
            open_time = datetime.datetime.strptime(testing_site['additionalInfo']['openTime'], "%H:%M:%S").time()
            close_time = datetime.datetime.strptime(testing_site['additionalInfo']['closeTime'], "%H:%M:%S").time()
        except ValueError:
            try:
                open_time = datetime.datetime.strptime(testing_site['additionalInfo']['openTime'], "%H:%M").time()
                close_time = datetime.datetime.strptime(testing_site['additionalInfo']['closeTime'], "%H:%M").time()
            except ValueError:
                raise ValidationError("Invalid format of time input")

        # Check if date is past date
        try:
            if start_date < datetime.date.today():
                raise ValidationError("The date entered has passed ")
        except TypeError:
            raise ValidationError("Invalid format date input")

        # Check if time is past time or is after testing site opening hours
        try:
            if start_date == datetime.date.today() and start_time < datetime.datetime.now().time():
                raise ValidationError("The time entered has passed ")
            elif not open_time <= start_time <= close_time:
                raise ValidationError("Testing site is closed during this time")
        except TypeError:
            raise ValidationError("Invalid format of time input")


class RevertBookingForm(forms.Form):
    """
    Form for revert booking subsystem
    """
    pin = forms.CharField()

    def clean(self):
        # Get user inputs
        cleaned_data = super(RevertBookingForm, self).clean()
        pin = cleaned_data.get('pin')

        # Validate PIN
        try:
            booking = BOOKING_HANDLER.get_booking(pin)
        except ImportError:
            raise ValidationError("The pin entered is invalid")
        else:
            # Check if booking is home booking
            if booking["notes"] == "Home":
                raise ValidationError("This booking is a Home Booking")

        # Check if booking has already lapsed
        booking_time = datetime.datetime.strptime(booking["startTime"], "%Y-%m-%dT%H:%M:%S.%fZ")
        if booking_time < datetime.datetime.now():
            raise ValidationError("Booking has lapsed and cannot be modified")

        # Check if booking cancelled
        if booking["status"] == "CANCELLED":
            raise ValidationError("Booking has been cancelled and cannot be modified")


class OnsiteBookForm(forms.Form):
    """
    Form for onsite test booking subsystem
    """
    customer_username = forms.CharField()
    testing_site = forms.CharField(widget=forms.Select(choices=TEST_SITES))
    start_date = forms.DateField()
    start_time = forms.TimeField()

    def clean(self):
        # Get user inputs
        cleaned_data = super(OnsiteBookForm, self).clean()
        username = cleaned_data.get('customer_username')
        start_date = cleaned_data.get('start_date')
        start_time = cleaned_data.get('start_time')

        # Get Testing site open and close time from user input
        testing_site = TEST_SITE_HANDLER.get_test_site(cleaned_data.get('testing_site'))
        try:
            open_time = datetime.datetime.strptime(testing_site['additionalInfo']['openTime'], "%H:%M:%S").time()
            close_time = datetime.datetime.strptime(testing_site['additionalInfo']['closeTime'], "%H:%M:%S").time()
        except ValueError:
            try:
                open_time = datetime.datetime.strptime(testing_site['additionalInfo']['openTime'], "%H:%M").time()
                close_time = datetime.datetime.strptime(testing_site['additionalInfo']['closeTime'], "%H:%M").time()
            except ValueError:
                raise ValidationError("Invalid format of time input")

        # Validate User ID
        try:
            USER_HANDLER.get_user_id(username)
        except KeyError:
            raise ValidationError("User not found.")

        # Check if date is past date
        try:
            if start_date < datetime.date.today():
                raise ValidationError("The date entered has passed ")
        except TypeError:
            raise ValidationError("Invalid format date input")

        # Check if time is past time or is after testing site opening hours
        try:
            if start_date == datetime.date.today() and start_time < datetime.datetime.now().time():
                raise ValidationError("The time entered has passed ")
            elif not open_time <= start_time <= close_time:
                raise ValidationError("Testing site is closed during this time")
        except TypeError:
            raise ValidationError("Invalid format of time input")


class OnsiteTestForm(forms.Form):
    """
    Form for onsite testing subsystem
    """
    test_type = forms.CharField(widget=forms.Select(choices=TEST_TYPES))
    patient_username = forms.CharField(validators=[validate_user])
    booking_pin = forms.CharField()
    result = forms.CharField(widget=forms.Select(choices=RESULTS))

    def clean(self):
        # Get user inputs
        cleaned_data = super(OnsiteTestForm, self).clean()

        try:
            booking = BOOKING_HANDLER.get_booking(cleaned_data.get("booking_pin"))
        except ImportError:
            # Invalid Format or does not exist
            raise ValidationError("The pin entered is invalid")
        else:
            # Check if booking is home booking
            if booking["notes"] == "Home":
                raise ValidationError("This booking is a Home Booking")

        # Check if booking cancelled
        if booking["status"] == "CANCELLED":
            raise ValidationError("Booking has been cancelled. The test is called off.")
