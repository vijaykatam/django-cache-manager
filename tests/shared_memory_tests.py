# -*- coding: utf-8 -*-

from unittest import TestCase

from django_cache_manager.model_cache_sharing import model_cache_backend
from django_cache_manager.model_cache_sharing.types import ModelCacheInfo

class SharedMemoryTests(TestCase):
    """
    Tests for django_cache_manager.model_cache_sharing.backends.shared_memory.SharedMemory
    """

    def setUp(self):
        self.shared_memory = model_cache_backend
        self.cache_model_info = ModelCacheInfo('table1', 'key1')
        self.shared_memory.share_model_cache_info(self.cache_model_info)

    def test_cache_backend(self):
        """
        The attribute '_cache_backend' should be created when accessing
        shared_memory.cache_backend
        """
        if hasattr(self.shared_memory, '_cache_backend'):
            del self.shared_memory._cache_backend
        self.shared_memory.cache_backend
        self.assertTrue(hasattr(self.shared_memory, '_cache_backend'))

    def test_share_model_cache_info_with_new_model(self):
        """
        New model should be added into cache when calling 'share_model_cache_info'
        """
        cached_model = self.shared_memory._cache_backend.get(
            self.cache_model_info.table_name, None
        )
        self.assertEqual(cached_model, self.cache_model_info)

    def test_share_model_cache_info_with_model_update(self):
        """
        Cached model should be updated when calling 'share_model_cache_info'
        """
        # Add a new model info with the same table name
        cache_model_info = ModelCacheInfo(
            self.cache_model_info.table_name, 'key2'
        )
        self.shared_memory.share_model_cache_info(cache_model_info)

        cached_model = self.shared_memory._cache_backend.get('table1', None)
        self.assertEqual(cached_model, cache_model_info)

    def test_retrieve_model_cache_info(self):
        """
        Cached model should be returned when calling 'retrieve_model_cache_info'
        with an existing table name
        """
        cached_model = self.shared_memory.retrieve_model_cache_info(
            self.cache_model_info.table_name
        )
        self.assertEqual(cached_model, self.cache_model_info)

    def test_retrieve_model_cache_info_with_nonexistent_model_cache(self):
        """
        None should be returned when calling 'retrieve_model_cache_info'
        with a nonexistent table name
        """
        cached_model = self.shared_memory.retrieve_model_cache_info(
            'secret_table_name_>O<'
        )
        self.assertEqual(cached_model, None)

