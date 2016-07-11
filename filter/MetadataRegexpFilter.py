

from .Filter import Filter
import re

class MetadataRegexpFilter(Filter):

    def __init__(self, header, pattern):
        Filter.__init__(self, "Metadata pattern (%s =~ /%s/)" % (header, pattern))
        self.header = header 
        self.pattern = pattern 

    def accept(self, body, metadata=None):
        '''Overrides Filter#accept.

        Rejects pages where the header given does not match the pattern given'''

        header = str(metadata[self.header])
        self._log.debug("Metadata %s = '%s', pattern '%s'" % (self.header, header, self.pattern))
        return re.match(self.pattern, header) != None



