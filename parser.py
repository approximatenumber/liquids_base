#!/usr/bin/env python

from urllib.request import urlopen
from urllib.parse import quote
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from time import sleep
import re


def soup_page(url):
    page = BeautifulSoup(urlopen(url), "html.parser")
    return page


def get_producers(page):
    producers_links = page.findAll('div',{'id':'sidebar-section'})[0].findAll('a')
    producers = []
    for producer_link in producers_links:
        producer = {"title": producer_link.get('title'),
                "link": 'https:'+producer_link.get('href')}
        producers.append(producer)
    return producers


def get_items_of_producer(u):
    page_num = 1
    items = []
    page = soup_page(u + "?PAGEN_1=" + str(page_num))

    order_links = page.findAll('a', {'class': 'item_title'})
    prices = page.findAll('span', {'class': 'min-offer-price'})
    descriptions = page.findAll('div', {'itemprop': 'description'})
    #ratings = page.findAll('span', {'class': 'ratingValue'})

    print(order_links, '\n', prices, '\n', descriptions)
    for order_link, price, description in zip(order_links, prices, descriptions):
        item = {"title": order_link.get('title'),
               "link": 'https:' + order_link.get('href'),
               "price": re.findall('[0-9]+', price.getText()),
               "description": description.getText(),
              # "rating": rating.getText()
                }
        print("f")
        items.append(item)
    print('FIRST:', items)
    page_num += 1
    sleep(5)
    while True:
        try:
            page = soup_page(u + "?PAGEN_1=" + str(page_num))
            order_links = page.findAll('a', {'class': 'item_title'})
            prices = page.findAll('span', {'class': 'min-offer-price'})
            descriptions = page.findAll('div', {'itemprop': 'description'})
            #ratings = page.findAll('span', {'class': 'ratingValue'})

            for order_link, price, description in zip(order_links, prices, descriptions):
                item = {"title": order_link.get('title'),
                           "link": 'https:' + order_link.get('href'),
                           "price": re.findall('[0-9]+', price.getText()),
                           "description": description.getText(),
                           #"rating": rating.getText()
                        }
                if item in items:
                    print('stop')
                    break
                else:
                    items.append(item)
                    sleep(5)
                    print('NEXT:', items)
        except HTTPError:
            break
    print("ALL:", items)
    return items


def get_items_of_producer_(url):
    page_num = 1
    items = []
    page = soup_page(url + "?PAGEN_1=" + str(page_num))
    order_links = page.findAll('a', {'class': 'item_title'})
    for order_link in order_links:
        item = {"title": order_link.get('title'),
                   "link": 'https:' + order_link.get('href')}
        items.append(item)
    print(items)
    page_num += 1
    sleep(5)
    while True:
        try:
            page = soup_page(u + "?PAGEN_1=" + str(page_num))
            order_links = page.findAll('a', {'class': 'item_title'})
            for order_link in order_links:
                item = {"title": order_link.get('title'),
                           "link": 'https:' + order_link.get('href')}
            if item in items:
                print('stop')
                break
            else:
                items.append(item)
                print(items)
                sleep(5)
        except HTTPError:
            break
    return items

START_PAGE = 'https://www.vardex.ru/e-juice.html'

catalog = []
producers_page = soup_page(START_PAGE)
producers = get_producers(producers_page)
for producer in producers:
    item_page = soup_page(producer['link'])
    item = {"producer": producer["title"],
               "items": get_items_of_producer(producer['link'])}
    # print(item)
    catalog.append(item)
    sleep(5)
print(catalog)
