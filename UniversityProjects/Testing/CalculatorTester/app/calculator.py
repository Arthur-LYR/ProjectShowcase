import math
import statistics
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import holidays
import requests
import json


class Calculator:
    def __init__(self):
        pass

    def is_surcharge_day(self, start_date):
        """ Checks if date will incur 1.1 surcharge
        :param start_date: Date to check as datetime object
        :return: True if is Weekday or Public Holiday, False otherwise
        """
        return start_date in holidays.CountryHoliday('AU') or (not start_date.strftime("%a") == "Sat" and not start_date.strftime("%a") == "Sun")

    def is_peak_hour(self, start_hour):
        """ Checks if date will incur 50% discount
        :param start_hour: Time to check as datetime object
        :return: True if between 06:00 to 18:00 inclusive, False otherwise
        """
        # Set day, month, year to constant value
        start_hour = start_hour.replace(year=1970, month=1, day=1)

        # Boundary
        lower_bound = datetime(1970, 1, 1, 6, 0, 0)
        upper_bound = datetime(1970, 1, 1, 18, 0, 0)

        # Check if peak or not
        if lower_bound <= start_hour < upper_bound:
            return True
        return False

    def get_base_price(self, charger_configuration):
        """ Returns appropriate base price given charger_configuration
        :param charger_configuration: 1-8 which represents the type of charge
        :return: Appropriate base price in cents
        """
        if charger_configuration == "1":
            return 5
        elif charger_configuration == "2":
            return 7.5
        elif charger_configuration == "3":
            return 10
        elif charger_configuration == "4":
            return 12.5
        elif charger_configuration == "5":
            return 15
        elif charger_configuration == "6":
            return 20
        elif charger_configuration == "7":
            return 30
        elif charger_configuration == "8":
            return 50
        else:
            raise AssertionError("Configuration must be between 1 and 8 inclusive")

    def get_power(self, charger_configuration):
        """ Returns appropriate power given charger_configuration
        :param charger_configuration: 1-8 which represents the type of charge
        :return: Appropriate power in kW
        """
        if charger_configuration == "1":
            return 2
        elif charger_configuration == "2":
            return 3.6
        elif charger_configuration == "3":
            return 7.2
        elif charger_configuration == "4":
            return 11
        elif charger_configuration == "5":
            return 22
        elif charger_configuration == "6":
            return 36
        elif charger_configuration == "7":
            return 90
        elif charger_configuration == "8":
            return 350
        else:
            raise AssertionError("Configuration must be between 1 and 8 inclusive")

    def str_to_datetime(self, start_date, start_time):
        """ Converts a string date and string time to datetime object
        :param start_date: Date in DD/MM/YYYY form
        :param start_time: Time in HH:MM form
        """
        try:
            # Extract Date Attributes
            start_date_attributes = start_date.split("/")
            start_day = int(start_date_attributes[0])
            start_month = int(start_date_attributes[1])
            start_year = int(start_date_attributes[2])

            # Extract Time Attributes
            start_time_attributes = start_time.split(":")
            start_hour = int(start_time_attributes[0])
            start_min = int(start_time_attributes[1])

            # Return in Datetime format
            return datetime(start_year, start_month, start_day, start_hour, start_min, 0)
        except (ValueError, IndexError):
            raise AssertionError("Invalid Date/Time Passed")

    def dates_between(self, start_date, end_date):
        """ Computes the appropriate date ranges from a start date and end date
        :param start_date: Start Date as datetime object
        :param end_date: End Date as datetime object
        :return: List of tuples of date ranges
        """
        dates = []
        current = start_date
        if start_date <= end_date:
            if start_date.date() == end_date.date():
                dates.append((current, end_date))
            else:
                dates.append((current, current.replace(hour=0, minute=0, second=0) + timedelta(days=1)))
                current = current.replace(hour=0, minute=0, second=0) + timedelta(days=1)
                while current <= end_date:
                    if current.replace(hour=0, minute=0, second=0) + timedelta(days=1) > end_date:
                        dates.append((current, end_date))
                    elif current < end_date:
                        dates.append((current, current.replace(hour=0, minute=0, second=0) + timedelta(days=1)))
                    current += timedelta(days=1)
        return dates

    def hours_between(self, start_time, end_time):
        """ Computes the appropriate hour ranges from a start time and end time
        :param start_time: Start Time as datetime object
        :param end_time: End Time as datetime object
        :return: List of tuples of time ranges
        """
        hours = []
        current = start_time
        if start_time <= end_time:
            if start_time.hour == end_time.hour and start_time.date() == end_time.date():
                hours.append((current, end_time))
            else:
                hours.append((current, current.replace(minute=0, second=0) + timedelta(hours=1)))
                current = current.replace(minute=0, second=0) + timedelta(hours=1)
                while current <= end_time:
                    if current.replace(minute=0, second=0) + timedelta(hours=1) > end_time:
                        hours.append((current, end_time))
                    elif current < end_time:
                        hours.append((current, current.replace(minute=0, second=0) + timedelta(hours=1)))
                    current += timedelta(hours=1)
        return hours

    def get_reference_dates(self, start_date, end_date, date_object=datetime):
        """ Computes the Reference Dates according to the specifications
        :param start_date: Start Date as datetime object
        :param end_date: End Date as datetime object
        :param date_object: Datetime object used to find current date
        :return: List of reference dates
        """
        if end_date <= date_object.now() - relativedelta(days=2):
            return [(start_date, end_date)]
        else:
            while end_date > date_object.now() - relativedelta(days=2):
                start_date = start_date - relativedelta(years=1)
                end_date = end_date - relativedelta(years=1)
            return [(start_date, end_date),
                    (start_date - relativedelta(years=1), end_date - relativedelta(years=1)),
                    (start_date - relativedelta(years=2), end_date - relativedelta(years=2))]

    def get_solar_proportion(self, start_hour, end_hour, sunrise, sunset):
        """ Computes the multiplier to the solar energy generated
        :param start_hour: Start Hour as datetime object
        :param end_hour: End Hour as datetime object
        :sunrise: Sunrise Time as datetime object
        :sunset: Sunset Time as datetime object
        """
        if end_hour <= sunrise or start_hour >= sunset:
            return 0
        elif start_hour < sunrise < end_hour:
            proportion = end_hour - sunrise
            return proportion.seconds / 3600
        elif start_hour < sunset < end_hour:
            proportion = sunset - start_hour
            return proportion.seconds / 3600
        else:
            proportion = end_hour - start_hour
            return proportion.seconds / 3600

    def get_sun_hour(self, date, location, api=requests):
        """ Obtains the solar insolation value of a specific location at a specific time
        :param date: Date as datetime object
        :param location: Location ID
        :param api: API to be used to get sun hour from
        :return: Solar Insolation Value
        """
        date = date.strftime("%Y-%m-%d")
        response = api.get("http://118.138.246.158/api/v1/weather?location=" + location + "&date=" + date)
        if response.status_code == 200:
            sun_hour = json.dumps(response.json()["sunHours"])
            return float(sun_hour)
        else:
            raise AssertionError("API Failed to provide response. Check Date and Location ID.")

    def get_sunrise_time(self, date, location, api=requests):
        """ Obtains the sunrise time of a specific location at a specific time
        :param date: Date as datetime object
        :param location: Location ID
        :param api: API to be used to get sunrise time from
        :return: Time of Sunrise
        """
        strdate = date.strftime("%Y-%m-%d")
        response = api.get("http://118.138.246.158/api/v1/weather?location=" + location + "&date=" + strdate)
        if response.status_code == 200:
            sun_rise = json.dumps(response.json()['sunrise'])
            hours, minutes, seconds = sun_rise.split(":")
            hours = hours[1:3]
            seconds = seconds[0:2]
            return datetime(date.year, date.month, date.day, int(hours), int(minutes), int(seconds))
        else:
            raise AssertionError("API Failed to provide response. Check Date and Location ID.")

    def get_sunset_time(self, date, location, api=requests):
        """ Obtains the sunset time of a specific location at a specific time
        :param date: Date as datetime object
        :param location: Location ID
        :param api: API to be used to get sunset time from
        :return: Time of Sunset
        """
        strdate = date.strftime("%Y-%m-%d")
        response = api.get("http://118.138.246.158/api/v1/weather?location=" + location + "&date=" + strdate)
        if response.status_code == 200:
            sun_set = json.dumps(response.json()['sunset'])
            hours, minutes, seconds = sun_set.split(":")
            hours = hours[1:3]
            seconds = seconds[0:2]
            return datetime(date.year, date.month, date.day, int(hours), int(minutes), int(seconds))
        else:
            raise AssertionError("API Failed to provide response. Check Date and Location ID.")

    def get_cloud_cover(self, date, location, api=requests):
        """ Obtains the cloud cover value of a specific location at a specific time
        :param date: Date as datetime object
        :param location: Location ID
        :param api: API to be used to get cloud cover from
        :return: Cloud Cover Value
        """
        hour = date.hour
        date = date.strftime("%Y-%m-%d")
        response = api.get("http://118.138.246.158/api/v1/weather?location=" + location + "&date=" + date)
        if response.status_code == 200:
            cloud_cover = json.dumps(response.json()["hourlyWeatherHistory"][hour]["cloudCoverPct"])
            return int(cloud_cover)
        else:
            raise AssertionError("API Failed to provide response. Check Date and Location ID.")

    def time_calculation(self, initial_state, final_state, capacity, charger_configuration):
        """ Calculates Time of Charge
        :param initial_state: Initial State of Charge in Percentage
        :param final_state: Final State of Charge in Percentage
        :param capacity: Capacity of Battery in kWh
        :param charger_configuration: Charger configuration used (1-8)
        :return: Time of Charge
        """
        # Convert to ints
        initial_state = int(initial_state)
        final_state = int(final_state)
        capacity = int(capacity)

        # Calculate
        power = self.get_power(charger_configuration)
        time = (final_state - initial_state) / 100 * capacity / power

        # Convert to Hours and Minutes and return
        time = (math.floor(time), (time % 1) * 60)
        return time

    def cost_calculation_1(self, time, start_date, start_time, charger_configuration):
        """ Calculates Cost of Charge based on Requirement 1
        :param time: Time taken to charge car in form of (hours, minutes)
        :param start_date: Date to start charge in DD/MM/YYYY string form
        :param start_time: Time to start charge in HH:MM string form
        :param charger_configuration: Charger configuration used (1-8)
        :return: Cost of Charge
        """
        # Initialise Important Variables
        cost = 0
        base_price = self.get_base_price(charger_configuration)
        power = self.get_power(charger_configuration)
        days = (time[0] + time[1] / 60) / 24

        # Calculate Start and End Date
        start_date = self.str_to_datetime(start_date, start_time)
        end_date = start_date + timedelta(days=days)

        # Get Dates Between
        date_ranges = self.dates_between(start_date, end_date)

        # Loop through Days
        for start_day, end_day in date_ranges:
            # Check if Surcharge Incurred
            if self.is_surcharge_day(start_day):
                surcharge = 1.1
            else:
                surcharge = 1

            # Get Hours Between
            hour_ranges = self.hours_between(start_day, end_day)

            # Loop through Hours
            for start_hour, end_hour in hour_ranges:
                # Check if peak hour
                if self.is_peak_hour(start_hour):
                    discount = 1
                else:
                    discount = 0.5

                # Calculate Net Power
                delta = end_hour - start_hour
                net_power = delta.seconds / 3600 * power

                # Update Cost
                cost += base_price / 100 * net_power * surcharge * discount

        # Return
        return cost

    def cost_calculation_2(self, time, start_date, start_time, charger_configuration, location, api=requests, date_object=datetime):
        """ Calculates Cost of Charge based on Requirement 2
        :param time: Time taken to charge car in form of (hours, minutes)
        :param start_date: Date to start charge in DD/MM/YYYY string form
        :param start_time: Time to start charge in HH:MM string form
        :param charger_configuration: Charger configuration used (1-8)
        :param location: ID of Location of Charge
        :param api: API to be used to get weather data from
        :return: Cost of Charge
        """
        # Initialise Important Variables
        cost = 0
        base_price = self.get_base_price(charger_configuration)
        power = self.get_power(charger_configuration)
        days = (time[0] + time[1] / 60) / 24

        # Calculate Start and End Date
        start_date = self.str_to_datetime(start_date, start_time)
        end_date = start_date + timedelta(days=days)

        # Check Dates
        if start_date < datetime(2008, 7, 1) or end_date > date_object.now() - relativedelta(days=2):
            raise ValueError("Invalid Date")

        # Get Dates Between
        date_ranges = self.dates_between(start_date, end_date)

        # Loop through Days
        for start_day, end_day in date_ranges:
            # Check if Surcharge Incurred
            if self.is_surcharge_day(start_day):
                surcharge = 1.1
            else:
                surcharge = 1

            # Get Hours Between
            hour_ranges = self.hours_between(start_day, end_day)

            # Get Solar Values
            si = self.get_sun_hour(start_day, location, api)
            sunrise = self.get_sunrise_time(start_day, location, api)
            sunset = self.get_sunset_time(start_day, location, api)
            suntime = sunset - sunrise
            dl = suntime.seconds / 3600

            # Loop through Hours
            for start_hour, end_hour in hour_ranges:
                # Check if peak hour
                if self.is_peak_hour(start_hour):
                    discount = 1
                else:
                    discount = 0.5

                # Calculate Solar Energy
                proportion = self.get_solar_proportion(start_hour, end_hour, sunrise, sunset)
                solar_energy = si * 1/dl * 50 * 0.20 * proportion

                # Calculate Net Power
                delta = end_hour - start_hour
                net_power = max(delta.seconds / 3600 * power - solar_energy, 0)

                # Update Cost
                cost += base_price / 100 * net_power * surcharge * discount

        # Return
        return cost

    def cost_calculation_3(self, time, start_date, start_time, charger_configuration, location, api=requests, date_object=datetime):
        """ Calculates Cost of Charge based on Requirement 3
        :param time: Time taken to charge car in form of (hours, minutes)
        :param start_date: Date to start charge in DD/MM/YYYY string form
        :param start_time: Time to start charge in HH:MM string form
        :param charger_configuration: Charger configuration used (1-8)
        :param location: ID of Location of Charge
        :param api: API to be used to get weather data from
        :return: Cost of Charge
        """
        # Initialise Important Variables
        cost = 0
        base_price = self.get_base_price(charger_configuration)
        power = self.get_power(charger_configuration)
        days = (time[0] + time[1] / 60) / 24

        # Calculate Start and End Date
        start_date = self.str_to_datetime(start_date, start_time)
        end_date = start_date + timedelta(days=days)

        # Check Dates
        if start_date < datetime(2008, 7, 1):
            raise ValueError("Invalid Date")

        # Get Dates Between
        date_ranges = self.dates_between(start_date, end_date)

        # Loop through Days
        for start_day, end_day in date_ranges:
            # Get Reference Dates
            costs = []
            references_dates = self.get_reference_dates(start_day, end_day, date_object)

            # Loop through Reference Dates
            for reference_start, reference_end in references_dates:
                # Initialise Cost for Reference Date
                current_cost = 0

                # Check if Surcharge Incurred
                if self.is_surcharge_day(reference_start):
                    surcharge = 1.1
                else:
                    surcharge = 1

                # Get Hours Between
                hour_ranges = self.hours_between(reference_start, reference_end)

                # Get Solar Values
                si = self.get_sun_hour(reference_start, location, api)
                sunrise = self.get_sunrise_time(reference_start, location, api)
                sunset = self.get_sunset_time(reference_start, location, api)
                suntime = sunset - sunrise
                dl = suntime.seconds / 3600

                # Loop through Hours
                for start_hour, end_hour in hour_ranges:
                    # Check if peak hour
                    if self.is_peak_hour(start_hour):
                        discount = 1
                    else:
                        discount = 0.5

                    # Calculate Solar Energy
                    cc = self.get_cloud_cover(start_hour, location, api)
                    proportion = self.get_solar_proportion(start_hour, end_hour, sunrise, sunset)
                    solar_energy = si * 1/dl * (1 - cc/100) * 50 * 0.20 * proportion

                    # Calculate Net Power
                    delta = end_hour - start_hour
                    net_power = max(delta.seconds / 3600 * power - solar_energy, 0)

                    # Update Cost for Reference Date
                    current_cost += base_price / 100 * net_power * surcharge * discount

                # Append to List of Costs
                costs.append(current_cost)

            # Update Final Cost with Mean of Reference Date Costs
            cost += statistics.mean(costs)

        # Return
        return cost
