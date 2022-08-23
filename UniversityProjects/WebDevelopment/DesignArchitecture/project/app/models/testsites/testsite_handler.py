from models.api.api_handler import APIHandler
from models.testsites.testsite import TestSite


class TestSiteHandler:
    """
    Test Site Handler
    """
    def __init__(self):
        """
        Constructor.
        """
        self.api_handler = APIHandler("/testing-site")
        self.facility_types = []
        for type in TestSite.VALID_TYPES:
            self.facility_types.append((type, type))

    def display_test_sites(self, suburb, facility_type):
        """
        Obtain simplified test site data for front end display

        :param suburb: Suburb as str
        :param facility_type: Facility type as str
        :return: Appropriate test site data
        """
        filtered_test_sites = []
        test_sites = self.get_test_sites()

        for test_site in test_sites:
            test_site = TestSite(test_site)
            if test_site.suburb == suburb and test_site.type == facility_type:
                filtered_test_sites.append(test_site)

        return filtered_test_sites

    def get_test_site_list(self, is_home):
        """
        Get the test site list for Django form dropdown list input

        :param is_home: True if for home booking models, False for onsite booking models
        :return: Appropriate test site data
        """
        dropdown = []
        test_sites = self.get_test_sites()

        for test_site in test_sites:
            test_site = TestSite(test_site)
            if test_site.has_onsite_book or is_home:
                dropdown.append((test_site.id, test_site.name))

        if is_home:
            dropdown.append(("Home", "I already have an RAT kit"))

        return dropdown

    def get_test_sites(self):
        """
        Gets all test sites from server

        :return: List of all test sites as TestSite objects
        """
        return self.api_handler.get(params={"fields": "bookings"})

    def get_test_site(self, test_site_id):
        """
        Gets a test site from its ID

        :param test_site_id: Test site ID
        :return: TestSite object
        """
        return self.api_handler.get(
            extension="/" + test_site_id,
            params={"fields": "bookings"}
        )
