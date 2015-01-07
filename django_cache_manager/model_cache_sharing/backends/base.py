# -*- coding: utf-8 -*-
import abc
from abc import abstractmethod


class BaseSharing(object):
    """
    Base API for sharing model cache info with all the processes.
    """

    __metaclass__ = abc.ABCMeta

    @abstractmethod
    def share_model_cache_info(self, model_cache_info, **kwargs):
        """
        Share model cache info with all processes

        Parameters
        ~~~~~~~~~~
        model_cache_info
            A named tuple of type django_cache_manager.model_cache_sharing.types.ModelCacheInfo
        """

    @abstractmethod
    def retrieve_model_cache_info(self, key, **kwargs):
        """
        Retrieve model cache info for the key.

        Parameters
        ~~~~~~~~~~
        key
            Key for a model, typically the table_name.

        Returns
        ~~~~~~~
        model_cache_info - A named tuple of type django_cache_manager.model_cache_sharing.types.ModelCacheInfo

        """
