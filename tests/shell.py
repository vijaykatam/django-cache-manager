# -*- coding: utf-8 -*-

import os
import django
from django.core.management import call_command

if __name__ == "__main__":
    if django.get_version() < '1.6':
        import settings
        from django.core.management import setup_environ
        setup_environ(settings)
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
        if django.get_version() >= '1.7':
            django.setup()

    call_command('syncdb')
    call_command('shell')
