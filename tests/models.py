# -*- coding: utf-8 -*-

"""
Models with CacheManager as model manager to be used for CacheManager integration tests
"""
from django.db import models

from django_cache_manager.cache_manager import CacheManager


class Manufacturer(models.Model):
    name = models.CharField(max_length=128)

    objects = CacheManager()


class Car(models.Model):
    make = models.ForeignKey('Manufacturer', related_name='cars')
    model = models.CharField(max_length=128)
    year = models.IntegerField()
    engine = models.OneToOneField('Engine')

    objects = CacheManager()


class Driver(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    cars = models.ManyToManyField('Car')

    objects = CacheManager()


class Engine(models.Model):
    name = models.CharField(max_length=128)
    horse_power = models.IntegerField()
    torque = models.CharField(max_length=128)

    objects = CacheManager()


class Person(models.Model):
    name = models.CharField(max_length=128)

    objects = CacheManager()


class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through='Membership', related_name='groups')

    objects = CacheManager()


class Membership(models.Model):
    person = models.ForeignKey(Person)
    group = models.ForeignKey(Group)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)

    objects = CacheManager()

