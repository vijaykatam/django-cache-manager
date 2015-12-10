# -*- coding: utf-8 -*-
import hashlib
import logging
import uuid

import django

if django.get_version() >= '1.7':
    from django.core.cache import caches
else:
    from django.core.cache import get_cache

from django.conf import settings
from django.db.models.fields.related import RelatedField

from .model_cache_sharing.types import ModelCacheInfo
from .model_cache_sharing import model_cache_backend
from .models import update_model_cache


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
        key = hashlib.md5(query_key.encode('utf-8')).hexdigest()
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
        related_tables = set([rel.model._meta.db_table for rel in self.model._meta.get_all_related_objects()])
        # temporary fix for m2m relations with an intermediate model, goes away after better join caching
        related_tables |= set([field.rel.to._meta.db_table for field in self.model._meta.fields if issubclass(type(field), RelatedField)])
        logger.debug('Related tables of model {0} are {1}'.format(self.model, related_tables))
        update_model_cache(self.model._meta.db_table)
        for related_table in related_tables:
            update_model_cache(related_table)


class CacheBackendMixin(object):

    @property
    def cache_backend(self):
        """
        Get the cache backend

        Returns
        ~~~~~~~
        Django cache backend

        """
        if not hasattr(self, '_cache_backend'):
            # determine django version for getting cache backend
            if django.get_version() >= '1.7':
                self._cache_backend = caches[_cache_name]
            else:
                self._cache_backend = get_cache(_cache_name)
        return self._cache_backend
