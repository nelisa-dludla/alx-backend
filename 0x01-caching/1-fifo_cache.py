#!/usr/bin/env python3
'''
This script defines class FIFOCache that
inherits from BaseCaching and is a caching system
'''

BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    def __init__(self):
        super().__init__()

    def put(self, key, item):
        if key is None or item is None:
            return

        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            discarded_key = next(iter(self.cache_data))

            if key in self.cache_data.keys():
                self.cache_data[key] = item
                return

            self.cache_data.pop(discarded_key)
            print('DISCARDED:', discarded_key)

        self.cache_data[key] = item

    def get(self, key):
        if key is None:
            return None

        return self.cache_data.get(key)
