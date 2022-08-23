import requests


class APIHandler:
    """
    APIHandler class for communicating with server
    """
    def __init__(self, extension):
        """
        Constructor.
        """
        self.root_url = "https://fit3077.com/api/v2" + extension
        self.api_token = open("api_token.txt", "r").read()

    def handle_response(self, response):
        """
        Handles an HTTP response after a GET or POST API Request is made.

        :param response: HTTP Response
        :return: Main body of response
        :raises ImportError: If HTTP request unsuccessful
        """
        if 200 <= response.status_code <= 299:
            try:
                return response.json()
            except Exception:
                return
        else:
            raise ImportError(str(response.status_code) + ": " + str(response.json()["message"]))

    def get(self, extension="", params=None, data=None):
        """
        GET Method

        :param extension: Any additional extension to the URL
        :param params: Parameters
        :param data: Data
        :return: Appropriate data (if any)
        """
        response = requests.get(
            url=self.root_url + extension,
            headers={'Authorization': self.api_token},
            params=params,
            json=data
        )
        return self.handle_response(response)

    def post(self, extension="", params=None, data=None):
        """
        POST Method

        :param extension: Any additional extension to the URL
        :param params: Parameters
        :param data: Data
        :return: Appropriate data (if any)
        """
        response = requests.post(
            url=self.root_url + extension,
            headers={'Authorization': self.api_token},
            params=params,
            json=data
        )
        return self.handle_response(response)

    def post(self, extension="", params=None, data=None):
        """
        POST Method

        :param extension: Any additional extension to the URL
        :param params: Parameters
        :param data: Data
        :return: Appropriate data (if any)
        """
        response = requests.post(
            url=self.root_url + extension,
            headers={'Authorization': self.api_token},
            params=params,
            json=data
        )
        return self.handle_response(response)

    def patch(self, extension="", params=None, data=None):
        """
        PATCH Method

        :param extension: Any additional extension to the URL
        :param params: Parameters
        :param data: Data
        :return: Appropriate data (if any)
        """
        response = requests.patch(
            url=self.root_url + extension,
            headers={'Authorization': self.api_token},
            params=params,
            json=data
        )
        return self.handle_response(response)

    def delete(self, extension="", params=None, data=None):
        """
        DELETE Method

        :param extension: Any additional extension to the URL
        :param params: Parameters
        :param data: Data
        :return: Appropriate data (if any)
        """
        response = requests.delete(
            url=self.root_url + extension,
            headers={'Authorization': self.api_token},
            params=params,
            json=data
        )
        return self.handle_response(response)

