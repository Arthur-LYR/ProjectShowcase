import requests
from flask import Flask, flash
from flask import render_template
from flask import request, jsonify
from app.calculator import Calculator

from app.calculator_form import Calculator_Form
import os

SECRET_KEY = os.urandom(32)

ev_calculator_app = Flask(__name__)
ev_calculator_app.config['SECRET_KEY'] = SECRET_KEY


@ev_calculator_app.route('/', methods=['GET', 'POST'])
def operation_result():
    # request.form looks for:
    # html tags with matching "name="

    calculator_form = Calculator_Form(request.form)

    # validation of the form
    if request.method == "POST" and calculator_form.validate():
        # if valid, create calculator to calculate the time and cost
        calculator = Calculator()
        # extract information from the form
        battery_capacity = request.form['BatteryPackCapacity']
        initial_charge = request.form['InitialCharge']
        final_charge = request.form['FinalCharge']
        start_date = request.form['StartDate']
        start_time = request.form['StartTime']
        charger_configuration = request.form['ChargerConfiguration']
        location = request.form['Location']

        calculator_form.Location = []

        # Calculate Time
        time = calculator.time_calculation(initial_charge, final_charge, battery_capacity, charger_configuration)
        time_display = str(time[0]) + " hours {:.2f} minutes".format(time[1])

        # Calculate Cost for Requirement 1
        cost1 = calculator.cost_calculation_1(time, start_date, start_time, charger_configuration)
        cost1 = "${:.2f}".format(cost1)

        # Calculate Cost for Requirement 2
        try:
            cost2 = calculator.cost_calculation_2(time, start_date, start_time, charger_configuration, location)
            cost2 = "${:.2f}".format(cost2)
        except ValueError:
            cost2 = "NA"

        # Calculate Cost for Requirement 3
        try:
            cost3 = calculator.cost_calculation_3(time, start_date, start_time, charger_configuration, location)
            cost3 = "${:.2f}".format(cost3)
        except ValueError:
            cost3 = "NA"

        # values of variables can be sent to the template for rendering the webpage that users will see
        return render_template('calculator.html', cost1=cost1, cost2=cost2, cost3=cost3, time=time_display,
                               calculation_success=True, form=calculator_form)

    else:
        flash_errors(calculator_form)
        return render_template('calculator.html', calculation_success=False, form=calculator_form)


# method to display all errors
def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')


@ev_calculator_app.route('/<postcode>', methods=['GET'])
def location(postcode):
    response = requests.get(f"http://118.138.246.158/api/v1/location?postcode={postcode}")
    return jsonify(response.json())


if __name__ == '__main__':
    ev_calculator_app.run()

