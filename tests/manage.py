#!/usr/bin/env python
# The nose plugin that I generally use for django tests is not open sourced so manage.py for tests until it can be open sourced.
from django.core.management import execute_manager
try:
    import settings
except ImportError:
    import sys
    sys.stderr.write("Error importing settings")
    sys.exit(1)

if __name__ == "__main__":
    execute_manager(settings)
