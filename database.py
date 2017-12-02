"""
Database logic for all things Goodreads.
"""

import logging
# import datetime
import sqlite3

logger = logging.getLogger('__name__')

# initialize the things and stuff. TODO: prettify
BOOK_DB_LOCATION = 'goodreads-scifi.sqlite'
BOOK_DB = sqlite3.connect(BOOK_DB_LOCATION)
BOOK_DB_CURSOR = BOOK_DB.cursor()


def init_database():
    """Creates a SQLite DB if one doesn't already exist."""
    # TODO: deduping check on init; logging

    # Check DB integrity
    BOOK_DB_CURSOR.execute('PRAGMA QUICK_CHECK')
    if BOOK_DB_CURSOR.fetchone()[0] != 'ok':
        logger.error('Due to a problem, the database must be rebuilt.')
        remake_database()

    BOOK_DB_CURSOR.execute('''
      CREATE TABLE IF NOT EXISTS "book_list" (
        "id" INTEGER PRIMARY KEY,
        "url" TEXT UNIQUE,
        "title" TEXT,
        "author" TEXT,
        "publish_year" INTEGER,
        UNIQUE ("title","author","publish_year") ON CONFLICT IGNORE
      )
    ''')

    BOOK_DB_CURSOR.execute('''
      CREATE TABLE IF NOT EXISTS "reviews" (
        "id" INTEGER PRIMARY KEY,
        "book_id" INTEGER,
        "stars" INTEGER,
        "post_date" TEXT,
        "url" TEXT UNIQUE,
        FOREIGN KEY("book_id") REFERENCES book_list("id")
      )
    ''')

    logger.debug('CREATE TABLE IF NOT EXIST statements successful')
    BOOK_DB.commit()


def remake_database():
    """Drops the DB tables and makes new ones."""

    # Drop tables, commit, make a new one.
    BOOK_DB_CURSOR.execute('''
        DROP TABLE IF EXISTS "book_list"
    ''')

    BOOK_DB.commit()

    init_database()


def add_book(title, author, publish_year, url):
    """Add newly-scraped books to the scifi DB"""
    BOOK_DB_CURSOR.execute('''
        INSERT INTO "book_list" (title, author, publish_year, url)
        VALUES (?, ?, ?, ?)
    ''', (title, author, publish_year, url))

    # TODO: consider moving commit statement outside function - inefficient to commit every time when bulk adding
    BOOK_DB.commit()


def call_book(id):  # TODO: split this into two fns
    """Grab a book from the table by its ID"""
    BOOK_DB_CURSOR.execute('''
        SELECT * FROM "book_list" WHERE "ID" = ?
    ''', (id))
    result = BOOK_DB_CURSOR.fetchone()

    if result is None:  # i.e., there is no book with a given ID
        return False
    else:
        return result


def book_list_size():
    """Get the number of books in the book_list table (for reference)"""
    BOOK_DB_CURSOR.execute('''
        SELECT COUNT(*) FROM "book_list"
    ''')

    return BOOK_DB_CURSOR.fetchone()[0]
