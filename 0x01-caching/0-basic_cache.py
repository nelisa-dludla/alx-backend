#!/usr/bin/env python3
'''
This script defines class BasicCache that
inherits from BaseCaching and is a caching system
'''

BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    '''
    This is the BasicCache class
    '''
    def __init__(self):
        super().__init__()

    def put(self, key, item):
        if key is None or item is None:
            return

        self.cache_data[key] = item

    def get(self, key):
        if key is None:
            return None

        return self.cache_data.get(key)
