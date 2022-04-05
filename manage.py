#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import imp
import os
import sys
from HISKPScreen.data_services.setup import database_setup
from HISKPScreen.data_services.database_connections import get_conn_and_cur
import time

__PG_TIMEOUT__ = 100

def wait_PG():
    for _ in range(__PG_TIMEOUT__):
        try:
            get_conn_and_cur("main_db")
            return True
        except:
            time.sleep(1)
    return False
def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HISKPScreen.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    database_setup()
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    wait_PG()
    main()
