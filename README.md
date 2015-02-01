===============================
django-cache-manager
===============================

Simple cache manager for django models that caches querysets for a model. Cache manager will cache any query that has been seen for a model. Model cache is evicted for any updates/deletes to the model. This manager is useful for models that don't change often.

[![Build Status](https://travis-ci.org/vijaykatam/django-cache-manager.svg?branch=master)](https://travis-ci.org/vijaykatam/django-cache-manager)
[![Coverage Status](https://img.shields.io/coveralls/vijaykatam/django-cache-manager.svg)](https://coveralls.io/r/vijaykatam/django-cache-manager)

## Installation

```sh
pip install django-cache-manager
```

### Caching strategy
* Cache results for a model on load.
* Evict cache for model on update.


## Usage

Add to installed apps
```
INSTALLED_APPS = (
    ...
    'django_cache_manager',
    ...
)
```
Define cache backend for `django_cache_manager.cache_backend` in `settings.py`. The backend can be any cache backend 
that implements django cache API.

```
CACHES = {
    'django_cache_manager.cache_backend': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp/django_cache_manager',
        'TIMEOUT': 0
    }
}
```

```
from django_cache_manager.cache_manager import CacheManager
class MyModel(models.Model):
   
   #set cache manager as default
   objects = CacheManager()

```   


## Django shell
To run django shell with sample models defined in tests.
```sh
make shell
```
Sample models
```
from tests.models import Manufacturer
from tests.models import Car
from tests.models import Driver
m = Manufacturer(name='Tesla')
m.save()
c = Car(make=m, model='Model S', year=2015)
c.save()
d = Driver(first_name ='ABC', last_name='XYZ')
d.save()
d.cars.add(c)
drivers = Driver.objects.select_related('car', 'manufacturer').all()
```

## Testing 

To run tests

```sh
make test
```

##### Supported Django versions 
Supported - 1.5, 1.6, 1.7




