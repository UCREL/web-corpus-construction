

from .URLRank import URLRank
from urllib.parse import urlparse

class SimplicityURLRank(URLRank):

    def __init__(self, max_score=10, scale=1):
        URLRank.__init__(self, "Simplicity (URL component count)", scale)
        self.max_score = max_score

    def goodness(self, url):
        '''Overrides URLRank#goodness.

        Returns a number between 0 and max_rank depending on how complex the URL is.
        Complexity is measured by parsing the URL into components, and then
        subtracting the number thereof from max_score.'''

        score = self.max_score
        try:
            parts = urlparse(str(url))
            score -= len(parts)
        except ValueError:
            self._log.error("Error parsing URL for scoring.")
            score = self.max_score

        return score * self.scale




