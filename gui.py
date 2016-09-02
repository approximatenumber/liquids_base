#!/usr/bin/env python

import sys
from PyQt4.QtGui import QApplication, QTableWidget, QTableWidgetItem, QLabel
from liquids import LiquidBase


def create_table(base, items):
    table = QTableWidget()
    table_item = QTableWidgetItem()
    table.setWindowTitle("Liquids Base")
    table.resize(400, 250)
    r_count = len(items)
    c_count = 5
    table.setRowCount(r_count)
    table.setColumnCount(c_count)
    row = 0
    column = 0
    for title in items:
        item = base.get_item(title)
        table.setItem(row, 0, QTableWidgetItem(item['producer']))
        table.setItem(row, 1, QTableWidgetItem(item['title']))
        table.setItem(row, 2, QTableWidgetItem(item['price']))
        table.setItem(row, 3, QTableWidgetItem(item['rating']))
        table.setItem(row, 4, QTableWidgetItem(item['description']))
        row += 1
    return table


def main_window():
    app = QApplication(sys.argv)

    base = LiquidBase('liquid_base.json')
    all_items = base.get_all_items()

    table = create_table(base, all_items)
    table.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main_window()
