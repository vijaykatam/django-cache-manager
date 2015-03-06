# -*- coding: utf-8 -*-

"""
Integration tests for models using CacheManager
"""
import django
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
from django.db import (
    connection,
    reset_queries
)
from django.db.models.sql import EmptyResultSet
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
    PersonFactory,

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
        Number of manufacturers returned by objects should increment after
        creating a new manufacturer
        """
        ManufacturerFactory.create()
        self.assertEqual(
            len(Manufacturer.objects.all()), len(self.manufacturers) + 1)

    def test_update_manufacturer(self):
        """
        Cache manager returns most recently updated record
        even if it has been cached and an update happens after.
        """
        m = self.manufacturers[0]
        self.assertEqual(
            model_to_dict(m), model_to_dict(Manufacturer.objects.get(id=m.id)))
        m.name = 'Toyota'
        m.save()
        self.assertEqual(
            model_to_dict(m), model_to_dict(Manufacturer.objects.get(id=m.id)))

    def test_delete_manufacturer(self):
        """
        When a cached record is deleted Cache manager raises ObjectDoesNotExist when trying to retrieve
        """
        m = self.manufacturers[0]
        self.assertEqual(
            model_to_dict(m), model_to_dict(Manufacturer.objects.get(id=m.id)))
        m.delete()
        with self.assertRaises(ObjectDoesNotExist):
            Manufacturer.objects.get(id=m.id)


@override_settings(DEBUG=True)
class ModelCacheTests(TestCase):
    """
    Test cache hits and misses
    """

    def setUp(self):
        self.manufacturer = ManufacturerFactory.create()
        reset_queries()

    def test_cache_hit(self):
        """
        The query should be cached when making the same query repeatedly.
        """
        for i in range(5):
            len(Manufacturer.objects.all())
        self.assertEqual(len(connection.queries), 1)

    def test_dummy_cache(self):
        """
        There should not be any query caching when cache backend is dummy.
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
                len(Manufacturer.objects.all())
            self.assertEqual(len(connection.queries), 5)

    def test_cache_invalidate_with_bulk_create(self):
        """
        Cache should be invalidated when calling 'bulk_create'
        """
        initial_count = len(Manufacturer.objects.all())
        Manufacturer.objects.bulk_create(
            [Manufacturer(name='m1'), Manufacturer(name='m2')]
        )
        reset_queries()

        new_count = len(Manufacturer.objects.all())
        self.assertEqual(len(connection.queries), 1)
        self.assertEqual(initial_count + 2, new_count)

    def test_cache_invalidate_with_update(self):
        """
        Cache should be invalidated when calling 'update'
        """
        len(Manufacturer.objects.all())
        Manufacturer.objects.all().update(name='new name')
        reset_queries()

        len(Manufacturer.objects.all())
        self.assertEqual(len(connection.queries), 1)


@override_settings(DEBUG=True)
class OneToOneModelCacheTests(TestCase):
    """
    Test cache hits and misses on models with one-to-one relationship
    """

    def setUp(self):
        self.engine = EngineFactory.create(name='test_engine')
        self.car = CarFactory.create(engine=self.engine, year=2015)
        reset_queries()

    def test_one_to_one_mapping_cache(self):
        """
        Queries should be cached when making the same select queries
        on related objects query repeatedly
        """
        for i in range(5):
            Car.objects.get(id=self.car.id).engine.name
        # The above query is actually composed of 2 sql queries:
        # one for fetching cars and the other engines.
        self.assertEqual(len(connection.queries), 2)

    def test_one_to_one_mapping_cache_with_save(self):
        """
        Cache should be invalidated when calling 'save' on related objects
        """
        Car.objects.get(id=self.car.id).engine.name
        self.engine.name = 'new_engine'
        self.engine.save()
        reset_queries()

        # Both car and engine caches will be invalidated due to car being related to engine
        Car.objects.get(id=self.car.id).engine.name
        self.assertEqual(len(connection.queries), 2)

    def test_one_to_one_mapping_cache_with_delete(self):
        """
        Cache should be invalidated when calling 'delete' related objects
        """
        Car.objects.get(id=self.car.id).engine.name
        self.engine.delete()
        reset_queries()

        with self.assertRaises(ObjectDoesNotExist):
            Car.objects.get(id=self.car.id).engine.name


