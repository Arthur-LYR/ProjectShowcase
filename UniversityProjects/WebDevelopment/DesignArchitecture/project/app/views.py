import requests
import datetime
import time
from django.http import HttpResponse
from django.template import loader, RequestContext
from django.shortcuts import redirect, render
from .forms import LoginForm, SearchTestSiteForm, HomeBookForm, CheckBookingForm, EditBookingForm, RevertBookingForm,\
    OnsiteBookForm, OnsiteTestForm
from models.users.user import User
from models.users.user_handler import UserHandler
from models.testsites.testsite_handler import TestSiteHandler
from models.bookings.booking_handler import BookingHandler
from models.tests.test_handler import TestHandler
from models.bookings.adminInterface import AdminInterface
from django.contrib import messages

"""
System Handlers
"""
USER_HANDLER = UserHandler()
TEST_SITE_HANDLER = TestSiteHandler()
BOOKING_HANDLER = BookingHandler()
TEST_HANDLER = TestHandler()


"""
Utility Functions
"""
def process_date(date, start_time):
    """
    This function converts the datetime obj into a ISO 8601 string

    :param date: date input by the user at the booking form
    :param start_time: time input by the user at booking form
    :return: datetime in ISO 8601 format
    """
    combine = datetime.datetime.combine(date, start_time)
    return combine.strftime('%Y-%m-%dT%H:%M:%S.%f%z')


"""
View Methods for Webpages
"""
def default(request):
    """
    When default URL used, redirect to login
    """
    return redirect("login")


def login(request):
    """
    Login subsystem. User enters username and password and models validates the input.
    """
    context = {}

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = LoginForm(request.POST)
        context['form'] = form

        # Check if the form is valid:
        if form.is_valid():
            # Authenticate User
            if USER_HANDLER.authenticate_user(form.cleaned_data['username'], form.cleaned_data['password']):
                User.create_instance(USER_HANDLER.get_user(form.cleaned_data['username']))
                return redirect("index")
            else:
                context['error'] = "Invalid User Credentials"

    # If this is a GET (or any other method) create the default form.
    else:
        form = LoginForm()
        context['form'] = form

    return render(request, "login.html", context)


def index(request):
    """
    Home page. Displays all subsystem buttons and performs access control depending on user type.
    """
    context = {}

    # Check if User logged in
    user = User.get_instance()
    if user is None:
        return redirect("login")

    # Add context
    context["username"] = user.username
    context["is_customer"] = user.is_customer
    context["is_receptionist"] = user.is_receptionist
    context["is_healthcare_worker"] = user.is_healthcare_worker

    return render(request, "index.html", context)


def profile(request):
    """
    User Profile Page. Displays user details and bookings.
    """
    context = {}

    # Check if User logged in
    user = User.get_instance()
    if user is None:
        return redirect("login")
    context["username"] = user.username

    # Display User Details
    context["id"] = user.user_id
    context["name"] = user.username
    context["is_customer"] = user.is_customer
    context["is_receptionist"] = user.is_receptionist
    context["is_healthcare_worker"] = user.is_healthcare_worker
    context["test_site"] = None if user.test_site is None else user.test_site["name"]
    context['bookings'] = []

    # Display Bookings
    bookings = BOOKING_HANDLER.get_bookings()
    for booking in bookings:
        if user.user_id == booking["customer"]["id"]:
            context['bookings'].append(booking)

    return render(request, "profile.html", context)


def searchTestSites(request):
    """
    Test site search subsystem. User provides suburb and test site type and models displays all valid test sites.
    """
    context = {}

    # Check if User logged in
    user = User.get_instance()
    if user is None:
        return redirect("login")
    context["username"] = user.username

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = SearchTestSiteForm(request.POST)
        context['form'] = form

        # Get Form Data and Search
        if form.is_valid():
            try:
                context["test_sites"] = TEST_SITE_HANDLER.display_test_sites(form.cleaned_data["suburb"],
                                                                             form.cleaned_data["facility_type"])
            except ImportError:
                context["message"] = "Test Sites could not be fetched"

    # If this is a GET (or any other method) create the default form.
    else:
        form = SearchTestSiteForm()
        context['form'] = form

    return render(request, "searchTestSites.html", context)


