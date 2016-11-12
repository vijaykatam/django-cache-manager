# -*- coding: utf-8 -*-

#!/usr/bin/env python
# The nose plugin that I generally use for django tests is not open sourced so manage.py for tests until it can be open sourced.
import os
import sys
import django
try:
    import settings
except ImportError:
    sys.stderr.write("Error importing settings")
    sys.exit(1)

if __name__ == "__main__":
    if django.VERSION < (1, 6):
        from django.core.management import execute_manager
        execute_manager(settings)
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
