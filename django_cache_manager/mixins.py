# -*- coding: utf-8 -*-
import hashlib
import logging
import uuid

from django.core.cache import get_cache
from django.conf import settings

from .model_cache_sharing.types import ModelCacheInfo
from .model_cache_sharing import model_cache_backend

_cache_name = getattr(settings, 'django_cache_manager.cache_backend', 'django_cache_manager.cache_backend')
logger = logging.getLogger(__name__)


class CacheKeyMixin(object):

    def generate_key(self):
        """
        Generate cache key for the current query. If a new key is created for the model it is
        then shared with other consumers.
        """
        sql = self.sql()
        key, created = self.get_or_create_model_key()
        if created:
            db_table = self.model._meta.db_table
            logger.debug('created new key {0} for model {1}'.format(key, db_table))
            model_cache_info = ModelCacheInfo(db_table, key)
            model_cache_backend.share_model_cache_info(model_cache_info)
        query_key = u'{model_key}{qs}{db}'.format(model_key=key,
                                                  qs=sql,
                                                  db=self.db)
        key = hashlib.md5(query_key).hexdigest()
        return key

    def sql(self):
        """
        Get sql for the current query.
        """
        clone = self.query.clone()
        sql, params = clone.get_compiler(using=self.db).as_sql()
        return sql % params

    def get_or_create_model_key(self):
        """
        Get or create key for the model.

        Returns
        ~~~~~~~
        (model_key, boolean) tuple

        """
        model_cache_info = model_cache_backend.retrieve_model_cache_info(self.model._meta.db_table)
        if not model_cache_info:
            return uuid.uuid4().hex, True
        return model_cache_info.table_key, False


class CacheInvalidateMixin(object):

    def invalidate_model_cache(self):
        """
        Invalidate model cache by generating new key for the model.
        """
        logger.info('Invalidating cache for table {0}'.format(self.model._meta.db_table))
        model_cache_info = ModelCacheInfo(self.model._meta.db_table, uuid.uuid4().hex)
        model_cache_backend.share_model_cache_info(model_cache_info)


class CacheBackendMixin(object):

    # TODO - django 1.7 has thread safe module level cache interface
    @property
    def cache_backend(self):
        """
        Get the cache backend

        Returns
        ~~~~~~~
        Django cache backend

        """
        if not hasattr(self, '_cache_backend'):
            self._cache_backend = get_cache(_cache_name)
        return self._cache_backend