def homeBook(request):
    """
    Home test booking subsystem. User chooses test site to collect RAT test (may choose not to if they already have an
    RAT test), enters date and time, and models makes the booking.
    """
    context = {}

    # Check if User logged in
    user = User.get_instance()
    if user is None:
        return redirect("login")
    context["username"] = user.username

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = HomeBookForm(request.POST)
        context['form'] = form

        # Make Booking
        if form.is_valid():
            # Get the sms pin
            try:
                id, pin = BOOKING_HANDLER.make_booking(user.user_id, form.cleaned_data['testing_site'],
                                                       process_date(form.cleaned_data['start_date'], form.cleaned_data['start_time']),
                                                       is_home=True)
                # Do the booking here
                context['message'] = "Booking Successful. ID is " + id + ". " + \
                                     "PIN is " + pin + ". " + \
                                     "Link is https://youtu.be/dQw4w9WgXcQ. QR Code is https://youtu.be/dQw4w9WgXcQ"
            except ImportError:
                context['message'] = "Booking could not be made"

    # If this is a GET (or any other method) create the default form.
    else:
        form = HomeBookForm()
        context['form'] = form

    return render(request, "homeBook.html", context)


def checkBooking(request):
    """
    Check Booking subsystem. User provides booking PIN and models displays booking details.
    """
    context = {}

    # Check if User logged in
    user = User.get_instance()
    if user is None:
        return redirect("login")
    context["username"] = user.username

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = CheckBookingForm(request.POST)
        context['form'] = form

        # Get Form Data and Search
        if form.is_valid():
            # Get the information of booking
            try:
                booking = BOOKING_HANDLER.get_booking(form.cleaned_data['pin'])

                context["id"] = booking["id"]
                context["pin"] = booking["smsPin"]
                context['booker'] = booking['customer']['userName']
                context['test_site'] = "Home Testing" if booking['testingSite'] is None else booking['testingSite']['name']
                context['start_date_and_time'] = booking['startTime']
                context['notes'] = booking['notes']
                context['status'] = booking['status']

            except ImportError:
                context["message"] = "Booking could not be displayed"

    # If this is a GET (or any other method) create the default form.
    else:
        form = CheckBookingForm()
        context['form'] = form

    return render(request, "checkBooking.html", context)


def editBooking(request):
    """
    Edit Booking Subsystem. Allows customers/receptionists to edit their bookings
    """
    context = {}

    # Check if User logged in
    user = User.get_instance()
    if user is None:
        return redirect("login")
    context["username"] = user.username

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):

        form = EditBookingForm(request.POST, initial={"pin": request.session.get("edit_pin",None)})
        form.fields['pin'].initial = "123123"

        context['form'] = form

        # Edit Booking
        if form.is_valid():
            if BOOKING_HANDLER.get_booking(form.cleaned_data["pin"])["customer"]["id"] != user.user_id and not user.is_receptionist:
                context['message'] = "Cannot Edit Booking that does not belong to you if you are not a receptionist"
            else:
                try:
                    BOOKING_HANDLER.edit_booking(form.cleaned_data["pin"],
                                                 TEST_SITE_HANDLER.get_test_site(form.cleaned_data["testing_site"]),
                                                 process_date(form.cleaned_data["start_date"], form.cleaned_data["start_time"]))
                    context['message'] = "Booking Successfully Edited"
                except ImportError:
                    context['message'] = "Booking could not be edited"
                finally:
                    try:
                        del request.session['edit_pin']
                    except KeyError:
                        pass

    # If this is a GET (or any other method) create the default form.
    else:
        form = EditBookingForm(initial={"pin": request.session.get("edit_pin")})
        context['form'] = form

    return render(request, "editBooking.html", context)


def revertBooking(request):
    """
    Revert Booking Subsystem. Allows customers/receptionists to revert their bookings
    """
    context = {}

    # Check if User logged in
    user = User.get_instance()
    if user is None:
        return redirect("login")
    context["username"] = user.username

    # User chooses to revert booking
    if 'revert' in request.POST:

        # Create a form instance and populate it with data from the request (binding):
        form = RevertBookingForm(request.POST, initial={"pin": request.session.get("revert_pin", None)})
        context['form'] = form

        # Revert Booking
        if form.is_valid():
            if BOOKING_HANDLER.get_booking(form.cleaned_data["pin"])["customer"]["id"] != user.user_id and not user.is_receptionist:
                context['message'] = "Cannot Revert Booking that does not belong to you if you are not a receptionist"
            else:
                try:
                    BOOKING_HANDLER.revert_booking(form.cleaned_data["pin"])
                    context['message'] = "Booking Successfully Reverted"
                except ImportError:
                    context['message'] = "Booking could not be reverted"
                except ValueError:
                    context['message'] = "Booking cannot be reverted as there are no previous records"
                finally:
                    try:
                        del request.session['revert_pin']
                    except KeyError:
                        pass

    # User chooses to delete booking
    elif 'cancel' in request.POST:

        # Create a form instance and populate it with data from the request (binding):
        form = RevertBookingForm(request.POST, initial={"pin": request.session.get("revert_pin",None)})
        context['form'] = form

        # Delete Booking
        if form.is_valid():
            if BOOKING_HANDLER.get_booking(form.cleaned_data["pin"])["customer"]["id"] != user.user_id and not user.is_receptionist:
                context['message'] = "Cannot Cancel Booking that does not belong to you if you are not a receptionist"
            else:
                try:
                    BOOKING_HANDLER.cancel_booking(form.cleaned_data["pin"])
                    context['message'] = "Booking Successfully Cancelled"
                except ImportError:
                    context['message'] = "Booking could not be Cancelled"
                finally:
                    try:
                        del request.session['revert_pin']
                    except KeyError:
                        pass

    # If this is a GET (or any other method) create the default form.
    else:
        form = RevertBookingForm(initial={"pin": request.session.get("revert_pin")})
        context['form'] = form

    return render(request, "revertBooking.html", context)


