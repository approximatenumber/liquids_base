#!/usr/bin/env python

from urllib.request import urlopen, Request
from urllib.parse import quote
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import re
import pickledb

def soup_page(url):
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, "html.parser")
    return soup


def get_producers(soup):
    producers_links = soup.findAll('div', {'id':'sidebar-section'})[0].findAll('a')
    producers = []
    for producer_link in producers_links:
        producer = {"producer": producer_link.get('title'),
                    "link": 'https:'+producer_link.get('href')}
        producers.append(producer)
    return producers


def get_items_of_producer(u):
    soup_num = 1
    items = []
    soup = soup_page(u + "?PAGEN_1=" + str(soup_num))
    order_links = soup.findAll('a', {'class': 'item_title'})
    prices = soup.findAll('span', {'class': 'min-offer-price'})
    descriptions = soup.findAll('div', {'itemprop': 'description'})
    ratings = soup.findAll('span', {'class': 'ratingValue'})

    for order_link, price, description, rating in zip(order_links, prices, descriptions, ratings):
        item = {"title": order_link.get('title'),
               "link": 'https:' + order_link.get('href'),
               "price": re.findall('[0-9]+', price.getText()),
               "description": description.getText(),
               "rating": rating.getText()
                }
        items.append(item)
    soup_num += 1
    sleep(5)
    while True:
        try:
            soup = soup_page(u + "?PAGEN_1=" + str(soup_num))
            order_links = soup.findAll('a', {'class': 'item_title'})
            prices = soup.findAll('span', {'class': 'min-offer-price'})
            descriptions = soup.findAll('div', {'itemprop': 'description'})
            ratings = soup.findAll('span', {'class': 'ratingValue'})

            for order_link, price, description, rating in zip(order_links, prices, descriptions, ratings):
                item = {"title": order_link.get('title'),
                           "link": 'https:' + order_link.get('href'),
                           "price": re.findall('[0-9]+', price.getText()),
                           "description": description.getText(),
                           "rating": rating.getText()
                        }
            if item in items:
                break
            else:
                items.append(item)
                sleep(5)
        except HTTPError:
            break
    return items


START_PAGE = 'https://www.vardex.ru/e-juice.html'

browser = webdriver.Firefox()

catalog = []
producers_soup = soup_page(START_PAGE)
producers = get_producers(producers_soup)
for producer in producers:
    print('parsing %s...' % producer['producer'])
    item_soup = soup_page(producer['link'])
    item = {"producer": producer["producer"],
            "items": get_items_of_producer(producer['link'])}
    catalog.append(item)
    sleep(5)

print(catalog)

base = pickledb.load('/tmp/vaper_liquids.db', False)
for producer_series in catalog:
    base.dcreate(producer_series['producer'])
    for item in producer_series['items']:
        for feature in item.items():
            base.dadd(producer_series['producer'], feature)
base.dump()
