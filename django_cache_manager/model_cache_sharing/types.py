# -*- coding: utf-8 -*-

from collections import namedtuple


# Type for cache metadata of a model. Conisits of table_name and table_key
ModelCacheInfo = namedtuple('ModelCacheInfo', ['table_name', 'table_key'])
