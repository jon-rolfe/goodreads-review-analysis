#!/usr/bin/env python
# coding=utf-8

"""
Usage TBD.

hey, don't actually commit the following:
TODO: hey, analysis -- Non-negative matrix factorization?
(github.com/duhaime/nmf)
LDA: pip install lda
scikit-learn
coreNLP
"""

from searcher import *

logging.basicConfig(level=logging.INFO, stream=sys.stdout,
                    format='%(levelname)s: %(message)s')  # TODO: file logging
logger = logging.getLogger('__name__')


def main():
    """Goodreads searcher main script. Execution logic flow director."""

    # init_database()

    # search_scraper()

    # review_scraper()

    # text_cleaning()

    # export_reviews()


# noinspection PyUnusedLocal
def close(*args):
    """Handles sigint/unexpected program exit"""
    sys.exit(1)
    try:
        browser.Dispose()
    except:
        logger.error('could not gracefully close browser object')
    try:
        closedb()
    except:
        logger.error('could not gracefully close database')


if __name__ == "__main__":
    # make a SIGINT handler for ctrl-c, etc
    signal.signal(signal.SIGINT, close)
    # call main
    main()
