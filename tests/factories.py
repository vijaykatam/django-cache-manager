# -*- coding: utf-8 -*-

import factory
from factory import fuzzy

from .models import(
    Manufacturer,
    Car,
    Driver
)


class ManufacturerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Manufacturer

    name = fuzzy.FuzzyText()


class CarFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Car

    make = factory.SubFactory(ManufacturerFactory)
    model = fuzzy.FuzzyText()
    year = fuzzy.FuzzyInteger(1980, 2015)


class DriverFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Driver

    first_name = fuzzy.FuzzyText()
    last_name = fuzzy.FuzzyText()
    cars = factory.SubFactory(CarFactory)
