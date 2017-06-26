
import re
from .URLRank import URLRank

class HumanReadableURLRank(URLRank):

    def __init__(self, scale=100):
        URLRank.__init__(self, "Simplicity (URL component count)", scale)

    def goodness(self, url):
        '''Overrides URLRank#goodness.

        Returns a score between 0 and 100 depending on the number of special
        characters and numbers in the URL.

        Designed to penalise URLs with hashes and such'''
        
        if len(url) == 0:
            return 0
        score = (len(re.findall("[a-zA-Z]", url)) / len(url))

        return int(score * self.scale)




