# -*- coding: utf-8 -*-

"""
Models with CacheManager as model manager to be used for CacheManager integration tests
"""
from django.db import models

from django_cache_manager.cache_manager import CacheManager


class Manufacturer(models.Model):
    name = models.CharField(max_length=128)

    objects = models.Manager()
    cached_objects = CacheManager()


class Car(models.Model):
    make = models.ForeignKey('Manufacturer', related_name='cars')
    model = models.CharField(max_length=128)
    year = models.IntegerField()
    engine = models.OneToOneField('Engine')

    objects = models.Manager()
    cached_objects = CacheManager()


class Driver(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    cars = models.ManyToManyField('Car')

    objects = models.Manager()
    cached_objects = CacheManager()


class Engine(models.Model):
    name = models.CharField(max_length=128)
    horse_power = models.IntegerField()
    torque = models.CharField(max_length=128)

    objects = models.Manager()
    cached_objects = CacheManager()
