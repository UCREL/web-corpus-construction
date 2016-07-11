
from .Filter import Filter

class MaximumLengthFilter(Filter):


    def __init__(self, threshold=80000):
        Filter.__init__(self, 'Maximum Length (chars)')
        self.threshold = threshold


    def accept(self, body, metadata=None):
        '''Overrides Filter#accept.

        Rejects pages with body length (chars) above the threshold given.'''

        return len(str(body)) < self.threshold



