from models.api.api_handler import APIHandler
from models.tests.test import Test


class TestHandler:

    def __init__(self):
        """
        Constructor
        """
        self.apiHandler = APIHandler("/covid-test")
        self.test_types = []
        for type in Test.VALID_TYPES:
            self.test_types.append((type, type))
        self.results = []
        for result in Test.VALID_RESULTS:
            self.results.append((result.upper(), result))

    def perform_test(self, test_type: str, patient_id: str, admin_id: str, booking_id: str, result: str):
        """
        This method is responsible to perform a test and create a test json object and made a POST request
        to the API server

        :param test_type: the type of covid test perform
        :param patient_id: the id of the patient taken the test
        :param admin_id: the id of administrator which entered the result and information of test
        :param booking_id: the id of the booking
        :param result: the result of the test
        :return: POST request to the API server
        """
        return self.apiHandler.post(
            data={
                'type': test_type,
                'patientId': patient_id,
                'administererId': admin_id,
                'bookingId': booking_id,
                'result': result
            }
        )
