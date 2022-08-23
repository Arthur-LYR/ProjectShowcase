#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


app_path = os.getcwd() + "\\app"
system_path = app_path + "\\models"
apihandlers_path = system_path + "\\apis"
sys.path.append(app_path)
sys.path.append(system_path)
sys.path.append(apihandlers_path)


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
