# -*- coding: utf-8 -*-
from .base import BaseSharing


class InterProcessCommunication(BaseSharing):
    """Share cache info by communicating.
    Some ideas:
    1. Cache info is broadcast to all processes. Processes recieve and ack.
    2. Processes ask for cache info periodically. This should mitigate any dropped broadcasts. Processes arrive to consensus based on voting or some other mechanism.
    3. 

    """

    def broadcast_model_cache_info(self, model_cache_info, **kwargs):
        pass

    def retrieve_model_cache_info(self, key, **kwargs):
        pass
