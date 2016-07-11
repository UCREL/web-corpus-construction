

# Native imports
import logging

# pip imports

class Filter:

    def __init__(self, name='Filter'):
        self._log = logging.getLogger('filter')
        self.name = name


    def accept(self, body, metadata=None):
        '''Returns true if the page given should be accepted, else false.'''

        return True

