# -*- coding: utf-8 -*-

from unittest import TestCase

from mock import MagicMock

from django_cache_manager.model_cache_sharing import model_cache_backend

class SharedMemoryTests(TestCase):
    """
    Tests for django_cache_manager.model_cache_sharing.backends.shared_memory.SharedMemory
    """

    def setUp(self):
        self.shared_memory = model_cache_backend

    def test_cache_backend(self):
        """
        The attribute '_cache_backend' should be created when accessing
        shared_memory.cache_backend
        """
        self.assertFalse(hasattr(self.shared_memory, '_cache_backend'))
        self.shared_memory.cache_backend
        self.assertTrue(hasattr(self.shared_memory, '_cache_backend'))

    # def test_share_model_cache_info_with_new_model(self):
    #     cache_model_info = MagicMock()
    #     cache_model_info.table_name = 'the table'
    #     self.shared_memory.share_model_cache_info(cache_model_info)

