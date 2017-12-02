#!/usr/bin/env python

"""
Usage TBD.
"""

import signal
import sys

from selenium import webdriver

from database import *

logging.basicConfig(level=logging.INFO, stream=sys.stdout,
                    format='%(levelname)s: %(message)s')  # TODO: file logging
logger = logging.getLogger('__name__')

# todo: from langdetect import detect


def main():
    """Goodreads searcher main script. Execution logic flow director."""

    init_database()

    # search_scraper()

    review_scraper()


def search_scraper():
    """Scrapes books from a goodreads search and sends them to be added to the DB"""
    # initiate logger, initialize DB, define path to geckodriver, create browser instance,

    geckopath = '/Users/jonathanrolfe/Desktop/geckodriver'
    browser = webdriver.Firefox(executable_path=geckopath)

    # initiate search; get starting locations
    search_term = 'science+fiction'
    browser.get('https://www.goodreads.com/search?q={}&search_type=books&search%5Bfield%5D=genre'.format(search_term))

    # xpath definitions
    book_root_location = '/html/body/div[1]/div[2]/div[1]/div[1]/div[2]/table/tbody/tr[{}]/'
    book_title_location = book_root_location + 'td[1]/a'
    book_url_location = book_root_location + 'td[1]/a'
    book_author_location = book_root_location + 'td[2]/span[2]/a'
    book_publish_year_location = book_root_location + 'td[2]/span[3]'

    page = 1
    # iterate through first 100 search pages (GR will not display past p 100)
    while page < 101:

        # iterate through each book on the page
        book_on_page = 1
        while book_on_page < 21:
            book_title = browser.find_element_by_xpath(book_title_location.format(book_on_page)).get_attribute(
                'title').encode('ascii', 'ignore')
            book_url = browser.find_element_by_xpath(
                book_url_location.format(book_on_page)).get_attribute('href').encode('ascii', 'ignore')
            book_author = browser.find_element_by_xpath(book_author_location.format(book_on_page)).text.encode('ascii',
                                                                                                               'ignore')
            try:  # every once in a while, goodreads doesn't list the publish date in search
                book_publish_year = int(
                    browser.find_element_by_xpath(book_publish_year_location.format(book_on_page)).text.split(
                        'published ', 1)[1][:4].encode('ascii', 'ignore'))
            except IndexError:
                logger.error('No publish year listed for {} - please fill manually in DB'.format(book_title))
                book_publish_year = '0'  # (dummy value for when no date listed)

            logger.debug('title: {}'.format(book_title))
            logger.debug('author: {}'.format(book_author))
            logger.debug('publish year: {}'.format(book_publish_year))
            logger.debug('url: {}'.format(book_url))

            # add to DB
            add_book(book_title, book_author, book_publish_year, book_url)
            logger.info('ADDED: {}'.format(book_title))

            book_on_page += 1

        # have it click "next" rather than iterate the page field of URL to make it vaguely less obviously a crawler
        browser.find_element_by_class_name('next_page').click()
        page += 1


def review_scraper():
    """Using the preexisting book_list database, scape reviews -
    TABLE REFERENCE:
        BOOK_DB_CURSOR.execute('''
          CREATE TABLE IF NOT EXISTS "reviews" (
            "id" INTEGER PRIMARY KEY,
            "book_id" INTEGER,
            "stars" INTEGER,
            "post_date" TEXT,
            "url" TEXT,
            FOREIGN KEY("book_id" REFERENCES book_list("id"))
          )
    """

    book_to_scrape = call_book('1')
    logger.debug(book_to_scrape)


def close(*args):
    """Handles sigint/unexpected program exit"""
    sys.exit(1)


if __name__ == "__main__":
    # make a SIGINT handler for ctrl-c, etc
    signal.signal(signal.SIGINT, close)
    # call main
    main()
