


# Native imports
import logging

# pip imports

class URLFilter:

    def __init__(self, name='URL Filter'):
        self._log = logging.getLogger('urlfilter')
        self.name = name


    def accept(self, url):
        return True

