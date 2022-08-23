class TestSite:
    """
    Wrapper class for TestSite
    """
    VALID_TYPES = [
        "Drive Through",
        "Walk-In",
        "Clinic",
        "GP",
        "Hospital"
    ]

    def __init__(self, test_site):
        """
        Constructor

        :param test_site: Test Site as dict
        """
        self.id = test_site["id"]
        self.name = test_site["name"]
        self.url = test_site["websiteUrl"]
        if test_site["additionalInfo"]["type"] in self.VALID_TYPES:
            self.type = test_site["additionalInfo"]["type"]
        else:
            raise TypeError("Type in input is invalid")
        self.suburb = test_site["address"]["suburb"]
        self.has_onsite_book = test_site["additionalInfo"]["hasOnsiteBooking"]
        self.has_onsite_test = test_site["additionalInfo"]["hasOnsiteTesting"]
        self.open_time = test_site["additionalInfo"]["openTime"]
        self.close_time = test_site["additionalInfo"]["closeTime"]
        self.wait_time = str(len(test_site["bookings"]) * 30) + " mins"