def onsiteBook(request):
    """
    Onsite test booking subsystem. user provides username, test site, date, and time to models and models performs
    booking
    """
    context = {}

    # Check if User logged in
    user = User.get_instance()
    if user is None:
        return redirect("login")
    context["username"] = user.username

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = OnsiteBookForm(request.POST)
        context['form'] = form

        # Make Booking
        if form.is_valid():
            try:
                # Get the user id and sms pin
                user_id = USER_HANDLER.get_user_id(form.cleaned_data['customer_username'])
                id, pin = BOOKING_HANDLER.make_booking(user_id, form.cleaned_data['testing_site'],
                                                   process_date(form.cleaned_data['start_date'], form.cleaned_data['start_time']),
                                                   is_home=False)
                # Do the booking here
                context['message'] = "Booking Successful. ID is " + id + ". PIN is " + pin + "."
            except ImportError:
                context['message'] = "Booking could not be made"

    # If this is a GET (or any other method) create the default form.
    else:
        form = OnsiteBookForm()
        context['form'] = form

    return render(request, "onsiteBook.html", context)


def adminInterface(request):
    """
    Admin Interface. Allows receptionists to edit/delete bookings and healthcare workers to process bookings
    """
    context = {}

    # Check if User logged in
    user = User.get_instance()
    if user is None:
        return redirect("login")
    ADMIN_INTERFACE = AdminInterface(user)

    # Add context
    bookings = ADMIN_INTERFACE.update()

    context['all_bookings'] = bookings

    for booking, i in bookings:
        edit = "edit" + i
        revert = "revert" + i
        cancel = "cancel" + i
        delete = "delete" + i
        # User chooses to edit booking
        if edit in request.POST:
            request.session['edit_pin'] = booking['smsPin']
            return redirect("editBooking")

        # User chooses to revert booking
        elif revert in request.POST:
            request.session['revert_pin'] = booking['smsPin']
            return redirect("revertBooking")

        # User chooses to cancel booking
        elif cancel in request.POST:
            request.session['revert_pin'] = booking['smsPin']
            return redirect("revertBooking")

        # User chooses to delete booking
        elif delete in request.POST:
            try:
                BOOKING_HANDLER.delete_booking(booking['smsPin'])
                return render(request, "adminInterface.html", context)
            except ImportError:
                context["delete_warning"] = "Could not delete booking as it has associated COVID tests"

    return render(request, "adminInterface.html", context)


def onsiteTest(request):
    """
    Onsite testing subsystem. User provides username, test type, booking pin, and result to models and models
    makes/updates the test.
    """
    context = {}

    # Check if User logged in
    user = User.get_instance()
    if user is None:
        return redirect("login")
    context["username"] = user.username

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = OnsiteTestForm(request.POST)
        context['form'] = form

        # Perform Testing
        if form.is_valid():
            try:
                patient_id = USER_HANDLER.get_user_id(form.cleaned_data['patient_username'])
                booking_id = BOOKING_HANDLER.get_booking_id(form.cleaned_data['booking_pin'])
                TEST_HANDLER.perform_test(form.cleaned_data['test_type'], patient_id, user.user_id,
                                          booking_id, form.cleaned_data['result'])
                # Do the testing here
                context['message'] = "Test Complete."
                try:
                    del request.session['process_pin']
                except KeyError:
                    pass
            except ImportError:
                context["message"] = "Test could not be made."

    # If this is a GET (or any other method) create the default form.
    else:
        form = OnsiteTestForm()
        context['form'] = form

    return render(request, "onsiteTest.html", context)
