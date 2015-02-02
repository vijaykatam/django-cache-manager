django-cache-manager
====================

Simple cache manager for django models that caches querysets for a model. Cache manager will cache any query that has been seen for a model. Model cache is evicted for any updates/deletes to the model. This manager is useful for models that don't change often.

Installation
------------

Install django-cache-manager by running::

    pip install django-cache-manager

Usage
------

Add to installed apps::

	INSTALLED_APPS = (
	    'django_cache_manager',
	)

Define cache backend for `django_cache_manager.cache_backend` in `settings.py`. The backend can be any cache backend 
that implements django cache API::

	CACHES = {
	    'django_cache_manager.cache_backend': {
	            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
	            'LOCATION': '/tmp/django_cache_manager',
	            'TIMEOUT': 0
	    }
	}

In your models::

    from django_cache_manager.cache_manager import CacheManager
    class MyModel(models.Model):
        #set cache manager as default
        objects = CacheManager()

Caching strategy
----------------

- Cache results for a model on load.
- Evict cache for model on update.

Contribute
----------

- Issue Tracker: https://github.com/vijaykatam/django-cache-manager/issues
- Source Code: https://github.com/vijaykatam/django-cache-manager

