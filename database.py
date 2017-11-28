"""
Database logic for all things Goodreads.
"""

# import datetime
import sqlite3

# initialize the things and stuff. TODO: prettify
DATABASE_LOCATION = 'gr-sf.sqlite'
BOOK_DB = sqlite3.connect(DATABASE_LOCATION)
DATABASE_CURSOR = BOOK_DB.cursor()


def init_database():
    """Creates a SQLite DB if one doesn't already exist."""

    # Check DB integrity
    BOOK_DB.execute('PRAGMA quick_check')
    if BOOK_DB.fetchone()[0] != 'ok':
        print 'Due to a problem, the database must be rebuilt.'
        destroy_database()

    BOOK_DB.execute('''
      CREATE TABLE IF NOT EXISTS `scifi` (
        `id` INTEGER PRIMARY KEY,
        `title` TEXT,
        `author` TEXT,
        `avg_rating` REAL,
        `num_ratings` INTEGER,
        `publish_year` INTEGER
      )
    ''')


def destroy_database():
    """Drops the DB tables and makes new ones."""

    # Drop tables, commit, make a new one.
    BOOK_DB.execute('''
        DROP TABLE IF EXISTS `scifi`
    ''')
    BOOK_DB.commit()

    init_database()
