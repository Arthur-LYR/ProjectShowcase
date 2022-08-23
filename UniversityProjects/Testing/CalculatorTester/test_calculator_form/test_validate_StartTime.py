import unittest
from unittest.mock import Mock
import main
from app.calculator_form import *
import datetime


class TestValidateStartTime(unittest.TestCase):
    CALCULATOR_FORM = None

    def test_start_time_none(self):
        main.ev_calculator_app.config["WTF_CSRF_ENABLED"] = False
        with main.ev_calculator_app.app_context():
            calculator_form = Calculator_Form()
            mock_field = Mock()
            mock_field.data = None
            with self.assertRaises(ValidationError):
                calculator_form.validate_StartTime(mock_field)

    def test_empty_start_time(self):
        main.ev_calculator_app.config["WTF_CSRF_ENABLED"] = False
        with main.ev_calculator_app.app_context():
            calculator_form = Calculator_Form()
            mock_field = Mock()
            mock_field.data = ''
            with self.assertRaises(ValueError):
                calculator_form.validate_StartTime(mock_field)

    def test_normal_condition(self):
        main.ev_calculator_app.config["WTF_CSRF_ENABLED"] = False
        with main.ev_calculator_app.app_context():
            calculator_form = Calculator_Form()
            mock_field = Mock()
            mock_field.data = datetime.time(17, 30, 0)
            calculator_form.validate_StartTime(mock_field)


if __name__ == '__main__':
    unittest.main()
