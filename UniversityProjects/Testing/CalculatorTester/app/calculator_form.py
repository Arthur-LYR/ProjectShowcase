import requests
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField, SelectField
from wtforms.validators import DataRequired, ValidationError, Optional


# validation for form inputs
class Calculator_Form(FlaskForm):
    # this variable name needs to match with the input attribute name in the html file
    # you are NOT ALLOWED to change the field type, however, you can add more built-in validators and custom messages
    BatteryPackCapacity = StringField("Battery Pack Capacity", [DataRequired()])
    InitialCharge = StringField("Initial Charge", [DataRequired()])
    FinalCharge = StringField("Final Charge", [DataRequired()])
    StartDate = DateField("Start Date", [DataRequired("Data is missing or format is incorrect")], format='%d/%m/%Y')
    StartTime = TimeField("Start Time", [DataRequired("Data is missing or format is incorrect")], format='%H:%M')
    ChargerConfiguration = StringField("Charger Configuration", [DataRequired()])
    PostCode = StringField("Post Code", [DataRequired()])
    Location = StringField("Location", [DataRequired()])

    # use validate_ + field_name to activate the flask-wtforms built-in validator
    # this is an example for you
    def validate_BatteryPackCapacity(self, field):
        if field.data is None:
            raise ValidationError('Field data is none')
        elif field.data == '':
            raise ValueError("cannot fetch data")
        elif int(field.data) < 0:
            raise ValueError("battery pack capacity cannot be negative")

    # validate initial charge here
    def validate_InitialCharge(self, field):
        # another example of how to compare initial charge with final charge
        # you may modify this part of the code
        if field.data is None:
            raise ValidationError("Field data is none")
        elif field.data == '':
            raise ValueError("cannot fetch data")
        elif int(field.data) > int(self.FinalCharge.data):
            raise ValueError("Initial charge data error")
        elif int(field.data) < 0:
            raise ValueError("Initial charge cannot be negative")
        elif int(field.data) > 100:
            raise ValueError("Initial charge value cannot be more than 100")

    # validate final charge here
    def validate_FinalCharge(self, field):
        if field.data is None:
            raise ValidationError("Field data is none")
        elif field.data == '':
            raise ValueError("cannot fetch data")
        elif int(field.data) < int(self.InitialCharge.data):
            raise ValueError("Final charge data error")
        elif int(field.data) < 0:
            raise ValueError("final charge value cannot be negative")
        elif int(field.data) > 100:
            raise ValueError("Final charge value cannot be more than 100")

    # validate start date here
    def validate_StartDate(self, field):
        if field.data is None:
            raise ValidationError("Field data is none")
        elif field.data == '':
            raise ValueError("cannot fetch data")

    # validate start time here
    def validate_StartTime(self, field):
        if field.data is None:
            raise ValidationError("Field data is none")
        elif field.data == '':
            raise ValueError("cannot fetch data")

    # validate charger configuration here
    def validate_ChargerConfiguration(self, field):
        try:
            if field.data is None:
                raise ValidationError("Field data is none")
            elif field.data == '':
                raise ValueError("cannot fetch data")
            elif not self.isInt(field.data):
                raise TypeError("Charger configuration must be integer type")
            elif not (1 <= int(field.data) <= 8):
                raise ValueError("Charger configuration invalid (must be 1-8)")
        except TypeError:
            raise ValidationError("Charger configuration must be integer type")

    # validate postcode here
    def validate_PostCode(self, field):
        try:
            response = requests.get("http://118.138.246.158/api/v1/location?postcode=" + field.data)
            if field.data is None:
                raise ValidationError("Field data is none")
            elif field.data == '':
                raise ValueError("cannot fetch data")
            elif not self.isInt(field.data):
                raise TypeError("Postcode must be integer type")
            elif response.status_code == 400:
                raise ValueError("Postcode invalid, and must consist of 4 digits.")
        except TypeError:
            raise ValidationError("Postcode must be integer type")

    # helper methods
    # function to check if the input is integer type
    def isInt(self, x):
        try:
            a = float(x)
            b = int(a)
        except (TypeError, ValueError):
            return False
        else:
            return a == b
