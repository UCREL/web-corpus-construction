#!/usr/bin/env python3

# Standard modules
import logging
import urllib.error
from urllib.request import urlopen
import types
import logging
from socket import timeout


class HTTPClient:



    def __init__(self, max_filesize=20971520, content_type_rx=None):
        self._log = logging.getLogger('spider')
        self.content_type_rx = content_type_rx
        self.max_filesize = max_filesize



    def incremental_read(self, response, chunk_size=4096):
        '''Read from a HTTP response incrementally, stopping when
        the max filesize is reached.'''

        body = b''
        size = 0
        while(size < self.max_filesize):
            chunk = response.read(chunk_size)
            body += chunk
            
            if not chunk:
                return body 
            
            size += len(chunk)
            self._log.debug("Read %s bytes (max: %s)" % (size, self.max_filesize))

        self._log.error("File is too long (read %s bytes of %s)" % (size, self.max_filesize))
        return None 



    def get_page(self, url, corpus_table, timeout=30):
        '''Given a url will return the page content and metadata in a tuple if not a duplicate else return None

        The page is returned as a String and the metadata is a dictionary where
        the keys describe the metadata content stored in the value of that
        key.

        Optional timeout parameter for requesting the data from the given url.
        '''

        page = None
        body = None
        try:
            # Start HTTP request
            page = urlopen(url, timeout=timeout)
    
            # Check content type BEFORE requesting the whole page
            if self.content_type_rx:
                content_type = page.info()['Content-Type']
                if re.match(self.content_type_rx, str(content_type)) == None:
                    self._log.error("Content type (%s) does not match pattern (%s)" % \
                            (content_type, self.content_type_rx))

            # Read page data up until the max size
            body = self.incremental_read(page)

        except urllib.error.HTTPError as error:
            self._log.error('HTTP code %d : %s, URL: %s' % (error.code, error.reason, url))
            return None, None
        except urllib.error.URLError as error:
            self._log.debug('URL error: %s, URL: %s' % (error.reason, url))
            return None, None

        return page, body




