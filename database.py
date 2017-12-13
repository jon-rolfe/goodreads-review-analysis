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
            "review_id" INTEGER PRIMARY KEY,
            "book_id" INTEGER,
            "review_text" TEXT,
            UNIQUE("book_id","review_text") ON CONFLICT IGNORE
            FOREIGN KEY("book_id") REFERENCES book_list("id")
      )
    ''')

    BOOK_DB_CURSOR.execute('''
      CREATE TABLE IF NOT EXISTS "clean_reviews" (
            "review_id" INTEGER PRIMARY KEY,
            "book_id" INTEGER,
            "review_text" TEXT,
            UNIQUE("book_id","review_text") ON CONFLICT IGNORE
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


def add_review(book_id, review_text, is_clean, review_id=False):
    """Adds a review to one of the review tables"""
    # While this code may be redundant, I couldn't bring myself to do unsanitized input. I just couldn't.
    if is_clean:
        BOOK_DB_CURSOR.execute('''
            INSERT INTO "clean_reviews" (review_id, book_id, review_text)
              VALUES (?, ?,?)
        ''', (review_id, book_id, review_text))
    else:
        # For new reviews, let review_id be autopopulated by the db.
        BOOK_DB_CURSOR.execute('''
            INSERT INTO "reviews" (book_id, review_text)
              VALUES (?,?)
        ''', (book_id, review_text))

    BOOK_DB.commit()


def call_book(book_num):  # TODO: split this into two fns for more efficiency
    """Grab a book from the table by its ID"""
    BOOK_DB_CURSOR.execute('''
        SELECT * FROM "book_list" WHERE "ID" = (?)
    ''', (book_num,))
    result = BOOK_DB_CURSOR.fetchone()

    if result is None:  # i.e., there is no book with a given ID
        return False
    else:
        return result


def call_review(review_num, is_clean):
    """Grab reviews -- TODO: consolidate functions?"""
    # Same thing as add_review -- redundant but keeps variables paramaterized
    if is_clean:
        BOOK_DB_CURSOR.execute('''
            SELECT * FROM "clean_reviews" WHERE "review_id" = (?)
        ''', (review_num,))
    else:
        BOOK_DB_CURSOR.execute('''
            SELECT * FROM "reviews" WHERE "review_id" = (?)
        ''', (review_num,))

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
