"""
Database logic for all things Goodreads.
"""

# import datetime
import sqlite3

# initialize the things and stuff. TODO: prettify
DATABASE_LOCATION = 'gr-sf.sqlite'
DATABASE = sqlite3.connect(DATABASE_LOCATION)
DATABASE_CURSOR = DATABASE.cursor()


def init_database():
    """Creates a SQLite DB if one doesn't already exist."""

    # Check DB integrity
    DATABASE.execute('PRAGMA quick_check')
    if DATABASE.fetchone()[0] != 'ok':
        print 'Due to a problem, the database must be rebuilt.'
        destroy_database()


def destroy_database():
    """Drops the DB tables and makes new ones."""

    # Drop tables, commit, make a new one.
    DATABASE.execute('''
        DROP TABLE IF EXISTS flights
    ''')
    DATABASE.commit()

    init_database()
