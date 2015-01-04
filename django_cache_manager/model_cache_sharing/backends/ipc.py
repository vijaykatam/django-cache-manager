# -*- coding: utf-8 -*-
from .base import BaseSharing


class InterProcessCommunication(BaseSharing):
    """Share cache info by communicating.
    Some ideas:
    1. Cache info is broadcast to all processes. Processes recieve and ack.
    2. Processes ask for cache info periodically. This should mitigate any dropped broadcasts. Processes arrive to consensus by implementing a consensus algorithm.
    3. 
    """

    def share_model_cache_info(self, model_cache_info, **kwargs):
        raise NotImplementedError()

    def retrieve_model_cache_info(self, key, **kwargs):
        raise NotImplementedError()
