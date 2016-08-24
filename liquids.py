#!/usr/bin/env python

import pickledb


class LiquidBase():
    def __init__(self, base_file):
        self.base = pickledb.load(base_file, False)

    def load_item_series(self, producer):
        return self.base.db[producer]

    def add_item_series(self, item_series):
        producer = item_series['producer']
        items = item_series['items']
        self.base.dcreate(producer)
        self.base.dadd(producer, tuple(items))

    def search(self, word):
        producers = self.base.db.keys()
        for producer in producers:
            if word in producer:
                return self.load_item_series(producer)
