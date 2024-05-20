#!/usr/bin/env python3
'''
This function returns a tuple of size two containing a
start index and an end index corresponding to the range
of indexes
'''


from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple:
    '''
    Returns a tuple of size two
    '''
    end_index = page * page_size
    start_index = end_index - page_size

    return tuple((start_index, end_index))
