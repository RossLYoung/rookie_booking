#!/usr/bin/env python
import os
import sys
from rookie_booking.config.env_vars import vars

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rookie_booking.settings")
    os.environ.setdefault("DJANGO_CONFIGURATION", "Development")

    try:
        for key, val in vars.items():
            os.environ.setdefault(key, val)
    except:
        pass

    from configurations.management import execute_from_command_line

    execute_from_command_line(sys.argv)
