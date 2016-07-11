

from .URLFilter import URLFilter 

class PreciseDuplicateURLFilter(URLFilter):

    def __init__(self, corpus_table):
        URLFilter.__init__(self, 'Duplicate URL')
        self.corpus_table = corpus_table


    def accept(self, url):
        '''Overrides URLFilter#accept.

        Rejects URLs if they already exist in the database'''

        urls = self.corpus_table.find_url('url', url)
        return len(urls.fetchall()) > 0



