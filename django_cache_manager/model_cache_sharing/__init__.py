# -*- coding: utf-8 -*-

"""
Module has backends for sharing model cache info with all django processes.
"""

from .backends.shared_memory import SharedMemory

model_cache_backend = SharedMemory()
