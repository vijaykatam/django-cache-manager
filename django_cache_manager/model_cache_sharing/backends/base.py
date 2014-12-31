# -*- coding: utf-8 -*-
import abc
from abc import abstractmethod


class BaseSharing(object):
    "Share cache info with all the processes"

    __metaclass__ = abc.ABCMeta

    @abstractmethod
    def broadcast_model_cache_info(self, model_cache_info, **kwargs):
        "Share model cache info with all processes"

    @abstractmethod
    def retrieve_model_cache_info(self, key, **kwargs):
        "Return model cache info for key"
