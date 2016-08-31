#!/usr/bin/env python

import pickledb


class LiquidBase():
    def __init__(self, base_file):
        self.base = pickledb.load(base_file, False)

    def load_item_series(self, producer):
        return self.base.db[producer]

    def add_item_series(self, item_series):
        #producer = item_series['producer']
        items = item_series['items']
        for item in items:
            self.base.dcreate(item['title'])
            for feature in item.items():
                self.base.dadd(item['title'], feature)
                self.base.dadd(item['title'], ('producer', item_series['producer']))
        self.base.dump()

    def search(self, word):
        producers = self.base.db.keys()
        for producer in producers:
            if word in producer:
                return self.load_item_series(producer)
