# -*- coding: utf-8 -*-

from django.db import models
from django_cache_manager.cache_manager import CacheManager


class Manufacturer(models.Model):
    name = models.CharField(max_length=128)
    objects = CacheManager()


class Car(models.Model):
    make = models.ForeignKey(Manufacturer, related_name='cars')
    model = models.CharField(max_length=128)
    year = models.IntegerField()
    objects = CacheManager()


class Driver(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    cars = models.ManyToManyField(Car)
    objects = CacheManager()

"""
from tests.models import Manufacturer
from tests.models import Car
from tests.models import Driver
m = Manufacturer(name='bmw')
m.save()
c = Car(make=m, model='328 ixDrive', year=2014)
c.save()
d = Driver(first_name ='vijay', last_name='katam')
d.save()
d.cars.add(c)
drivers = Driver.objects.select_related('car', 'manufacturer').all()


"""