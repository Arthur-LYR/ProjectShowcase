import unittest
from unittest.mock import Mock
from app.calculator import *


class TestGetSunHour(unittest.TestCase):
    CALCULATOR = Calculator()

    # Valid date and valid location id
    def test_case1(self):
        date = datetime(2020, 8, 1)
        location = "5bea7b46-9809-4189-aafe-160208da94f7"

        requests_mock = Mock()
        response_mock = Mock()
        requests_mock.get.return_value = response_mock
        response_mock.status_code = 200
        response_mock.json.return_value ={"date":"2020-08-01","sunrise":"07:05:00","sunset":"17:41:00","moonrise":"15:19:00","moonset":"05:03:00","moonPhase":"Waxing Gibbous","moonIlluminationPct":82,"minTempC":11,"maxTempC":17,"avgTempC":14,"sunHours":3.7,"uvIndex":4,"location":{"id":"5bea7b46-9809-4189-aafe-160208da94f7","postcode":"6001","name":"PERTH","state":"WA","latitude":"-31.9505269","longitude":"115.8604572","distanceToNearestWeatherStationMetres":3672.959393589811,"nearestWeatherStation":{"name":"PERTH METRO","state":"WA","latitude":"-31.9192","longitude":"115.8728"}},"hourlyWeatherHistory":[{"hour":0,"tempC":12,"weatherDesc":"Partly cloudy","cloudCoverPct":1,"uvIndex":1,"windspeedKph":10,"windDirectionDeg":146,"windDirectionCompass":"SSE","precipitationMm":0,"humidityPct":82,"visibilityKm":10,"pressureMb":1024},{"hour":1,"tempC":12,"weatherDesc":"Partly cloudy","cloudCoverPct":2,"uvIndex":1,"windspeedKph":10,"windDirectionDeg":143,"windDirectionCompass":"SE","precipitationMm":0,"humidityPct":82,"visibilityKm":10,"pressureMb":1024},{"hour":2,"tempC":12,"weatherDesc":"Partly cloudy","cloudCoverPct":3,"uvIndex":1,"windspeedKph":10,"windDirectionDeg":140,"windDirectionCompass":"SE","precipitationMm":0,"humidityPct":82,"visibilityKm":10,"pressureMb":1024},{"hour":3,"tempC":11,"weatherDesc":"Partly cloudy","cloudCoverPct":4,"uvIndex":1,"windspeedKph":9,"windDirectionDeg":136,"windDirectionCompass":"SE","precipitationMm":0,"humidityPct":82,"visibilityKm":10,"pressureMb":1024},{"hour":4,"tempC":11,"weatherDesc":"Partly cloudy","cloudCoverPct":8,"uvIndex":1,"windspeedKph":9,"windDirectionDeg":130,"windDirectionCompass":"SE","precipitationMm":0,"humidityPct":81,"visibilityKm":10,"pressureMb":1025},{"hour":5,"tempC":11,"weatherDesc":"Partly cloudy","cloudCoverPct":12,"uvIndex":1,"windspeedKph":10,"windDirectionDeg":123,"windDirectionCompass":"ESE","precipitationMm":0,"humidityPct":81,"visibilityKm":10,"pressureMb":1025},{"hour":6,"tempC":11,"weatherDesc":"Partly cloudy","cloudCoverPct":17,"uvIndex":4,"windspeedKph":10,"windDirectionDeg":117,"windDirectionCompass":"ESE","precipitationMm":0,"humidityPct":80,"visibilityKm":10,"pressureMb":1025},{"hour":7,"tempC":11,"weatherDesc":"Partly cloudy","cloudCoverPct":20,"uvIndex":4,"windspeedKph":10,"windDirectionDeg":113,"windDirectionCompass":"ESE","precipitationMm":0,"humidityPct":77,"visibilityKm":10,"pressureMb":1025},{"hour":8,"tempC":11,"weatherDesc":"Partly cloudy","cloudCoverPct":23,"uvIndex":4,"windspeedKph":10,"windDirectionDeg":109,"windDirectionCompass":"ESE","precipitationMm":0,"humidityPct":74,"visibilityKm":10,"pressureMb":1026},{"hour":9,"tempC":12,"weatherDesc":"Partly cloudy","cloudCoverPct":26,"uvIndex":4,"windspeedKph":10,"windDirectionDeg":105,"windDirectionCompass":"ESE","precipitationMm":0,"humidityPct":71,"visibilityKm":10,"pressureMb":1026},{"hour":10,"tempC":13,"weatherDesc":"Partly cloudy","cloudCoverPct":24,"uvIndex":4,"windspeedKph":9,"windDirectionDeg":109,"windDirectionCompass":"ESE","precipitationMm":0,"humidityPct":66,"visibilityKm":10,"pressureMb":1026},{"hour":11,"tempC":15,"weatherDesc":"Partly cloudy","cloudCoverPct":21,"uvIndex":4,"windspeedKph":9,"windDirectionDeg":113,"windDirectionCompass":"ESE","precipitationMm":0,"humidityPct":61,"visibilityKm":10,"pressureMb":1026},{"hour":12,"tempC":16,"weatherDesc":"Partly cloudy","cloudCoverPct":19,"uvIndex":5,"windspeedKph":8,"windDirectionDeg":116,"windDirectionCompass":"ESE","precipitationMm":0,"humidityPct":56,"visibilityKm":10,"pressureMb":1026},{"hour":13,"tempC":16,"weatherDesc":"Partly cloudy","cloudCoverPct":31,"uvIndex":5,"windspeedKph":7,"windDirectionDeg":123,"windDirectionCompass":"ESE","precipitationMm":0,"humidityPct":55,"visibilityKm":10,"pressureMb":1025},{"hour":14,"tempC":17,"weatherDesc":"Overcast","cloudCoverPct":43,"uvIndex":4,"windspeedKph":6,"windDirectionDeg":129,"windDirectionCompass":"SE","precipitationMm":0,"humidityPct":54,"visibilityKm":10,"pressureMb":1025},{"hour":15,"tempC":17,"weatherDesc":"Overcast","cloudCoverPct":55,"uvIndex":4,"windspeedKph":6,"windDirectionDeg":136,"windDirectionCompass":"SE","precipitationMm":0,"humidityPct":53,"visibilityKm":10,"pressureMb":1024},{"hour":16,"tempC":17,"weatherDesc":"Overcast","cloudCoverPct":60,"uvIndex":4,"windspeedKph":6,"windDirectionDeg":131,"windDirectionCompass":"SE","precipitationMm":0,"humidityPct":55,"visibilityKm":10,"pressureMb":1024},{"hour":17,"tempC":16,"weatherDesc":"Partly cloudy","cloudCoverPct":65,"uvIndex":5,"windspeedKph":7,"windDirectionDeg":126,"windDirectionCompass":"SE","precipitationMm":0,"humidityPct":58,"visibilityKm":10,"pressureMb":1024},{"hour":18,"tempC":16,"weatherDesc":"Partly cloudy","cloudCoverPct":70,"uvIndex":1,"windspeedKph":8,"windDirectionDeg":121,"windDirectionCompass":"ESE","precipitationMm":0,"humidityPct":60,"visibilityKm":10,"pressureMb":1025},{"hour":19,"tempC":15,"weatherDesc":"Partly cloudy","cloudCoverPct":53,"uvIndex":1,"windspeedKph":8,"windDirectionDeg":120,"windDirectionCompass":"ESE","precipitationMm":0,"humidityPct":62,"visibilityKm":10,"pressureMb":1025},{"hour":20,"tempC":14,"weatherDesc":"Partly cloudy","cloudCoverPct":37,"uvIndex":1,"windspeedKph":9,"windDirectionDeg":119,"windDirectionCompass":"ESE","precipitationMm":0,"humidityPct":64,"visibilityKm":10,"pressureMb":1025},{"hour":21,"tempC":13,"weatherDesc":"Partly cloudy","cloudCoverPct":20,"uvIndex":1,"windspeedKph":9,"windDirectionDeg":118,"windDirectionCompass":"ESE","precipitationMm":0,"humidityPct":66,"visibilityKm":10,"pressureMb":1025},{"hour":22,"tempC":13,"weatherDesc":"Partly cloudy","cloudCoverPct":16,"uvIndex":1,"windspeedKph":9,"windDirectionDeg":120,"windDirectionCompass":"ESE","precipitationMm":0,"humidityPct":68,"visibilityKm":10,"pressureMb":1025},{"hour":23,"tempC":12,"weatherDesc":"Partly cloudy","cloudCoverPct":12,"uvIndex":1,"windspeedKph":8,"windDirectionDeg":123,"windDirectionCompass":"ESE","precipitationMm":0,"humidityPct":70,"visibilityKm":10,"pressureMb":1024}]}

        expected = 3.7
        actual = self.CALCULATOR.get_sun_hour(date, location, api=requests_mock)
        requests_mock.get.assert_called_once_with("http://118.138.246.158/api/v1/weather?location=" + location + "&date=" + date.strftime("%Y-%m-%d"))
        self.assertEqual(expected, actual)

     # Invalid Location id but valid date
    def test_case2(self):
        date = datetime(2020, 8, 1)
        location = "abdsf324"

        requests_mock = Mock()
        response_mock = Mock()
        requests_mock.get.return_value = response_mock
        response_mock.status_code = 400
        expected_mock_call_count = 0
        self.assertEqual(expected_mock_call_count,requests_mock.call_count)
        with self.assertRaises(AssertionError):
            self.CALCULATOR.get_sun_hour(date, location, api=requests_mock)

    # Invalid date (out of range of the date for the api) and valid location id
    def test_case3(self):
        date = datetime(1980,8, 1)
        location = "5bea7b46-9809-4189-aafe-160208da94f7"

        requests_mock = Mock()
        response_mock = Mock()
        requests_mock.get.return_value = response_mock
        response_mock.status_code = 400
        expected_mock_call_count = 0
        self.assertEqual(expected_mock_call_count, requests_mock.call_count)
        with self.assertRaises(AssertionError):
            self.CALCULATOR.get_sun_hour(date, location, api=requests_mock)


if __name__ == '__main__':
    unittest.main()
