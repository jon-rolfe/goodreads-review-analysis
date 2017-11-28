#!/usr/bin/env python

"""
Usage: ./goodanalyzer.py database
"""

import signal
import sys

from selenium import webdriver


def main():
    """Does most of the magic."""

    geckopath = '/Users/jonathanrolfe/Desktop/geckodriver'

    browser = webdriver.Firefox(executable_path=geckopath)

    browser.get('https://www.goodreads.com/search?q=science+fiction&search_type=books&search%5Bfield%5D=genre')

    book_title_location = '/html/body/div[1]/div[2]/div[1]/div[1]/div[2]/table/tbody/tr[{}]/td[2]/a'
    page = 1

    while page < 101:
        book_on_page = 1
        while book_on_page < 21:
            print browser.find_element_by_xpath(book_title_location.format(book_on_page)).get_attribute('href')
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
