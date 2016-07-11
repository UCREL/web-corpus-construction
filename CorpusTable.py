#!/usr/bin/env python3

# Standard modules
import sqlite3 as lite
import os.path
import sys

# Non-standard modules
import code
import hashlib
import logging

class CorpusTable:
    '''Object that stores all the content from a web page.

    Methods:
    1) get_data
    2) insert_page
    3) is_duplicate
    4) close_con

    Private Instance variables:
    2) con -- The connection class that is connected to table_name table.
    '''

    db_filename = 'metadata.db'
    schema      = ["CREATE TABLE urls (id INTEGER PRIMARY KEY AUTOINCREMENT, url text, goodness numeric, depth integer, hash text, downloaded integer);",
              "CREATE TABLE output (url_id integer, date text, charset text, content_type text, title text, h1 text, hash text);"]


    def __init__(self, dirname):
        '''Creates the database connection and adds output table, returns None.'''

        self.dirname = dirname
        self.filename = os.path.join(dirname, CorpusTable.db_filename)

        # Create dir if not in existence
        self._log = logging.getLogger('storage')

        self._log.info("Using output database at %s" % dirname)
        os.makedirs(dirname, exist_ok=True)

        # Connect to/create a database file
        new_db                = not os.path.isfile(self.filename)
        self._con             = lite.connect(self.filename)
        self._con.text_factory = lambda x: str(x, "utf-8", "ignore")
        self._cursor          = self._con.cursor()
        if new_db:
            self._log.info("Metadata DB does not exist.  Creating now at %s" % self.filename)
            for command in CorpusTable.schema:
                self.execute(command)

    def execute(self, sql, data = None, get_rowid = False):
        '''Execute a single transaction with the SQL given, and return the result.'''

        self._log.debug("SQL: %s" % sql)
        c = self._con.cursor()
        if data:
            c = c.execute(sql, data)
        else:
            c = c.execute(sql)
        self._con.commit()

        # If the last row ID is requested, return it here.
        # SQLite3 doesn't support multiple statements per call, else this could be
        # included in the sql parameter
        if get_rowid:
            c.execute("select last_insert_rowid();")
            self._con.commit()
            c = c.fetchone()[0]

        return c

    def insert_url(self, url, goodness, depth = 0):
        ''' Add a URL to the pending list'''

        hsh = hashlib.sha1(url.encode('utf-8')).hexdigest()
        row = self.execute("insert into `urls` (url, goodness, depth, hash, downloaded) values (?, ?, ?, ?, ?);",
                     [url, goodness, depth, hsh, 0], get_rowid=True)
        self._log.debug("URL inserted as ID %s with goodness %s: %s" % (row, goodness, url))


    def best_url(self, downloaded = False):
        '''Return a random URL from the urls table'''
        c = self.execute("select url, id, goodness, depth from urls where downloaded = ? order by goodness DESC limit 1;",
                [1 if downloaded else 0]);
        return c.fetchone()


    def url_count(self, downloaded = False):
        ''' Return the number of URLs downloaded or pending. '''
        c = self.execute("select count(*) from `urls` where downloaded = ?;",
                     [1 if downloaded else 0]);
        return c.fetchone()[0]

    def update_url(self, url_id):
        '''Updates the input/url table so that the url is now stated as downloaded.'''

        c = self.execute("UPDATE `urls` SET downloaded = 1 WHERE id = ?;", [url_id])

    def get_data(self, column):
        '''Given a list of columns returns a cursor interator of tuple values from the associated columns.'''

        return self.execute("select `%s` from `output`;" % column)

    def find_url(self, field, value):
        '''Find an item in the urls table by a given field.'''

        return self.execute("select * from `urls` where `%s` = ?;" % field, [value])

    def find_page(self, field, value):
        '''Find an item in the output table by a given field.'''

        return self.execute("select * from `output` where `%s` = ?;" % field, [value])

    def insert_page(self, metadata, body):
        '''Inserts the data (dictionary) into the SQLite table returns None.

        The data is a dictionary, the keys are the names of columns in the
        database table and the associated values in the dictionary are the
        values associated with the database table as well.

        The hash of the content is created within this method and added to the
        data dictionary and inserted into the database table.
        '''

        insert_query = "INSERT INTO output (" + ', '.join(map(lambda x: "'%s'" % x, metadata.keys())) + \
            ") VALUES (" + \
            ', '.join(['?'] * len(metadata.keys())) + ");"
        self.execute(insert_query, list(metadata.values()))

        # Write the HTML to relevant file based on url_id
        filename = os.path.join(self.dirname, str(metadata['url_id']) + ".html")
        self._log.debug("Writing %s bytes of page data to %s" % (str(sys.getsizeof(body)), filename))
        with open(filename, 'wb') as fd:
            fd.write(body)

        # Updates the url in the input table as now downloaded.
        self.update_url(metadata['url_id'])


    def output_count(self):
        '''Returns the total corpus size'''

        c = self.execute('select count(*) from output;')
        return c.fetchone()[0]

    def disconnect(self):
        '''Close the open connection to the database.'''

        self._log.debug("Closing DB connection")
        self._con.close()
