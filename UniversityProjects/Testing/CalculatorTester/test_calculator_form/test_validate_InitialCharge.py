import unittest
from unittest.mock import Mock
import main
from app.calculator_form import *


class TestValidateInitialCharge(unittest.TestCase):
    CALCULATOR_FORM = None

    def test_initial_charge_none(self):
        main.ev_calculator_app.config["WTF_CSRF_ENABLED"] = False
        with main.ev_calculator_app.app_context():
            calculator_form = Calculator_Form()
            mock_field = Mock()
            mock_field.data = None
            with self.assertRaises(ValidationError):
                calculator_form.validate_InitialCharge(mock_field)

    def test_empty_initial_charge(self):
        main.ev_calculator_app.config["WTF_CSRF_ENABLED"] = False
        with main.ev_calculator_app.app_context():
            calculator_form = Calculator_Form()
            mock_field = Mock()
            mock_field.data = ''
            with self.assertRaises(ValueError):
                calculator_form.validate_InitialCharge(mock_field)

    def test_initial_charge_greater_than_final_charge(self):
        main.ev_calculator_app.config["WTF_CSRF_ENABLED"] = False
        with main.ev_calculator_app.app_context():
            calculator_form = Calculator_Form()
            calculator_form.FinalCharge.data = 50  # initialize the value of final charge
            mock_field = Mock()
            mock_field.data = 51
            with self.assertRaises(ValueError):
                calculator_form.validate_InitialCharge(mock_field)

    def test_negative_initial_charge(self):
        main.ev_calculator_app.config["WTF_CSRF_ENABLED"] = False
        with main.ev_calculator_app.app_context():
            calculator_form = Calculator_Form()
            calculator_form.FinalCharge.data = 50  # initialize the value of final charge
            mock_field = Mock()
            mock_field.data = -1
            with self.assertRaises(ValueError):
                calculator_form.validate_InitialCharge(mock_field)

    def test_initial_charge_exceed_100(self):
        main.ev_calculator_app.config["WTF_CSRF_ENABLED"] = False
        with main.ev_calculator_app.app_context():
            calculator_form = Calculator_Form()
            calculator_form.FinalCharge.data = 100  # initialize the value of final charge
            mock_field = Mock()
            mock_field.data = 101
            with self.assertRaises(ValueError):
                calculator_form.validate_InitialCharge(mock_field)

    def test_normal_condition(self):
        main.ev_calculator_app.config["WTF_CSRF_ENABLED"] = False
        with main.ev_calculator_app.app_context():
            calculator_form = Calculator_Form()
            calculator_form.FinalCharge.data = 100  # initialize the value of final charge
            mock_field = Mock()
            mock_field.data = 99
            calculator_form.validate_InitialCharge(mock_field)


if __name__ == '__main__':
    unittest.main()
