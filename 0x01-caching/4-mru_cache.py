#!/usr/bin/env python3
'''
This script defines class MRUCache that
inherits from BaseCaching and is a caching system
'''

from typing import OrderedDict


BaseCaching = __import__('base_caching').BaseCaching


class MRUCache(BaseCaching):
    '''Defines the MRUCache class'''
    def __init__(self):
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        '''Adds item to self.cache_data dict'''
        if key is None or item is None:
            return

        if key in self.cache_data.keys():
            self.cache_data.move_to_end(key)
            self.cache_data[key] = item
            return

        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            discarded_key, _ = self.cache_data.popitem(last=True)
            print(f'DISCARD:', discarded_key)

        self.cache_data[key] = item

    def get(self, key):
        '''Returns value assigned to key'''
        if key is None or key not in self.cache_data:
            return None

        self.cache_data.move_to_end(key)
        return self.cache_data.get(key)
