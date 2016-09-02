#!/usr/bin/env python

import pickledb

"""
Item example:

{'description': ' This is description...',
 'link': 'https://www.this.is.link.html',
 'price': '999',
 'producer': 'Producer',
 'rating': '3.33',
 'title': 'This is title'}
"""


class LiquidBase():
    def __init__(self, base_file):
        self.base = pickledb.load(base_file, False)

    def get_all_items(self):
        return sorted(self.base.db)

    def get_item(self, title):
        return self.base.db[title]

    def add_item(self, item_series):
        items = item_series['items']
        for item in items:
            self.base.dcreate(item['title'])
            for feature in item.items():
                self.base.dadd(item['title'], ('producer', item_series['producer']))
                self.base.dadd(item['title'], feature)
        self.base.dump()

    def search_item(self, word):
        for title in self.base.db:
            item = self.base.dgetall(title)
            for value in item.values():
                if word in value:
                    return item

    def delete_item(self, title):
        self.base.drem(title)
        self.base.dump()

