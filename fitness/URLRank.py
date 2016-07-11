



# Native imports
import logging

# pip imports

class URLRank:

    def __init__(self, name='URLRank', scale=1):
        self._log = logging.getLogger('rank')
        self.name = name
        self.scale = scale


    def goodness(self, url):
        '''Returns a numeric goodness score for a given URL.  High is good.'''

        return 0 




