#!/usr/bin/env python3
'''
This script defines class LIFOCache that
inherits from BaseCaching and is a caching system
'''

BaseCaching = __import__('base_caching').BaseCaching


class LIFOCache(BaseCaching):
    def __init__(self):
        super().__init__()

    def put(self, key, item):
        if key is None or item is None:
            return

        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:

            if key in self.cache_data.keys():
                self.cache_data[key] = item
                return

            discarded_item = self.cache_data.popitem()
            print('DISCARD:', discarded_item[0])

        self.cache_data[key] = item

    def get(self, key):
        if key is None:
            return None

        return self.cache_data.get(key)
