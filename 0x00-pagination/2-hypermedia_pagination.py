#!/usr/bin/env python3
'''
This script builds upon 1-simple_pagination.py
'''

import csv
import math
from typing import Dict, List, Tuple


def index_range(page: int, page_size: int) -> Tuple:
    '''
    Returns a tuple of size two
    '''
    end_index = page * page_size
    start_index = end_index - page_size

    return tuple((start_index, end_index))


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        start_index, end_index = index_range(page, page_size)
        data = self.dataset()

        if start_index > len(data):
            return []

        return data[start_index:end_index]

    def get_hyper(self,  page: int = 1, page_size: int = 10) -> Dict:
        pagination = {}

        pagination['page_size'] = page_size
        pagination['page'] = page
        pagination['data'] = self.get_page(page, page_size)
        total_pages = len(self.dataset()) / page_size

        if page == math.ceil(total_pages):
            pagination['next_page'] = None
        else:
            pagination['next_page'] = page + 1

        if page == 1:
            pagination['prev_page'] = None
        else:
            pagination['prev_page'] = page - 1

        pagination['total_pages'] = math.ceil(total_pages)
        return pagination
