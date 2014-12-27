# -*- coding: utf-8 -*-

from django.db import models
from django.db.models.query import QuerySet

from .mixins import (
    CacheBackendMixin,
    CacheInvalidateMixin,
    CacheKeyMixin,
)


class CacheManager(models.Manager, CacheInvalidateMixin):

    # use this manager when accessing objects that are related to from some other model
    use_for_related_fields = True

    def get_query_set(self):
        return CachingQuerySet(self.model, using=self._db)

    # used by save for force_insert or when record does not exist
    def _insert(self, objs, fields, **kwargs):
        self.invalidate()
        return super(CacheManager, self)._insert(objs, fields, **kwargs)


class CachingQuerySet(QuerySet, CacheBackendMixin, CacheKeyMixin, CacheInvalidateMixin):

    def iterator(self):
        key = self.generate_key()
        result_set = self.cache_backend.get(key)
        if not result_set:
            result_set = list(super(CachingQuerySet, self).iterator())
            self.cache_backend.set(key, result_set)
        for result in result_set:
            yield result

    def get_or_create(self, **kwargs):
        self.invalidate()
        return super(CachingQuerySet, self).get_or_create(**kwargs)

    def create(self, **kwargs):
        self.invalidate()
        return super(CachingQuerySet, self).create(**kwargs)

    def bulk_create(self, *args, **kwargs):
        self.invalidate()
        return super(CachingQuerySet, self).bulk_create(*args, **kwargs)

    def delete(self):
        self.invalidate()
        return super(CachingQuerySet, self).delete()

    def update(self, **kwargs):
        self.invalidate()
        return super(CachingQuerySet, self).update(**kwargs)

    # used by save
    def _update(self, values):
        self.invalidate()
        return super(CachingQuerySet, self)._update(values)
