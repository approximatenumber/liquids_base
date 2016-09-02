#!/usr/bin/env python

from urllib.request import urlopen, Request
from urllib.parse import quote
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import re
import pickledb
from liquids import LiquidBase


def soup_page(url):
    browser.get(url)
    sleep(5)
    soup = BeautifulSoup(browser.page_source, "html.parser")
    return soup


def get_producers(soup):
    producers_links = soup.findAll('div', {'id': 'sidebar-section'})[0].findAll('a')
    producers = []
    for producer_link in producers_links:
        producer = {"producer": producer_link.get('title'),
                    "link": 'https:'+producer_link.get('href')}
        producers.append(producer)
    return producers


def get_items_of_producer(u):
    page_num = 1
    items = []
    while True:
        soup = soup_page(u + "?PAGEN_1=" + str(page_num))
        order_links = soup.findAll('a', {'class': 'item_title'})
        prices = soup.findAll('span', {'class': 'min-offer-price'})
        descriptions = soup.findAll('div', {'itemprop': 'description'})
        ratings = soup.findAll('span', {'class': 'ratingValue'})
        for order_link, price, description, rating in zip(order_links, prices, descriptions, ratings):
            item = {"title": order_link.get('title'),
                    "link": 'https:' + order_link.get('href'),
                    "price": ''.join(re.findall('[0-9]+', price.getText())),
                    "description": description.getText(),
                    "rating": rating.getText()
                    }
        if item in items:
            break
        else:
            items.append(item)
            page_num += 1
            sleep(5)
    return items


def create_report(db_file):

    def create_html(base, html_db):
        from jinja2 import Environment, FileSystemLoader
        import pdfkit
        html_items = []
        for item in sorted(base.db):
            html_items.append({
                'producer': base.dget(item, 'producer'),
                'description': base.dget(item, 'description'),
                'title': base.dget(item, 'title'),
                'rating': base.dget(item, 'rating'),
                'price': base.dget(item, 'price'),
                'link': base.dget(item, 'link')
            })
        env = Environment(loader=FileSystemLoader('template'))
        template = env.get_template('template.html')
        parsed_report = template.render(items=html_items)
        with open(html_db, 'wt') as html:
            html.write(parsed_report)

    def create_csv(base, csv_db):
        import csv
        with open(csv_db, 'w', newline='') as fp:
            csv_file = csv.writer(fp, delimiter=',')
            data = []
            for item in sorted(base.db):
                data.append(
                    [base.dget(item, 'producer'),
                     base.dget(item, 'title'),
                     base.dget(item, 'rating'),
                     base.dget(item, 'price'),
                     base.dget(item, 'description')]
                 )
            csv_file.writerows(data)

    base = pickledb.load(db_file, False)
    # create_html(base, 'liquids.html')
    create_csv(base, 'liquids.csv')


START_PAGE = 'https://www.vardex.ru/e-juice.html'
json_db = 'liquid_base.json'

browser = webdriver.Firefox()
catalog = []
producers_soup = soup_page(START_PAGE)
producers = get_producers(producers_soup)
for producer in producers:
    print('parsing %d/%d: %s...' % (producers.index(producer)+1, len(producers), producer['producer']))
    item_soup = soup_page(producer['link'])
    item = {"producer": producer["producer"],
            "items": get_items_of_producer(producer['link'])}
    catalog.append(item)
    sleep(5)
browser.close()

base = LiquidBase(json_db)
for producer_series in catalog:
    base.add_item(producer_series)

create_report(json_db)
