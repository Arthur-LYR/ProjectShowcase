import unittest
from unittest.mock import Mock
import main
from app.calculator_form import *


class TestIsInt(unittest.TestCase):
    CALCULATOR_FORM = None

    def test_float_given(self):
        main.ev_calculator_app.config["WTF_CSRF_ENABLED"] = False
        with main.ev_calculator_app.app_context():
            calculator_form = Calculator_Form()
            mock_field = Mock()
            mock_field.data = 1.1
            self.assertFalse(calculator_form.isInt(mock_field.data), "Test result did not return False")

    def test_int_given(self):
        main.ev_calculator_app.config["WTF_CSRF_ENABLED"] = False
        with main.ev_calculator_app.app_context():
            calculator_form = Calculator_Form()
            mock_field = Mock()
            mock_field.data = 1
            self.assertTrue(calculator_form.isInt(mock_field.data), "Test result did not return False")

    def test_string_given(self):
        main.ev_calculator_app.config["WTF_CSRF_ENABLED"] = False
        with main.ev_calculator_app.app_context():
            calculator_form = Calculator_Form()
            mock_field = Mock()
            mock_field.data = "Ganyu"
            self.assertFalse(calculator_form.isInt(mock_field.data), "Test result did not return False")

    def test_empty_string_given(self):
        main.ev_calculator_app.config["WTF_CSRF_ENABLED"] = False
        with main.ev_calculator_app.app_context():
            calculator_form = Calculator_Form()
            mock_field = Mock()
            mock_field.data = ''
            self.assertFalse(calculator_form.isInt(mock_field.data), "Test result did not return False")


if __name__ == '__main__':
    unittest.main()
