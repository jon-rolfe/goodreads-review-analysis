#!/usr/bin/env python

"""
Usage TBD.
"""

import signal
import sys

from selenium import webdriver


# import logging - TODO: real logging


def main():
    """Does most of the magic."""

    geckopath = '/Users/jonathanrolfe/Desktop/geckodriver'

    browser = webdriver.Firefox(executable_path=geckopath)

    search_term = 'science+fiction'
    browser.get('https://www.goodreads.com/search?q={}&search_type=books&search%5Bfield%5D=genre'.format(search_term))

    book_root_location = '/html/body/div[1]/div[2]/div[1]/div[1]/div[2]/table/tbody/tr[{}]/'
    book_title_location = book_root_location + 'td[1]/a'
    book_url_location = book_root_location + 'td[1]/a'
    book_author_location = book_root_location + 'td[2]/span[2]/a'
    book_rating_info_location = book_root_location + 'td[2]/span[3]/span'
    book_publish_year = book_root_location + 'td[2]/span[3]'

    page = 1

    while page < 101:  # GR has max 100 pages per search term
        book_on_page = 1
        while book_on_page < 21:
            print 'title: ' + browser.find_element_by_xpath(book_title_location.format(book_on_page)).get_attribute(
                'title')
            print 'url: ' + browser.find_element_by_xpath(book_url_location.format(book_on_page)).get_attribute('href')
            print 'author: ' + browser.find_element_by_xpath(book_author_location.format(book_on_page)).text
            print 'rating info: ' + browser.find_element_by_xpath(book_rating_info_location.format(book_on_page)).text
            print 'publish year: ' + \
                  browser.find_element_by_xpath(book_publish_year.format(book_on_page)).text.split('published ', 1)[1][
                  :4] + '\n'  # TODO: oh god please make this less hacky
            book_on_page += 1

        browser.find_element_by_class_name('next_page').click()
        page += 1


def close(*args):
    """Handles sigint/unexpected program exit"""
    sys.exit(1)


if __name__ == "__main__":
    # make a SIGINT handler for ctrl-c, etc
    signal.signal(signal.SIGINT, close)
    # call main
    main()
