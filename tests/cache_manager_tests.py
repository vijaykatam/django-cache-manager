# -*- coding: utf-8 -*-

import hashlib
from unittest import TestCase
from mock import patch, Mock


from django_cache_manager.cache_manager import (
    CacheManager,
    CachingQuerySet
)
from django_cache_manager.mixins import CacheKeyMixin
from .models import Manufacturer
from tests.factories import ManufacturerFactory



class CacheManagerTests(TestCase):
    """
    Tests for django_cache_manager.cache_manager.CacheManager
    """

    def setUp(self):
        self.cache_manager = CacheManager()
        self.cache_manager.model = Manufacturer()

    def test_get_query_set(self):
        self.assertTrue(isinstance(self.cache_manager.get_query_set(), CachingQuerySet))

    def test_get_queryset(self):
        self.assertTrue(isinstance(self.cache_manager.get_queryset(), CachingQuerySet))        
        

@patch.object(CachingQuerySet, 'invalidate_model_cache')
@patch.object(CachingQuerySet, 'cache_backend')
@patch.object(CachingQuerySet, 'generate_key')
class CachingQuerySetTests(TestCase):
    """
    Tests for django_cache_manager.cache_manager.CachingQuerySet
    """    

    def setUp(self):
        self.cache_manager = CacheManager()
        self.cache_manager.model = Manufacturer()
        self.query_set = Manufacturer.objects.filter(name='name')
        ManufacturerFactory.create(name='name')

    def test_iterate_cache_hit(self, mock_generate_key, mock_cache_backend, invalidate_model_cache):
        """
        A cache hit will not result in call to the database.
        """
        mock_generate_key.return_value = 'key'
        mock_cache_backend.get.return_value = ['result_1', 'result_2']
        results = list(self.query_set.iterator())
        self.assertEquals(results, ['result_1', 'result_2'])
        self.assertEquals(mock_cache_backend.set.call_count, 0)

    def test_iterate_cache_miss(self, mock_generate_key, mock_cache_backend, invalidate_model_cache):
        """
        A cache miss will result in call to the database.
        """
        mock_generate_key.return_value = 'key'
        mock_cache_backend.get.return_value = None
        results = list(self.query_set.iterator())
        self.assertEquals(results[0].name, 'name')
        self.assertEquals(mock_cache_backend.set.call_count, 1)

    def test_bulk_create(self, mock_generate_key, mock_cache_backend, invalidate_model_cache):
        """
        Bulk create invalidates model cache
        """
        self.cache_manager.bulk_create([
            Manufacturer(name='Toyota'),
            Manufacturer(name='BMW'),
        ])
        self.assertEquals(invalidate_model_cache.call_count, 1)

    def test_update(self, mock_generate_key, mock_cache_backend, invalidate_model_cache):
        """
        Updating several records at once invalidates model cache
        """
        self.query_set.update(name='name')
        self.assertEquals(invalidate_model_cache.call_count, 1)




