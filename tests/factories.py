# -*- coding: utf-8 -*-

import datetime
import factory
from factory import fuzzy

from tests.models import(
    Manufacturer,
    Car,
    Driver,
    Engine,
    Person,
    Group,
    Membership
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
    engine = factory.SubFactory('tests.factories.EngineFactory')


class DriverFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Driver

    first_name = fuzzy.FuzzyText()
    last_name = fuzzy.FuzzyText()

    @factory.post_generation
    def cars(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for car in extracted:
                self.cars.add(car)


class EngineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Engine

    name = fuzzy.FuzzyText()
    horse_power = fuzzy.FuzzyInteger(50, 3000)
    torque = fuzzy.FuzzyText()


class PersonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Person

    name = fuzzy.FuzzyText()


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    name = fuzzy.FuzzyText()


class MembershipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Membership

    person = factory.SubFactory(PersonFactory)
    group = factory.SubFactory(GroupFactory)
    date_joined = fuzzy.FuzzyDate(datetime.date(2013, 1, 1))
    invite_reason = fuzzy.FuzzyText()

