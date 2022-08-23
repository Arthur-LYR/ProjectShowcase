import unittest
from unittest.mock import Mock
import main
from app.calculator_form import *


class TestValidateChargerConfiguration(unittest.TestCase):
    CALCULATOR_FORM = None

    def test_charger_configuration_none(self):
        main.ev_calculator_app.config["WTF_CSRF_ENABLED"] = False
        with main.ev_calculator_app.app_context():
            calculator_form = Calculator_Form()
            mock_field = Mock()
            mock_field.data = None
            with self.assertRaises(ValidationError):
                calculator_form.validate_ChargerConfiguration(mock_field)

    def test_empty_charger_configuration(self):
        main.ev_calculator_app.config["WTF_CSRF_ENABLED"] = False
        with main.ev_calculator_app.app_context():
            calculator_form = Calculator_Form()
            mock_field = Mock()
            mock_field.data = ''
            with self.assertRaises(ValueError):
                calculator_form.validate_ChargerConfiguration(mock_field)

    def test_charger_configuration_not_integer(self):
        main.ev_calculator_app.config["WTF_CSRF_ENABLED"] = False
        with main.ev_calculator_app.app_context():
            calculator_form = Calculator_Form()
            mock_field = Mock()
            mock_field.data = "1.1"
            with self.assertRaises(ValidationError):
                calculator_form.validate_ChargerConfiguration(mock_field)

    def test_charger_configuration_outside_integer_range(self):
        main.ev_calculator_app.config["WTF_CSRF_ENABLED"] = False
        with main.ev_calculator_app.app_context():
            calculator_form = Calculator_Form()
            mock_field = Mock()
            mock_field.data = "9"
            with self.assertRaises(ValueError):
                calculator_form.validate_ChargerConfiguration(mock_field)

    def test_normal_condition(self):
        main.ev_calculator_app.config["WTF_CSRF_ENABLED"] = False
        with main.ev_calculator_app.app_context():
            calculator_form = Calculator_Form()
            mock_field = Mock()
            mock_field.data = "8"
            calculator_form.validate_ChargerConfiguration(mock_field)


if __name__ == '__main__':
    unittest.main()
