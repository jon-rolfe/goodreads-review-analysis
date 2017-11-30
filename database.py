"""
Database logic for all things Goodreads.
"""

# import datetime
import sqlite3

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
        print 'Due to a problem, the database must be rebuilt.'
        remake_database()

    BOOK_DB_CURSOR.execute('''
      CREATE TABLE IF NOT EXISTS "book_list" (
        "id" INTEGER PRIMARY KEY,
        "url" TEXT,
        "title" TEXT,
        "author" TEXT,
        "publish_year" INTEGER,
        UNIQUE ("title","author","publish_year") ON CONFLICT IGNORE
      )
    ''')

    BOOK_DB_CURSOR.execute('''
      CREATE TABLE IF NOT EXISTS "reviews"
        "id" INTEGER PRIMARY KEY,
        
    ''')

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

    BOOK_DB.commit()
