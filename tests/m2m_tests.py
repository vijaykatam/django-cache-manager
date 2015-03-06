# -*- coding: utf-8 -*-

"""
Tests for many to many
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
    Person,
    Group,
    Membership
)
from tests.factories import(
    CarFactory,
    DriverFactory,
    EngineFactory,
    ManufacturerFactory,
    PersonFactory,
    GroupFactory,
    MembershipFactory
)


@override_settings(DEBUG=True)
class ManyToManyModelCacheTests(TestCase):
    """
    Test cache hits and misses on models with many-to-many relationship
    """

    def setUp(self):
        self.car = CarFactory.create(year=2015)
        self.driver = DriverFactory.create(cars=[self.car])
        reset_queries()

    def test_many_to_many_mapping_cache(self):
        """
        Queries should be cached when making the same select queries
        on related objects repeatedly
        """
        car2 = CarFactory.create()
        self.driver.cars.add(car2)
        reset_queries()

        for i in range(5):
            Driver.objects.get(id=self.driver.id).cars.all()[0].year
        # The above query is actually composed of 2 sql queries:
        # one for fetching drivers and the other cars.
        self.assertEqual(len(connection.queries), 2)
        # no. of cars for the driver increased by 1
        self.assertEqual(len(self.driver.cars.all()), 2)

    def test_many_to_many_mapping_cache_with_save(self):
        """
        Cache should be invalidated when calling 'save' on related objects
        """
        car2 = CarFactory.create()
        self.driver.cars.add(car2)
        Driver.objects.get(id=self.driver.id).cars.all()[0].year
        car2.name = 'gti'
        car2.save()
        reset_queries()

        # Only 1 cache (the one for car selection query) will be invalidated
        # as we only update data on Car table
        Driver.objects.get(id=self.driver.id).cars.all()[0].year
        self.assertEqual(len(connection.queries), 1)

    def test_many_to_many_mapping_cache_with_delete(self):
        """
        Cache should be invalidated when calling 'delete' on related objects
        """
        car2 = CarFactory.create()
        self.driver.cars.add(car2)
        initial_count = len(Driver.objects.get(id=self.driver.id).cars.all())
        car2.delete()
        reset_queries()

        # Only 1 cache (the one for car selection query) will be invalidated
        # as we only delete data on Car table
        new_count = len(Driver.objects.get(id=self.driver.id).cars.all())
        self.assertEqual(len(connection.queries), 1)
        self.assertEqual(initial_count - 1, new_count)

    def test_many_to_many_mapping_cache_with_add(self):
        """
        Cache for both models in this many-to-many relationship should
        be updated when calling 'add' on related objects
        """
        new_cars = CarFactory.create_batch(size=3)
        initial_count = len(Driver.objects.get(id=self.driver.id).cars.all())
        self.driver.cars.add(*new_cars)
        reset_queries()

        # Cache for both models should be invalidated as add is an m2m change
        new_count = len(Driver.objects.get(id=self.driver.id).cars.all())
        self.assertEqual(len(connection.queries), 2)
        self.assertEqual(initial_count + 3, new_count)

    def test_many_to_many_mapping_cache_with_remove(self):
        """
        Cache for both models in this many-to-many relationship should
        be updated when calling 'remove' on related objects
        """
        new_car = CarFactory.create()
        self.driver.cars.add(new_car)
        Driver.objects.get(id=self.driver.id).cars.all()[0].year
        number_of_cars = len(self.driver.cars.all())
        self.driver.cars.remove(self.car)
        reset_queries()

        # Cache for both models should be invalidated as remove is an m2m change
        Driver.objects.get(id=self.driver.id).cars.all()[0].year
        self.assertEqual(len(connection.queries), 2)
        # number of cars decreases by 1
        self.assertEqual(len(self.driver.cars.all()), number_of_cars - 1)

    def test_many_to_many_mapping_cache_with_clear(self):
        """
        Cache for both models in this many-to-many relationship should
        be updated when calling 'clear' on related objects
        """
        len(Driver.objects.get(id=self.driver.id).cars.all())
        self.driver.cars.clear()
        reset_queries()

        # Cache for both models should be invalidated as clear is an m2m change
        self.assertEqual(len(Driver.objects.get(id=self.driver.id).cars.all()), 0)
        self.assertEqual(len(connection.queries), 2)


class ManyToManyModelThroughTests(TestCase):
    """
    Test cache eviction for m2m relation with a through model
    """

    def setUp(self):
        self.person = PersonFactory.create()
        self.group = GroupFactory.create()
        self.membership = MembershipFactory(person=self.person, group=self.group).save()

    def test_m2m_add_person(self):
        person2 = PersonFactory.create()
        g = Group.objects.get(id=self.group.id)
        self.assertEqual(len(g.members.all()), 1)
        MembershipFactory(person=person2, group=self.group).save()
        self.assertEqual(len(g.members.all()), 2)

    def test_m2m_add_group(self):
        group2 = GroupFactory.create()
        p = Person.objects.get(id=self.person.id)
        self.assertEqual(len(p.groups.all()), 1)
        MembershipFactory(person=self.person, group=group2).save()
        self.assertEqual(len(p.groups.all()), 2)

