# -*- coding: utf-8 -*-

"""
Integration tests for models using CacheManager
Use models defined in tests t

1. Black box tests - input model data,  retrieve, delete, update -assert that right data is retrieved
"""
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

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


class ModelIntegrationTests(TestCase):

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
        m = self.manufacturers[0]
        self.assertEquals(model_to_dict(m), model_to_dict(Manufacturer.cached_objects.get(id=m.id)))
        m.name = 'Toyota'
        m.save()
        self.assertEquals(model_to_dict(m), model_to_dict(Manufacturer.cached_objects.get(id=m.id)))

    def test_delete_manufacturer(self):
        m = self.manufacturers[0]
        self.assertEquals(model_to_dict(m), model_to_dict(Manufacturer.cached_objects.get(id=m.id)))
        m.delete()
        with self.assertRaises(ObjectDoesNotExist):
            Manufacturer.cached_objects.get(id=m.id)

    """
    Add tests for bulk create and update
    """
