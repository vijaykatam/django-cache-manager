# -*- coding: utf-8 -*-

"""
Integration tests for models using CacheManager
Use models defined in tests t

1. Black box tests - input model data,  retrieve, delete, update -assert that right data is retrieved
"""
import django
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
from django.db import (
    connection,
    reset_queries
)
from django.test import TestCase
if django.get_version() > '1.7':
    from django.test import override_settings
else:
    from django.test.utils import override_settings

from tests.models import(
    Car,
    Driver,
    Engine,
    Manufacturer,
)
from tests.factories import(
    CarFactory,
    DriverFactory,
    EngineFactory,
    ManufacturerFactory,
)


class ModelCRUDTests(TestCase):
    """
    Create, read, update and delete tests
    """

    def setUp(self):
        self.manufacturers = ManufacturerFactory.create_batch(size=5)
        self.cars = CarFactory.create_batch(size=5, make=self.manufacturers[0])
        self.drivers = DriverFactory.create_batch(size=5, cars=[self.cars[0]])

    def test_create_new_manufacturer(self):
        """
        Number of manufacturers returned by cached_objects is same as regular objects when a new manufacturer is created.
        """
        self.assertEquals(len(self.manufacturers), len(Manufacturer.cached_objects.all()))
        ManufacturerFactory.create()
        self.assertEquals(len(Manufacturer.objects.all()), len(Manufacturer.objects.all()))

    def test_update_manufacturer(self):
        """
        Cache manager returns most recently updated record even if it has been cached and an update happens after.
        """        
        m = self.manufacturers[0]
        self.assertEquals(model_to_dict(m), model_to_dict(Manufacturer.cached_objects.get(id=m.id)))
        m.name = 'Toyota'
        m.save()
        self.assertEquals(model_to_dict(m), model_to_dict(Manufacturer.cached_objects.get(id=m.id)))

    def test_delete_manufacturer(self):
        """
        When a cached record is deleted Cache manager raises ObjectDoesNotExist when trying to retrieve
        """        
        m = self.manufacturers[0]
        self.assertEquals(model_to_dict(m), model_to_dict(Manufacturer.cached_objects.get(id=m.id)))
        m.delete()
        with self.assertRaises(ObjectDoesNotExist):
            Manufacturer.cached_objects.get(id=m.id)


class ModelCacheTests(TestCase):
    """
    Test cache hits and misses
    """

    def setUp(self):
        self.manufacturers = ManufacturerFactory.create_batch(size=5)
        reset_queries()

    @override_settings(DEBUG=True)
    def test_cache_hit(self):
        """
        Number of sql queries should be 1 when making the same query repeatedly.
        """
        for i in range(5):
            len(Manufacturer.cached_objects.all())
        self.assertEquals(1, len(connection.queries))

    
    def test_dummy_cache(self):
        """
        Number of sql queries is equal to the number of manager accesses when cache backend is dummy.
        """        
        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
            },
            'django_cache_manager.cache_backend': {
                'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
            }
        }       
        with override_settings(DEBUG=True, CACHES=CACHES):
            for i in range(5):
                len(Manufacturer.cached_objects.all())
            self.assertEquals(5, len(connection.queries))



#TODO Add tests for bulk create and update

