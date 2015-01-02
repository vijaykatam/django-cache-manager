# -*- coding: utf-8 -*-

from django.core.management import (
    setup_environ,
    call_command
)

try:
    import settings
except ImportError:
    import sys
    sys.stderr.write("Error importing settings")
    sys.exit(1)

if __name__ == "__main__":
    setup_environ(settings)
    call_command('syncdb')
    call_command('shell')
