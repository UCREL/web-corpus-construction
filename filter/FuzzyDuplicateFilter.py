



# 
import CorpusTable
from .Filter import Filter
import ssdeep

class FuzzyDuplicateFilter(Filter):


    def __init__(self, db, threshold=80):
        Filter.__init__(self,'Body Duplicate (fuzzy hash)' )
        self._db = db
        self.threshold = threshold


    def accept(self, body, metadata=None):
        '''Overrides Filter#accept.
        
        Compares a fuzzy hash of the body value to those already in the database,
        and rejects if they are more similar than the given threshold.'''

        content_hash = metadata['hash'] if metadata else ssdeep.hash(str(body))
        hash_cursor = self._db.get_data('hash')

        # comp_hash will be a tuple of size 1 containing just the hash.
        # (If it never breaks then goes into the else clause)
        for comp_hash in hash_cursor:
            if comp_hash[0] is None:
                continue
            related_value = ssdeep.compare(content_hash, comp_hash[0])
            self._log.debug("Comparing body hash: %s > %s" % (related_value, self.threshold))
            if related_value > self.threshold:
                self._log.info("Body found in output table (similarity = %s)" % related_value)
                return True

        return False

