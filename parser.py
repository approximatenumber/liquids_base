#!/usr/bin/env python

from urllib.request import urlopen
from urllib.parse import quote
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from time import sleep


def soup_page(url):
    page = BeautifulSoup(urlopen(url), "html.parser")
    return page


def get_firms(page):
    firms_links = page.findAll('div',{'id':'sidebar-section'})[0].findAll('a')
    firms = []
    for firm_link in firms_links:
        firm = {"title": firm_link.get('title'),
                "link": 'https:'+firm_link.get('href')}
        firms.append(firm)
    return firms


def get_products_of_firm(u):
    page_num = 1
    products = []
    page = soup_page(u + "?PAGEN_1=" + str(page_num))
    order_links = page.findAll('a', {'class': 'item_title'})
    for order_link in order_links:
        product = {"title": order_link.get('title'),
                   "link": 'https:' + order_link.get('href')}
        products.append(product)
    print(products)
    page_num += 1
    sleep(5)
    while True:
        try:
            page = soup_page(u + "?PAGEN_1=" + str(page_num))
            order_links = page.findAll('a', {'class': 'item_title'})
            for order_link in order_links:
                product = {"title": order_link.get('title'),
                           "link": 'https:' + order_link.get('href')}
            if product in products:
                print('stop')
                break
            else:
                products.append(product)
                print(products)
                sleep(5)
        except HTTPError:
            break
    return products

START_PAGE = 'https://www.vardex.ru/e-juice.html'

catalog = []
firms_page = soup_page(START_PAGE)
firms = get_firms(firms_page)
for firm in firms:
    product_page = soup_page(firm['link'])
    product = {"firm": firm["title"],
               "products": get_products_of_firm(firm['link'])}
    # print(product)
    catalog.append(product)
    sleep(5)
print(catalog)
