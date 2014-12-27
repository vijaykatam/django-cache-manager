# -*- coding: utf-8 -*-
import hashlib
import logging
import uuid

from django.core.cache import get_cache
from django.conf import settings

from .backends.sharing.types import ModelCacheInfo
from .backends.sharing import sharing_backend

_cache_name = getattr(settings, 'django_cache_manager.cache_backend', 'django_cache_manager.cache_backend')
logger = logging.getLogger(__name__)


class CacheKeyMixin(object):

    def generate_key(self):
        sql = self.sql()
        query_key = u'{table_key}{qs}{db}'.format(table_key=self.table_key(),
                                                  qs=sql,
                                                  db=self.db)
        key = hashlib.md5(query_key).hexdigest()
        logger.debug('generated key {0} for sql {1}'.format(key, sql))
        return key

    def sql(self):
        clone = self.query.clone()
        sql, params = clone.get_compiler(using=self.db).as_sql()
        return sql % params

    def table_key(self):
        table_name = self.model._meta.db_table
        model_cache_info = sharing_backend.retrieve_model_cache_info(table_name)
        if not model_cache_info:
            key = uuid.uuid4().hex
            model_cache_info = ModelCacheInfo(table_name, key)
            sharing_backend.broadcast_model_cache_info(model_cache_info)
        return model_cache_info.table_key


class CacheInvalidateMixin(object):

    def invalidate(self):
        "Invalidate cache for the model by generating a new key"
        logger.info('Invalidating cache for table {0}'.format(self.model._meta.db_table))
        model_cache_info = ModelCacheInfo(self.model._meta.db_table, uuid.uuid4().hex)
        sharing_backend.broadcast_model_cache_info(model_cache_info)


class CacheBackendMixin(object):

    # TODO - django 1.7 has thread safe module level cache interface

    @property
    def cache_backend(self):
        if not hasattr(self, '_cache_backend'):
            self._cache_backend = get_cache(_cache_name)
        return self._cache_backend