@override_settings(DEBUG=True)
class ManyToOneModelCacheTests(TestCase):
    """
    Test cache hits and misses on models with many-to-one relationship
    """

    def setUp(self):
        self.manufacturer = ManufacturerFactory.create()
        self.car = CarFactory.create(make=self.manufacturer, year=2015)
        reset_queries()

    def test_many_to_one_mapping_cache(self):
        """
        Queries should be cached when making the same select queries
        on related objects repeatedly
        """
        for i in range(5):
            len(Manufacturer.objects.get(id=self.manufacturer.id).cars.all())
        # The above query is actually composed of 2 sql queries:
        # one for fetching the manufacturer and the other cars.
        self.assertEqual(len(connection.queries), 2)

    def test_many_to_one_mapping_cache_with_save(self):
        """
        Cache should be invalidated when calling 'save' on related objects
        """
        car2 = CarFactory.create(make=self.manufacturer)
        len(Manufacturer.objects.get(id=self.manufacturer.id).cars.all())
        car2.name = 'gti'
        car2.save()
        reset_queries()

        # Only 1 cache (the one for car selection query) will be invalidated
        # as we only update data on Car table
        len(Manufacturer.objects.get(id=self.manufacturer.id).cars.all())
        # Because of m2m fix the no. of queries will be 2 instead of 1
        self.assertEqual(len(connection.queries), 2)

    def test_many_to_one_mapping_cache_with_delete(self):
        """
        Cache should be invalidated when calling 'delete' on related objects
        """
        car2 = CarFactory.create(make=self.manufacturer)
        initial_count = len(
            Manufacturer.objects.get(id=self.manufacturer.id).cars.all())
        car2.delete()
        reset_queries()

        # Only 1 cache (the one for car selection query) will be invalidated
        # as we only delete data on Car table
        new_count = len(
            Manufacturer.objects.get(id=self.manufacturer.id).cars.all())
        # Because of m2m fix the no. of queries will be 2 instead of 1
        self.assertEqual(len(connection.queries), 2)
        self.assertEqual(initial_count - 1, new_count)


@override_settings(DEBUG=True)
class SelectRelatedTests(TestCase):
    """
    Tests for select_related
    """

    def setUp(self):
        self.manufacturer = ManufacturerFactory.create(name='Honda')
        self.car = CarFactory.create(make=self.manufacturer, year=2015, model='Civic')
        reset_queries()

    def test_select_related(self):
        """
        Select related query retrieves updated data when related model changes independently.
        """
        civic = Car.objects.select_related('make').get(model='Civic')
        self.assertEquals(civic.make.name, 'Honda')
        self.assertEquals(len(connection.queries), 1)
        honda = Manufacturer.objects.get(name='Honda')
        honda.name = 'Honda Inc'
        honda.save()
        civic = Car.objects.select_related('make').get(model='Civic')
        self.assertEquals(civic.make.name, 'Honda Inc')


@override_settings(DEBUG=True)
class EmptyResultSetTests(TestCase):
    """
    Tests validating behavior when as_sql returns EmptyResultSet.
    """
    def setUp(self):
        self.manufacturer = ManufacturerFactory.create(name='Honda')
        self.car = CarFactory.create(make=self.manufacturer, year=2015, model='Civic')
        reset_queries()

    def test_empty_list_on_filter_in(self):
        """
        A filter call with __in being passed an empty list should correctly
        handle the EmptyResultSet exception and return None.
        """
        self.assertEqual([], list(Car.objects.filter(make__in=[])))
