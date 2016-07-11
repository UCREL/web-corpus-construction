
from .Filter import Filter

class MinimumLengthFilter(Filter):


    def __init__(self, threshold=80):
        Filter.__init__(self, 'Minimum length (chars)')
        self.threshold = threshold


    def accept(self, body, metadata=None):
        '''Overrides Filter#accept.

        Rejects pages with body length (chars) below the threshold given.'''

        return len(str(body)) >= self.threshold


