# -*- coding: utf-8 -*-
import os.path
import random
import sys

import django

here = lambda *x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)
SECRET_KEY = 's3cr3t'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': here('test.db')
    },
}

INSTALLED_APPS = (
    'django_cache_manager',
    'tests',
    'django_nose',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# static cache location for django shell
cache_location = '/tmp/django_cache_manager'
# random cache location for each test run
if 'test' in sys.argv:
    cache_location = '/tmp/django_cache_manager_{0}'.format(random.randint(1, 1000))

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    'django_cache_manager.cache_backend': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': cache_location,
        'TIMEOUT': 1800
    }
}
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = False

USE_TZ = False

DEBUG = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S",
        },
        'simple': {
            'format': ' [%(levelname)s] %(name)s: process_id="%(process)s";thread_id="%(thread)s": %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'DEBUG',
        },
        'factory': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'ERROR',
        },
    },


}

if django.get_version() > '1.7':
    MIDDLEWARE_CLASSES = ()
