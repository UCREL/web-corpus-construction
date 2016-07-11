



# 
import CorpusTable
from .Filter import Filter
import hashlib 


class DuplicateFilter(Filter):

    def __init__(self, db, threshold=80):
        Filter.__init__(self,'Body Duplicate (precise)' )
        self._db = db
        self.threshold = threshold


    def accept(self, body, metadata=None):
        '''Overrides Filter#accept.
        
        Compares an SHA1 hash of the body value to those already in the database,
        and rejects if found.'''

        content_hash = metadata['hash']
        pages = self._db.find_page('hash', content_hash)
        return len(pages.fetchall()) == 0

