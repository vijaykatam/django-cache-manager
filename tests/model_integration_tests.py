# -*- coding: utf-8 -*-

"""
Integration tests for models using CacheManager
Use models defined in tests t

1. Black box tests - input model data,  retrieve, delete, update -assert that right data is retrieved
"""

from django.test import TestCase

from .models import(
    Manufacturer,
    Car,
    Driver
)
from .factories import(
    ManufacturerFactory,
    CarFactory,
    DriverFactory
)

class ManufacturerTests(TestCase):

    def setUp(self):
        ManufacturerFactory.create_batch(size=5)
        Manufacturer.cached_objects.all()

    def test_number_of_objects(self):
        "Number of objects returned by default object manager is same as cached objects manager when a new record is created"
        ManufacturerFactory.create()
        self.assertEquals(len(Manufacturer.objects.all()), len(Manufacturer.cached_objects.all()))

    def test_new_record(self):
        pass
