# Software Engineering Design and Architecture

NOTE: This project will not be run anymore as the API it relies on is now deactivated. The project involved me working in a pair to develop a web app that applies good software engineering design patterns and OOP. A class diagram was also designed as part of the project.

## Setup
1. Activate virtualenv. Installation may only be done once.
```
# Windows
python -m venv env
. env\Scripts\activate

# Mac/Linux
python -m venv env
source env/bin/activate
```
2. Install Required Dependencies/Packages
```
pip install -r requirements.txt
```
3. Create new file called `api_token.txt` in `project` containing your personal API token 

## Run Program
1. cd to project. This only needs to be done once.
```
cd project
```
2. Run the following command.
```
python manage.py runserver
```