# -*- coding: utf-8 -*-
import logging
import uuid

from django.db.models.signals import post_save, post_delete, m2m_changed

from .model_cache_sharing.types import ModelCacheInfo
from .model_cache_sharing import model_cache_backend

"""
Signal receivers for django model post_save and post_delete. Used to evict a model cache when
an update or delete happens on the model.
For compatibility with Django 1.5 these receivers live in models.py
"""

logger = logging.getLogger(__name__)


def _update_model_cache(table_name):
    """
    Updates model cache by generating a new key for the model
    """
    model_cache_info = ModelCacheInfo(table_name, uuid.uuid4().hex)
    model_cache_backend.share_model_cache_info(model_cache_info)


def invalidate_model_cache(sender, instance, **kwargs):
    """
    Signal receiver for models to invalidate model cache of sender and related models.
    Model cache is invalidated by generating new key for each model.

    Parameters
    ~~~~~~~~~~
    sender
        The model class
    instance
        The actual instance being saved.
    """
    logger.debug('Received post_save/post_delete signal from sender {0}'.format(sender))
    related_models = [rel.model for rel in sender._meta.get_all_related_objects()]
    logger.debug('Related models of sender {0}'.format(related_models))
    _update_model_cache(sender._meta.db_table)
    for related_model in related_models:
        _update_model_cache(related_model._meta.db_table)

def invalidate_m2m_cache(sender, instance, model, **kwargs):
    """
    Signal receiver for models to invalidate model cache for many-to-many relationship.

    Parameters
    ~~~~~~~~~~
    sender
        The model class
    instance
        The instance whose many-to-many relation is updated.
    model
        The class of the objects that are added to, removed from or cleared from the relation.
    """
    logger.debug('Received m2m_changed signals from sender {0}'.format(sender))
    _update_model_cache(instance._meta.db_table)
    _update_model_cache(model._meta.db_table)


post_save.connect(invalidate_model_cache)
post_delete.connect(invalidate_model_cache)
m2m_changed.connect(invalidate_m2m_cache)
