import unittest
from unittest.mock import Mock
import main
from app.calculator_form import *


class TestValidatePostCode(unittest.TestCase):
    CALCULATOR_FORM = None

    def test_postcode_none(self):
        main.ev_calculator_app.config["WTF_CSRF_ENABLED"] = False
        with main.ev_calculator_app.app_context():
            calculator_form = Calculator_Form()
            mock_field = Mock()
            mock_field.data = None
            with self.assertRaises(ValidationError):
                calculator_form.validate_PostCode(mock_field)

    def test_empty_postcode(self):
        main.ev_calculator_app.config["WTF_CSRF_ENABLED"] = False
        with main.ev_calculator_app.app_context():
            calculator_form = Calculator_Form()
            mock_field = Mock()
            mock_field.data = ''
            with self.assertRaises(ValueError):
                calculator_form.validate_PostCode(mock_field)

    def test_postcode_not_integer(self):
        main.ev_calculator_app.config["WTF_CSRF_ENABLED"] = False
        with main.ev_calculator_app.app_context():
            calculator_form = Calculator_Form()
            mock_field = Mock()
            mock_field.data = "5000.1"
            with self.assertRaises(ValidationError):
                calculator_form.validate_PostCode(mock_field)

    def test_response_code_400(self):
        main.ev_calculator_app.config["WTF_CSRF_ENABLED"] = False
        with main.ev_calculator_app.app_context():
            calculator_form = Calculator_Form()
            mock_field = Mock()
            mock_field.data = "500"
            with self.assertRaises(ValueError):
                calculator_form.validate_PostCode(mock_field)

    def test_normal_condition(self):
        main.ev_calculator_app.config["WTF_CSRF_ENABLED"] = False
        with main.ev_calculator_app.app_context():
            calculator_form = Calculator_Form()
            mock_field = Mock()
            mock_field.data = "5000"
            calculator_form.validate_PostCode(mock_field)


if __name__ == '__main__':
    unittest.main()
