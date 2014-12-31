# -*- coding: utf-8 -*-

from unittest import TestCase
from mock import patch
# from django.test import TestCase
from django_cache_manager.mixins import CacheKeyMixin
from .models import Manufacturer


@patch.object(CacheKeyMixin, 'sql')
class CacheKeyMixinTests(TestCase):

    def setUp(self):
        self.mixin = CacheKeyMixin()
        self.mixin.model = Manufacturer()
        self.mixin.db = 'db'

    def test_generate_key(self, mock_sql):
        "Mixin generates identical keys when sql and model are the same"
        mock_sql.return_value = 'sql'
        key1 = self.mixin.generate_key()
        key2 = self.mixin.generate_key()
        self.assertEquals(key1, key2)
