# -*- coding: utf-8 -*-
import logging
import uuid

from django.db.models.signals import post_save, post_delete

from .backends.sharing.types import ModelCacheInfo
from .backends.sharing import sharing_backend
from .cache_manager import CacheManager

"""
Signal receivers for django model post_save and post_delete. Used to evict a model cache when
a model does not use manager provide by django-cache-manager.
For Django 1.5 these receivers live in models.py
"""

logger = logging.getLogger(__name__)


def _invalidate(sender, instance, **kwargs):
    "Signal receiver for models"
    logger.debug('Received post_save/post_delete signal from sender {0}'.format(sender))
    if type(sender.objects) == CacheManager:
        logger.info('Ignoring post_save/post_delete signal from sender {0} as model manager is CachingManager'.format(sender))
        return
    model_cache_info = ModelCacheInfo(sender._meta.db_table, uuid.uuid4().hex)
    sharing_backend.broadcast_model_cache_info(model_cache_info)

post_save.connect(_invalidate)
post_delete.connect(_invalidate)
