

from .URLFilter import URLFilter 
import re

class HTTPURLFilter(URLFilter):

    def __init__(self):
        URLFilter.__init__(self, 'HTTP URLs')


    def accept(self, url):
        '''Overrides URLFilter#accept.

        Rejects URLs that do not start with http(s)?://'''
        
        return re.match('^https?://', url) != None


